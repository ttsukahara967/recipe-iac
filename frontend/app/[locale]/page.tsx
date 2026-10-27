import Link from "next/link";
import { Suspense } from "react";
import RecipeCard from "@/app/components/RecipeCard";
import type { Locale } from "@/i18n/config";
import { categoryLabel, getDictionary } from "@/i18n/dictionaries";
import { fetchCategories, fetchRecipes } from "@/lib/api";
import { categoryHref, homeHref, searchHref } from "@/lib/links";

// Always render per request so the build never needs to reach the API
export const dynamic = "force-dynamic";

const RECENT_COUNT = 6;

type Props = {
  params: Promise<{ locale: Locale }>;
  searchParams: Promise<{ category?: string; q?: string }>;
};

export default async function Home({ params, searchParams }: Props) {
  const { locale } = await params;
  const { category, q } = await searchParams;
  const query = q?.trim() || undefined;
  const showRecent = !category && !query;
  const dict = getDictionary(locale);

  return (
    <>
      <section className="hero">
        <h1>{dict.heroTitle}</h1>
        <p>{dict.heroText}</p>
      </section>

      {showRecent && (
        <Suspense fallback={<RecentSkeleton />}>
          <RecentRecipes locale={locale} />
        </Suspense>
      )}

      {/* Keyed by category and query so switching shows the skeleton immediately
          instead of keeping the old list on screen while the API (or a paused Aurora) responds */}
      <Suspense key={`${category ?? ""}|${query ?? ""}`} fallback={<RecipeListSkeleton />}>
        <RecipeList locale={locale} category={category} q={query} />
      </Suspense>
    </>
  );
}

async function RecentRecipes({ locale }: { locale: Locale }) {
  const recipes = await fetchRecipes(locale, { sort: "new", limit: RECENT_COUNT });
  if (recipes.length === 0) return null;
  const dict = getDictionary(locale);
  return (
    <section className="recent" aria-labelledby="recent-heading">
      <h2 id="recent-heading" className="section-title">
        {dict.recentHeading}
      </h2>
      <ul className="recent-row">
        {recipes.map((r) => (
          <RecipeCard key={r.id} recipe={r} locale={locale} isNew />
        ))}
      </ul>
    </section>
  );
}

async function RecipeList({ locale, category, q }: { locale: Locale; category?: string; q?: string }) {
  const [recipes, categories] = await Promise.all([fetchRecipes(locale, { category, q }), fetchCategories()]);
  const dict = getDictionary(locale);

  return (
    <>
      <nav className="chips" aria-label={dict.categoryNavAria}>
        <Link href={q ? searchHref(locale, { q }) : homeHref(locale)} className={`chip ${!category ? "chip-active" : ""}`}>
          {dict.allChip}
        </Link>
        {categories.map((c) => (
          <Link
            key={c}
            href={q ? searchHref(locale, { category: c, q }) : categoryHref(locale, c)}
            className={`chip ${category === c ? "chip-active" : ""}`}
          >
            {categoryLabel(locale, c)}
          </Link>
        ))}
      </nav>

      {q ? (
        <div className="search-summary">
          <h2 className="section-title">
            {dict.searchResult(q, recipes.length, category ? categoryLabel(locale, category) : undefined)}
          </h2>
          <Link href={category ? categoryHref(locale, category) : homeHref(locale)} className="search-clear">
            {dict.clearSearch}
          </Link>
        </div>
      ) : (
        !category && <h2 className="section-title">{dict.allRecipes}</h2>
      )}

      {recipes.length === 0 ? (
        <p className="empty">
          {dict.emptyBase}
          {q && dict.emptyHint}
        </p>
      ) : (
        <ul className="grid">
          {recipes.map((r) => (
            <RecipeCard key={r.id} recipe={r} locale={locale} />
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
    <section className="recent" aria-busy="true">
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
    <div aria-busy="true">
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
