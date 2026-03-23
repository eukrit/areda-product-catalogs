"""Seed areda-product-catalogs via Firestore REST API. Token passed as argv[1]."""
import json, urllib.request, sys

token = sys.argv[1]
PROJECT = "ai-agents-go"
DATABASE = "areda-product-catalogs"
BASE = f"https://firestore.googleapis.com/v1/projects/{PROJECT}/databases/{DATABASE}/documents"
NOW = "2026-03-23T11:30:00Z"

def to_fv(val):
    if isinstance(val, bool): return {"booleanValue": val}
    elif isinstance(val, int): return {"integerValue": str(val)}
    elif isinstance(val, float): return {"doubleValue": val}
    elif isinstance(val, str): return {"stringValue": val}
    elif isinstance(val, list): return {"arrayValue": {"values": [to_fv(v) for v in val]}}
    return {"stringValue": str(val)}

def create_doc(coll, doc_id, data):
    url = f"{BASE}/{coll}?documentId={doc_id}"
    fields = {k: to_fv(v) for k, v in data.items()}
    body = json.dumps({"fields": fields}).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    try:
        resp = urllib.request.urlopen(req)
        return resp.status
    except urllib.error.HTTPError as e:
        print(f"  ERR {e.code}: {e.read().decode()[:200]}")
        return e.code

