import type { Metadata } from "next";

import { AppNav } from "@/components/app-nav";
import "./globals.css";

export const metadata: Metadata = {
  title: "Nawat Corpus Concordance",
  description: "A Nawat / Pipil concordance and lexicographic research application."
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AppNav />
        {children}
      </body>
    </html>
  );
}
