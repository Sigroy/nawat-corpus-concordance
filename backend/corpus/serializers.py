from __future__ import annotations

from rest_framework import serializers

from .models import Document, Page, Sentence, Source, TextUnit, Token
from .search import KwicResult


class SourceListSerializer(serializers.ModelSerializer):
    document_count = serializers.SerializerMethodField()

    class Meta:
        model = Source
        fields = [
            "id",
            "slug",
            "title",
            "short_title",
            "author",
            "year",
            "source_type",
            "genre",
            "citation",
            "document_count",
        ]

    def get_document_count(self, obj: Source) -> int:
        return getattr(obj, "document_total", obj.documents.count())


class PageSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ["id", "page_number", "label", "is_reviewed"]


class DocumentSerializer(serializers.ModelSerializer):
    pages = PageSummarySerializer(many=True, read_only=True)

    class Meta:
        model = Document
        fields = [
            "id",
            "title",
            "description",
            "document_type",
            "original_file_name",
            "pages",
        ]


class SourceDetailSerializer(SourceListSerializer):
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta(SourceListSerializer.Meta):
        fields = SourceListSerializer.Meta.fields + [
            "publication_info",
            "language_codes",
            "rights_notes",
            "permissions_url",
            "external_url",
            "editorial_notes",
            "legacy_source_id",
            "metadata",
            "documents",
        ]


class SentenceContextSerializer(serializers.ModelSerializer):
    source = SourceListSerializer(source="document.source", read_only=True)
    page_number = serializers.IntegerField(source="page.page_number", read_only=True, allow_null=True)
    paragraph_text = serializers.CharField(source="text_unit.text", read_only=True)

    class Meta:
        model = Sentence
        fields = [
            "id",
            "text",
            "paragraph_text",
            "page_number",
            "start_offset",
            "end_offset",
            "source",
        ]


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = [
            "id",
            "original",
            "normalized",
            "normalized_unaccented",
            "sequence",
            "sentence_token_index",
        ]


class TextUnitSerializer(serializers.ModelSerializer):
    page_number = serializers.IntegerField(source="page.page_number", read_only=True, allow_null=True)

    class Meta:
        model = TextUnit
        fields = [
            "id",
            "unit_type",
            "sequence",
            "heading",
            "text",
            "review_status",
            "is_approved_for_search",
            "page_number",
        ]


class KwicResultSerializer(serializers.Serializer):
    token_id = serializers.IntegerField()
    left_context = serializers.CharField()
    match = serializers.CharField()
    right_context = serializers.CharField()
    sentence = serializers.CharField()
    citation = serializers.CharField()
    source_title = serializers.CharField()
    source_author = serializers.CharField(allow_blank=True)
    source_year = serializers.IntegerField(allow_null=True)
    page_number = serializers.IntegerField(allow_null=True)

    @staticmethod
    def from_result(result: KwicResult) -> dict[str, object]:
        return {
            "token_id": result.token.id,
            "left_context": result.left_context,
            "match": result.match,
            "right_context": result.right_context,
            "sentence": result.sentence,
            "citation": result.citation,
            "source_title": result.source_title,
            "source_author": result.source_author,
            "source_year": result.source_year,
            "page_number": result.page_number,
        }
