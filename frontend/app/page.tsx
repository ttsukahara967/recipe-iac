import Link from "next/link";
import { fetchCategories, fetchRecipes } from "@/lib/api";

// Always render per request so the build never needs to reach the API
export const dynamic = "force-dynamic";

type Props = { searchParams: Promise<{ category?: string }> };

export default async function Home({ searchParams }: Props) {
  const { category } = await searchParams;
  const [recipes, categories] = await Promise.all([fetchRecipes(category), fetchCategories()]);

  return (
    <>
      <section className="hero">
        <h1>今日はなにつくる？</h1>
        <p>毎日のごはんに使える、かんたんで美味しいレシピを集めました。</p>
      </section>

      <nav className="chips" aria-label="カテゴリ">
        <Link href="/" className={`chip ${!category ? "chip-active" : ""}`}>
          すべて
        </Link>
        {categories.map((c) => (
          <Link
            key={c}
            href={`/?category=${encodeURIComponent(c)}`}
            className={`chip ${category === c ? "chip-active" : ""}`}
          >
            {c}
          </Link>
        ))}
      </nav>

      {recipes.length === 0 ? (
        <p className="empty">レシピが見つかりませんでした。</p>
      ) : (
        <ul className="grid">
          {recipes.map((r) => (
            <li key={r.id}>
              <Link href={`/recipes/${r.slug}`} className="card">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={r.image_path} alt={r.title} className="card-img" />
                <div className="card-body">
                  <span className="badge">{r.category}</span>
                  <h2>{r.title}</h2>
                  <p>{r.description}</p>
                  <div className="meta">
                    <span>⏱ {r.cook_time_minutes}分</span>
                    <span>🍽 {r.servings}人分</span>
                  </div>
                </div>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </>
  );
}
