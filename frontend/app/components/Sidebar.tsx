import { Suspense } from "react";
import type { Locale } from "@/i18n/config";
import { getDictionary } from "@/i18n/dictionaries";
import { fetchCategories, fetchRecipes } from "@/lib/api";
import SidebarNav, { type SidebarGroup } from "./SidebarNav";

// Left-hand navigation: every category with its recipes, shared by all pages via the locale layout
export default function Sidebar({ locale }: { locale: Locale }) {
  const dict = getDictionary(locale);
  return (
    <aside className="sidebar" aria-label={dict.sidebarAria}>
      <Suspense fallback={<SidebarSkeleton />}>
        <SidebarContent locale={locale} />
      </Suspense>
    </aside>
  );
}

async function SidebarContent({ locale }: { locale: Locale }) {
  const [categories, recipes] = await Promise.all([fetchCategories(), fetchRecipes(locale)]);
  const groups: SidebarGroup[] = categories.map((category) => ({
    category,
    recipes: recipes.filter((r) => r.category === category).map(({ slug, title }) => ({ slug, title })),
  }));
  return <SidebarNav groups={groups} locale={locale} />;
}

function SidebarSkeleton() {
  return (
    <div aria-busy="true">
      {Array.from({ length: 10 }, (_, i) => (
        <div key={i} className="skeleton skeleton-line" />
      ))}
    </div>
  );
}
