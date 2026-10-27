"""Keyword helpers for recipe search: Unicode/kana normalization, food synonyms and LIKE escaping."""

import unicodedata

_HIRA_START, _HIRA_END = ord("ぁ"), ord("ゖ")
_KANA_OFFSET = ord("ァ") - ord("ぁ")

# Words that mean the same ingredient but differ in kanji/kana spelling (hiragana vs katakana is
# already handled separately). If a search term contains one of these words, the other spellings
# are searched too, e.g. たまご → 卵 / 玉子, ぶたこま → 豚こま. Add entries here as needed.
SYNONYM_GROUPS: list[tuple[str, ...]] = [
    ("卵", "たまご", "玉子"),
    ("豚肉", "ぶたにく", "ポーク"),
    ("豚", "ぶた"),
    ("牛肉", "ぎゅうにく", "ビーフ"),
    ("鶏肉", "とりにく", "チキン"),
    ("鶏", "とり", "鳥"),
    ("ひき肉", "挽き肉", "挽肉", "ミンチ"),
    ("鮭", "さけ", "しゃけ", "サーモン"),
    ("鯖", "さば"),
    ("鰯", "いわし"),
    ("海老", "えび"),
    ("烏賊", "いか"),
    ("蛸", "たこ"),
    ("鰹節", "かつお節", "かつおぶし"),
    ("昆布", "こんぶ"),
    ("海苔", "のり"),
    ("豆腐", "とうふ"),
    ("味噌", "みそ"),
    ("醤油", "しょうゆ"),
    ("生姜", "しょうが"),
    ("大蒜", "にんにく", "ガーリック"),
    ("葱", "ねぎ"),
    ("玉葱", "玉ねぎ", "たまねぎ"),
    ("大根", "だいこん"),
    ("人参", "にんじん"),
    ("牛蒡", "ごぼう"),
    ("茄子", "なす"),
    ("胡瓜", "きゅうり"),
    ("南瓜", "かぼちゃ"),
    ("白菜", "はくさい"),
    ("椎茸", "しいたけ"),
    ("韮", "にら"),
    ("蒟蒻", "こんにゃく"),
    ("胡麻", "ごま"),
    ("林檎", "りんご"),
    ("苺", "いちご"),
    ("檸檬", "れもん"),
    ("牛乳", "ぎゅうにゅう", "ミルク"),
    ("ご飯", "ごはん"),
    ("饂飩", "うどん"),
    ("唐揚げ", "から揚げ", "からあげ"),
    ("餃子", "ぎょうざ"),
    ("炒飯", "チャーハン"),
    ("天かす", "揚げ玉"),
]


def _to_katakana(text: str) -> str:
    return "".join(chr(ord(c) + _KANA_OFFSET) if _HIRA_START <= ord(c) <= _HIRA_END else c for c in text)


def _to_hiragana(text: str) -> str:
    start, end = _HIRA_START + _KANA_OFFSET, _HIRA_END + _KANA_OFFSET
    return "".join(chr(ord(c) - _KANA_OFFSET) if start <= ord(c) <= end else c for c in text)


def _escape_like(text: str) -> str:
    return text.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def split_terms(q: str | None) -> list[str]:
    """NFKC-normalize (full-width letters, half-width kana, full-width spaces) and split on spaces."""
    if not q:
        return []
    return [t for t in unicodedata.normalize("NFKC", q).split() if t]


def english_terms(q: str | None) -> list[str]:
    """Split an English query into LIKE-escaped, whitespace-separated terms (matched case-insensitively)."""
    if not q:
        return []
    return [_escape_like(t) for t in q.split() if t]


def _synonym_spellings(term: str) -> set[str]:
    """The term plus copies where a synonym-group word inside it is swapped for the other spellings.

    Matching is done in katakana so it ignores the hiragana/katakana difference.
    """
    kterm = _to_katakana(term)
    spellings = {term}
    for group in SYNONYM_GROUPS:
        kgroup = [_to_katakana(w) for w in group]
        for word in kgroup:
            if _contains_word(kterm, word):
                spellings.update(kterm.replace(word, other) for other in kgroup)
    return spellings


def _contains_word(kterm: str, word: str) -> bool:
    # Short kana words (タコ, イカ, ナス, ...) easily appear inside other words (ブタコマ), so they only
    # count at the start or end of the term
    if len(word) <= 2 and all(_is_kana(c) for c in word):
        return kterm.startswith(word) or kterm.endswith(word)
    return word in kterm


def _is_kana(c: str) -> bool:
    return "ァ" <= c <= "ヶ" or c == "ー"


def query_variants(term: str) -> set[str]:
    """LIKE-escaped forms of a term: synonym spellings (たまご ⇔ 卵) in both hiragana and katakana
    (はんばーぐ ⇔ ハンバーグ)."""
    variants = set()
    for spelling in _synonym_spellings(term):
        variants.update((spelling, _to_katakana(spelling), _to_hiragana(spelling)))
    return {_escape_like(v) for v in variants}
