from __future__ import annotations

from django.contrib import admin

from .models import Document, ImportIssue, ImportJob, Page, Sentence, Source, SourceCitation, TextUnit, Token


class PageInline(admin.TabularInline):
    model = Page
    extra = 0
    fields = ["page_number", "label", "is_reviewed", "extraction_method"]
    readonly_fields = ["extraction_method"]


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "year", "source_type", "genre", "legacy_source_id"]
    list_filter = ["source_type", "genre", "year"]
    search_fields = ["title", "short_title", "author", "citation", "legacy_source_id"]
    prepopulated_fields = {"slug": ("short_title", "title")}


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["title", "source", "document_type", "original_file_name", "created_at"]
    list_filter = ["document_type", "source"]
    search_fields = ["title", "source__title", "source__author", "original_file_name"]
    inlines = [PageInline]


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ["document", "page_number", "label", "is_reviewed", "updated_at"]
    list_filter = ["is_reviewed", "document__source"]
    search_fields = ["document__title", "raw_text", "corrected_text"]


@admin.register(TextUnit)
class TextUnitAdmin(admin.ModelAdmin):
    list_display = ["document", "page", "sequence", "unit_type", "review_status", "is_approved_for_search", "heading"]
    list_filter = ["unit_type", "review_status", "is_approved_for_search", "document__source"]
    search_fields = ["heading", "raw_text", "corrected_text", "document__title"]
    actions = ["approve_for_search"]

    @admin.action(description="Approve selected text units for concordance search")
    def approve_for_search(self, request, queryset):
        queryset.update(review_status="approved", is_approved_for_search=True)


@admin.register(Sentence)
class SentenceAdmin(admin.ModelAdmin):
    list_display = ["document", "page", "sequence", "text"]
    list_filter = ["document__source"]
    search_fields = ["text", "normalized_text"]


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ["original", "normalized", "document", "page", "sequence"]
    list_filter = ["document__source"]
    search_fields = ["original", "normalized", "normalized_unaccented"]


class ImportIssueInline(admin.TabularInline):
    model = ImportIssue
    extra = 0
    readonly_fields = ["severity", "page_number", "code", "message", "created_at"]


@admin.register(ImportJob)
class ImportJobAdmin(admin.ModelAdmin):
    list_display = ["source", "status", "input_file_name", "input_sha256", "created_at", "completed_at"]
    list_filter = ["status", "importer"]
    search_fields = ["input_file_name", "input_path", "input_sha256", "summary"]
    inlines = [ImportIssueInline]


@admin.register(SourceCitation)
class SourceCitationAdmin(admin.ModelAdmin):
    list_display = ["source", "document", "locator", "label"]
    search_fields = ["citation_text", "label", "locator", "source__title"]
