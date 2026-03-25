"""Seed all products to Firestore areda-product-catalogs"""
import json, os
from google.cloud.firestore_v1 import Client
from datetime import datetime, timezone

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\eukri\OneDrive\Documents\Claude Code\Credentials Claude Code\ai-agents-go-4c81b70995db.json"

db = Client(project="ai-agents-go", database="areda-product-catalogs")
now = datetime.now(timezone.utc).isoformat()

EXCHANGE_RATE = 7.2  # RMB per USD
RETAIL_MARKUP = 1.2  # 20% international markup

def compute_retail_usd(rmb: float) -> float:
    """Auto-convert RetailPriceRMB to RetailPriceUSD: RMB / exchangeRate * 1.2"""
    if rmb > 0:
        return round(rmb / EXCHANGE_RATE * RETAIL_MARKUP, 2)
    return 0

# Delete existing
print("Deleting existing products...")
for doc in db.collection("products").stream():
    db.collection("products").document(doc.id).delete()
print("Cleared.")

PRODUCTS = [
    {"productCode":"VIS23-DPX-1060A","brand":"VISCONTI","style":"Horizon","name":"Modular Sofa Single Module","nameCn":"地平线 单座模块","dimensions":"W1060 x D1060 x H650 mm","material":"FAB.1 220 fabric; Matte black legs","features":"Single seat module","category":"modular-sofas","priceExwUsd":689.44,"priceFobUsd":0,"volumeCbm":0,"moq":1,"collection":"Horizon","tags":["modular","sofa"]},
    {"productCode":"VIS23-DPX-1320A","brand":"VISCONTI","style":"Horizon","name":"Modular Sofa 2-Seat","nameCn":"地平线 双座模块","dimensions":"W1320 x D1060 x H650 mm","material":"FAB.1 1188 Velvet; Matte black legs","features":"2-seat module","category":"modular-sofas","priceExwUsd":858.19,"priceFobUsd":0,"volumeCbm":0,"moq":1,"collection":"Horizon","tags":["modular","sofa","velvet"]},
    {"productCode":"VIS23-DPX-2100A-L","brand":"VISCONTI","style":"Horizon","name":"Modular Left Chaise + Marble Table","nameCn":"地平线 左贵妃含茶几","dimensions":"W2100 x D1060 x H650 mm","material":"FAB.1 1188 Velvet; Carrara marble","features":"Left chaise, marble coffee table","category":"modular-sofas","priceExwUsd":1537.50,"priceFobUsd":0,"volumeCbm":0,"moq":1,"collection":"Horizon","tags":["modular","marble","chaise"]},
    {"productCode":"VIS23-DPX-2360A-L","brand":"VISCONTI","style":"Horizon","name":"Modular Left Corner A + Marble Table","nameCn":"地平线 左转角A含茶几","dimensions":"W2360 x D1060 x H650 mm","material":"FAB.1 1188 Velvet; Carrara marble","features":"Left corner A, marble table","category":"modular-sofas","priceExwUsd":1706.25,"priceFobUsd":0,"volumeCbm":0,"moq":1,"collection":"Horizon","tags":["modular","marble","l-shape"]},
    {"productCode":"VIS23-DPX-3170A-R","brand":"VISCONTI","style":"Horizon","name":"Modular Right L-Shape + Marble Table","nameCn":"地平线 右L型含茶几","dimensions":"W3170 x D1950 x H650 mm","material":"FAB.1 1188 Velvet; Carrara marble","features":"Right L-shape, marble table","category":"modular-sofas","priceExwUsd":2781.81,"priceFobUsd":0,"volumeCbm":0,"moq":1,"collection":"Horizon","tags":["modular","marble","l-shape"]},
    {"productCode":"VIS23-MDLA-1850A","brand":"VISCONTI","style":"Mondrian","name":"Coffee Table Large","nameCn":"蒙德里安 茶几 大","dimensions":"W1850 x D1000 x H340 mm","material":"Black Oak Veneer + Solid Wood Legs","features":"Large coffee table","category":"tables","priceExwUsd":583.89,"priceFobUsd":0,"volumeCbm":0,"moq":1,"collection":"Mondrian","tags":["table","oak"]},
    {"productCode":"VIS23-TLA-1800B","brand":"VISCONTI","style":"Trio","name":"Dining Table","nameCn":"三重奏 餐桌","dimensions":"W1800 x D900 x H750 mm","material":"Graphite lacquer legs; Mocha Oak top","features":"Dining table","category":"tables","priceExwUsd":910.69,"priceFobUsd":0,"volumeCbm":0,"moq":1,"collection":"Trio","tags":["table","dining","oak"]},
    {"productCode":"VIS01-SF-13B","brand":"VISCONTI","style":"Osman","name":"Modular Corner (Full Grain Leather)","nameCn":"奥斯曼 转角模块","dimensions":"W1050 x D1050 x H820 mm","material":"Full Grain Leather; 304 SS Gunmetal legs","features":"Corner module, full grain leather","category":"modular-sofas","priceExwUsd":1794.17,"priceFobUsd":0,"volumeCbm":0,"moq":1,"collection":"Osman","tags":["modular","leather","premium"]},
    {"productCode":"VIS23-LRE-940A","brand":"VISCONTI","style":"Laurel","name":"Lounge Chair 360 Swivel","nameCn":"劳瑞尔 休闲椅","dimensions":"W940 x D970 x H750 mm","material":"FAB.1 Modern Vintage; Mirror Gun Black metal; Ash wood","features":"360-degree swivel","category":"lounge-chairs","priceExwUsd":756.39,"priceFobUsd":0,"volumeCbm":1.0,"moq":1,"collection":"Laurel","tags":["swivel","lounge","modern"]},
    {"productCode":"VIS23-RN-900A","brand":"VISCONTI","style":"Ryan","name":"Single Sofa Litchi Leather","nameCn":"瑞恩 单人沙发","dimensions":"W900 x D920 x H980 mm","material":"Litchi SODA leather; FAB.1 fabric; Mirror SS legs","features":"Litchi leather shell, mirror SS legs","category":"sofas","priceExwUsd":920.40,"priceFobUsd":0,"volumeCbm":1.0,"moq":1,"collection":"Ryan","tags":["sofa","leather"]},
    {"productCode":"VIS01-QL-490A","brand":"VISCONTI","style":"P-Qiluo","name":"Dining Chair Cuoio Leather","nameCn":"齐洛 餐椅","dimensions":"W490 x D570 x H810 mm","material":"Ash wood + Italian Cuoio leather","features":"Italian cuoio leather","category":"dining-chairs","priceExwUsd":496.00,"priceFobUsd":0,"volumeCbm":0,"moq":1,"collection":"P-Qiluo","tags":["dining","leather","italian"]},
    {"productCode":"VIS16-NY-610A","brand":"VISCONTI","style":"Niya","name":"Dining Chair Ash","nameCn":"尼雅 餐椅 白蜡木","dimensions":"W610 x D600 x H790 mm","material":"Ash wood + FAB.2 fabric","features":"Solid ash wood frame","category":"dining-chairs","priceExwUsd":402.00,"priceFobUsd":0,"volumeCbm":0,"moq":1,"collection":"Niya","tags":["dining","ash","fabric"]},
    {"productCode":"VIS16-NY-610A-WAL","brand":"VISCONTI","style":"Niya","name":"Dining Chair Walnut","nameCn":"尼雅 餐椅 胡桃木","dimensions":"W610 x D600 x H790 mm","material":"Walnut wood + FAB.2 fabric","features":"Solid walnut frame","category":"dining-chairs","priceExwUsd":619.00,"priceFobUsd":0,"volumeCbm":0,"moq":1,"collection":"Niya","tags":["dining","walnut","fabric"]},
    {"productCode":"VIS-LINA","brand":"VISCONTI","style":"Lina","name":"Dining Chair GAMMA Leather","nameCn":"丽娜 餐椅","dimensions":"W480 x D520 x H800 mm","material":"Ash wood + GAMMA leather 666","features":"Italian GAMMA leather","category":"dining-chairs","priceExwUsd":317.00,"priceFobUsd":0,"volumeCbm":0,"moq":1,"collection":"Lina","tags":["dining","leather","italian"]},
    {"productCode":"VIS-SCHILLING","brand":"VISCONTI","style":"Schilling","name":"Dining Table White Marble","nameCn":"席勒 大理石餐桌","dimensions":"W1800 x D1000 x H750 mm","material":"Ash wood + White marble top","features":"Marble top, seats 6","category":"tables","priceExwUsd":1403.00,"priceFobUsd":0,"volumeCbm":2.0,"moq":1,"collection":"Schilling","tags":["table","marble","dining"]},
    {"productCode":"VIS-HOUSTON","brand":"VISCONTI","style":"Houston","name":"Bed King 180x200","nameCn":"休斯顿 大床","dimensions":"W2160 x D1960 x H490 mm","material":"Leather boxer 07","features":"King bed frame","category":"beds","priceExwUsd":1575.00,"priceFobUsd":0,"volumeCbm":3.45,"moq":1,"collection":"Houston","tags":["bed","leather","king"]},
    {"productCode":"VIS-SIMPSON","brand":"VISCONTI","style":"Simpson","name":"Bed King Simpson","nameCn":"辛普森 大床","dimensions":"W1960 x D2160 x H490 mm","material":"Leather boxer 07","features":"King bed frame","category":"beds","priceExwUsd":1506.00,"priceFobUsd":0,"volumeCbm":3.44,"moq":1,"collection":"Simpson","tags":["bed","leather","king"]},
    {"productCode":"VIS-BED-CUSTOM-180-FULL","brand":"VISCONTI","style":"Custom","name":"Bed King Full + Headboard","nameCn":"定制整套床含床头","dimensions":"W1960 x D2200 x H1200 mm","material":"Leather boxer 07","features":"Full bed with headboard","category":"beds","priceExwUsd":2545.00,"priceFobUsd":0,"volumeCbm":6.87,"moq":1,"collection":"Custom","tags":["bed","leather","headboard"]},
    {"productCode":"VIS-ROBERT","brand":"VISCONTI","style":"Robert","name":"Side Table Marble","nameCn":"罗伯特 边几","dimensions":"W610 x D450 x H530 mm","material":"Black oak + White marble","features":"Black oak, polished marble","category":"tables","priceExwUsd":291.00,"priceFobUsd":0,"volumeCbm":0.30,"moq":1,"collection":"Robert","tags":["side-table","marble"]},
    {"productCode":"VIS-WILDER","brand":"VISCONTI","style":"Wilder","name":"Side Table Round","nameCn":"怀尔德 圆边几","dimensions":"D500 x H500 mm","material":"Ash wood + Chrome SS","features":"Round side table","category":"tables","priceExwUsd":298.00,"priceFobUsd":0,"volumeCbm":0.27,"moq":1,"collection":"Wilder","tags":["side-table","ash"]},
    {"productCode":"VIS-CONSOLE-GOLD","brand":"VISCONTI","style":"Custom","name":"Console Table Gold-Plated","nameCn":"金色拉丝金属玄关柜","dimensions":"W1600 x D400 x H600 mm","material":"Gold-plated brushed metal","features":"Gold-plated metal","category":"tables","priceExwUsd":1190.00,"priceFobUsd":0,"volumeCbm":0.72,"moq":1,"collection":"Custom","tags":["console","gold"]},
    {"productCode":"VIS-CONSOLE-ASH-SS","brand":"VISCONTI","style":"Custom","name":"Console Table Ash + SS","nameCn":"白蜡木不锈钢玄关柜","dimensions":"W1830 x D380 x H780 mm","material":"Ash wood + Brushed SS","features":"Ash wood, brushed SS","category":"tables","priceExwUsd":1637.00,"priceFobUsd":0,"volumeCbm":0.54,"moq":1,"collection":"Custom","tags":["console","ash"]},
    {"productCode":"VIS-ARCAHORN-CONSOLE","brand":"VISCONTI","style":"Arcahorn","name":"Console Table Horn Inlays","nameCn":"牛角镶嵌漆面玄关柜","dimensions":"W1500 x D400 x H800 mm","material":"Black gloss lacquer, 24K gold brass, horn inlays","features":"24K gold, horn inlays","category":"tables","priceExwUsd":1333.00,"priceFobUsd":0,"volumeCbm":0.84,"moq":1,"collection":"Arcahorn","tags":["console","luxury","gold"]},
    {"productCode":"VIS-SOFA-GAMMA-3SEAT","brand":"VISCONTI","style":"Custom","name":"3-Seat Sofa Adjustable Back","nameCn":"三座沙发 可调靠背","dimensions":"W2130 x D1100 x H860 mm","material":"GAMMA leather boxer 08","features":"Adjustable backrest","category":"sofas","priceExwUsd":3061.00,"priceFobUsd":0,"volumeCbm":2.97,"moq":1,"collection":"Custom","tags":["sofa","leather","adjustable"]},
    {"productCode":"VIS-OTTOMAN-GAMMA","brand":"VISCONTI","style":"Custom","name":"Ottoman GAMMA Leather","nameCn":"脚凳","dimensions":"W1100 x D1100 x H430 mm","material":"GAMMA leather boxer 08","features":"Large square ottoman","category":"sofas","priceExwUsd":1286.00,"priceFobUsd":0,"volumeCbm":0.97,"moq":1,"collection":"Custom","tags":["ottoman","leather"]},
    {"productCode":"VIS-CT-MINOTTI-VENICE","brand":"VISCONTI","style":"Minotti","name":"Coffee Table Venice Brown Marble","nameCn":"威尼斯棕大理石茶几","dimensions":"W1480 x D800 x H280 mm","material":"Venice Brown marble + Mocha oak + gold-brown metal","features":"Venice brown marble","category":"tables","priceExwUsd":1200.00,"priceFobUsd":0,"volumeCbm":0.75,"moq":1,"collection":"Minotti","tags":["coffee-table","marble"]},
    {"productCode":"VIS-CHAIR-MAXALTO","brand":"VISCONTI","style":"Maxalto","name":"Lounge Chair GAMMA + Oak","nameCn":"休闲椅","dimensions":"W690 x D690 x H720 mm","material":"GAMMA leather 622 + Black OAK shell + BRONX fabric","features":"Leather-oak shell","category":"lounge-chairs","priceExwUsd":1327.00,"priceFobUsd":0,"volumeCbm":0.60,"moq":1,"collection":"Maxalto","tags":["lounge","leather","oak"]},
    {"productCode":"VIS-DESK-MINOTTI","brand":"VISCONTI","style":"Minotti","name":"Writing Desk Mocha Oak","nameCn":"书桌","dimensions":"W1800 x D600 x H730 mm","material":"Moka OAK + Lacquer + Bronze metal","features":"Mocha oak, bronze details","category":"tables","priceExwUsd":1151.00,"priceFobUsd":0,"volumeCbm":1.30,"moq":1,"collection":"Minotti","tags":["desk","oak","bronze"]},
    {"productCode":"VIS-DCHAIR-MINOTTI-49","brand":"VISCONTI","style":"Minotti","name":"Dining Armchair Mocha Oak","nameCn":"摩卡橡木餐扶手椅","dimensions":"W570 x D610 x H780 mm","material":"Leather boxer 49 + Mocha oak legs","features":"Dining armchair","category":"dining-chairs","priceExwUsd":612.00,"priceFobUsd":0,"volumeCbm":0.49,"moq":1,"collection":"Minotti","tags":["dining","leather","oak"]},
    {"productCode":"VIS-DTABLE-PORRO-MARBLE","brand":"VISCONTI","style":"Porro","name":"Round Dining Table Carrara","nameCn":"爵士白大理石圆餐桌","dimensions":"D1800 x H743 mm","material":"Carrara marble + SS + 90cm lazy susan","features":"Seats 6, lazy susan","category":"tables","priceExwUsd":3673.00,"priceFobUsd":0,"volumeCbm":3.61,"moq":1,"collection":"Porro","tags":["table","marble","round","luxury"]},
    {"productCode":"VIS-MARBLE-ST-BB","brand":"VISCONTI","style":"B&B Italia","name":"Side Table Port Laurent Marble","nameCn":"劳伦黑金大理石边几","dimensions":"W390 x D390 x H260 mm","material":"Port Laurent marble + Matt SS","features":"Black-gold marble","category":"tables","priceExwUsd":653.00,"priceFobUsd":0,"volumeCbm":0.12,"moq":1,"collection":"B&B Italia","tags":["side-table","marble","luxury"]},
    {"productCode":"VIS-OFFICE-GIORGETTI","brand":"VISCONTI","style":"Giorgetti","name":"Executive Office Chair","nameCn":"办公椅","dimensions":"W640 x D790 x H1260 mm","material":"Leather boxer 11 + 5-caster","features":"Executive, adjustable","category":"lounge-chairs","priceExwUsd":1531.00,"priceFobUsd":0,"volumeCbm":1.04,"moq":1,"collection":"Giorgetti","tags":["office","leather"]},
    {"productCode":"VIS-NS-CUSTOM-LEATHER","brand":"VISCONTI","style":"Custom","name":"Night Stand Leather","nameCn":"皮质床头柜","dimensions":"W400 x D400 x H450 mm","material":"Leather boxer 10","features":"Leather-wrapped","category":"storage","priceExwUsd":655.00,"priceFobUsd":0,"volumeCbm":0.17,"moq":1,"collection":"Custom","tags":["nightstand","leather"]},
    {"productCode":"VIS-FETES-2","brand":"VISCONTI","style":"Fetes","name":"Night Stand White Lacquer","nameCn":"费特斯 床头柜","dimensions":"W480 x D480 x H480 mm","material":"White lacquer + Gun metal base","features":"Cubic, white lacquer","category":"storage","priceExwUsd":455.00,"priceFobUsd":0,"volumeCbm":0.25,"moq":1,"collection":"Fetes","tags":["nightstand","lacquer"]},
    {"productCode":"VIS-CLOSET-PORRO","brand":"VISCONTI","style":"Porro","name":"Walk-in Closet Cabinet","nameCn":"衣帽间柜","dimensions":"W620 x D540 x H740 mm","material":"Leather boxer 20 + Bronze metal","features":"Leather, bronze hardware","category":"storage","priceExwUsd":755.00,"priceFobUsd":0,"volumeCbm":0.47,"moq":1,"collection":"Porro","tags":["storage","leather"]},
    {"productCode":"VIS-BENCH-MOLTENI","brand":"VISCONTI","style":"Molteni","name":"Bathroom Bench","nameCn":"浴室长凳","dimensions":"W1800 x D400 x H420 mm","material":"SODA leather 17 + Chrome legs","features":"Low bench","category":"sofas","priceExwUsd":1388.00,"priceFobUsd":0,"volumeCbm":0.64,"moq":1,"collection":"Molteni","tags":["bench","leather"]},
    {"productCode":"VIS-CUSHION-GAMMA","brand":"VISCONTI","style":"Custom","name":"Throw Cushion Leather","nameCn":"靠垫","dimensions":"W670 x D300 x H100 mm","material":"GAMMA leather boxer 08","features":"Decorative cushion","category":"accessories","priceExwUsd":122.00,"priceFobUsd":0,"volumeCbm":0.10,"moq":4,"collection":"Custom","tags":["cushion","leather"]},
    {"productCode":"VIS-SAMPLE-BOX","brand":"VISCONTI","style":"Samples","name":"Material Sample Box Set","nameCn":"材料样品盒","dimensions":"W400 x D360 x H150 (3 boxes)","material":"FABRIC+LEATHER+METAL+MARBLE+LACQUER","features":"Complete sample set, 31KG","category":"accessories","priceExwUsd":2143.00,"priceFobUsd":0,"volumeCbm":0,"moq":1,"collection":"Custom","tags":["samples"]},
    {"productCode":"HW4-SZ001-V02","brand":"VISCONTI","style":"Hardware","name":"SZ001 Hardware Unit V02","nameCn":"","dimensions":"","material":"","features":"","category":"accessories","priceExwUsd":0,"priceFobUsd":175.60,"volumeCbm":0.21406,"moq":1,"collection":"Visconti Accessories","tags":["hardware"]},
    {"productCode":"HW5-SD001-V01","brand":"VISCONTI","style":"Hardware","name":"SD001 Hardware Unit V01","nameCn":"","dimensions":"","material":"","features":"","category":"accessories","priceExwUsd":0,"priceFobUsd":72.30,"volumeCbm":0.053868,"moq":1,"collection":"Visconti Accessories","tags":["hardware"]},
    {"productCode":"HW1-S723","brand":"VISCONTI","style":"Kids","name":"Doodle Chalkboard L120","nameCn":"","dimensions":"150.4 x 9.3 x 1 cm","material":"PE + plastic","features":"Wall-mountable chalkboard","category":"accessories","priceExwUsd":0,"priceFobUsd":202.86,"volumeCbm":0.11968,"moq":1,"collection":"Visconti Kids","tags":["kids","chalkboard"]},
    {"productCode":"HW1-S237","brand":"VISCONTI","style":"Kids","name":"Balance Stumps Set of 12","nameCn":"","dimensions":"dia 15cm each","material":"Wood","features":"12 balance stumps","category":"accessories","priceExwUsd":0,"priceFobUsd":251.95,"volumeCbm":0.163296,"moq":1,"collection":"Visconti Kids","tags":["kids","wood"]},
    {"productCode":"VIS-TRINITY-OUTDOOR-WOOD","brand":"VISCONTI","style":"Trinity","name":"Outdoor Armchair Mangrove","nameCn":"户外红树木扶手椅","dimensions":"W800 x D800 x H640 mm","material":"Mangrove wood + Waterproof fabric","features":"Outdoor, mangrove wood","category":"outdoor","priceExwUsd":0,"priceFobUsd":0,"volumeCbm":0,"moq":1,"collection":"Trinity Hotel","tags":["outdoor","wood"]},
    {"productCode":"VIS-TRINITY-OUTDOOR-ALU","brand":"VISCONTI","style":"Trinity","name":"Outdoor Armchair Aluminum","nameCn":"户外铝合金扶手椅","dimensions":"W790 x D790 x H590 mm","material":"Aluminum powder coated + Waterproof fabric","features":"Outdoor, aluminum","category":"outdoor","priceExwUsd":0,"priceFobUsd":0,"volumeCbm":0,"moq":1,"collection":"Trinity Hotel","tags":["outdoor","aluminum"]},
    {"productCode":"VIS-TRINITY-SOFA-OUT","brand":"VISCONTI","style":"Trinity","name":"Outdoor 2-Seater Sofa","nameCn":"户外双座沙发","dimensions":"W1600 x D800 x H600 mm","material":"Aluminum powder coated + Waterproof fabric","features":"Outdoor 2-seater","category":"outdoor","priceExwUsd":0,"priceFobUsd":0,"volumeCbm":0,"moq":1,"collection":"Trinity Hotel","tags":["outdoor","sofa"]},
    {"productCode":"VIS-DCHAIR-MINOTTI-33","brand":"VISCONTI","style":"Minotti","name":"Dining Armchair SODA Leather","nameCn":"SODA 餐扶手椅","dimensions":"W570 x D610 x H780 mm","material":"SODA leather 33 + Mocha oak legs","features":"SODA leather dining armchair","category":"dining-chairs","priceExwUsd":571.00,"priceFobUsd":0,"volumeCbm":0.49,"moq":1,"collection":"Minotti","tags":["dining","leather","oak"]},
    {"productCode":"VIS-SOFA-GAMMA-1SEAT","brand":"VISCONTI","style":"Custom","name":"Single Sofa Adjustable Back","nameCn":"单座沙发 可调靠背","dimensions":"W900 x D1100 x H860 mm","material":"GAMMA leather boxer 08","features":"Adjustable backrest","category":"sofas","priceExwUsd":1347.00,"priceFobUsd":0,"volumeCbm":1.32,"moq":1,"collection":"Custom","tags":["sofa","leather","adjustable"]},
    {"productCode":"VIS22-TN-640A","brand":"VISCONTI","style":"Classic","name":"Dining Chair Mixed Material","nameCn":"餐椅","dimensions":"W640 x D625 x H830 mm","material":"FAB.2 fabric + Saddle leather; Sandblasted metal frame","features":"Mixed material upholstery","category":"dining-chairs","priceExwUsd":626.25,"priceFobUsd":0,"volumeCbm":0,"moq":1,"collection":"Visconti Classic","tags":["dining","leather","metal"]},
    {"productCode":"VIS24-XZ-555A","brand":"VISCONTI","style":"Classic","name":"Stool Napa Leather Woven","nameCn":"凳子","dimensions":"W555 x D360 x H440 mm","material":"Ash Black oak veneer; Napa GAMMA leather woven","features":"Compact stool, woven leather","category":"dining-chairs","priceExwUsd":265.83,"priceFobUsd":0,"volumeCbm":0,"moq":1,"collection":"Visconti Classic","tags":["stool","leather","ash"]},
]

