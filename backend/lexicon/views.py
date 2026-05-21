from __future__ import annotations

from django.db.models import Q
from rest_framework import generics

from corpus.normalizers import normalize_token

from .models import Entry
from .serializers import EntryDetailSerializer, EntryListSerializer


class DictionarySearchView(generics.ListAPIView):
    serializer_class = EntryListSerializer

    def get_queryset(self):
        query = (self.request.query_params.get("q") or "").strip()
        queryset = Entry.objects.prefetch_related("forms").order_by("headword")
        if not query:
            return queryset[:50]
        normalized = normalize_token(query, strip_accents=True)
        return queryset.filter(
            Q(normalized_headword__icontains=normalized)
            | Q(forms__normalized_form__icontains=normalized)
            | Q(headword__icontains=query)
        ).distinct()


class EntryDetailView(generics.RetrieveAPIView):
    serializer_class = EntryDetailSerializer
    queryset = Entry.objects.prefetch_related("forms", "senses__definitions__source")
