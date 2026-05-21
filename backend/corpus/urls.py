from __future__ import annotations

from django.urls import path

from .views import ConcordanceHitView, ConcordanceSearchView, SourceDetailView, SourceListView

urlpatterns = [
    path("sources", SourceListView.as_view(), name="source-list"),
    path("sources/<int:pk>", SourceDetailView.as_view(), name="source-detail"),
    path("search/concordance", ConcordanceSearchView.as_view(), name="concordance-search"),
    path("concordance/<int:token_id>", ConcordanceHitView.as_view(), name="concordance-hit"),
]
