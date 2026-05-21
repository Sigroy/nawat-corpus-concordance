from __future__ import annotations

import re
import unicodedata

APOSTROPHE_TRANSLATION = str.maketrans(
    {
        "’": "'",
        "‘": "'",
        "ʼ": "'",
        "`": "'",
        "´": "'",
    }
)

EDGE_PUNCT_RE = re.compile(r"^[\W_]+|[\W_]+$", flags=re.UNICODE)
INNER_SPACE_RE = re.compile(r"\s+")


def normalize_apostrophes(value: str) -> str:
    return value.translate(APOSTROPHE_TRANSLATION)


def strip_diacritics(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value)
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))


def normalize_token(value: str, *, strip_accents: bool = False) -> str:
    normalized = normalize_apostrophes(value).casefold().strip()
    normalized = EDGE_PUNCT_RE.sub("", normalized)
    normalized = INNER_SPACE_RE.sub(" ", normalized)
    if strip_accents:
        normalized = strip_diacritics(normalized)
    return normalized


def normalize_text(value: str, *, strip_accents: bool = False) -> str:
    normalized = normalize_apostrophes(value).casefold()
    normalized = INNER_SPACE_RE.sub(" ", normalized).strip()
    if strip_accents:
        normalized = strip_diacritics(normalized)
    return normalized


def query_normalizations(query: str) -> dict[str, str]:
    normalized = normalize_token(query)
    return {
        "original": query,
        "normalized": normalized,
        "normalized_unaccented": normalize_token(normalized, strip_accents=True),
    }
