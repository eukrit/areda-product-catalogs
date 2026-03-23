"use client";

import Link from "next/link";
import { useAuth } from "@/lib/auth-context";
import { LogIn, LogOut, Lock } from "lucide-react";

export function Header() {
  const { user, isInternal, signIn, signOut } = useAuth();

  return (
    <header className="sticky top-0 z-50 border-b border-border bg-areda-white/95 backdrop-blur-sm">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6 md:px-8 lg:px-12">
        {/* Logo / Wordmark */}
        <Link href="/" className="flex items-center">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src="/logo.svg" alt="Areda Atelier" className="h-7 w-auto" />
        </Link>

        {/* Navigation */}
        <nav className="hidden items-center gap-8 md:flex">
          <Link
            href="/"
            className="text-sm font-medium text-charcoal transition-colors hover:text-taupe"
          >
            Catalog
          </Link>
          <Link
            href="/collections"
            className="text-sm font-medium text-charcoal transition-colors hover:text-taupe"
          >
            Collections
          </Link>
          <Link
            href="/about"
            className="text-sm font-medium text-charcoal transition-colors hover:text-taupe"
          >
            About
          </Link>
        </nav>

        {/* Auth */}
        <div className="flex items-center gap-3">
          {isInternal && (
            <span className="hidden items-center gap-1 rounded-full bg-surface-cream px-3 py-1 text-xs font-medium text-taupe sm:flex">
              <Lock size={12} />
              Internal
            </span>
          )}

          {user ? (
            <button
              onClick={signOut}
              className="flex items-center gap-1 text-sm text-taupe transition-colors hover:text-charcoal"
            >
              <LogOut size={16} />
              <span className="hidden sm:inline">Sign out</span>
            </button>
          ) : (
            <button
              onClick={signIn}
              className="flex items-center gap-1 rounded-md bg-charcoal px-4 py-2 text-sm font-medium text-areda-white transition-colors hover:bg-deep-dark"
            >
              <LogIn size={16} />
              Sign in
            </button>
          )}
        </div>
      </div>
    </header>
  );
}
