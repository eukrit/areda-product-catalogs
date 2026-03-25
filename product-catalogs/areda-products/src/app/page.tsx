"use client";

import { useState, useEffect, useMemo, useRef, useCallback, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { collection, getDocs } from "firebase/firestore";
import { db } from "@/lib/firebase";
import { useAuth } from "@/lib/auth-context";
import { Product, ProductFilter, ProductCategory } from "@/types/product";
import { FilterBar } from "@/components/FilterBar";
import { ProductCard } from "@/components/ProductCard";

const PAGE_SIZE = 12;

export default function CatalogPageWrapper() {
  return (
    <Suspense fallback={<div className="mx-auto max-w-7xl px-6 py-16">Loading...</div>}>
      <CatalogPage />
    </Suspense>
  );
}

function CatalogPage() {
  const { isInternal } = useAuth();
  const searchParams = useSearchParams();
  const [allProducts, setAllProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<ProductFilter>(() => {
    const col = searchParams.get("collection");
    return col ? { collection: col } : {};
  });
  const [visibleCount, setVisibleCount] = useState(PAGE_SIZE);
  const [loadingMore, setLoadingMore] = useState(false);
  const sentinelRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    async function load() {
      try {
        const snap = await getDocs(collection(db, "products"));
        const products = snap.docs
          .map((d) => ({ id: d.id, ...d.data() } as Product))
          .filter((p) => p.visible !== false)
          .sort((a, b) => a.name.localeCompare(b.name));
        setAllProducts(products);
      } catch (err) {
        console.error("Failed to load products:", err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  // Extract available categories from loaded products
  const availableCategories = useMemo(() => {
    const cats = new Map<ProductCategory, number>();
    allProducts.forEach((p) => {
      cats.set(p.category, (cats.get(p.category) || 0) + 1);
    });
    return cats;
  }, [allProducts]);

  // Extract available collections
  const availableCollections = useMemo(() => {
    const cols = new Set<string>();
    allProducts.forEach((p) => {
      if (p.collection) cols.add(p.collection);
    });
    return Array.from(cols).sort();
  }, [allProducts]);

  // Filtered + sorted products
  const filtered = useMemo(() => {
    let result = [...allProducts];

    if (filter.category) {
      result = result.filter((p) => p.category === filter.category);
    }
    if (filter.collection) {
      result = result.filter((p) => p.collection === filter.collection);
    }
    if (filter.search) {
      const q = filter.search.toLowerCase();
      result = result.filter(
        (p) =>
          p.name.toLowerCase().includes(q) ||
          p.productCode.toLowerCase().includes(q) ||
          p.material?.toLowerCase().includes(q) ||
          p.style?.toLowerCase().includes(q)
      );
    }

    switch (filter.sortBy) {
      case "price-asc":
        result.sort((a, b) => (a.priceFobUsd || 0) - (b.priceFobUsd || 0));
        break;
      case "price-desc":
        result.sort((a, b) => (b.priceFobUsd || 0) - (a.priceFobUsd || 0));
        break;
      case "newest":
        result.sort(
          (a, b) =>
            new Date(b.createdAt || 0).getTime() -
            new Date(a.createdAt || 0).getTime()
        );
        break;
      default:
        result.sort((a, b) => a.name.localeCompare(b.name));
    }

    return result;
  }, [allProducts, filter]);

  // Reset visible count when filter changes
  useEffect(() => {
    setVisibleCount(PAGE_SIZE);
  }, [filter]);

  const visibleProducts = filtered.slice(0, visibleCount);
  const hasMore = visibleCount < filtered.length;

  // Infinite scroll via IntersectionObserver
  const loadMore = useCallback(() => {
    if (!hasMore || loadingMore) return;
    setLoadingMore(true);
    // Simulate a slight delay for smooth UX
    setTimeout(() => {
      setVisibleCount((prev) => Math.min(prev + PAGE_SIZE, filtered.length));
      setLoadingMore(false);
    }, 200);
  }, [hasMore, loadingMore, filtered.length]);

  useEffect(() => {
    const sentinel = sentinelRef.current;
    if (!sentinel) return;

    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          loadMore();
        }
      },
      { rootMargin: "200px" }
    );

    observer.observe(sentinel);
    return () => observer.disconnect();
  }, [loadMore]);

  return (
    <>
      {/* Hero */}
      <section className="w-full bg-surface-cream">
        <div className="mx-auto max-w-7xl px-6 py-16 md:px-8 lg:px-12">
          <h1 className="text-4xl font-bold tracking-tight text-charcoal md:text-5xl lg:text-6xl">
            Product Catalog
          </h1>
          <p className="mt-4 max-w-2xl text-lg leading-relaxed text-taupe">
            Explore our curated collection of furniture and interior pieces.
            Each product is crafted with attention to material, form, and
            function.
          </p>
        </div>
      </section>

      {/* Collection filter banner */}
      {filter.collection && (
        <div className="border-b border-border bg-charcoal text-areda-white">
          <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-3 md:px-8 lg:px-12">
            <span className="text-sm font-medium">
              Collection: <strong>{filter.collection}</strong>
            </span>
            <button
              onClick={() => setFilter({ ...filter, collection: undefined })}
              className="rounded-full bg-areda-white/20 px-3 py-1 text-xs font-medium hover:bg-areda-white/30 transition-colors"
            >
              Clear filter
            </button>
          </div>
        </div>
      )}

      {/* Category Pills */}
      <div className="border-b border-border bg-areda-white">
        <div className="mx-auto max-w-7xl px-6 py-4 md:px-8 lg:px-12">
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setFilter({ ...filter, category: undefined })}
              className={`rounded-full px-4 py-1.5 text-sm font-medium transition-colors ${
                !filter.category
                  ? "bg-charcoal text-areda-white"
                  : "bg-surface-cream text-charcoal hover:bg-cream"
              }`}
            >
              All ({allProducts.length})
            </button>
            {Array.from(availableCategories.entries())
              .sort(([a], [b]) => a.localeCompare(b))
              .map(([cat, count]) => {
                const label = cat
                  .replace(/-/g, " ")
                  .replace(/\b\w/g, (c) => c.toUpperCase());
                return (
                  <button
                    key={cat}
                    onClick={() =>
                      setFilter({
                        ...filter,
                        category: filter.category === cat ? undefined : cat,
                      })
                    }
                    className={`rounded-full px-4 py-1.5 text-sm font-medium transition-colors ${
                      filter.category === cat
                        ? "bg-charcoal text-areda-white"
                        : "bg-surface-cream text-charcoal hover:bg-cream"
                    }`}
                  >
                    {label} ({count})
                  </button>
                );
              })}
          </div>
        </div>
      </div>

      {/* Search & Sort */}
      <FilterBar
        filter={filter}
        onFilterChange={setFilter}
        showPriceSort={isInternal}
        totalCount={filtered.length}
        collections={availableCollections}
      />

      {/* Product Grid */}
      {loading ? (
        <div className="mx-auto max-w-7xl px-6 py-8 md:px-8 lg:px-12">
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {Array.from({ length: 8 }).map((_, i) => (
              <div key={i} className="animate-pulse">
                <div className="aspect-[4/3] rounded-lg bg-surface-cream" />
                <div className="mt-4 space-y-2">
                  <div className="h-3 w-16 rounded bg-surface-cream" />
                  <div className="h-5 w-3/4 rounded bg-surface-cream" />
                  <div className="h-3 w-1/2 rounded bg-surface-cream" />
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : filtered.length === 0 ? (
        <div className="mx-auto max-w-7xl px-6 py-24 text-center md:px-8 lg:px-12">
          <p className="text-lg text-taupe">No products found.</p>
          <p className="mt-2 text-sm text-muted">Try adjusting your filters.</p>
        </div>
      ) : (
        <div className="mx-auto max-w-7xl px-6 py-8 md:px-8 lg:px-12">
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {visibleProducts.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>

          {/* Infinite scroll sentinel */}
          {hasMore && (
            <div ref={sentinelRef} className="flex items-center justify-center py-12">
              <div className="flex items-center gap-3 text-sm text-taupe">
                <svg
                  className="h-5 w-5 animate-spin text-taupe"
                  viewBox="0 0 24 24"
                  fill="none"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  />
                </svg>
                Loading more products...
              </div>
            </div>
          )}

          {/* End indicator */}
          {!hasMore && filtered.length > PAGE_SIZE && (
            <p className="py-8 text-center text-sm text-taupe">
              Showing all {filtered.length} products
            </p>
          )}
        </div>
      )}
    </>
  );
}
