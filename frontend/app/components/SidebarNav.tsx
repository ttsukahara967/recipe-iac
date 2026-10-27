"use client";

import Link from "next/link";
import { usePathname, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import type { Locale } from "@/i18n/config";
import { categoryLabel, getDictionary } from "@/i18n/dictionaries";
import { categoryHref, homeHref, recipeHref } from "@/lib/links";

export type SidebarGroup = {
  category: string;
  recipes: { slug: string; title: string }[];
};

export default function SidebarNav({ groups, locale }: { groups: SidebarGroup[]; locale: Locale }) {
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const dict = getDictionary(locale);

  // Paths are locale-prefixed: /<locale>, /<locale>/recipes/<slug>
  const segments = pathname.split("/");
  const activeSlug = segments[2] === "recipes" ? decodeURIComponent(segments[3] ?? "") : null;
  const activeCategory =
    searchParams.get("category") ?? groups.find((g) => g.recipes.some((r) => r.slug === activeSlug))?.category ?? null;
  const isAll = pathname === `/${locale}` && !searchParams.get("category") && !searchParams.get("q");

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
        {mobileOpen ? dict.menuClose : dict.menuOpen}
      </button>

      <nav className={`sidebar-nav ${mobileOpen ? "is-open" : ""}`}>
        <Link href={homeHref(locale)} className={`sidebar-all ${isAll ? "is-active" : ""}`}>
          {dict.allRecipes}
        </Link>

        <ul className="sidebar-groups">
          {groups.map((g) => {
            const isOpen = open.has(g.category);
            const label = categoryLabel(locale, g.category);
            return (
              <li key={g.category}>
                <div className={`sidebar-category ${activeCategory === g.category ? "is-active" : ""}`}>
                  <button
                    type="button"
                    className="sidebar-expand"
                    aria-expanded={isOpen}
                    aria-label={dict.categoryMenuAria(label, isOpen)}
                    onClick={() => toggle(g.category)}
                  >
                    {isOpen ? "▾" : "▸"}
                  </button>
                  <Link href={categoryHref(locale, g.category)} className="sidebar-category-link">
                    {label}
                  </Link>
                  <span className="sidebar-count">{g.recipes.length}</span>
                </div>
                {isOpen && (
                  <ul className="sidebar-recipes">
                    {g.recipes.map((r) => (
                      <li key={r.slug}>
                        <Link
                          href={recipeHref(locale, r.slug)}
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
