import type { Locale } from "@/i18n/config";

// All API calls happen in server components, so the API URL is never exposed to the browser
const API_URL = (process.env.API_URL ?? "http://localhost:8000").replace(/\/$/, "");

export type Ingredient = { name: string; amount: string };

export type RecipeSummary = {
  id: number;
  slug: string;
  title: string;
  description: string;
  category: string;
  cook_time_minutes: number;
  servings: number;
  image_path: string;
};

export type RecipeDetail = RecipeSummary & {
  ingredients: Ingredient[];
  steps: string[];
};

async function get<T>(path: string): Promise<T | null> {
  const res = await fetch(`${API_URL}${path}`, { cache: "no-store" });
  if (res.status === 404) return null;
  if (!res.ok) throw new Error(`API ${path} failed: ${res.status}`);
  return res.json() as Promise<T>;
}

// English content comes from ?lang=en; Japanese is the API default, so the param is omitted.
function langParam(locale: Locale): string {
  return locale === "en" ? "lang=en" : "";
}

export type RecipeQuery = {
  category?: string;
  q?: string;
  sort?: "default" | "new";
  limit?: number;
};

export async function fetchRecipes(locale: Locale, { category, q, sort, limit }: RecipeQuery = {}) {
  const params = new URLSearchParams();
  if (category) params.set("category", category);
  if (q) params.set("q", q);
  if (sort) params.set("sort", sort);
  if (limit) params.set("limit", String(limit));
  if (locale === "en") params.set("lang", "en");
  const query = params.size ? `?${params}` : "";
  return (await get<RecipeSummary[]>(`/api/recipes${query}`)) ?? [];
}

export async function fetchCategories() {
  // Categories are the Japanese grouping keys regardless of locale; the UI maps them to labels.
  return (await get<string[]>("/api/categories")) ?? [];
}

export async function fetchRecipe(locale: Locale, slug: string) {
  const lang = langParam(locale);
  const query = lang ? `?${lang}` : "";
  return get<RecipeDetail>(`/api/recipes/${encodeURIComponent(slug)}${query}`);
}
