from __future__ import annotations

from django.contrib import admin

from .models import Attestation, Definition, Entry, Example, Form, Sense


class FormInline(admin.TabularInline):
    model = Form
    extra = 0


class SenseInline(admin.TabularInline):
    model = Sense
    extra = 0


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ["headword", "part_of_speech", "status", "normalized_headword"]
    list_filter = ["status", "part_of_speech"]
    search_fields = ["headword", "normalized_headword", "learner_notes", "researcher_notes"]
    inlines = [FormInline, SenseInline]


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ["form", "entry", "kind", "source", "grammatical_description"]
    list_filter = ["kind", "source"]
    search_fields = ["form", "normalized_form", "entry__headword"]


@admin.register(Sense)
class SenseAdmin(admin.ModelAdmin):
    list_display = ["entry", "sense_number", "part_of_speech", "semantic_domain"]
    search_fields = ["entry__headword", "notes", "semantic_domain"]


@admin.register(Definition)
class DefinitionAdmin(admin.ModelAdmin):
    list_display = ["sense", "language", "source", "is_source_specific", "text"]
    list_filter = ["language", "is_source_specific", "source"]
    search_fields = ["text", "sense__entry__headword"]


@admin.register(Example)
class ExampleAdmin(admin.ModelAdmin):
    list_display = ["sense", "source", "nawat_text"]
    search_fields = ["nawat_text", "spanish_text", "english_text", "citation"]


@admin.register(Attestation)
class AttestationAdmin(admin.ModelAdmin):
    list_display = ["entry", "form", "source", "original_form", "confidence"]
    list_filter = ["confidence", "source"]
    search_fields = ["entry__headword", "original_form", "citation"]
