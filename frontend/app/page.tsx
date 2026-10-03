import Link from "next/link";
import { Suspense } from "react";
import { fetchCategories, fetchRecipes } from "@/lib/api";
import { categoryHref } from "@/lib/links";

// Always render per request so the build never needs to reach the API
export const dynamic = "force-dynamic";

type Props = { searchParams: Promise<{ category?: string }> };

export default async function Home({ searchParams }: Props) {
  const { category } = await searchParams;

  return (
    <>
      <section className="hero">
        <h1>今日はなにつくる？</h1>
        <p>毎日のごはんに使える、かんたんで美味しいレシピを集めました。</p>
      </section>

      {/* Keyed by category so switching categories shows the skeleton immediately
          instead of keeping the old list on screen while the API (or a paused Aurora) responds */}
      <Suspense key={category ?? ""} fallback={<RecipeListSkeleton />}>
        <RecipeList category={category} />
      </Suspense>
    </>
  );
}

async function RecipeList({ category }: { category?: string }) {
  const [recipes, categories] = await Promise.all([fetchRecipes(category), fetchCategories()]);

  return (
    <>
      <nav className="chips" aria-label="カテゴリ">
        <Link href="/" className={`chip ${!category ? "chip-active" : ""}`}>
          すべて
        </Link>
        {categories.map((c) => (
          <Link key={c} href={categoryHref(c)} className={`chip ${category === c ? "chip-active" : ""}`}>
            {c}
          </Link>
        ))}
      </nav>

      {recipes.length === 0 ? (
        <p className="empty">レシピが見つかりませんでした。</p>
      ) : (
        <ul className="grid">
          {recipes.map((r) => (
            // The title link stretches over the whole card; the badge sits above it as its own link
            <li key={r.id} className="card">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={r.image_path} alt="" className="card-img" />
              <div className="card-body">
                <Link href={categoryHref(r.category)} className="badge badge-link">
                  {r.category}
                </Link>
                <h2>
                  <Link href={`/recipes/${r.slug}`} className="card-link">
                    {r.title}
                  </Link>
                </h2>
                <p>{r.description}</p>
                <div className="meta">
                  <span>⏱ {r.cook_time_minutes}分</span>
                  <span>🍽 {r.servings}人分</span>
                </div>
              </div>
            </li>
          ))}
        </ul>
      )}
    </>
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
          <li key={i} className="card">
            <div className="card-img skeleton" />
            <div className="card-body">
              <div className="skeleton skeleton-line short" />
              <div className="skeleton skeleton-line" />
              <div className="skeleton skeleton-line" />
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
