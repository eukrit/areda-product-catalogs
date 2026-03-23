"""Use Gemini 2.5 Flash to describe and verify ALL product images."""
import os, json, time, urllib.request, base64, re

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\eukri\OneDrive\Documents\Claude Code\Credentials Claude Code\ai-agents-go-4c81b70995db.json"
from google.cloud.firestore_v1 import Client

db = Client(project="ai-agents-go", database="areda-product-catalogs")
API_KEY = "REDACTED_GEMINI_KEY"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

def call_gemini(img_b64, product_desc):
    body = {
        "contents": [{"parts": [
            {"inlineData": {"mimeType": "image/jpeg", "data": img_b64}},
            {"text": f"""Look at this furniture image and answer these 4 questions. Use | as separator.

1. DESCRIPTION: Describe the furniture shown in 2 sentences (type, style, color, material)
2. MATCH: Does this image match this product? "{product_desc}" Answer YES or NO
3. CATEGORY: Best category from this list: armchairs, sofas, modular-sofas, dining-chairs, lounge-chairs, coffee-tables, side-tables, dining-tables, console-tables, desks, beds, nightstands, sideboards, storage, lighting, accessories, outdoor
4. CONFIDENCE: 0-100 how confident you are

Format: DESCRIPTION|MATCH|CATEGORY|CONFIDENCE
Example: A modern gray fabric sofa with clean lines and metal legs.|YES|sofas|95"""}
        ]}],
        "generationConfig": {"temperature": 0.1, "maxOutputTokens": 200, "thinkingConfig": {"thinkingBudget": 0}}
    }
    req = urllib.request.Request(ENDPOINT, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    resp = urllib.request.urlopen(req, timeout=60)
    result = json.loads(resp.read())
    text = result["candidates"][0]["content"]["parts"][0]["text"].strip()
    # Parse pipe-separated response
    parts = text.split("|")
    if len(parts) >= 4:
        return {
            "description": parts[0].strip(),
            "match": "YES" in parts[1].upper(),
            "category": parts[2].strip().lower(),
            "confidence": int(re.search(r'\d+', parts[3]).group()) if re.search(r'\d+', parts[3]) else 50
        }
    # Fallback: just use the full text as description
    return {"description": text[:200], "match": True, "category": "", "confidence": 0}

docs = list(db.collection("products").stream())
docs.sort(key=lambda d: d.to_dict().get("name", ""))
print(f"Verifying {len(docs)} products...", flush=True)

mismatches = []
for i, doc in enumerate(docs):
    data = doc.to_dict()
    img_url = data.get("imageUrl", "")
    if not img_url:
        continue
    try:
        img_data = urllib.request.urlopen(img_url, timeout=15).read()
        img_b64 = base64.b64encode(img_data).decode()
        desc_text = f"{data['name']} - {data.get('nameCn','')} - {data['category']} - {data.get('dimensions','')}"
        result = call_gemini(img_b64, desc_text)

        icon = "Y" if result["match"] else "N"
        print(f"[{icon}][{result['confidence']:3d}] {data['name'][:40]:<42}| {result['description'][:60]}", flush=True)

        db.collection("products").document(doc.id).update({
            "imageDescription": result["description"],
            "imageVerified": result["match"],
            "suggestedCategory": result["category"]
        })

        if not result["match"]:
            mismatches.append({"id": doc.id, "name": data["name"],
                "current_cat": data["category"], "correct_cat": result["category"],
                "image_shows": result["description"]})

    except Exception as e:
        print(f"[E]     {data['name'][:40]:<42}| {str(e)[:50]}", flush=True)

    time.sleep(0.3)
    if (i+1) % 30 == 0:
        print(f"--- {i+1}/{len(docs)} ---", flush=True)

print(f"\nDONE: {len(docs)} products", flush=True)
print(f"Mismatches: {len(mismatches)}", flush=True)
for m in mismatches:
    print(f"  {m['name']}: {m['current_cat']} -> {m['correct_cat']}", flush=True)

with open("image_verification_results.json", "w", encoding="utf-8") as f:
    json.dump(mismatches, f, ensure_ascii=False, indent=2)
