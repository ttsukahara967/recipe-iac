"use client";

import { useSearchParams } from "next/navigation";

// Plain GET form to /?q=..., so results are shareable URLs and it works before hydration
export default function SearchBox() {
  const q = useSearchParams().get("q") ?? "";
  return (
    <form action="/" method="get" role="search" className="search-box">
      <input
        key={q}
        type="search"
        name="q"
        defaultValue={q}
        placeholder="料理名や材料で探す（例：卵、豚こま）"
        aria-label="レシピを検索"
        maxLength={100}
      />
      <button type="submit" aria-label="検索">
        🔍
      </button>
    </form>
  );
}
