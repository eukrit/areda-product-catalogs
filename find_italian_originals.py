"""Find original Italian furniture designs for Areda products using Gemini + web search."""
import sys, io, os, json, time, urllib.request, urllib.parse, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\eukri\OneDrive\Documents\Claude Code\Credentials Claude Code\ai-agents-go-4c81b70995db.json"

from google.cloud.firestore_v1 import Client
from datetime import datetime, timezone

db = Client(project="ai-agents-go", database="areda-product-catalogs")
now = datetime.now(timezone.utc).isoformat()

# Auth via service account OAuth (API keys expired)
import google.auth
import google.auth.transport.requests
_creds, _ = google.auth.default(scopes=[
    "https://www.googleapis.com/auth/generative-language",
    "https://www.googleapis.com/auth/cloud-platform",
])
_auth_req = google.auth.transport.requests.Request()
_creds.refresh(_auth_req)

GEMINI_EP = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

def _get_auth_header():
    if _creds.expired:
        _creds.refresh(_auth_req)
    return f"Bearer {_creds.token}"

# Get all visible products
docs = list(db.collection("products").stream())
visible = [d for d in docs if d.to_dict().get("visible", True)]
visible.sort(key=lambda d: d.to_dict().get("name", ""))
print(f"Processing {len(visible)} visible products...\n")

def search_italian_original(product_data):
    """Use Gemini with grounding to find the original Italian furniture design."""
    name = product_data.get("name", "")
    name_cn = product_data.get("nameCn", "")
    dims = product_data.get("dimensions", "")
    material = product_data.get("material", "")
    material_cn = product_data.get("materialCn", "")
    category = product_data.get("category", "")
    features = product_data.get("features", "")
    img_desc = product_data.get("imageDescription", "")
    collection = product_data.get("collection", "")
    style = product_data.get("style", "")

    prompt = f"""You are a furniture industry expert. Identify the ORIGINAL Italian designer furniture that this Chinese-manufactured product is based on or inspired by.

Product details:
- Name: {name}
- Chinese name: {name_cn}
- Category: {category}
- Dimensions: {dims}
- Material: {material} {material_cn}
- Features: {features}
- Style reference: {style}
- Image description: {img_desc}

Search the web to find the original Italian furniture piece. Look for matches from brands like:
Minotti, B&B Italia, Poliform, Molteni&C, Cassina, Flexform, Giorgetti, Maxalto, Porro, Baxter, Fendi Casa, Versace Home, Armani Casa, Turri, Visionnaire, Natuzzi Italia, Poltrona Frau, Zanotta, Moroso, Cappellini, Driade, Kartell, Edra, Living Divani, De Padova, Meridiani, Lema, Rimadesio, MDF Italia, Lago

IMPORTANT: Search for the product using the name, dimensions, and visual description. Many Chinese furniture names are transliterations of Italian product names.

For PRICE: search specifically for "[brand] [model] price" or look for retailer listings, dealer quotes, or price comparison sites. Italian luxury furniture typically costs EUR 2,000-30,000+ depending on category. If exact price not found, provide your best estimate based on similar items from the same brand/collection.

Respond with ONLY this JSON (no markdown, no code blocks):
{{"found": true/false, "brand": "Italian brand name", "model": "Model/collection name", "designer": "Designer name", "retailPriceEur": 0, "retailPriceUsd": 0, "productUrl": "official product page URL", "dimensions": "original dimensions", "material": "original materials", "confidence": "high/medium/low", "matchReason": "why this is the match"}}

If you cannot find a match, set found to false and leave other fields empty.
For prices, search for the retail/list price in EUR and USD. Use 0 only if absolutely no price info found.
"""

    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 500,
            "thinkingConfig": {"thinkingBudget": 0},
        },
        "tools": [{"googleSearch": {}}],
    }

    try:
        req = urllib.request.Request(
            GEMINI_EP,
            data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json", "Authorization": _get_auth_header()},
        )
        resp = urllib.request.urlopen(req, timeout=30)
        result = json.loads(resp.read())

        text = ""
        candidate = result.get("candidates", [{}])[0]
        for part in candidate.get("content", {}).get("parts", []):
            if "text" in part:
                text += part["text"]

        # Extract grounding source URLs from Gemini response
        source_urls = []
        grounding = candidate.get("groundingMetadata", {})
        for chunk in grounding.get("groundingChunks", []):
            web = chunk.get("web", {})
            if web.get("uri"):
                source_urls.append({"url": web["uri"], "title": web.get("title", "")})
        # Also check search results
        for entry in grounding.get("searchEntryPoint", {}).get("renderedContent", "").split("href=\""):
            if entry.startswith("http"):
                url = entry.split("\"")[0]
                if url not in [s["url"] for s in source_urls]:
                    source_urls.append({"url": url, "title": ""})

        # Parse JSON response
        text = text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        parsed = json.loads(text)
        parsed["sourceLinks"] = source_urls
        return parsed
    except Exception as e:
        return {"found": False, "error": str(e)[:100]}


