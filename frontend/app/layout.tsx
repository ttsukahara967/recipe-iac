import type { Metadata } from "next";
import Link from "next/link";
import { Suspense } from "react";
import SearchBox from "./components/SearchBox";
import Sidebar from "./components/Sidebar";
import "./globals.css";

const REPO_URL = "https://github.com/ttsukahara967/recipe-iac";

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
          <Suspense>
            <SearchBox />
          </Suspense>
        </header>
        <div className="layout">
          <Sidebar />
          <main className="container">{children}</main>
        </div>
        <footer className="site-footer">
          <p className="footer-tech">
            このサイトは Next.js（SST）・FastAPI・AWS（ECS Fargate / Aurora）・Terraform で作っています。
          </p>
          <p>
            <a href={REPO_URL} target="_blank" rel="noopener noreferrer" className="footer-link">
              ソースコードを GitHub で見る ↗
            </a>
          </p>
          <p>© おうちレシピ帖</p>
        </footer>
      </body>
    </html>
  );
}
