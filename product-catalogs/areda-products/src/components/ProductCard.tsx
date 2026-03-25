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

  const listPrice = product.listPriceUsd || 0;
  const exwCny = product.exwPriceCny || 0;
  const retailRmb = product.retailPriceRmb || 0;
  const retailUsd = product.retailPriceUsd || 0;

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
          {product.nameCn && (
            <p className="mb-1 text-sm text-taupe">{product.nameCn}</p>
          )}

          {product.dimensions && (
            <p className="caption text-muted">{product.dimensions}</p>
          )}

          {/* Public list price */}
          {listPrice > 0 && (
            <div className="mt-3 border-t border-border pt-3">
              <span className="text-base font-bold text-charcoal">
                ${listPrice.toLocaleString("en-US", {
                  minimumFractionDigits: 0,
                  maximumFractionDigits: 0,
                })}
              </span>
              <p className="caption mt-0.5 text-muted">
                USD
              </p>
            </div>
          )}

          {/* Internal pricing — EXW + Retail shown when logged in */}
          {isInternal && (exwCny > 0 || retailRmb > 0) && (
            <div className="price-reveal mt-2 rounded bg-amber-50 px-3 py-2">
              {exwCny > 0 && (
                <div className="flex items-baseline justify-between">
                  <span className="text-xs font-medium text-taupe">EXW Factory</span>
                  <span className="text-sm font-semibold text-charcoal">
                    ¥{exwCny.toLocaleString("zh-CN", { minimumFractionDigits: 0 })}
                  </span>
                </div>
              )}
              {retailRmb > 0 && (
                <div className="flex items-baseline justify-between">
                  <span className="text-xs font-medium text-taupe">Retail RMB</span>
                  <span className="text-sm font-semibold text-charcoal">
                    ¥{retailRmb.toLocaleString("zh-CN", { minimumFractionDigits: 0 })}
                  </span>
                </div>
              )}
              {retailUsd > 0 && (
                <div className="flex items-baseline justify-between">
                  <span className="text-xs font-medium text-taupe">Retail USD</span>
                  <span className="text-sm font-semibold text-charcoal">
                    ${retailUsd.toLocaleString("en-US", { minimumFractionDigits: 0, maximumFractionDigits: 0 })}
                  </span>
                </div>
              )}
            </div>
          )}
        </div>
      </article>
    </Link>
  );
}
