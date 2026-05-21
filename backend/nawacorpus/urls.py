from __future__ import annotations

from django.contrib import admin
from django.urls import include, path
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def health(_: object) -> Response:
    return Response({"status": "ok", "service": "nawat-corpus"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health", health, name="health"),
    path("api/", include("corpus.urls")),
    path("api/", include("lexicon.urls")),
]
