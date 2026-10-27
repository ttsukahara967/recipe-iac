import Link from "next/link";
import type { Locale } from "@/i18n/config";
import { categoryLabel, getDictionary } from "@/i18n/dictionaries";
import type { RecipeSummary } from "@/lib/api";
import { categoryHref, recipeHref } from "@/lib/links";

// The title link stretches over the whole card; the badge sits above it as its own link
export default function RecipeCard({
  recipe: r,
  locale,
  isNew = false,
}: {
  recipe: RecipeSummary;
  locale: Locale;
  isNew?: boolean;
}) {
  const dict = getDictionary(locale);
  return (
    <li className="card">
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img src={r.image_path} alt="" className="card-img" />
      <div className="card-body">
        {isNew && <span className="badge badge-new">{dict.newBadge}</span>}
        <Link href={categoryHref(locale, r.category)} className="badge badge-link">
          {categoryLabel(locale, r.category)}
        </Link>
        <h2>
          <Link href={recipeHref(locale, r.slug)} className="card-link">
            {r.title}
          </Link>
        </h2>
        <p>{r.description}</p>
        <div className="meta">
          <span>{dict.cookTimeShort(r.cook_time_minutes)}</span>
          <span>{dict.servings(r.servings)}</span>
        </div>
      </div>
    </li>
  );
}
