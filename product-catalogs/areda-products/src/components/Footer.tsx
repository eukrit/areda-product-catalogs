export function Footer() {
  return (
    <footer className="bg-charcoal py-12 text-on-dark">
      <div className="mx-auto max-w-7xl px-6 md:px-8 lg:px-12">
        <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
          <div>
            <h3 className="mb-3 text-lg font-bold text-cream">areda atelier</h3>
            <p className="text-sm leading-relaxed text-taupe">
              Curated furniture and interior products.
              <br />
              Designed for modern living.
            </p>
          </div>
          <div>
            <h4 className="overline mb-3 text-taupe">Contact</h4>
            <p className="text-sm text-cream/80">
              Bangkok, Thailand
              <br />
              info@aredaatelier.com
            </p>
          </div>
          <div>
            <h4 className="overline mb-3 text-taupe">Links</h4>
            <ul className="space-y-1 text-sm text-cream/80">
              <li>
                <a href="/" className="transition-colors hover:text-cream">
                  Catalog
                </a>
              </li>
              <li>
                <a href="/collections" className="transition-colors hover:text-cream">
                  Collections
                </a>
              </li>
            </ul>
          </div>
        </div>
        <div className="mt-8 border-t border-taupe/30 pt-6 text-center">
          <p className="caption text-taupe">
            &copy; {new Date().getFullYear()} Areda Atelier. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}
