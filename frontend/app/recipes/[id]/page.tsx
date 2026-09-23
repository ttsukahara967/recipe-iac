import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { fetchRecipe } from "@/lib/api";

export const dynamic = "force-dynamic";

type Props = { params: Promise<{ id: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const recipe = await fetchRecipe((await params).id);
  return { title: recipe ? `${recipe.title} | おうちレシピ帖` : "おうちレシピ帖" };
}

export default async function RecipePage({ params }: Props) {
  const recipe = await fetchRecipe((await params).id);
  if (!recipe) notFound();

  return (
    <article className="detail">
      <Link href="/" className="back">
        ← レシピ一覧へ
      </Link>

      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img src={recipe.image_path} alt={recipe.title} className="detail-img" />

      <header className="detail-header">
        <span className="badge">{recipe.category}</span>
        <h1>{recipe.title}</h1>
        <p>{recipe.description}</p>
        <div className="meta">
          <span>⏱ 調理時間 {recipe.cook_time_minutes}分</span>
          <span>🍽 {recipe.servings}人分</span>
        </div>
      </header>

      <div className="detail-body">
        <section className="panel">
          <h2>材料</h2>
          <ul className="ingredients">
            {recipe.ingredients.map((i) => (
              <li key={i.name}>
                <span>{i.name}</span>
                <span className="amount">{i.amount}</span>
              </li>
            ))}
          </ul>
        </section>

        <section className="panel">
          <h2>作り方</h2>
          <ol className="steps">
            {recipe.steps.map((s, idx) => (
              <li key={idx}>{s}</li>
            ))}
          </ol>
        </section>
      </div>
    </article>
  );
}
