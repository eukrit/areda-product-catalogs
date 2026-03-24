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
  currency: string;
  moq: number;
  leadTimeDays: number;
  collection: string;
  tags: string[];
  visible: boolean;
  createdAt: string;
  updatedAt: string;
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
  | "outdoor";

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
