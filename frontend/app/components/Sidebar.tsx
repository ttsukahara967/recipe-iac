import { Suspense } from "react";
import { fetchCategories, fetchRecipes } from "@/lib/api";
import SidebarNav, { type SidebarGroup } from "./SidebarNav";

// Left-hand navigation: every category with its recipes, shared by all pages via the root layout
export default function Sidebar() {
  return (
    <aside className="sidebar" aria-label="カテゴリーとメニュー">
      <Suspense fallback={<SidebarSkeleton />}>
        <SidebarContent />
      </Suspense>
    </aside>
  );
}

async function SidebarContent() {
  const [categories, recipes] = await Promise.all([fetchCategories(), fetchRecipes()]);
  const groups: SidebarGroup[] = categories.map((category) => ({
    category,
    recipes: recipes.filter((r) => r.category === category).map(({ slug, title }) => ({ slug, title })),
  }));
  return <SidebarNav groups={groups} />;
}

function SidebarSkeleton() {
  return (
    <div aria-busy="true" aria-label="読み込み中">
      {Array.from({ length: 10 }, (_, i) => (
        <div key={i} className="skeleton skeleton-line" />
      ))}
    </div>
  );
}
