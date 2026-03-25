"use client";

import { ProductFilter } from "@/types/product";
import { Search } from "lucide-react";

const SORT_OPTIONS = [
  { value: "name", label: "Name A-Z" },
  { value: "price-asc", label: "Price: Low to High" },
  { value: "price-desc", label: "Price: High to Low" },
  { value: "newest", label: "Newest First" },
];

interface Props {
  filter: ProductFilter;
  onFilterChange: (filter: ProductFilter) => void;
  showPriceSort: boolean;
  totalCount: number;
  collections?: string[];
}

export function FilterBar({ filter, onFilterChange, showPriceSort, totalCount, collections }: Props) {
  return (
    <div className="border-b border-border bg-surface-cream/50">
      <div className="mx-auto max-w-7xl px-6 py-3 md:px-8 lg:px-12">
        <div className="flex flex-col items-start gap-3 sm:flex-row sm:items-center">
          {/* Search */}
          <div className="relative max-w-sm flex-1">
            <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-taupe" />
            <input
              type="text"
              placeholder="Search products..."
              value={filter.search || ""}
              onChange={(e) => onFilterChange({ ...filter, search: e.target.value })}
              className="w-full rounded-md border border-border bg-areda-white py-2 pl-10 pr-4 text-sm placeholder:text-taupe/60 transition-all focus:border-charcoal focus:outline-none focus:ring-2 focus:ring-charcoal/20"
            />
          </div>

          {/* Collection filter */}
          {collections && collections.length > 1 && (
            <select
              value={filter.collection || ""}
              onChange={(e) =>
                onFilterChange({
                  ...filter,
                  collection: e.target.value || undefined,
                })
              }
              className="cursor-pointer rounded-md border border-border bg-areda-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-charcoal/20"
            >
              <option value="">All Collections</option>
              {collections.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          )}

          {/* Sort */}
          <select
            value={filter.sortBy || "name"}
            onChange={(e) =>
              onFilterChange({
                ...filter,
                sortBy: e.target.value as ProductFilter["sortBy"],
              })
            }
            className="cursor-pointer rounded-md border border-border bg-areda-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-charcoal/20"
          >
            {SORT_OPTIONS.filter(
              (o) => showPriceSort || !o.value.startsWith("price")
            ).map((o) => (
              <option key={o.value} value={o.value}>
                {o.label}
              </option>
            ))}
          </select>

          {/* Count */}
          <span className="caption ml-auto text-taupe">
            {totalCount} product{totalCount !== 1 ? "s" : ""}
          </span>
        </div>
      </div>
    </div>
  );
}
