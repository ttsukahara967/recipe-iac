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

export async function fetchRecipes(category?: string) {
  const query = category ? `?category=${encodeURIComponent(category)}` : "";
  return (await get<RecipeSummary[]>(`/api/recipes${query}`)) ?? [];
}

export async function fetchCategories() {
  return (await get<string[]>("/api/categories")) ?? [];
}

export async function fetchRecipe(slug: string) {
  return get<RecipeDetail>(`/api/recipes/${encodeURIComponent(slug)}`);
}
