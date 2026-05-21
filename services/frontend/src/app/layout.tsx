import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "EduMetric - Grant Management System",
  description: "PDP University Grant Management System",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="uz">
      <body>{children}</body>
    </html>
  );
}
