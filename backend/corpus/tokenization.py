from __future__ import annotations

import re
from dataclasses import dataclass

from .normalizers import normalize_text, normalize_token

TOKEN_RE = re.compile(r"[^\W\d_]+(?:[’'ʼ:-][^\W\d_]+)*", flags=re.UNICODE)
SENTENCE_END_RE = re.compile(r"(?<=[.!?;:…])\s+(?=[A-ZÁÉÍÓÚÜÑ¿¡\"'“‘(]|\d)", flags=re.UNICODE)


@dataclass(frozen=True)
class SentenceSpan:
    text: str
    start: int
    end: int


@dataclass(frozen=True)
class TokenSpan:
    original: str
    lower: str
    normalized: str
    normalized_unaccented: str
    start: int
    end: int


def split_sentences(text: str) -> list[SentenceSpan]:
    spans: list[SentenceSpan] = []
    cursor = 0
    for part in SENTENCE_END_RE.split(text):
        raw = part.strip()
        if not raw:
            cursor += len(part)
            continue
        start = text.find(raw, cursor)
        end = start + len(raw)
        spans.append(SentenceSpan(text=raw, start=start, end=end))
        cursor = end
    if not spans and text.strip():
        raw = text.strip()
        spans.append(SentenceSpan(text=raw, start=text.find(raw), end=text.find(raw) + len(raw)))
    return spans


def iter_tokens(text: str, *, base_offset: int = 0) -> list[TokenSpan]:
    tokens: list[TokenSpan] = []
    for match in TOKEN_RE.finditer(text):
        original = match.group(0)
        normalized = normalize_token(original)
        if not normalized:
            continue
        tokens.append(
            TokenSpan(
                original=original,
                lower=original.casefold(),
                normalized=normalized,
                normalized_unaccented=normalize_token(original, strip_accents=True),
                start=base_offset + match.start(),
                end=base_offset + match.end(),
            )
        )
    return tokens


def normalized_sentence_text(text: str) -> str:
    return normalize_text(text, strip_accents=True)
