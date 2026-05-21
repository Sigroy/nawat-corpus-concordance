from __future__ import annotations

from dataclasses import dataclass

from django.db.models import Q, QuerySet

from .models import Token
from .normalizers import query_normalizations


@dataclass(frozen=True)
class KwicResult:
    token: Token
    left_context: str
    match: str
    right_context: str
    sentence: str
    citation: str
    source_title: str
    source_author: str
    source_year: int | None
    page_number: int | None


def token_query(query: str, *, match_mode: str = "exact") -> Q:
    normalized = query_normalizations(query)
    value = normalized["normalized_unaccented"]
    if match_mode == "contains":
        return Q(normalized_unaccented__icontains=value)
    if match_mode == "prefix":
        return Q(normalized_unaccented__istartswith=value)
    if match_mode == "suffix":
        return Q(normalized_unaccented__iendswith=value)
    return Q(normalized_unaccented=value)


def search_tokens(
    query: str,
    *,
    match_mode: str = "exact",
    source_id: int | None = None,
    limit: int = 100,
) -> QuerySet[Token]:
    qs = (
        Token.objects.select_related("sentence", "page", "document", "document__source", "text_unit")
        .filter(token_query(query, match_mode=match_mode), text_unit__is_approved_for_search=True)
        .order_by("document__source__author", "document__source__year", "document__title", "sequence")
    )
    if source_id:
        qs = qs.filter(document__source_id=source_id)
    return qs[:limit]


def kwic_for_token(token: Token, *, window: int = 7) -> KwicResult:
    sentence_tokens = list(token.sentence.tokens.order_by("sentence_token_index"))
    index = next((idx for idx, item in enumerate(sentence_tokens) if item.id == token.id), 0)
    left = sentence_tokens[max(0, index - window) : index]
    right = sentence_tokens[index + 1 : index + 1 + window]
    source = token.document.source
    page_number = token.page.page_number if token.page else None
    citation = source.citation or str(source)
    if page_number:
        citation = f"{citation}, p. {page_number}"
    return KwicResult(
        token=token,
        left_context=" ".join(item.original for item in left),
        match=token.original,
        right_context=" ".join(item.original for item in right),
        sentence=token.sentence.text,
        citation=citation,
        source_title=source.title,
        source_author=source.author,
        source_year=source.year,
        page_number=page_number,
    )


def concordance_results(
    query: str,
    *,
    match_mode: str = "exact",
    source_id: int | None = None,
    sort: str = "source",
    limit: int = 100,
    window: int = 7,
) -> list[KwicResult]:
    results = [kwic_for_token(token, window=window) for token in search_tokens(query, match_mode=match_mode, source_id=source_id, limit=limit)]
    if sort == "left":
        return sorted(results, key=lambda item: item.left_context.casefold())
    if sort == "right":
        return sorted(results, key=lambda item: item.right_context.casefold())
    if sort == "year":
        return sorted(results, key=lambda item: (item.source_year or 9999, item.source_title, item.token.sequence))
    return results
