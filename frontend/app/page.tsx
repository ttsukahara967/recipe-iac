import Link from "next/link";
import { Suspense } from "react";
import RecipeCard from "./components/RecipeCard";
import { fetchCategories, fetchRecipes } from "@/lib/api";
import { categoryHref } from "@/lib/links";

// Always render per request so the build never needs to reach the API
export const dynamic = "force-dynamic";

const RECENT_COUNT = 6;

type Props = { searchParams: Promise<{ category?: string; q?: string }> };

export default async function Home({ searchParams }: Props) {
  const { category, q } = await searchParams;
  const query = q?.trim() || undefined;
  const showRecent = !category && !query;

  return (
    <>
      <section className="hero">
        <h1>今日はなにつくる？</h1>
        <p>毎日のごはんに使える、かんたんで美味しいレシピを集めました。</p>
      </section>

      {showRecent && (
        <Suspense fallback={<RecentSkeleton />}>
          <RecentRecipes />
        </Suspense>
      )}

      {/* Keyed by category and query so switching shows the skeleton immediately
          instead of keeping the old list on screen while the API (or a paused Aurora) responds */}
      <Suspense key={`${category ?? ""}|${query ?? ""}`} fallback={<RecipeListSkeleton />}>
        <RecipeList category={category} q={query} />
      </Suspense>
    </>
  );
}

async function RecentRecipes() {
  const recipes = await fetchRecipes({ sort: "new", limit: RECENT_COUNT });
  if (recipes.length === 0) return null;
  return (
    <section className="recent" aria-labelledby="recent-heading">
      <h2 id="recent-heading" className="section-title">
        🆕 最近追加されたレシピ
      </h2>
      <ul className="recent-row">
        {recipes.map((r) => (
          <RecipeCard key={r.id} recipe={r} isNew />
        ))}
      </ul>
    </section>
  );
}

async function RecipeList({ category, q }: { category?: string; q?: string }) {
  const [recipes, categories] = await Promise.all([fetchRecipes({ category, q }), fetchCategories()]);

  return (
    <>
      <nav className="chips" aria-label="カテゴリ">
        <Link href={q ? `/?q=${encodeURIComponent(q)}` : "/"} className={`chip ${!category ? "chip-active" : ""}`}>
          すべて
        </Link>
        {categories.map((c) => (
          <Link
            key={c}
            href={q ? `${categoryHref(c)}&q=${encodeURIComponent(q)}` : categoryHref(c)}
            className={`chip ${category === c ? "chip-active" : ""}`}
          >
            {c}
          </Link>
        ))}
      </nav>

      {q ? (
        <div className="search-summary">
          <h2 className="section-title">
            「{q}」の検索結果 {recipes.length}件{category && `（${category}）`}
          </h2>
          <Link href={category ? categoryHref(category) : "/"} className="search-clear">
            ✕ 検索をクリア
          </Link>
        </div>
      ) : (
        !category && <h2 className="section-title">すべてのレシピ</h2>
      )}

      {recipes.length === 0 ? (
        <p className="empty">
          レシピが見つかりませんでした。
          {q && "よく使う食材は「たまご」「卵」のような書き方の違いも気にせず探せます。見つからないときは、別の言い方や食材名でも試してみてください。"}
        </p>
      ) : (
        <ul className="grid">
          {recipes.map((r) => (
            <RecipeCard key={r.id} recipe={r} />
          ))}
        </ul>
      )}
    </>
  );
}

function CardSkeleton() {
  return (
    <li className="card">
      <div className="card-img skeleton" />
      <div className="card-body">
        <div className="skeleton skeleton-line short" />
        <div className="skeleton skeleton-line" />
        <div className="skeleton skeleton-line" />
      </div>
    </li>
  );
}

function RecentSkeleton() {
  return (
    <section className="recent" aria-busy="true" aria-label="読み込み中">
      <div className="skeleton skeleton-line short" />
      <ul className="recent-row">
        {Array.from({ length: 4 }, (_, i) => (
          <CardSkeleton key={i} />
        ))}
      </ul>
    </section>
  );
}

function RecipeListSkeleton() {
  return (
    <div aria-busy="true" aria-label="読み込み中">
      <div className="chips">
        {Array.from({ length: 5 }, (_, i) => (
          <span key={i} className="chip skeleton skeleton-chip" />
        ))}
      </div>
      <ul className="grid">
        {Array.from({ length: 6 }, (_, i) => (
          <CardSkeleton key={i} />
        ))}
      </ul>
    </div>
  );
}
