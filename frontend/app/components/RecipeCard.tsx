import Link from "next/link";
import type { RecipeSummary } from "@/lib/api";
import { categoryHref } from "@/lib/links";

// The title link stretches over the whole card; the badge sits above it as its own link
export default function RecipeCard({ recipe: r, isNew = false }: { recipe: RecipeSummary; isNew?: boolean }) {
  return (
    <li className="card">
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img src={r.image_path} alt="" className="card-img" />
      <div className="card-body">
        {isNew && <span className="badge badge-new">NEW</span>}
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
  );
}