# Process products in batches
results = []
found_count = 0
error_count = 0
batch = db.batch()
batch_count = 0

# Track unique Italian products to avoid duplicates
italian_products = {}  # key: brand+model -> data

for i, doc in enumerate(visible):
    data = doc.to_dict()
    product_name = data.get("name", "")

    print(f"[{i+1}/{len(visible)}] {product_name[:45]}...", end=" ", flush=True)

    result = search_italian_original(data)

    if result.get("found"):
        brand = result.get("brand", "Unknown")
        model = result.get("model", "Unknown")
        confidence = result.get("confidence", "low")
        price_eur = result.get("retailPriceEur", 0)
        price_usd = result.get("retailPriceUsd", 0)

        # Create unique key for Italian product
        italian_key = f"{brand}-{model}".lower().replace(" ", "-")
        italian_key = "".join(c for c in italian_key if c.isalnum() or c == "-")

        # Build Italian product record
        italian_record = {
            "brand": brand,
            "model": model,
            "designer": result.get("designer", ""),
            "retailPriceEur": price_eur or 0,
            "retailPriceUsd": price_usd or 0,
            "productUrl": result.get("productUrl", ""),
            "dimensions": result.get("dimensions", ""),
            "material": result.get("material", ""),
            "category": data["category"],
            "confidence": confidence,
            "matchReason": result.get("matchReason", ""),
            "sourceLinks": result.get("sourceLinks", []),
            "linkedAredaProducts": [],
            "createdAt": now,
            "updatedAt": now,
        }

        # Merge if we've seen this Italian product before
        if italian_key in italian_products:
            existing = italian_products[italian_key]
            if doc.id not in existing["linkedAredaProducts"]:
                existing["linkedAredaProducts"].append(doc.id)
            # Keep higher confidence
            if confidence == "high" and existing.get("confidence") != "high":
                existing.update({k: v for k, v in italian_record.items() if k != "linkedAredaProducts" and v})
        else:
            italian_record["linkedAredaProducts"] = [doc.id]
            italian_products[italian_key] = italian_record

        # Update areda product with link to Italian original
        areda_update = {
            "italianOriginalRef": italian_key,
            "italianBrand": brand,
            "italianModel": model,
            "italianRetailPriceEur": price_eur or 0,
            "italianRetailPriceUsd": price_usd or 0,
            "updatedAt": now,
        }
        batch.update(db.collection("products").document(doc.id), areda_update)
        batch_count += 1

        found_count += 1
        print(f"FOUND: {brand} {model} ({confidence}) EUR {price_eur} USD {price_usd}")
    else:
        err = result.get("error", "no match")
        if "error" in result:
            error_count += 1
            print(f"ERROR: {err[:60]}")
        else:
            print(f"NO MATCH")

    # Commit batches
    if batch_count >= 400:
        batch.commit()
        batch = db.batch()
        batch_count = 0
        print(f"  --- committed areda updates ---")

    # Rate limit: Gemini free tier = 15 RPM for flash
    time.sleep(4.5)

    # Progress update
    if (i + 1) % 20 == 0:
        print(f"\n=== Progress: {i+1}/{len(visible)} | Found: {found_count} | Errors: {error_count} ===\n")

# Final commit for areda product updates
if batch_count > 0:
    batch.commit()
    print(f"Committed final areda updates ({batch_count})")

# Write italian-products collection
print(f"\n=== Writing {len(italian_products)} Italian products to Firestore ===")
batch = db.batch()
batch_count = 0
for key, record in italian_products.items():
    ref = db.collection("italian-products").document(key)
    batch.set(ref, record)
    batch_count += 1
    if batch_count >= 400:
        batch.commit()
        batch = db.batch()
        batch_count = 0

if batch_count > 0:
    batch.commit()

print(f"\nDONE!")
print(f"  Products processed: {len(visible)}")
print(f"  Italian matches found: {found_count}")
print(f"  Unique Italian products: {len(italian_products)}")
print(f"  Errors: {error_count}")

# Summary of top brands found
from collections import Counter
brands = Counter(r["brand"] for r in italian_products.values())
print(f"\nTop Italian brands:")
for brand, count in brands.most_common(15):
    print(f"  {brand}: {count}")
