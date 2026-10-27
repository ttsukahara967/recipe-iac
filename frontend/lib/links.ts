import type { Locale } from "@/i18n/config";

// All internal links are locale-prefixed (/ja/... or /en/...).
export const homeHref = (locale: Locale) => `/${locale}`;

export const recipeHref = (locale: Locale, slug: string) => `/${locale}/recipes/${slug}`;

export const categoryHref = (locale: Locale, category: string) =>
  `/${locale}?category=${encodeURIComponent(category)}`;

export const searchHref = (locale: Locale, { q, category }: { q?: string; category?: string }) => {
  const params = new URLSearchParams();
  if (category) params.set("category", category);
  if (q) params.set("q", q);
  const query = params.size ? `?${params}` : "";
  return `/${locale}${query}`;
};
