import {
  collection,
  getDocs,
  getDoc,
  doc,
  query,
  where,
  orderBy,
  limit,
  startAfter,
  DocumentSnapshot,
} from "firebase/firestore";
import { db } from "./firebase";
import { Product, ProductFilter } from "@/types/product";

const PRODUCTS_COLLECTION = "products";
const PAGE_SIZE = 24;
const DEFAULT_EXCHANGE_RATE = 7.2; // RMB per USD
const RETAIL_MARKUP = 1.2; // 20% international markup

/** Compute retailPriceUsd from retailPriceRmb if not already set */
export function withRetailUsd(product: Product): Product {
  const rmb = product.retailPriceRmb || 0;
  const rate = product.exchangeRate || DEFAULT_EXCHANGE_RATE;
  if (rmb > 0 && !product.retailPriceUsd) {
    return { ...product, retailPriceUsd: Math.round((rmb / rate) * RETAIL_MARKUP * 100) / 100 };
  }
  return product;
}

export async function getProducts(
  filter: ProductFilter = {},
  lastDoc?: DocumentSnapshot
): Promise<{ products: Product[]; lastVisible: DocumentSnapshot | null }> {
  let q = query(collection(db, PRODUCTS_COLLECTION), where("visible", "==", true));

  if (filter.category) {
    q = query(q, where("category", "==", filter.category));
  }

  if (filter.collection) {
    q = query(q, where("collection", "==", filter.collection));
  }

  switch (filter.sortBy) {
    case "price-asc":
      q = query(q, orderBy("priceFobUsd", "asc"));
      break;
    case "price-desc":
      q = query(q, orderBy("priceFobUsd", "desc"));
      break;
    case "newest":
      q = query(q, orderBy("createdAt", "desc"));
      break;
    default:
      q = query(q, orderBy("name", "asc"));
  }

  if (lastDoc) {
    q = query(q, startAfter(lastDoc));
  }

  q = query(q, limit(PAGE_SIZE));

  const snapshot = await getDocs(q);
  const products = snapshot.docs.map((d) => withRetailUsd({ id: d.id, ...d.data() } as Product));
  const lastVisible = snapshot.docs[snapshot.docs.length - 1] || null;

  return { products, lastVisible };
}

export async function getProduct(id: string): Promise<Product | null> {
  const snap = await getDoc(doc(db, PRODUCTS_COLLECTION, id));
  if (!snap.exists()) return null;
  return withRetailUsd({ id: snap.id, ...snap.data() } as Product);
}

export async function getCollections(): Promise<string[]> {
  const snap = await getDocs(collection(db, "catalog-meta"));
  const meta = snap.docs[0]?.data();
  return meta?.collections || [];
}

export async function getCategories(): Promise<string[]> {
  const snap = await getDocs(collection(db, "catalog-meta"));
  const meta = snap.docs[0]?.data();
  return meta?.categories || [];
}
