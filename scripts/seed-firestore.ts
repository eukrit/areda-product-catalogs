/**
 * Seed the areda-product-catalogs Firestore database
 * with Visconti product data extracted from quotation files.
 *
 * Usage: npx tsx scripts/seed-firestore.ts
 */

import { initializeApp, cert } from "firebase-admin/app";
import { getFirestore, FieldValue } from "firebase-admin/firestore";

// Initialize with ADC or service account
const app = initializeApp({ projectId: "ai-agents-go" });
const db = getFirestore(app, "areda-product-catalogs");

interface ProductSeed {
  productCode: string;
  brand: string;
  style: string;
  styleCn: string;
  name: string;
  nameCn: string;
  model: string;
  dimensions: string;
  material: string;
  materialCn: string;
  features: string;
  featuresCn: string;
  category: string;
  imageUrl: string;
  galleryUrls: string[];
  volumeCbm: number;
  priceExwUsd: number;
  priceFobUsd: number;
  currency: string;
  moq: number;
  leadTimeDays: number;
  collection: string;
  tags: string[];
  visible: boolean;
}

// ── Product data extracted from Visconti quotation files ──────────────
const PRODUCTS: ProductSeed[] = [
  {
    productCode: "VIS16-NY-610A",
    brand: "VISCONTI",
    style: "Classic",
    styleCn: "经典单椅",
    name: "Niya Dining Chair",
    nameCn: "餐椅 尼娅",
    model: "VIS16-NY-610A",
    dimensions: "W610 × D600 × H790 mm",
    material: "Walnut frame (N-series), Fabric/Faux leather upholstery",
    materialCn: "框架材质 N系列 胡桃, 主体材质 fabric/fake leather",
    features: "Solid wood frame, ergonomic backrest",
    featuresCn: "实木框架，人体工学靠背",
    category: "dining-chairs",
    imageUrl: "",
    galleryUrls: [],
    volumeCbm: 0,
    priceExwUsd: 618.55,
    priceFobUsd: 0,
    currency: "USD",
    moq: 6,
    leadTimeDays: 60,
    collection: "Visconti Classic",
    tags: ["walnut", "dining", "classic", "fabric"],
    visible: true,
  },
  {
    productCode: "VIS16-NY-610A-ASH",
    brand: "VISCONTI",
    style: "Classic",
    styleCn: "经典单椅",
    name: "Niya Dining Chair (Ash)",
    nameCn: "餐椅 尼娅 (白蜡木)",
    model: "VIS16-NY-610A",
    dimensions: "W610 × D600 × H790 mm",
    material: "Ash wood frame (smoked), FAB.2 CA01 upholstery",
    materialCn: "框架材质 N系列 白蜡 熏咖白蜡, 主体材质 FAB.2 CA01",
    features: "Solid wood frame, ergonomic backrest",
    featuresCn: "实木框架，人体工学靠背",
    category: "dining-chairs",
    imageUrl: "",
    galleryUrls: [],
    volumeCbm: 0,
    priceExwUsd: 401.9,
    priceFobUsd: 0,
    currency: "USD",
    moq: 8,
    leadTimeDays: 60,
    collection: "Visconti Classic",
    tags: ["ash", "dining", "classic", "fabric"],
    visible: true,
  },
  {
    productCode: "VIS23-LRE-940A",
    brand: "VISCONTI",
    style: "Modern",
    styleCn: "现代时尚",
    name: "Laurel Lounge Chair",
    nameCn: "休闲椅 劳瑞尔",
    model: "VIS23-LRE-940A",
    dimensions: "W940 × D970 × H750 mm",
    material: "FAB.2 mid-century fabric, Black wood veneer shell",
    materialCn: "主体材质 FAB.2 现代中古, 椅外壳 木皮 黑",
    features: "360° swivel base",
    featuresCn: "360°可旋转",
    category: "lounge-chairs",
    imageUrl: "",
    galleryUrls: [],
    volumeCbm: 0,
    priceExwUsd: 701.6,
    priceFobUsd: 0,
    currency: "USD",
    moq: 1,
    leadTimeDays: 60,
    collection: "Visconti Modern",
    tags: ["swivel", "lounge", "modern", "mid-century"],
    visible: true,
  },
  {
    productCode: "VIS23-RN-900A",
    brand: "VISCONTI",
    style: "Modern",
    styleCn: "现代时尚",
    name: "Ryan Single Sofa",
    nameCn: "单人沙发 瑞恩",
    model: "VIS23-RN-900A",
    dimensions: "W900 × D920 × H980 mm",
    material: "Litchi-grain leather shell (SODA 17), Fabric interior cushion",
    materialCn: "外壳+底框 荔枝纹 SODA, 内部+坐垫+头枕 Fabric",
    features: "Mirror-finish stainless steel legs",
    featuresCn: "镜面不锈钢金属腿",
    category: "sofas",
    imageUrl: "",
    galleryUrls: [],
    volumeCbm: 0,
    priceExwUsd: 920.4,
    priceFobUsd: 0,
    currency: "USD",
    moq: 1,
    leadTimeDays: 60,
    collection: "Visconti Modern",
    tags: ["leather", "sofa", "modern", "stainless-steel"],
    visible: true,
  },
  {
    productCode: "VIS23-DPX-1060A",
    brand: "VISCONTI",
    style: "Modern",
    styleCn: "现代时尚",
    name: "Horizon Modular Sofa (Single)",
    nameCn: "模块沙发 地平线 (单模块)",
    model: "VIS23-DPX-1060A",
    dimensions: "W1060 × D1060 × H650 mm",
    material: "FAB.2 minimalist fabric base, FAB cushions & back",
    materialCn: "底座 FAB.2 现代极简, 坐垫+靠背+靠包 FAB",
    features: "Black matte metal legs, modular configuration",
    featuresCn: "黑色哑光漆金属腿",
    category: "modular-sofas",
    imageUrl: "",
    galleryUrls: [],
    volumeCbm: 0,
    priceExwUsd: 782.6,
    priceFobUsd: 0,
    currency: "USD",
    moq: 1,
    leadTimeDays: 60,
    collection: "Visconti Modern",
    tags: ["modular", "sofa", "modern", "minimalist"],
    visible: true,
  },
  {
    productCode: "VIS23-DPX-2360A-L",
    brand: "VISCONTI",
    style: "Modern",
    styleCn: "现代时尚",
    name: "Horizon Modular Sofa (L-Shape)",
    nameCn: "模块沙发 地平线 (L型)",
    model: "VIS23-DPX-2360A-L",
    dimensions: "W2360 × D1060 × H650 mm",
    material: "FAB.2 minimalist fabric base, FAB cushions & back",
    materialCn: "底座 FAB.2 现代极简, 坐垫+靠背+靠包 FAB",
    features: "Black matte metal legs, L-shaped configuration",
    featuresCn: "黑色哑光漆金属腿, L型配置",
    category: "modular-sofas",
    imageUrl: "",
    galleryUrls: [],
    volumeCbm: 0,
    priceExwUsd: 1670.5,
    priceFobUsd: 0,
    currency: "USD",
    moq: 1,
    leadTimeDays: 60,
    collection: "Visconti Modern",
    tags: ["modular", "sofa", "modern", "l-shape"],
    visible: true,
  },
  // ── From Quotation20260318 files ──
  {
    productCode: "HW4-SZ001-V02",
    brand: "VISCONTI",
    style: "Hardware",
    styleCn: "",
    name: "SZ001 Hardware Unit V02",
    nameCn: "",
    model: "HW4-SZ001-V02",
    dimensions: "",
    material: "",
    materialCn: "",
    features: "",
    featuresCn: "",
    category: "accessories",
    imageUrl: "",
    galleryUrls: [],
    volumeCbm: 0.21406,
    priceExwUsd: 0,
    priceFobUsd: 175.6,
    currency: "USD",
    moq: 1,
    leadTimeDays: 60,
    collection: "Visconti Accessories",
    tags: ["hardware"],
    visible: true,
  },
  {
    productCode: "HW5-SD001-V01",
    brand: "VISCONTI",
    style: "Hardware",
    styleCn: "",
    name: "SD001 Hardware Unit V01",
    nameCn: "",
    model: "HW5-SD001-V01",
    dimensions: "",
    material: "",
    materialCn: "",
    features: "",
    featuresCn: "",
    category: "accessories",
    imageUrl: "",
    galleryUrls: [],
    volumeCbm: 0.053868,
    priceExwUsd: 0,
    priceFobUsd: 72.3,
    currency: "USD",
    moq: 1,
    leadTimeDays: 60,
    collection: "Visconti Accessories",
    tags: ["hardware"],
    visible: true,
  },
  {
    productCode: "HW1-S723",
    brand: "VISCONTI",
    style: "Kids",
    styleCn: "",
    name: "Doodle Chalkboard L120",
    nameCn: "",
    model: "HW1-S723",
    dimensions: "150.4 × 9.3 × 1 cm",
    material: "PE + plastic",
    materialCn: "",
    features: "Chalkboard surface, wall-mountable",
    featuresCn: "",
    category: "accessories",
    imageUrl: "",
    galleryUrls: [],
    volumeCbm: 0.11968,
    priceExwUsd: 0,
    priceFobUsd: 202.86,
    currency: "USD",
    moq: 1,
    leadTimeDays: 60,
    collection: "Visconti Kids",
    tags: ["kids", "chalkboard", "play"],
    visible: true,
  },
  {
    productCode: "HW1-S237",
    brand: "VISCONTI",
    style: "Kids",
    styleCn: "",
    name: "Balance Stumps Set of 12",
    nameCn: "",
    model: "HW1-S237",
    dimensions: "Diameter 15 cm each",
    material: "Wood",
    materialCn: "",
    features: "Set of 12 balance stumps for play",
    featuresCn: "",
    category: "accessories",
    imageUrl: "",
    galleryUrls: [],
    volumeCbm: 0.163296,
    priceExwUsd: 0,
    priceFobUsd: 251.95,
    currency: "USD",
    moq: 1,
    leadTimeDays: 60,
    collection: "Visconti Kids",
    tags: ["kids", "wood", "play", "balance"],
    visible: true,
  },
];

async function seed() {
  console.log("Seeding areda-product-catalogs database...");
  console.log(`Database: areda-product-catalogs (asia-southeast1)`);
  console.log(`Products to seed: ${PRODUCTS.length}`);

  const batch = db.batch();
  const now = new Date().toISOString();

  for (const p of PRODUCTS) {
    const ref = db.collection("products").doc();
    batch.set(ref, {
      ...p,
      createdAt: now,
      updatedAt: now,
    });
    console.log(`  + ${p.productCode}: ${p.name}`);
  }

  // Catalog metadata
  const collections = [...new Set(PRODUCTS.map((p) => p.collection))];
  const categories = [...new Set(PRODUCTS.map((p) => p.category))];

  const metaRef = db.collection("catalog-meta").doc("visconti");
  batch.set(metaRef, {
    name: "Visconti Furniture",
    vendor: "Visconti",
    totalProducts: PRODUCTS.length,
    lastUpdated: now,
    collections,
    categories,
  });

  await batch.commit();
  console.log(`\nSeeded ${PRODUCTS.length} products + catalog metadata.`);
  console.log("Collections:", collections);
  console.log("Categories:", categories);
}

seed().catch(console.error);
