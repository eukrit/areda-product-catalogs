"""Seed areda-product-catalogs via Firestore REST API using gcloud access token."""

import json, subprocess, urllib.request, uuid
from datetime import datetime, timezone

# Get access token from gcloud
token = subprocess.check_output(
    ["gcloud", "auth", "print-access-token"], text=True
).strip()

PROJECT = "ai-agents-go"
DATABASE = "areda-product-catalogs"
BASE = f"https://firestore.googleapis.com/v1/projects/{PROJECT}/databases/{DATABASE}/documents"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def to_firestore_value(val):
    if isinstance(val, bool):
        return {"booleanValue": val}
    elif isinstance(val, int):
        return {"integerValue": str(val)}
    elif isinstance(val, float):
        return {"doubleValue": val}
    elif isinstance(val, str):
        return {"stringValue": val}
    elif isinstance(val, list):
        return {"arrayValue": {"values": [to_firestore_value(v) for v in val]}}
    elif val is None:
        return {"nullValue": None}
    return {"stringValue": str(val)}

def create_doc(collection, doc_id, data):
    url = f"{BASE}/{collection}?documentId={doc_id}"
    fields = {k: to_firestore_value(v) for k, v in data.items()}
    body = json.dumps({"fields": fields}).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    try:
        resp = urllib.request.urlopen(req)
        return resp.status
    except urllib.error.HTTPError as e:
        print(f"  ERROR {e.code}: {e.read().decode()[:200]}")
        return e.code

