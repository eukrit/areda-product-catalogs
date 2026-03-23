export default function AboutPage() {
  return (
    <>
      <section className="w-full bg-surface-cream">
        <div className="mx-auto max-w-7xl px-6 py-16 md:px-8 lg:px-12">
          <h1 className="text-4xl font-bold tracking-tight text-charcoal md:text-5xl">
            About Areda Atelier
          </h1>
        </div>
      </section>

      <div className="mx-auto max-w-3xl px-6 py-8 md:px-8 lg:px-12">
        <p className="text-lg leading-relaxed text-taupe">
          Areda Atelier curates and sources premium furniture and interior
          products from leading manufacturers. Our catalog features carefully
          selected pieces that balance craftsmanship, design, and value.
        </p>

        <h2 className="mb-4 mt-8 text-2xl font-bold text-charcoal">
          Our Partners
        </h2>
        <p className="text-base leading-relaxed text-taupe">
          We work with established furniture brands including Visconti,
          sourcing products across dining, lounge, modular, and specialty
          categories. Each piece is selected for quality of materials,
          construction, and design relevance to the Southeast Asian market.
        </p>

        <h2 className="mb-4 mt-8 text-2xl font-bold text-charcoal">
          Contact
        </h2>
        <p className="text-base leading-relaxed text-taupe">
          For inquiries, pricing, or to arrange a showroom visit:
          <br />
          <a
            href="mailto:info@aredaatelier.com"
            className="text-charcoal underline hover:text-taupe"
          >
            info@aredaatelier.com
          </a>
        </p>
      </div>
    </>
  );
}
