"use client";

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

  // Compute display price: prefer FOB USD, else convert RMB -> USD (÷7.25) then ×2.0 markup
  const RMB_TO_USD = 7.25;
  const MARKUP = 2.0;
  const displayPrice =
    product.priceFobUsd > 0
      ? product.priceFobUsd
      : product.priceExwUsd > 0
        ? product.priceExwUsd
        : product.priceRmb > 0
          ? (product.priceRmb / RMB_TO_USD) * MARKUP
          : 0;

  return (
    <Link href={`/product/${product.id}`}>
      <article className="product-card group overflow-hidden rounded-lg border border-border bg-areda-white">
        {/* Image */}
        <div className="relative aspect-[4/3] overflow-hidden bg-surface-cream">
          {product.imageUrl ? (
            /* eslint-disable-next-line @next/next/no-img-element */
            <img
              src={product.imageUrl}
              alt={product.name}
              loading="lazy"
              className="absolute inset-0 h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
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
          {isInternal && displayPrice > 0 && (
            <div className="price-reveal mt-3 border-t border-border pt-3">
              <div className="flex items-baseline gap-3">
                <span className="text-base font-bold text-charcoal">
                  ${displayPrice.toLocaleString("en-US", {
                    minimumFractionDigits: 0,
                    maximumFractionDigits: 0,
                  })}
                </span>
                {product.priceRmb > 0 && !product.priceFobUsd && !product.priceExwUsd && (
                  <span className="text-xs text-taupe">
                    (¥{product.priceRmb.toLocaleString("zh-CN")})
                  </span>
                )}
              </div>
              <p className="caption mt-1 text-muted">
                USD est. · Excl. delivery &amp; installation
              </p>
            </div>
          )}
        </div>
      </article>
    </Link>
  );
}
