import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "おうちレシピ帖",
  description: "毎日のごはんづくりに使える、かんたんレシピ集",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ja">
      <body>
        <header className="site-header">
          <Link href="/" className="logo">
            <span className="logo-mark" aria-hidden>
              🍳
            </span>
            おうちレシピ帖
          </Link>
        </header>
        <main className="container">{children}</main>
        <footer className="site-footer">© おうちレシピ帖</footer>
      </body>
    </html>
  );
}
