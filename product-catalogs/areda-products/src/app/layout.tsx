import type { Metadata } from "next";
import "./globals.css";
import { AuthProvider } from "@/lib/auth-context";
import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";

export const metadata: Metadata = {
  title: "Areda Atelier | Product Catalog",
  description:
    "Curated furniture and interior products by Areda Atelier. Explore our collections of dining chairs, lounge seating, sofas, and more.",
  icons: { icon: "/favicon.ico" },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen flex flex-col bg-areda-white text-charcoal">
        <AuthProvider>
          <Header />
          <main className="flex-1 page-transition">{children}</main>
          <Footer />
        </AuthProvider>
      </body>
    </html>
  );
}
