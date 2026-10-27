"use client";

import Link from "next/link";
import { usePathname, useSearchParams } from "next/navigation";
import { defaultLocale, isLocale, locales } from "@/i18n/config";
import { getDictionary } from "@/i18n/dictionaries";

// Links to the same page in the other locale, swapping the leading /<locale> segment.
export default function LangSwitch() {
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const segments = pathname.split("/");
  const current = isLocale(segments[1] ?? "") ? segments[1] : defaultLocale;
  const query = searchParams.toString();

  return (
    <nav className="lang-switch" aria-label="Language">
      {locales.map((locale) => {
        const next = [...segments];
        next[1] = locale;
        const href = `${next.join("/") || "/"}${query ? `?${query}` : ""}`;
        return (
          <Link
            key={locale}
            href={href}
            className={`lang-link ${locale === current ? "is-active" : ""}`}
            aria-current={locale === current ? "true" : undefined}
          >
            {getDictionary(locale).langName}
          </Link>
        );
      })}
    </nav>
  );
}
