import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import type { Locale } from "@/i18n/config";
import { categoryLabel, getDictionary } from "@/i18n/dictionaries";
import { fetchRecipe } from "@/lib/api";
import { categoryHref, homeHref } from "@/lib/links";

export const dynamic = "force-dynamic";

type Props = { params: Promise<{ locale: Locale; id: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale, id } = await params;
  const recipe = await fetchRecipe(locale, id);
  const dict = getDictionary(locale);
  return { title: recipe ? dict.recipePageTitle(recipe.title) : dict.siteTitle };
}

export default async function RecipePage({ params }: Props) {
  const { locale, id } = await params;
  const recipe = await fetchRecipe(locale, id);
  if (!recipe) notFound();
  const dict = getDictionary(locale);

  return (
    <article className="detail">
      <Link href={homeHref(locale)} className="back">
        {dict.back}
      </Link>

      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img src={recipe.image_path} alt={recipe.title} className="detail-img" />

      <header className="detail-header">
        <Link href={categoryHref(locale, recipe.category)} className="badge badge-link">
          {categoryLabel(locale, recipe.category)}
        </Link>
        <h1>{recipe.title}</h1>
        <p>{recipe.description}</p>
        <div className="meta">
          <span>{dict.cookTime(recipe.cook_time_minutes)}</span>
          <span>{dict.servings(recipe.servings)}</span>
        </div>
      </header>

      <div className="detail-body">
        <section className="panel">
          <h2>{dict.ingredients}</h2>
          <ul className="ingredients">
            {recipe.ingredients.map((i, idx) => (
              <li key={idx}>
                <span>{i.name}</span>
                <span className="amount">{i.amount}</span>
              </li>
            ))}
          </ul>
        </section>

        <section className="panel">
          <h2>{dict.steps}</h2>
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