PRODUCTS = [
    {"productCode": "VIS16-NY-610A", "brand": "VISCONTI", "style": "Classic", "name": "Niya Dining Chair", "nameCn": "餐椅 尼娅", "dimensions": "W610 x D600 x H790 mm", "material": "Walnut frame (N-series), Fabric/Faux leather upholstery", "features": "Solid wood frame, ergonomic backrest", "category": "dining-chairs", "imageUrl": "", "galleryUrls": [], "volumeCbm": 0.0, "priceExwUsd": 618.55, "priceFobUsd": 0.0, "currency": "USD", "moq": 6, "leadTimeDays": 60, "collection": "Visconti Classic", "tags": ["walnut", "dining", "classic", "fabric"], "visible": True},
    {"productCode": "VIS16-NY-610A-ASH", "brand": "VISCONTI", "style": "Classic", "name": "Niya Dining Chair (Ash)", "nameCn": "餐椅 尼娅 白蜡木", "dimensions": "W610 x D600 x H790 mm", "material": "Ash wood frame (smoked), FAB.2 CA01 upholstery", "features": "Solid wood frame, ergonomic backrest", "category": "dining-chairs", "imageUrl": "", "galleryUrls": [], "volumeCbm": 0.0, "priceExwUsd": 401.9, "priceFobUsd": 0.0, "currency": "USD", "moq": 8, "leadTimeDays": 60, "collection": "Visconti Classic", "tags": ["ash", "dining", "classic", "fabric"], "visible": True},
    {"productCode": "VIS23-LRE-940A", "brand": "VISCONTI", "style": "Modern", "name": "Laurel Lounge Chair", "nameCn": "休闲椅 劳瑞尔", "dimensions": "W940 x D970 x H750 mm", "material": "FAB.2 mid-century fabric, Black wood veneer shell", "features": "360 degree swivel base", "category": "lounge-chairs", "imageUrl": "", "galleryUrls": [], "volumeCbm": 0.0, "priceExwUsd": 701.6, "priceFobUsd": 0.0, "currency": "USD", "moq": 1, "leadTimeDays": 60, "collection": "Visconti Modern", "tags": ["swivel", "lounge", "modern", "mid-century"], "visible": True},
    {"productCode": "VIS23-RN-900A", "brand": "VISCONTI", "style": "Modern", "name": "Ryan Single Sofa", "nameCn": "单人沙发 瑞恩", "dimensions": "W900 x D920 x H980 mm", "material": "Litchi-grain leather shell, Fabric interior cushion", "features": "Mirror-finish stainless steel legs", "category": "sofas", "imageUrl": "", "galleryUrls": [], "volumeCbm": 0.0, "priceExwUsd": 920.4, "priceFobUsd": 0.0, "currency": "USD", "moq": 1, "leadTimeDays": 60, "collection": "Visconti Modern", "tags": ["leather", "sofa", "modern", "stainless-steel"], "visible": True},
    {"productCode": "VIS23-DPX-1060A", "brand": "VISCONTI", "style": "Modern", "name": "Horizon Modular Sofa (Single)", "nameCn": "模块沙发 地平线", "dimensions": "W1060 x D1060 x H650 mm", "material": "FAB.2 minimalist fabric base, FAB cushions", "features": "Black matte metal legs, modular configuration", "category": "modular-sofas", "imageUrl": "", "galleryUrls": [], "volumeCbm": 0.0, "priceExwUsd": 782.6, "priceFobUsd": 0.0, "currency": "USD", "moq": 1, "leadTimeDays": 60, "collection": "Visconti Modern", "tags": ["modular", "sofa", "modern", "minimalist"], "visible": True},
    {"productCode": "VIS23-DPX-2360A-L", "brand": "VISCONTI", "style": "Modern", "name": "Horizon Modular Sofa (L-Shape)", "nameCn": "模块沙发 地平线 L型", "dimensions": "W2360 x D1060 x H650 mm", "material": "FAB.2 minimalist fabric base, FAB cushions", "features": "Black matte metal legs, L-shape configuration", "category": "modular-sofas", "imageUrl": "", "galleryUrls": [], "volumeCbm": 0.0, "priceExwUsd": 1670.5, "priceFobUsd": 0.0, "currency": "USD", "moq": 1, "leadTimeDays": 60, "collection": "Visconti Modern", "tags": ["modular", "sofa", "modern", "l-shape"], "visible": True},
    {"productCode": "HW4-SZ001-V02", "brand": "VISCONTI", "style": "Hardware", "name": "SZ001 Hardware Unit V02", "nameCn": "", "dimensions": "", "material": "", "features": "", "category": "accessories", "imageUrl": "", "galleryUrls": [], "volumeCbm": 0.21406, "priceExwUsd": 0.0, "priceFobUsd": 175.6, "currency": "USD", "moq": 1, "leadTimeDays": 60, "collection": "Visconti Accessories", "tags": ["hardware"], "visible": True},
    {"productCode": "HW5-SD001-V01", "brand": "VISCONTI", "style": "Hardware", "name": "SD001 Hardware Unit V01", "nameCn": "", "dimensions": "", "material": "", "features": "", "category": "accessories", "imageUrl": "", "galleryUrls": [], "volumeCbm": 0.053868, "priceExwUsd": 0.0, "priceFobUsd": 72.3, "currency": "USD", "moq": 1, "leadTimeDays": 60, "collection": "Visconti Accessories", "tags": ["hardware"], "visible": True},
    {"productCode": "HW1-S723", "brand": "VISCONTI", "style": "Kids", "name": "Doodle Chalkboard L120", "nameCn": "", "dimensions": "150.4 x 9.3 x 1 cm", "material": "PE + plastic", "features": "Chalkboard surface, wall-mountable", "category": "accessories", "imageUrl": "", "galleryUrls": [], "volumeCbm": 0.11968, "priceExwUsd": 0.0, "priceFobUsd": 202.86, "currency": "USD", "moq": 1, "leadTimeDays": 60, "collection": "Visconti Kids", "tags": ["kids", "chalkboard", "play"], "visible": True},
    {"productCode": "HW1-S237", "brand": "VISCONTI", "style": "Kids", "name": "Balance Stumps Set of 12", "nameCn": "", "dimensions": "dia 15 cm each", "material": "Wood", "features": "Set of 12 balance stumps", "category": "accessories", "imageUrl": "", "galleryUrls": [], "volumeCbm": 0.163296, "priceExwUsd": 0.0, "priceFobUsd": 251.95, "currency": "USD", "moq": 1, "leadTimeDays": 60, "collection": "Visconti Kids", "tags": ["kids", "wood", "play", "balance"], "visible": True},
]

print(f"Seeding {len(PRODUCTS)} products to areda-product-catalogs...")
ok = 0
for p in PRODUCTS:
    p["createdAt"] = NOW
    p["updatedAt"] = NOW
    doc_id = p["productCode"].lower()
    s = create_doc("products", doc_id, p)
    status_text = "OK" if s == 200 else "FAIL"
    print(f"  {status_text} {p['productCode']}: {p['name']}")
    if s == 200:
        ok += 1

colls = list(set(p["collection"] for p in PRODUCTS))
cats = list(set(p["category"] for p in PRODUCTS))
meta = {"name": "Visconti Furniture", "vendor": "Visconti", "totalProducts": len(PRODUCTS), "lastUpdated": NOW, "collections": colls, "categories": cats}
s = create_doc("catalog-meta", "visconti", meta)
status_text = "OK" if s == 200 else "FAIL"
print(f"  {status_text} catalog-meta/visconti")
print(f"\nDone! {ok}/{len(PRODUCTS)} products seeded successfully.")
