"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
/* eslint-disable @next/next/no-img-element */
import Link from "next/link";
import { doc, getDoc } from "firebase/firestore";
import { db } from "@/lib/firebase";
import { useAuth } from "@/lib/auth-context";
import { Product } from "@/types/product";
import { ArrowLeft, Ruler, Package, Layers } from "lucide-react";

export default function ProductDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { isInternal } = useAuth();
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeImage, setActiveImage] = useState(0);

  useEffect(() => {
    async function load() {
      try {
        const snap = await getDoc(doc(db, "products", id));
        if (snap.exists()) {
          setProduct({ id: snap.id, ...snap.data() } as Product);
        }
      } catch (err) {
        console.error("Failed to load product:", err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [id]);

  if (loading) {
    return (
      <div className="mx-auto max-w-7xl px-6 py-8 md:px-8 lg:px-12">
        <div className="animate-pulse grid grid-cols-1 gap-8 lg:grid-cols-2">
          <div className="aspect-square rounded-lg bg-surface-cream" />
          <div className="space-y-4">
            <div className="h-4 w-20 rounded bg-surface-cream" />
            <div className="h-8 w-3/4 rounded bg-surface-cream" />
            <div className="h-4 w-1/3 rounded bg-surface-cream" />
          </div>
        </div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="mx-auto max-w-7xl px-6 py-24 text-center md:px-8 lg:px-12">
        <h2 className="text-2xl font-bold text-charcoal">Product not found</h2>
        <Link href="/" className="mt-4 inline-block text-sm text-taupe hover:text-charcoal">
          &larr; Back to catalog
        </Link>
      </div>
    );
  }

  const allImages = [product.imageUrl, ...(product.galleryUrls || [])].filter(Boolean);
  const categoryLabel = product.category.replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

  return (
    <div className="mx-auto max-w-7xl px-6 py-8 md:px-8 lg:px-12">
      {/* Breadcrumb */}
      <Link
        href="/"
        className="mb-6 inline-flex items-center gap-1 text-sm text-taupe transition-colors hover:text-charcoal"
      >
        <ArrowLeft size={16} />
        Back to catalog
      </Link>

      <div className="grid grid-cols-1 gap-8 lg:grid-cols-2 lg:gap-12">
        {/* Images */}
        <div>
          <div className="relative aspect-square overflow-hidden rounded-lg bg-surface-cream">
            {allImages.length > 0 ? (
              <img
                src={allImages[activeImage]}
                alt={product.name}
                className="absolute inset-0 h-full w-full object-cover"
              />
            ) : (
              <div className="absolute inset-0 flex items-center justify-center text-taupe">
                <Package size={64} strokeWidth={1} />
              </div>
            )}
          </div>

          {/* Thumbnails */}
          {allImages.length > 1 && (
            <div className="mt-3 flex gap-2 overflow-x-auto">
              {allImages.map((url, i) => (
                <button
                  key={i}
                  onClick={() => setActiveImage(i)}
                  className={`relative h-20 w-20 flex-shrink-0 overflow-hidden rounded-md border-2 transition-all ${
                    i === activeImage ? "border-charcoal" : "border-border hover:border-taupe"
                  }`}
                >
                  <img src={url} alt="" className="absolute inset-0 h-full w-full object-cover" />
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Details */}
        <div>
          <p className="overline text-taupe">{product.brand} &middot; {categoryLabel}</p>
          <h1 className="mt-2 text-3xl font-bold tracking-tight text-charcoal md:text-4xl">
            {product.name}
          </h1>
          {product.nameCn && (
            <p className="mt-1 text-lg text-taupe">{product.nameCn}</p>
          )}
          <p className="mt-2 text-sm text-muted">{product.productCode}</p>

          {/* Price — internal only */}
          {isInternal && (() => {
            const RMB_TO_USD = 7.25;
            const MARKUP = 2.0;
            const displayPrice =
              product.priceFobUsd > 0 ? product.priceFobUsd
              : product.priceExwUsd > 0 ? product.priceExwUsd
              : product.priceRmb > 0 ? (product.priceRmb / RMB_TO_USD) * MARKUP
              : 0;
            const isConverted = !product.priceFobUsd && !product.priceExwUsd && product.priceRmb > 0;
            return displayPrice > 0 ? (
              <div className="price-reveal mt-6 rounded-lg bg-surface-cream p-4">
                <p className="overline mb-2 text-taupe">Pricing (Internal)</p>
                <div className="flex items-baseline gap-4">
                  <span className="text-2xl font-bold text-charcoal">
                    ${displayPrice.toLocaleString("en-US", { minimumFractionDigits: 0, maximumFractionDigits: 0 })}
                  </span>
                  {isConverted && (
                    <span className="text-sm text-taupe">
                      (¥{product.priceRmb.toLocaleString("zh-CN")} × 2.0)
                    </span>
                  )}
                  {!isConverted && product.priceFobUsd > 0 && (
                    <span className="text-sm text-taupe">FOB Shanghai</span>
                  )}
                </div>
                {product.moq > 0 && (
                  <p className="caption mt-2 text-muted">MOQ: {product.moq} units</p>
                )}
                <p className="mt-3 text-xs text-taupe italic">
                  * Price excludes local delivery and installation
                </p>
              </div>
            ) : null;
          })()}

          {/* Specs */}
          <div className="mt-6 space-y-4">
            {product.dimensions && (
              <div className="flex items-start gap-3">
                <Ruler size={18} className="mt-0.5 flex-shrink-0 text-taupe" />
                <div>
                  <p className="text-sm font-semibold text-charcoal">Dimensions</p>
                  <p className="text-sm text-taupe">{product.dimensions}</p>
                </div>
              </div>
            )}

            {product.material && (
              <div className="flex items-start gap-3">
                <Layers size={18} className="mt-0.5 flex-shrink-0 text-taupe" />
                <div>
                  <p className="text-sm font-semibold text-charcoal">Materials</p>
                  <p className="text-sm text-taupe">{product.material}</p>
                </div>
              </div>
            )}

            {product.features && (
              <div className="flex items-start gap-3">
                <Package size={18} className="mt-0.5 flex-shrink-0 text-taupe" />
                <div>
                  <p className="text-sm font-semibold text-charcoal">Features</p>
                  <p className="text-sm text-taupe">{product.features}</p>
                </div>
              </div>
            )}
          </div>

          {/* Tags */}
          {product.tags?.length > 0 && (
            <div className="mt-6 flex flex-wrap gap-2">
              {product.tags.map((tag) => (
                <span
                  key={tag}
                  className="rounded-full bg-surface-cream px-3 py-1 text-xs font-medium text-charcoal"
                >
                  {tag}
                </span>
              ))}
            </div>
          )}

          {/* Volume — internal */}
          {isInternal && product.volumeCbm > 0 && (
            <p className="caption mt-4 text-muted">
              Shipping volume: {product.volumeCbm.toFixed(4)} CBM
              &middot; Lead time: {product.leadTimeDays || 60} working days
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
