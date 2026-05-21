from __future__ import annotations

from rest_framework import serializers

from .models import Definition, Entry, Form, Sense


class DefinitionSerializer(serializers.ModelSerializer):
    source_title = serializers.CharField(source="source.title", read_only=True, allow_null=True)

    class Meta:
        model = Definition
        fields = ["id", "language", "text", "is_source_specific", "source_title", "notes", "legacy_marker"]


class SenseSerializer(serializers.ModelSerializer):
    definitions = DefinitionSerializer(many=True, read_only=True)

    class Meta:
        model = Sense
        fields = ["id", "sense_number", "part_of_speech", "semantic_domain", "notes", "definitions"]


class FormSerializer(serializers.ModelSerializer):
    source_title = serializers.CharField(source="source.title", read_only=True, allow_null=True)

    class Meta:
        model = Form
        fields = ["id", "form", "normalized_form", "kind", "grammatical_description", "source_title", "notes"]


class EntryListSerializer(serializers.ModelSerializer):
    forms = FormSerializer(many=True, read_only=True)

    class Meta:
        model = Entry
        fields = ["id", "headword", "normalized_headword", "part_of_speech", "status", "forms"]


class EntryDetailSerializer(EntryListSerializer):
    senses = SenseSerializer(many=True, read_only=True)

    class Meta(EntryListSerializer.Meta):
        fields = EntryListSerializer.Meta.fields + [
            "etymology",
            "pronunciation_ipa",
            "learner_notes",
            "researcher_notes",
            "senses",
        ]
