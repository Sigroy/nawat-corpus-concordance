from __future__ import annotations

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("corpus", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Entry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("headword", models.CharField(max_length=255)),
                ("normalized_headword", models.CharField(db_index=True, max_length=255)),
                ("part_of_speech", models.CharField(blank=True, max_length=120)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("attested", "Traditional attested form"),
                            ("revived", "Revived form"),
                            ("modern_coinage", "Modern coinage"),
                            ("loanword", "Loanword"),
                            ("uncertain", "Uncertain"),
                        ],
                        db_index=True,
                        default="attested",
                        max_length=40,
                    ),
                ),
                ("etymology", models.TextField(blank=True)),
                ("pronunciation_ipa", models.CharField(blank=True, max_length=255)),
                ("learner_notes", models.TextField(blank=True)),
                ("researcher_notes", models.TextField(blank=True)),
                ("legacy_payload", models.JSONField(blank=True, default=dict)),
            ],
            options={
                "ordering": ["headword"],
            },
        ),
        migrations.CreateModel(
            name="Sense",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("sense_number", models.CharField(blank=True, max_length=40)),
                ("part_of_speech", models.CharField(blank=True, max_length=120)),
                ("semantic_domain", models.CharField(blank=True, max_length=160)),
                ("notes", models.TextField(blank=True)),
                ("legacy_payload", models.JSONField(blank=True, default=dict)),
                ("entry", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="senses", to="lexicon.entry")),
            ],
            options={
                "ordering": ["entry", "sense_number", "id"],
            },
        ),
        migrations.CreateModel(
            name="Form",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("form", models.CharField(max_length=255)),
                ("normalized_form", models.CharField(db_index=True, max_length=255)),
                (
                    "kind",
                    models.CharField(
                        choices=[
                            ("headword", "Headword"),
                            ("variant", "Variant spelling"),
                            ("inflected", "Inflected form"),
                            ("derived", "Derived form"),
                            ("compound", "Compound"),
                            ("morpheme", "Morpheme"),
                            ("source_spelling", "Source spelling"),
                            ("other", "Other"),
                        ],
                        default="variant",
                        max_length=40,
                    ),
                ),
                ("grammatical_description", models.CharField(blank=True, max_length=255)),
                ("notes", models.TextField(blank=True)),
                ("legacy_marker", models.CharField(blank=True, max_length=80)),
                ("legacy_payload", models.JSONField(blank=True, default=dict)),
                ("entry", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="forms", to="lexicon.entry")),
                (
                    "source",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="lexical_forms",
                        to="corpus.source",
                    ),
                ),
            ],
            options={
                "ordering": ["entry", "kind", "form"],
            },
        ),
        migrations.CreateModel(
            name="Definition",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "language",
                    models.CharField(
                        choices=[
                            ("es", "Spanish"),
                            ("en", "English"),
                            ("de", "German"),
                            ("nah", "Nawat"),
                            ("other", "Other"),
                        ],
                        default="es",
                        max_length=12,
                    ),
                ),
                ("text", models.TextField()),
                ("is_source_specific", models.BooleanField(default=False)),
                ("notes", models.TextField(blank=True)),
                ("legacy_marker", models.CharField(blank=True, max_length=80)),
                ("sense", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="definitions", to="lexicon.sense")),
                (
                    "source",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="definitions",
                        to="corpus.source",
                    ),
                ),
            ],
            options={
                "ordering": ["sense", "language", "id"],
            },
        ),
        migrations.CreateModel(
            name="Example",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("nawat_text", models.TextField()),
                ("spanish_text", models.TextField(blank=True)),
                ("english_text", models.TextField(blank=True)),
                ("citation", models.TextField(blank=True)),
                ("notes", models.TextField(blank=True)),
                ("legacy_payload", models.JSONField(blank=True, default=dict)),
                ("sense", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="examples", to="lexicon.sense")),
                (
                    "source",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="lexicon_examples",
                        to="corpus.source",
                    ),
                ),
            ],
            options={
                "ordering": ["sense", "id"],
            },
        ),
        migrations.CreateModel(
            name="Attestation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("original_form", models.CharField(blank=True, max_length=255)),
                ("citation", models.TextField(blank=True)),
                (
                    "confidence",
                    models.CharField(
                        choices=[("certain", "Certain"), ("probable", "Probable"), ("uncertain", "Uncertain")],
                        default="uncertain",
                        max_length=40,
                    ),
                ),
                ("notes", models.TextField(blank=True)),
                ("entry", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="attestations", to="lexicon.entry")),
                (
                    "form",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="attestations",
                        to="lexicon.form",
                    ),
                ),
                (
                    "sense",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="attestations",
                        to="lexicon.sense",
                    ),
                ),
                (
                    "source",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="attestations",
                        to="corpus.source",
                    ),
                ),
                (
                    "token",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="attestations",
                        to="corpus.token",
                    ),
                ),
            ],
            options={
                "ordering": ["entry", "source", "id"],
            },
        ),
        migrations.AddIndex(
            model_name="entry",
            index=models.Index(fields=["normalized_headword"], name="lexicon_ent_normali_d0a226_idx"),
        ),
        migrations.AddIndex(
            model_name="entry",
            index=models.Index(fields=["part_of_speech", "status"], name="lexicon_ent_part_of_6f9ce3_idx"),
        ),
        migrations.AddIndex(
            model_name="form",
            index=models.Index(fields=["normalized_form", "kind"], name="lexicon_for_normali_b162c8_idx"),
        ),
        migrations.AddIndex(
            model_name="attestation",
            index=models.Index(fields=["confidence"], name="lexicon_att_confide_43f915_idx"),
        ),
    ]
