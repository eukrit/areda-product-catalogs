"use client";

import Image from "next/image";
import Link from "next/link";
import { useAuth } from "@/lib/auth-context";
import { Product } from "@/types/product";

interface Props {
  product: Product;
}

export function ProductCard({ product }: Props) {
  const { isInternal } = useAuth();

  const categoryLabel = product.category
    .replace(/-/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());

  return (
    <Link href={`/product/${product.id}`}>
      <article className="product-card group overflow-hidden rounded-lg border border-border bg-areda-white">
        {/* Image */}
        <div className="relative aspect-[4/3] overflow-hidden bg-surface-cream">
          {product.imageUrl ? (
            <Image
              src={product.imageUrl}
              alt={product.name}
              fill
              unoptimized
              className="object-cover transition-transform duration-500 group-hover:scale-105"
              sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
            />
          ) : (
            <div className="absolute inset-0 flex items-center justify-center text-taupe">
              <svg
                width="48"
                height="48"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1"
              >
                <rect x="3" y="3" width="18" height="18" rx="2" />
                <circle cx="8.5" cy="8.5" r="1.5" />
                <path d="m21 15-5-5L5 21" />
              </svg>
            </div>
          )}
        </div>

        {/* Info */}
        <div className="p-4">
          <p className="overline mb-1 text-taupe">{categoryLabel}</p>
          <h3 className="mb-1 text-base font-semibold leading-snug text-charcoal">
            {product.name}
          </h3>
          <p className="mb-2 text-sm text-taupe">{product.productCode}</p>

          {product.dimensions && (
            <p className="caption text-muted">{product.dimensions}</p>
          )}

          {/* Price — only visible to internal users */}
          {isInternal && (
            <div className="price-reveal mt-3 border-t border-border pt-3">
              <div className="flex items-baseline gap-3">
                {product.priceFobUsd > 0 && (
                  <span className="text-base font-bold text-charcoal">
                    ${product.priceFobUsd.toLocaleString("en-US", {
                      minimumFractionDigits: 2,
                    })}
                  </span>
                )}
                {product.priceExwUsd > 0 && product.priceExwUsd !== product.priceFobUsd && (
                  <span className="text-xs text-taupe">
                    EXW ${product.priceExwUsd.toLocaleString("en-US", {
                      minimumFractionDigits: 2,
                    })}
                  </span>
                )}
              </div>
              <p className="caption mt-1 text-muted">FOB Shanghai (USD)</p>
            </div>
          )}
        </div>
      </article>
    </Link>
  );
}
