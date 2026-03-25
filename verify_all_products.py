"""Verify all products: names, categories, prices using Gemini + Italian price cross-check."""
import sys, io, os, json, time, re, urllib.request
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\eukri\OneDrive\Documents\Claude Code\Credentials Claude Code\ai-agents-go-4c81b70995db.json"

from google.cloud.firestore_v1 import Client
from datetime import datetime, timezone
import google.auth, google.auth.transport.requests

db = Client(project="ai-agents-go", database="areda-product-catalogs")
now = datetime.now(timezone.utc).isoformat()

_creds, _ = google.auth.default(scopes=[
    "https://www.googleapis.com/auth/generative-language",
    "https://www.googleapis.com/auth/cloud-platform",
])
_creds.refresh(google.auth.transport.requests.Request())
EP = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

# Load all visible products
docs = list(db.collection("products").stream())
visible = [d for d in docs if d.to_dict().get("visible", True)]
visible.sort(key=lambda d: d.to_dict().get("name", ""))
print(f"Verifying {len(visible)} products...\n")

fixes = []
BATCH = 10

for start in range(0, len(visible), BATCH):
    chunk = visible[start : start + BATCH]

    products_text = ""
    for d in chunk:
        data = d.to_dict()
        ital_usd = data.get("italianRetailPriceUsd", 0) or 0
        ital_brand = data.get("italianBrand", "")
        ital_model = data.get("italianModel", "")
        products_text += (
            f"ID: {d.id}\n"
            f"Name: {data.get('name','')}\n"
            f"Chinese name: {data.get('nameCn','')}\n"
            f"Category: {data['category']}\n"
            f"Dimensions: {data.get('dimensions','')}\n"
            f"Material: {data.get('material','')}\n"
            f"Image description: {data.get('imageDescription','')}\n"
            f"Price RMB: {data.get('retailPriceRmb',0)}\n"
            f"Price USD (Areda): {data.get('retailPriceUsd',0)}\n"
            f"Italian original: {ital_brand} {ital_model} at USD {ital_usd}\n"
            f"---\n"
        )

    prompt = (
        "You are verifying a Chinese furniture product database. For EACH product below, check:\n"
        "1. NAME: Does the English name match the Chinese name? Key terms: "
        "餐桌=dining table, 餐椅=dining chair, 沙发=sofa, 茶几=coffee table, "
        "边几=side table, 床=bed, 床头柜=nightstand, 书桌=desk, 柜=cabinet/sideboard, "
        "凳/墩=stool/ottoman, 吧椅=bar stool, 榻=daybed/bench, 转角=corner, 模块=modular\n"
        "2. CATEGORY: Is the category correct for this item?\n"
        "3. PRICE: Is the Areda price reasonable? Compare with the Italian original price. "
        "Areda should typically be 30-70% of Italian retail price. "
        "If Areda price > Italian price, something may be wrong (unless it includes multiple items). "
        "Also flag if Areda price seems unreasonable for the furniture type "
        "(e.g. a single chair over 50000 RMB is suspicious unless it's a premium piece).\n\n"
        "Only report items with REAL ERRORS. Output one JSON object per error line:\n"
        '{"id":"doc_id","issue":"description","correctName":"new name or empty","correctCategory":"new category or empty","note":"explanation"}\n\n'
        "If ALL products in the batch are fine, output: {\"allOk\":true}\n\n"
        f"Products:\n{products_text}"
    )

    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 1500,
            "thinkingConfig": {"thinkingBudget": 0},
        },
    }

    if _creds.expired:
        _creds.refresh(google.auth.transport.requests.Request())

    try:
        req = urllib.request.Request(
            EP,
            data=json.dumps(body).encode(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {_creds.token}",
            },
        )
        resp = urllib.request.urlopen(req, timeout=30)
        result = json.loads(resp.read())
        text = result["candidates"][0]["content"]["parts"][0]["text"].strip()

        for match in re.finditer(r"\{[^}]+\}", text):
            try:
                obj = json.loads(match.group())
                if obj.get("allOk"):
                    continue
                if obj.get("id"):
                    fixes.append(obj)
                    print(
                        f"  FIX: {obj['id']:22s} {obj.get('issue','')[:50]:52s} "
                        f"-> name={obj.get('correctName','')[:25]} cat={obj.get('correctCategory','')}"
                    )
            except json.JSONDecodeError:
                pass
    except Exception as e:
        print(f"  ERROR batch {start}: {str(e)[:80]}")

    time.sleep(2)
    if (start + BATCH) % 50 == 0:
        print(f"  --- {start+BATCH}/{len(visible)} checked, {len(fixes)} issues ---")

print(f"\n=== TOTAL ISSUES: {len(fixes)} ===\n")

# Deduplicate
fix_map = {}
for f in fixes:
    fid = f.get("id", "")
    if fid and fid not in fix_map:
        fix_map[fid] = f

print(f"Unique products to fix: {len(fix_map)}")
for fid, f in sorted(fix_map.items()):
    print(
        f"  {fid:22s} {f.get('issue','')[:40]:42s} "
        f"name={f.get('correctName','')[:25]:27s} "
        f"cat={f.get('correctCategory',''):18s} "
        f"note={f.get('note','')[:60]}"
    )

# Save
with open("verification_fixes.json", "w", encoding="utf-8") as fp:
    json.dump(fix_map, fp, indent=2, ensure_ascii=False)
print(f"\nSaved to verification_fixes.json")

# ---- AUTO-APPLY FIXES ----
print(f"\n=== APPLYING {len(fix_map)} FIXES ===")
batch = db.batch()
batch_count = 0
applied = 0

for fid, f in fix_map.items():
    update = {"updatedAt": now, "verifiedAt": now}
    new_name = f.get("correctName", "")
    new_cat = f.get("correctCategory", "")
    note = f.get("note", "")

    if new_name:
        update["name"] = new_name
    if new_cat:
        update["category"] = new_cat
    if note:
        update["verificationNote"] = note

    if len(update) > 2:  # more than just timestamps
        batch.update(db.collection("products").document(fid), update)
        batch_count += 1
        applied += 1
        print(f"  Applied: {fid} -> {new_name or '(no name change)'} / {new_cat or '(no cat change)'}")

    if batch_count >= 400:
        batch.commit()
        batch = db.batch()
        batch_count = 0

if batch_count > 0:
    batch.commit()

print(f"\nApplied {applied} fixes to Firestore")
