"use client";

import { usePathname, useSearchParams } from "next/navigation";
import { defaultLocale, isLocale } from "@/i18n/config";
import { getDictionary } from "@/i18n/dictionaries";

// Plain GET form to /<locale>?q=..., so results are shareable URLs and it works before hydration
export default function SearchBox() {
  const seg = usePathname().split("/")[1] ?? "";
  const locale = isLocale(seg) ? seg : defaultLocale;
  const dict = getDictionary(locale);
  const q = useSearchParams().get("q") ?? "";
  return (
    <form action={`/${locale}`} method="get" role="search" className="search-box">
      <input
        key={q}
        type="search"
        name="q"
        defaultValue={q}
        placeholder={dict.searchPlaceholder}
        aria-label={dict.searchLabel}
        maxLength={100}
      />
      <button type="submit" aria-label={dict.searchButton}>
        🔍
      </button>
    </form>
  );
}
