from __future__ import annotations

from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Source, Token
from .search import concordance_results, kwic_for_token
from .serializers import (
    KwicResultSerializer,
    SentenceContextSerializer,
    SourceDetailSerializer,
    SourceListSerializer,
    TokenSerializer,
)


class SourceListView(generics.ListAPIView):
    serializer_class = SourceListSerializer

    def get_queryset(self):
        queryset = Source.objects.annotate(document_total=Count("documents"))
        query = self.request.query_params.get("q")
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(author__icontains=query))
        return queryset.order_by("author", "year", "title")


class SourceDetailView(generics.RetrieveAPIView):
    serializer_class = SourceDetailSerializer
    queryset = Source.objects.prefetch_related("documents__pages")


class ConcordanceSearchView(APIView):
    def get(self, request):
        query = (request.query_params.get("q") or "").strip()
        if not query:
            return Response(
                {
                    "query": "",
                    "count": 0,
                    "results": [],
                    "detail": "Provide a q parameter to search the corpus.",
                }
            )

        match_mode = request.query_params.get("match", "exact")
        if match_mode not in {"exact", "contains", "prefix", "suffix"}:
            match_mode = "exact"
        sort = request.query_params.get("sort", "source")
        source_id = request.query_params.get("source")
        limit = min(int(request.query_params.get("limit", 100)), 500)
        window = min(int(request.query_params.get("window", 7)), 20)

        results = concordance_results(
            query,
            match_mode=match_mode,
            source_id=int(source_id) if source_id else None,
            sort=sort,
            limit=limit,
            window=window,
        )
        return Response(
            {
                "query": query,
                "match_mode": match_mode,
                "sort": sort,
                "count": len(results),
                "results": [KwicResultSerializer.from_result(result) for result in results],
            }
        )


class ConcordanceHitView(APIView):
    def get(self, request, token_id: int):
        token = get_object_or_404(
            Token.objects.select_related("sentence", "text_unit", "page", "document", "document__source"),
            pk=token_id,
        )
        kwic = kwic_for_token(token, window=min(int(request.query_params.get("window", 10)), 30))
        sentence_payload = SentenceContextSerializer(token.sentence).data
        sentence_payload["tokens"] = TokenSerializer(token.sentence.tokens.order_by("sentence_token_index"), many=True).data
        return Response(
            {
                "hit": KwicResultSerializer.from_result(kwic),
                "context": sentence_payload,
            }
        )
