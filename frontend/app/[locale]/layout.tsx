import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { Suspense } from "react";
import LangSwitch from "@/app/components/LangSwitch";
import SearchBox from "@/app/components/SearchBox";
import Sidebar from "@/app/components/Sidebar";
import { isLocale, locales, type Locale } from "@/i18n/config";
import { getDictionary } from "@/i18n/dictionaries";
import { homeHref } from "@/lib/links";

const REPO_URL = "https://github.com/ttsukahara967/recipe-iac";

export function generateStaticParams() {
  return locales.map((locale) => ({ locale }));
}

export async function generateMetadata({ params }: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  const dict = getDictionary(isLocale(locale) ? locale : "ja");
  return { title: dict.siteTitle, description: dict.metaDescription };
}

export default async function LocaleLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  const dict = getDictionary(locale as Locale);

  return (
    <>
      <header className="site-header">
        <Link href={homeHref(locale as Locale)} className="logo">
          <span className="logo-mark" aria-hidden>
            🍳
          </span>
          {dict.siteTitle}
        </Link>
        <Suspense>
          <SearchBox />
        </Suspense>
        <LangSwitch />
      </header>
      <div className="layout">
        <Sidebar locale={locale as Locale} />
        <main className="container">{children}</main>
      </div>
      <footer className="site-footer">
        <p className="footer-tech">{dict.footerTech}</p>
        <p>
          <a href={REPO_URL} target="_blank" rel="noopener noreferrer" className="footer-link">
            {dict.footerGithub}
          </a>
        </p>
        <p>{dict.footerCopyright}</p>
      </footer>
    </>
  );
}
