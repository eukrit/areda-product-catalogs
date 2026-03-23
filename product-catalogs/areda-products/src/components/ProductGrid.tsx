"use client";

import { Product } from "@/types/product";
import { ProductCard } from "./ProductCard";

interface Props {
  products: Product[];
  loading?: boolean;
}

export function ProductGrid({ products, loading }: Props) {
  if (loading) {
    return (
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
    );
  }

  if (products.length === 0) {
    return (
      <div className="mx-auto max-w-7xl px-6 py-24 text-center md:px-8 lg:px-12">
        <p className="text-lg text-taupe">No products found.</p>
        <p className="mt-2 text-sm text-muted">Try adjusting your filters.</p>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-7xl px-6 py-8 md:px-8 lg:px-12">
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {products.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </div>
  );
}
