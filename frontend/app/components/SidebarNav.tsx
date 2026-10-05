"use client";

import Link from "next/link";
import { usePathname, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import { categoryHref } from "@/lib/links";

export type SidebarGroup = {
  category: string;
  recipes: { slug: string; title: string }[];
};

export default function SidebarNav({ groups }: { groups: SidebarGroup[] }) {
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const activeSlug = pathname.startsWith("/recipes/") ? decodeURIComponent(pathname.split("/")[2] ?? "") : null;
  const activeCategory =
    searchParams.get("category") ?? groups.find((g) => g.recipes.some((r) => r.slug === activeSlug))?.category ?? null;
  const isAll = pathname === "/" && !searchParams.get("category");

  const [open, setOpen] = useState<Set<string>>(() => new Set(activeCategory ? [activeCategory] : []));
  const [mobileOpen, setMobileOpen] = useState(false);

  // Follow navigation: expand the category being viewed and close the mobile panel
  useEffect(() => {
    if (activeCategory) setOpen((prev) => (prev.has(activeCategory) ? prev : new Set(prev).add(activeCategory)));
    setMobileOpen(false);
  }, [activeCategory, pathname]);

  const toggle = (category: string) =>
    setOpen((prev) => {
      const next = new Set(prev);
      if (next.has(category)) next.delete(category);
      else next.add(category);
      return next;
    });

  return (
    <>
      <button
        type="button"
        className="sidebar-toggle"
        aria-expanded={mobileOpen}
        onClick={() => setMobileOpen((o) => !o)}
      >
        {mobileOpen ? "✕ 閉じる" : "☰ カテゴリー・メニュー"}
      </button>

      <nav className={`sidebar-nav ${mobileOpen ? "is-open" : ""}`}>
        <Link href="/" className={`sidebar-all ${isAll ? "is-active" : ""}`}>
          すべてのレシピ
        </Link>

        <ul className="sidebar-groups">
          {groups.map((g) => {
            const isOpen = open.has(g.category);
            return (
              <li key={g.category}>
                <div className={`sidebar-category ${activeCategory === g.category ? "is-active" : ""}`}>
                  <button
                    type="button"
                    className="sidebar-expand"
                    aria-expanded={isOpen}
                    aria-label={`${g.category}のメニューを${isOpen ? "閉じる" : "開く"}`}
                    onClick={() => toggle(g.category)}
                  >
                    {isOpen ? "▾" : "▸"}
                  </button>
                  <Link href={categoryHref(g.category)} className="sidebar-category-link">
                    {g.category}
                  </Link>
                  <span className="sidebar-count">{g.recipes.length}</span>
                </div>
                {isOpen && (
                  <ul className="sidebar-recipes">
                    {g.recipes.map((r) => (
                      <li key={r.slug}>
                        <Link
                          href={`/recipes/${r.slug}`}
                          className={r.slug === activeSlug ? "is-active" : ""}
                          aria-current={r.slug === activeSlug ? "page" : undefined}
                        >
                          {r.title}
                        </Link>
                      </li>
                    ))}
                  </ul>
                )}
              </li>
            );
          })}
        </ul>
      </nav>
    </>
  );
}