PRODUCTS = [
    {"productCode": "VIS16-NY-610A", "brand": "VISCONTI", "style": "Classic", "styleCn": "经典单椅", "name": "Niya Dining Chair", "nameCn": "餐椅 尼娅", "model": "VIS16-NY-610A", "dimensions": "W610 × D600 × H790 mm", "material": "Walnut frame (N-series), Fabric/Faux leather upholstery", "materialCn": "框架材质 N系列 胡桃", "features": "Solid wood frame, ergonomic backrest", "featuresCn": "实木框架，人体工学靠背", "category": "dining-chairs", "imageUrl": "", "galleryUrls": [], "volumeCbm": 0.0, "priceExwUsd": 618.55, "priceFobUsd": 0.0, "currency": "USD", "moq": 6, "leadTimeDays": 60, "collection": "Visconti Classic", "tags": ["walnut", "dining", "classic", "fabric"], "visible": True},
    {"productCode": "VIS16-NY-610A-ASH", "brand": "VISCONTI", "style": "Classic", "styleCn": "经典单椅", "name": "Niya Dining Chair (Ash)", "nameCn": "餐椅 尼娅 (白蜡木)", "model": "VIS16-NY-610A", "dimensions": "W610 × D600 × H790 mm", "material": "Ash wood frame (smoked), FAB.2 CA01 upholstery", "materialCn": "框架材质 白蜡 熏咖白蜡", "features": "Solid wood frame, ergonomic backrest", "featuresCn": "实木框架，人体工学靠背", "category": "dining-chairs", "imageUrl": "", "galleryUrls": [], "volumeCbm": 0.0, "priceExwUsd": 401.9, "priceFobUsd": 0.0, "currency": "USD", "moq": 8, "leadTimeDays": 60, "collection": "Visconti Classic", "tags": ["ash", "dining", "classic", "fabric"], "visible": True},
    {"productCode": "VIS23-LRE-940A", "brand": "VISCONTI", "style": "Modern", "styleCn": "现代时尚", "name": "Laurel Lounge Chair", "nameCn": "休闲椅 劳瑞尔", "model": "VIS23-LRE-940A", "dimensions": "W940 × D970 × H750 mm", "material": "FAB.2 mid-century fabric, Black wood veneer shell", "materialCn": "FAB.2 现代中古, 椅外壳 木皮 黑", "features": "360 degree swivel base", "featuresCn": "360°可旋转", "category": "lounge-chairs", "imageUrl": "", "galleryUrls": [], "volumeCbm": 0.0, "priceExwUsd": 701.6, "priceFobUsd": 0.0, "currency": "USD", "moq": 1, "leadTimeDays": 60, "collection": "Visconti Modern", "tags": ["swivel", "lounge", "modern", "mid-century"], "visible": True},
    {"productCode": "VIS23-RN-900A", "brand": "VISCONTI", "style": "Modern", "styleCn": "现代时尚", "name": "Ryan Single Sofa", "nameCn": "单人沙发 瑞恩", "model": "VIS23-RN-900A", "dimensions": "W900 × D920 × H980 mm", "material": "Litchi-grain leather shell, Fabric interior cushion", "materialCn": "荔枝纹 SODA, Fabric", "features": "Mirror-finish stainless steel legs", "featuresCn": "镜面不锈钢金属腿", "category": "sofas", "imageUrl": "", "galleryUrls": [], "volumeCbm": 0.0, "priceExwUsd": 920.4, "priceFobUsd": 0.0, "currency": "USD", "moq": 1, "leadTimeDays": 60, "collection": "Visconti Modern", "tags": ["leather", "sofa", "modern", "stainless-steel"], "visible": True},
    {"productCode": "VIS23-DPX-1060A", "brand": "VISCONTI", "style": "Modern", "styleCn": "现代时尚", "name": "Horizon Modular Sofa (Single)", "nameCn": "模块沙发 地平线", "model": "VIS23-DPX-1060A", "dimensions": "W1060 × D1060 × H650 mm", "material": "FAB.2 minimalist fabric base, FAB cushions", "materialCn": "FAB.2 现代极简", "features": "Black matte metal legs, modular", "featuresCn": "黑色哑光漆金属腿", "category": "modular-sofas", "imageUrl": "", "galleryUrls": [], "volumeCbm": 0.0, "priceExwUsd": 782.6, "priceFobUsd": 0.0, "currency": "USD", "moq": 1, "leadTimeDays": 60, "collection": "Visconti Modern", "tags": ["modular", "sofa", "modern", "minimalist"], "visible": True},
    {"productCode": "VIS23-DPX-2360A-L", "brand": "VISCONTI", "style": "Modern", "styleCn": "现代时尚", "name": "Horizon Modular Sofa (L-Shape)", "nameCn": "模块沙发 地平线 L型", "model": "VIS23-DPX-2360A-L", "dimensions": "W2360 × D1060 × H650 mm", "material": "FAB.2 minimalist fabric base, FAB cushions", "materialCn": "FAB.2 现代极简", "features": "Black matte metal legs, L-shape", "featuresCn": "黑色哑光漆金属腿, L型", "category": "modular-sofas", "imageUrl": "", "galleryUrls": [], "volumeCbm": 0.0, "priceExwUsd": 1670.5, "priceFobUsd": 0.0, "currency": "USD", "moq": 1, "leadTimeDays": 60, "collection": "Visconti Modern", "tags": ["modular", "sofa", "modern", "l-shape"], "visible": True},
    {"productCode": "HW4-SZ001-V02", "brand": "VISCONTI", "style": "Hardware", "styleCn": "", "name": "SZ001 Hardware Unit V02", "nameCn": "", "model": "HW4-SZ001-V02", "dimensions": "", "material": "", "materialCn": "", "features": "", "featuresCn": "", "category": "accessories", "imageUrl": "", "galleryUrls": [], "volumeCbm": 0.21406, "priceExwUsd": 0.0, "priceFobUsd": 175.6, "currency": "USD", "moq": 1, "leadTimeDays": 60, "collection": "Visconti Accessories", "tags": ["hardware"], "visible": True},
    {"productCode": "HW5-SD001-V01", "brand": "VISCONTI", "style": "Hardware", "styleCn": "", "name": "SD001 Hardware Unit V01", "nameCn": "", "model": "HW5-SD001-V01", "dimensions": "", "material": "", "materialCn": "", "features": "", "featuresCn": "", "category": "accessories", "imageUrl": "", "galleryUrls": [], "volumeCbm": 0.053868, "priceExwUsd": 0.0, "priceFobUsd": 72.3, "currency": "USD", "moq": 1, "leadTimeDays": 60, "collection": "Visconti Accessories", "tags": ["hardware"], "visible": True},
    {"productCode": "HW1-S723", "brand": "VISCONTI", "style": "Kids", "styleCn": "", "name": "Doodle Chalkboard L120", "nameCn": "", "model": "HW1-S723", "dimensions": "150.4 x 9.3 x 1 cm", "material": "PE + plastic", "materialCn": "", "features": "Chalkboard surface, wall-mountable", "featuresCn": "", "category": "accessories", "imageUrl": "", "galleryUrls": [], "volumeCbm": 0.11968, "priceExwUsd": 0.0, "priceFobUsd": 202.86, "currency": "USD", "moq": 1, "leadTimeDays": 60, "collection": "Visconti Kids", "tags": ["kids", "chalkboard", "play"], "visible": True},
    {"productCode": "HW1-S237", "brand": "VISCONTI", "style": "Kids", "styleCn": "", "name": "Balance Stumps Set of 12", "nameCn": "", "model": "HW1-S237", "dimensions": "dia 15 cm each", "material": "Wood", "materialCn": "", "features": "Set of 12 balance stumps", "featuresCn": "", "category": "accessories", "imageUrl": "", "galleryUrls": [], "volumeCbm": 0.163296, "priceExwUsd": 0.0, "priceFobUsd": 251.95, "currency": "USD", "moq": 1, "leadTimeDays": 60, "collection": "Visconti Kids", "tags": ["kids", "wood", "play", "balance"], "visible": True},
]

print(f"Seeding {len(PRODUCTS)} products to areda-product-catalogs...")

for p in PRODUCTS:
    p["createdAt"] = NOW
    p["updatedAt"] = NOW
    doc_id = p["productCode"].lower().replace(" ", "-")
    status = create_doc("products", doc_id, p)
    print(f"  {'OK' if status == 200 else 'FAIL'} {p['productCode']}: {p['name']}")

# Catalog metadata
collections = list(set(p["collection"] for p in PRODUCTS))
categories = list(set(p["category"] for p in PRODUCTS))
meta = {
    "name": "Visconti Furniture",
    "vendor": "Visconti",
    "totalProducts": len(PRODUCTS),
    "lastUpdated": NOW,
    "collections": collections,
    "categories": categories,
}
status = create_doc("catalog-meta", "visconti", meta)
print(f"\n  {'OK' if status == 200 else 'FAIL'} catalog-meta/visconti")
print(f"\nDone! {len(PRODUCTS)} products seeded.")
