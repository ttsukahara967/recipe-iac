import type { Locale } from "./config";

// UI strings per locale. Recipe content itself is translated by the API (?lang=); this file only
// covers the surrounding chrome. Category labels map the Japanese grouping key to a display label.
export type Dictionary = {
  siteTitle: string;
  metaDescription: string;
  footerTech: string;
  footerGithub: string;
  footerCopyright: string;
  heroTitle: string;
  heroText: string;
  recentHeading: string;
  allChip: string;
  allRecipes: string;
  categoryNavAria: string;
  clearSearch: string;
  emptyBase: string;
  emptyHint: string;
  searchPlaceholder: string;
  searchLabel: string;
  searchButton: string;
  sidebarAria: string;
  loading: string;
  menuOpen: string;
  menuClose: string;
  ingredients: string;
  steps: string;
  back: string;
  newBadge: string;
  langName: string;
  categories: Record<string, string>;
  // functions kept out of props; components import the dictionary directly
  searchResult: (q: string, count: number, category?: string) => string;
  categoryMenuAria: (category: string, open: boolean) => string;
  cookTime: (minutes: number) => string;
  cookTimeShort: (minutes: number) => string;
  servings: (people: number) => string;
  recipePageTitle: (title: string) => string;
};

const ja: Dictionary = {
  siteTitle: "おうちレシピ帖",
  metaDescription: "毎日のごはんづくりに使える、かんたんレシピ集",
  footerTech: "このサイトは Next.js（SST）・FastAPI・AWS（ECS Fargate / Aurora）・Terraform で作っています。",
  footerGithub: "ソースコードを GitHub で見る ↗",
  footerCopyright: "© おうちレシピ帖",
  heroTitle: "今日はなにつくる？",
  heroText: "毎日のごはんに使える、かんたんで美味しいレシピを集めました。",
  recentHeading: "🆕 最近追加されたレシピ",
  allChip: "すべて",
  allRecipes: "すべてのレシピ",
  categoryNavAria: "カテゴリ",
  clearSearch: "✕ 検索をクリア",
  emptyBase: "レシピが見つかりませんでした。",
  emptyHint: "よく使う食材は「たまご」「卵」のような書き方の違いも気にせず探せます。見つからないときは、別の言い方や食材名でも試してみてください。",
  searchPlaceholder: "料理名や材料で探す（例：卵、豚こま）",
  searchLabel: "レシピを検索",
  searchButton: "検索",
  sidebarAria: "カテゴリーとメニュー",
  loading: "読み込み中",
  menuOpen: "☰ カテゴリー・メニュー",
  menuClose: "✕ 閉じる",
  ingredients: "材料",
  steps: "作り方",
  back: "← レシピ一覧へ",
  newBadge: "NEW",
  langName: "日本語",
  categories: {},
  searchResult: (q, count, category) => `「${q}」の検索結果 ${count}件${category ? `（${category}）` : ""}`,
  categoryMenuAria: (category, open) => `${category}のメニューを${open ? "閉じる" : "開く"}`,
  cookTime: (m) => `⏱ 調理時間 ${m}分`,
  cookTimeShort: (m) => `⏱ ${m}分`,
  servings: (p) => `🍽 ${p}人分`,
  recipePageTitle: (title) => `${title} | おうちレシピ帖`,
};

const en: Dictionary = {
  siteTitle: "Ouchi Recipes",
  metaDescription: "A collection of simple recipes for everyday home cooking.",
  footerTech: "Built with Next.js (SST), FastAPI, AWS (ECS Fargate / Aurora) and Terraform.",
  footerGithub: "View the source on GitHub ↗",
  footerCopyright: "© Ouchi Recipes",
  heroTitle: "What shall we cook today?",
  heroText: "Simple, tasty recipes for your everyday meals.",
  recentHeading: "🆕 Recently added",
  allChip: "All",
  allRecipes: "All recipes",
  categoryNavAria: "Categories",
  clearSearch: "✕ Clear search",
  emptyBase: "No recipes found.",
  emptyHint: "Try a different wording or ingredient name.",
  searchPlaceholder: "Search by dish or ingredient (e.g. egg, pork)",
  searchLabel: "Search recipes",
  searchButton: "Search",
  sidebarAria: "Categories and menu",
  loading: "Loading",
  menuOpen: "☰ Categories & menu",
  menuClose: "✕ Close",
  ingredients: "Ingredients",
  steps: "Directions",
  back: "← Back to all recipes",
  newBadge: "NEW",
  langName: "English",
  categories: {
    "お弁当": "Bento",
    "ごはんのお供": "Rice Companions",
    "エスニック": "Ethnic",
    "キャンプ飯": "Camp Cooking",
    "デザート": "Dessert",
    "中華": "Chinese",
    "和食": "Japanese",
    "夜食・軽食": "Late-night & Snacks",
    "定食": "Set Meals",
    "沖縄料理": "Okinawan",
    "洋食": "Western",
    "粉もん・鉄板焼き": "Flour & Griddle",
    "飲んだあとの〆": "After-drink Finishers",
  },
  searchResult: (q, count, category) =>
    `${count} result${count === 1 ? "" : "s"} for "${q}"${category ? ` (${category})` : ""}`,
  categoryMenuAria: (category, open) => `${open ? "Collapse" : "Expand"} the ${category} menu`,
  cookTime: (m) => `⏱ Cook time ${m} min`,
  cookTimeShort: (m) => `⏱ ${m} min`,
  servings: (p) => `🍽 Serves ${p}`,
  recipePageTitle: (title) => `${title} | Ouchi Recipes`,
};

const dictionaries: Record<Locale, Dictionary> = { ja, en };

export function getDictionary(locale: Locale): Dictionary {
  return dictionaries[locale] ?? ja;
}

// Localized label for a category (stored as its Japanese key). Falls back to the key itself.
export function categoryLabel(locale: Locale, category: string): string {
  return getDictionary(locale).categories[category] ?? category;
}
