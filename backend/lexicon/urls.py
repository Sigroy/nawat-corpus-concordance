from __future__ import annotations

from django.urls import path

from .views import DictionarySearchView, EntryDetailView

urlpatterns = [
    path("dictionary/search", DictionarySearchView.as_view(), name="dictionary-search"),
    path("entries/<int:pk>", EntryDetailView.as_view(), name="entry-detail"),
]
