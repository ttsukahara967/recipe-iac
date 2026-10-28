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

const ko: Dictionary = {
  siteTitle: "우치 레시피",
  metaDescription: "매일 집밥에 쓰기 좋은 간단 레시피 모음.",
  footerTech: "이 사이트는 Next.js(SST)·FastAPI·AWS(ECS Fargate / Aurora)·Terraform으로 만들었습니다.",
  footerGithub: "GitHub에서 소스 코드 보기 ↗",
  footerCopyright: "© 우치 레시피",
  heroTitle: "오늘 뭐 먹지?",
  heroText: "매일의 집밥에 쓸 수 있는 간단하고 맛있는 레시피를 모았습니다.",
  recentHeading: "🆕 최근 추가된 레시피",
  allChip: "전체",
  allRecipes: "전체 레시피",
  categoryNavAria: "카테고리",
  clearSearch: "✕ 검색 지우기",
  emptyBase: "레시피를 찾을 수 없습니다.",
  emptyHint: "다른 표현이나 재료 이름으로 검색해 보세요.",
  searchPlaceholder: "요리명·재료로 검색 (예: 계란, 돼지고기)",
  searchLabel: "레시피 검색",
  searchButton: "검색",
  sidebarAria: "카테고리와 메뉴",
  loading: "불러오는 중",
  menuOpen: "☰ 카테고리·메뉴",
  menuClose: "✕ 닫기",
  ingredients: "재료",
  steps: "만드는 법",
  back: "← 레시피 목록으로",
  newBadge: "NEW",
  langName: "한국어",
  categories: {
    "お弁当": "도시락",
    "ごはんのお供": "밥반찬",
    "エスニック": "에스닉",
    "キャンプ飯": "캠핑 요리",
    "デザート": "디저트",
    "中華": "중화요리",
    "和食": "일식",
    "夜食・軽食": "야식·간식",
    "定食": "정식",
    "沖縄料理": "오키나와 요리",
    "洋食": "양식",
    "粉もん・鉄板焼き": "가루음식·철판구이",
    "飲んだあとの〆": "해장·마무리",
  },
  searchResult: (q, count, category) => `"${q}" 검색 결과 ${count}건${category ? `(${category})` : ""}`,
  categoryMenuAria: (category, open) => `${category} 메뉴 ${open ? "닫기" : "열기"}`,
  cookTime: (m) => `⏱ 조리시간 ${m}분`,
  cookTimeShort: (m) => `⏱ ${m}분`,
  servings: (p) => `🍽 ${p}인분`,
  recipePageTitle: (title) => `${title} | 우치 레시피`,
};

const zhHans: Dictionary = {
  siteTitle: "居家食谱",
  metaDescription: "适合日常家庭料理的简单食谱集。",
  footerTech: "本站使用 Next.js（SST）、FastAPI、AWS（ECS Fargate / Aurora）、Terraform 构建。",
  footerGithub: "在 GitHub 查看源代码 ↗",
  footerCopyright: "© 居家食谱",
  heroTitle: "今天做什么？",
  heroText: "汇集了日常家庭料理可用的简单又美味的食谱。",
  recentHeading: "🆕 最近添加的食谱",
  allChip: "全部",
  allRecipes: "全部食谱",
  categoryNavAria: "分类",
  clearSearch: "✕ 清除搜索",
  emptyBase: "未找到食谱。",
  emptyHint: "换个说法或食材名再试试。",
  searchPlaceholder: "按菜名或食材搜索（如：鸡蛋、猪肉）",
  searchLabel: "搜索食谱",
  searchButton: "搜索",
  sidebarAria: "分类与菜单",
  loading: "加载中",
  menuOpen: "☰ 分类·菜单",
  menuClose: "✕ 关闭",
  ingredients: "食材",
  steps: "做法",
  back: "← 返回食谱列表",
  newBadge: "NEW",
  langName: "简体中文",
  categories: {
    "お弁当": "便当",
    "ごはんのお供": "下饭菜",
    "エスニック": "异国风味",
    "キャンプ飯": "露营餐",
    "デザート": "甜点",
    "中華": "中式",
    "和食": "日式",
    "夜食・軽食": "夜宵·小食",
    "定食": "定食",
    "沖縄料理": "冲绳料理",
    "洋食": "西式",
    "粉もん・鉄板焼き": "面食·铁板烧",
    "飲んだあとの〆": "酒后收尾",
  },
  searchResult: (q, count, category) => `“${q}”的搜索结果 ${count}项${category ? `（${category}）` : ""}`,
  categoryMenuAria: (category, open) => `${open ? "收起" : "展开"}${category}菜单`,
  cookTime: (m) => `⏱ 烹饪时间 ${m}分钟`,
  cookTimeShort: (m) => `⏱ ${m}分钟`,
  servings: (p) => `🍽 ${p}人份`,
  recipePageTitle: (title) => `${title} | 居家食谱`,
};

const zhHant: Dictionary = {
  siteTitle: "居家食譜",
  metaDescription: "適合日常家常料理的簡單食譜集。",
  footerTech: "本站使用 Next.js（SST）、FastAPI、AWS（ECS Fargate / Aurora）、Terraform 建置。",
  footerGithub: "在 GitHub 查看原始碼 ↗",
  footerCopyright: "© 居家食譜",
  heroTitle: "今天煮什麼？",
  heroText: "彙整了日常家常料理可用的簡單又美味的食譜。",
  recentHeading: "🆕 最近新增的食譜",
  allChip: "全部",
  allRecipes: "全部食譜",
  categoryNavAria: "分類",
  clearSearch: "✕ 清除搜尋",
  emptyBase: "找不到食譜。",
  emptyHint: "換個說法或食材名稱再試試。",
  searchPlaceholder: "依菜名或食材搜尋（如：雞蛋、豬肉）",
  searchLabel: "搜尋食譜",
  searchButton: "搜尋",
  sidebarAria: "分類與選單",
  loading: "載入中",
  menuOpen: "☰ 分類·選單",
  menuClose: "✕ 關閉",
  ingredients: "食材",
  steps: "做法",
  back: "← 返回食譜列表",
  newBadge: "NEW",
  langName: "繁體中文",
  categories: {
    "お弁当": "便當",
    "ごはんのお供": "配飯小菜",
    "エスニック": "異國風味",
    "キャンプ飯": "露營餐",
    "デザート": "甜點",
    "中華": "中式",
    "和食": "日式",
    "夜食・軽食": "宵夜·輕食",
    "定食": "定食",
    "沖縄料理": "沖繩料理",
    "洋食": "西式",
    "粉もん・鉄板焼き": "麵粉料理·鐵板燒",
    "飲んだあとの〆": "續攤收尾",
  },
  searchResult: (q, count, category) => `「${q}」的搜尋結果 ${count}項${category ? `（${category}）` : ""}`,
  categoryMenuAria: (category, open) => `${open ? "收合" : "展開"}${category}選單`,
  cookTime: (m) => `⏱ 烹調時間 ${m}分鐘`,
  cookTimeShort: (m) => `⏱ ${m}分鐘`,
  servings: (p) => `🍽 ${p}人份`,
  recipePageTitle: (title) => `${title} | 居家食譜`,
};

const dictionaries: Record<Locale, Dictionary> = { ja, en, ko, "zh-Hans": zhHans, "zh-Hant": zhHant };

export function getDictionary(locale: Locale): Dictionary {
  return dictionaries[locale] ?? ja;
}

// Localized label for a category (stored as its Japanese key). Falls back to the key itself.
export function categoryLabel(locale: Locale, category: string): string {
  return getDictionary(locale).categories[category] ?? category;
}
