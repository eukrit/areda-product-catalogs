"use client";

import { useEffect, useState } from "react";
import { collection, getDocs } from "firebase/firestore";
import { db } from "@/lib/firebase";
import Link from "next/link";

interface CollectionInfo {
  name: string;
  count: number;
}

export default function CollectionsPage() {
  const [collections, setCollections] = useState<CollectionInfo[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const snap = await getDocs(collection(db, "products"));
        const counts: Record<string, number> = {};
        snap.docs.forEach((d) => {
          const col = d.data().collection || "Uncategorized";
          counts[col] = (counts[col] || 0) + 1;
        });
        setCollections(
          Object.entries(counts)
            .map(([name, count]) => ({ name, count }))
            .sort((a, b) => a.name.localeCompare(b.name))
        );
      } catch (err) {
        console.error("Failed to load collections:", err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  return (
    <>
      <section className="w-full bg-surface-cream">
        <div className="mx-auto max-w-7xl px-6 py-16 md:px-8 lg:px-12">
          <h1 className="text-4xl font-bold tracking-tight text-charcoal md:text-5xl">
            Collections
          </h1>
          <p className="mt-4 max-w-2xl text-lg leading-relaxed text-taupe">
            Browse our product lines organized by collection and style.
          </p>
        </div>
      </section>

      <div className="mx-auto max-w-7xl px-6 py-8 md:px-8 lg:px-12">
        {loading ? (
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {Array.from({ length: 4 }).map((_, i) => (
              <div key={i} className="h-40 animate-pulse rounded-lg bg-surface-cream" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {collections.map((col) => (
              <Link
                key={col.name}
                href={`/?collection=${encodeURIComponent(col.name)}`}
                className="group block rounded-lg border border-border bg-areda-white p-8 transition-all hover:border-charcoal hover:shadow-lg"
              >
                <h2 className="text-xl font-bold text-charcoal group-hover:text-deep-dark">
                  {col.name}
                </h2>
                <p className="mt-2 text-sm text-taupe">
                  {col.count} product{col.count !== 1 ? "s" : ""}
                </p>
              </Link>
            ))}
          </div>
        )}
      </div>
    </>
  );
}
