export interface Product {
  id: string;
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
  category: ProductCategory;
  imageUrl: string;
  galleryUrls: string[];
  volumeCbm: number;
  priceExwUsd: number;
  priceFobUsd: number;
  priceRmb: number;
  listPriceUsd: number;
  exwPriceCny: number;
  retailPriceRmb: number;
  retailPriceUsd: number;
  exchangeRate: number;
  currency: string;
  moq: number;
  leadTimeDays: number;
  collection: string;
  tags: string[];
  visible: boolean;
  createdAt: string;
  updatedAt: string;
  // Italian original reference
  italianOriginalRef?: string;
  italianBrand?: string;
  italianModel?: string;
  italianDesigner?: string;
  italianRetailPriceEur?: number;
  italianRetailPriceUsd?: number;
  italianProductUrl?: string;
  italianOriginalMaterial?: string;
  italianOriginalDimensions?: string;
  italianMatchConfidence?: string;
  italianMatchReason?: string;
  italianSourceLinks?: { url: string; title: string }[];
  priceRatioItalianVsAreda?: number;
}

export type ProductCategory =
  | "dining-chairs"
  | "lounge-chairs"
  | "armchairs"
  | "sofas"
  | "modular-sofas"
  | "coffee-tables"
  | "side-tables"
  | "dining-tables"
  | "console-tables"
  | "desks"
  | "tables"
  | "beds"
  | "nightstands"
  | "sideboards"
  | "storage"
  | "lighting"
  | "accessories"
  | "outdoor"
  | "bar-stools"
  | "benches"
  | "ottomans";

export interface ProductFilter {
  category?: ProductCategory;
  collection?: string;
  search?: string;
  minPrice?: number;
  maxPrice?: number;
  sortBy?: "name" | "price-asc" | "price-desc" | "newest";
}

export interface CatalogMeta {
  id: string;
  name: string;
  vendor: string;
  totalProducts: number;
  lastUpdated: string;
  collections: string[];
  categories: ProductCategory[];
}