print(f"Seeding {len(PRODUCTS)} products...")
batch = db.batch()
for i, p in enumerate(PRODUCTS):
    p.setdefault("imageUrl", "")
    p.setdefault("galleryUrls", [])
    p.setdefault("featuresCn", "")
    p.setdefault("materialCn", "")
    p.setdefault("styleCn", "")
    p.setdefault("currency", "USD")
    p.setdefault("leadTimeDays", 60)
    p.setdefault("retailPriceRmb", p.get("priceRmb", 0))
    p["retailPriceUsd"] = compute_retail_usd(p.get("retailPriceRmb", 0))
    p["exchangeRate"] = EXCHANGE_RATE
    p["visible"] = True
    p["createdAt"] = now
    p["updatedAt"] = now
    p.setdefault("model", p["productCode"])
    ref = db.collection("products").document(p["productCode"].lower().replace(" ", "-"))
    batch.set(ref, p)

batch.commit()

collections = sorted(set(p["collection"] for p in PRODUCTS if p.get("collection")))
categories = sorted(set(p["category"] for p in PRODUCTS))
db.collection("catalog-meta").document("visconti").set({
    "name": "Visconti Furniture",
    "vendor": "Visconti",
    "totalProducts": len(PRODUCTS),
    "lastUpdated": now,
    "collections": collections,
    "categories": categories,
})
print(f"Done: {len(PRODUCTS)} products")
print(f"Collections: {collections}")
print(f"Categories: {categories}")
