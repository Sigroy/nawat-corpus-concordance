from __future__ import annotations

from django.db import models

from corpus.models import Source, TimestampedModel


class EntryStatus(models.TextChoices):
    ATTESTED = "attested", "Traditional attested form"
    REVIVED = "revived", "Revived form"
    MODERN_COINAGE = "modern_coinage", "Modern coinage"
    LOANWORD = "loanword", "Loanword"
    UNCERTAIN = "uncertain", "Uncertain"


class Entry(TimestampedModel):
    headword = models.CharField(max_length=255)
    normalized_headword = models.CharField(max_length=255, db_index=True)
    part_of_speech = models.CharField(max_length=120, blank=True)
    status = models.CharField(
        max_length=40,
        choices=EntryStatus.choices,
        default=EntryStatus.ATTESTED,
        db_index=True,
    )
    etymology = models.TextField(blank=True)
    pronunciation_ipa = models.CharField(max_length=255, blank=True)
    learner_notes = models.TextField(blank=True)
    researcher_notes = models.TextField(blank=True)
    legacy_payload = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["headword"]
        indexes = [
            models.Index(fields=["normalized_headword"], name="lexicon_ent_normali_d0a226_idx"),
            models.Index(fields=["part_of_speech", "status"], name="lexicon_ent_part_of_6f9ce3_idx"),
        ]

    def __str__(self) -> str:
        return self.headword


class FormKind(models.TextChoices):
    HEADWORD = "headword", "Headword"
    VARIANT = "variant", "Variant spelling"
    INFLECTED = "inflected", "Inflected form"
    DERIVED = "derived", "Derived form"
    COMPOUND = "compound", "Compound"
    MORPHEME = "morpheme", "Morpheme"
    SOURCE_SPELLING = "source_spelling", "Source spelling"
    OTHER = "other", "Other"


class Form(TimestampedModel):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="forms")
    source = models.ForeignKey(Source, null=True, blank=True, on_delete=models.SET_NULL, related_name="lexical_forms")
    form = models.CharField(max_length=255)
    normalized_form = models.CharField(max_length=255, db_index=True)
    kind = models.CharField(max_length=40, choices=FormKind.choices, default=FormKind.VARIANT)
    grammatical_description = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    legacy_marker = models.CharField(max_length=80, blank=True)
    legacy_payload = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["entry", "kind", "form"]
        indexes = [
            models.Index(fields=["normalized_form", "kind"], name="lexicon_for_normali_b162c8_idx"),
        ]

    def __str__(self) -> str:
        return self.form


class Sense(TimestampedModel):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="senses")
    sense_number = models.CharField(max_length=40, blank=True)
    part_of_speech = models.CharField(max_length=120, blank=True)
    semantic_domain = models.CharField(max_length=160, blank=True)
    notes = models.TextField(blank=True)
    legacy_payload = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["entry", "sense_number", "id"]

    def __str__(self) -> str:
        suffix = f" {self.sense_number}" if self.sense_number else ""
        return f"{self.entry.headword}{suffix}"


class Definition(TimestampedModel):
    sense = models.ForeignKey(Sense, on_delete=models.CASCADE, related_name="definitions")
    source = models.ForeignKey(Source, null=True, blank=True, on_delete=models.SET_NULL, related_name="definitions")
    language = models.CharField(
        max_length=12,
        choices=[("es", "Spanish"), ("en", "English"), ("de", "German"), ("nah", "Nawat"), ("other", "Other")],
        default="es",
    )
    text = models.TextField()
    is_source_specific = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    legacy_marker = models.CharField(max_length=80, blank=True)

    class Meta:
        ordering = ["sense", "language", "id"]

    def __str__(self) -> str:
        return f"{self.language}: {self.text[:80]}"


class Example(TimestampedModel):
    sense = models.ForeignKey(Sense, on_delete=models.CASCADE, related_name="examples")
    source = models.ForeignKey(Source, null=True, blank=True, on_delete=models.SET_NULL, related_name="lexicon_examples")
    nawat_text = models.TextField()
    spanish_text = models.TextField(blank=True)
    english_text = models.TextField(blank=True)
    citation = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    legacy_payload = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["sense", "id"]

    def __str__(self) -> str:
        return self.nawat_text[:100]


class Attestation(TimestampedModel):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="attestations")
    form = models.ForeignKey(Form, null=True, blank=True, on_delete=models.SET_NULL, related_name="attestations")
    sense = models.ForeignKey(Sense, null=True, blank=True, on_delete=models.SET_NULL, related_name="attestations")
    token = models.ForeignKey("corpus.Token", null=True, blank=True, on_delete=models.SET_NULL, related_name="attestations")
    source = models.ForeignKey(Source, null=True, blank=True, on_delete=models.SET_NULL, related_name="attestations")
    original_form = models.CharField(max_length=255, blank=True)
    citation = models.TextField(blank=True)
    confidence = models.CharField(
        max_length=40,
        choices=[("certain", "Certain"), ("probable", "Probable"), ("uncertain", "Uncertain")],
        default="uncertain",
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["entry", "source", "id"]
        indexes = [
            models.Index(fields=["confidence"], name="lexicon_att_confide_43f915_idx"),
        ]

    def __str__(self) -> str:
        return self.original_form or self.entry.headword
