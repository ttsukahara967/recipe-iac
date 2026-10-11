"""Keyword helpers for recipe search: Unicode/kana normalization and LIKE escaping."""

import unicodedata

_HIRA_START, _HIRA_END = ord("ぁ"), ord("ゖ")
_KANA_OFFSET = ord("ァ") - ord("ぁ")


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


def query_variants(term: str) -> set[str]:
    """LIKE-escaped forms of a term so hiragana and katakana match each other (はんばーぐ ⇔ ハンバーグ)."""
    return {_escape_like(v) for v in (term, _to_katakana(term), _to_hiragana(term))}
