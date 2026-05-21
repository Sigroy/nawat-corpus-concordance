from __future__ import annotations

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Source",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("slug", models.SlugField(max_length=160, unique=True)),
                ("title", models.CharField(max_length=500)),
                ("short_title", models.CharField(blank=True, max_length=180)),
                ("author", models.CharField(blank=True, max_length=255)),
                ("year", models.IntegerField(blank=True, null=True)),
                ("publication_info", models.TextField(blank=True)),
                (
                    "source_type",
                    models.CharField(
                        choices=[
                            ("grammar", "Grammar"),
                            ("dictionary", "Dictionary"),
                            ("story", "Story"),
                            ("bible", "Bible translation"),
                            ("field_notes", "Field notes"),
                            ("textbook", "Textbook"),
                            ("article", "Article"),
                            ("other", "Other"),
                        ],
                        default="other",
                        max_length=40,
                    ),
                ),
                ("genre", models.CharField(blank=True, max_length=120)),
                (
                    "language_codes",
                    models.CharField(
                        blank=True,
                        help_text="Comma-separated language labels/codes represented in the source.",
                        max_length=120,
                    ),
                ),
                ("rights_notes", models.TextField(blank=True)),
                ("permissions_url", models.URLField(blank=True)),
                ("citation", models.TextField(blank=True)),
                ("external_url", models.URLField(blank=True)),
                ("editorial_notes", models.TextField(blank=True)),
                ("legacy_source_id", models.CharField(blank=True, db_index=True, max_length=120)),
                ("metadata", models.JSONField(blank=True, default=dict)),
            ],
            options={
                "ordering": ["author", "year", "title"],
            },
        ),
        migrations.CreateModel(
            name="ImportJob",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("running", "Running"),
                            ("completed", "Completed"),
                            ("completed_with_warnings", "Completed with warnings"),
                            ("failed", "Failed"),
                        ],
                        default="pending",
                        max_length=40,
                    ),
                ),
                ("input_path", models.TextField(blank=True)),
                ("input_file_name", models.CharField(blank=True, max_length=255)),
                ("input_sha256", models.CharField(blank=True, db_index=True, max_length=64)),
                ("importer", models.CharField(default="manual", max_length=120)),
                ("options", models.JSONField(blank=True, default=dict)),
                ("started_at", models.DateTimeField(blank=True, null=True)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                ("summary", models.TextField(blank=True)),
                (
                    "source",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="import_jobs", to="corpus.source"),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Document",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=500)),
                ("description", models.TextField(blank=True)),
                ("document_type", models.CharField(default="pdf", max_length=80)),
                ("original_file_name", models.CharField(blank=True, max_length=255)),
                ("file_sha256", models.CharField(blank=True, db_index=True, max_length=64)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                (
                    "import_job",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="documents",
                        to="corpus.importjob",
                    ),
                ),
                (
                    "source",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="documents", to="corpus.source"),
                ),
            ],
            options={
                "ordering": ["source", "title"],
            },
        ),
        migrations.CreateModel(
            name="Page",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("page_number", models.PositiveIntegerField()),
                ("label", models.CharField(blank=True, max_length=80)),
                ("raw_text", models.TextField(blank=True)),
                ("corrected_text", models.TextField(blank=True)),
                ("extraction_method", models.CharField(default="pdfplumber", max_length=80)),
                ("extraction_confidence", models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ("is_reviewed", models.BooleanField(default=False)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                (
                    "document",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="pages", to="corpus.document"),
                ),
            ],
            options={
                "ordering": ["document", "page_number"],
            },
        ),
        migrations.CreateModel(
            name="TextUnit",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "unit_type",
                    models.CharField(
                        choices=[("section", "Section"), ("paragraph", "Paragraph"), ("excerpt", "Excerpt"), ("note", "Note")],
                        default="paragraph",
                        max_length=40,
                    ),
                ),
                ("sequence", models.PositiveIntegerField(default=1)),
                ("heading", models.CharField(blank=True, max_length=255)),
                ("raw_text", models.TextField(blank=True)),
                ("corrected_text", models.TextField(blank=True)),
                (
                    "review_status",
                    models.CharField(
                        choices=[
                            ("draft", "Draft"),
                            ("needs_review", "Needs review"),
                            ("reviewed", "Reviewed"),
                            ("approved", "Approved for corpus"),
                        ],
                        default="needs_review",
                        max_length=40,
                    ),
                ),
                ("is_approved_for_search", models.BooleanField(default=False)),
                ("notes", models.TextField(blank=True)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                (
                    "document",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="text_units", to="corpus.document"),
                ),
                (
                    "page",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="text_units",
                        to="corpus.page",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="corpus.textunit",
                    ),
                ),
            ],
            options={
                "ordering": ["document", "sequence", "id"],
            },
        ),
        migrations.CreateModel(
            name="Sentence",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("sequence", models.PositiveIntegerField()),
                ("text", models.TextField()),
                ("normalized_text", models.TextField(db_index=True)),
                ("start_offset", models.PositiveIntegerField(default=0)),
                ("end_offset", models.PositiveIntegerField(default=0)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                (
                    "document",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="sentences", to="corpus.document"),
                ),
                (
                    "page",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="sentences",
                        to="corpus.page",
                    ),
                ),
                (
                    "text_unit",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="sentences", to="corpus.textunit"),
                ),
            ],
            options={
                "ordering": ["document", "text_unit", "sequence"],
            },
        ),
        migrations.CreateModel(
            name="Token",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("sequence", models.PositiveIntegerField()),
                ("sentence_token_index", models.PositiveIntegerField()),
                ("original", models.CharField(max_length=255)),
                ("lower", models.CharField(db_index=True, max_length=255)),
                ("normalized", models.CharField(db_index=True, max_length=255)),
                ("normalized_unaccented", models.CharField(db_index=True, max_length=255)),
                ("start_offset", models.PositiveIntegerField(default=0)),
                ("end_offset", models.PositiveIntegerField(default=0)),
                ("is_word", models.BooleanField(default=True)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                (
                    "document",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="tokens", to="corpus.document"),
                ),
                (
                    "page",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="tokens",
                        to="corpus.page",
                    ),
                ),
                (
                    "sentence",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="tokens", to="corpus.sentence"),
                ),
                (
                    "text_unit",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="tokens", to="corpus.textunit"),
                ),
            ],
            options={
                "ordering": ["document", "sequence"],
            },
        ),
        migrations.CreateModel(
            name="SourceCitation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("label", models.CharField(blank=True, max_length=255)),
                ("locator", models.CharField(blank=True, max_length=120)),
                ("citation_text", models.TextField()),
                ("notes", models.TextField(blank=True)),
                (
                    "document",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="citations",
                        to="corpus.document",
                    ),
                ),
                (
                    "page",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="citations",
                        to="corpus.page",
                    ),
                ),
                (
                    "sentence",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="citations",
                        to="corpus.sentence",
                    ),
                ),
                (
                    "source",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="citations", to="corpus.source"),
                ),
                (
                    "text_unit",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="citations",
                        to="corpus.textunit",
                    ),
                ),
            ],
            options={
                "ordering": ["source", "document", "locator", "id"],
            },
        ),
        migrations.CreateModel(
            name="ImportIssue",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "severity",
                    models.CharField(
                        choices=[("info", "Info"), ("warning", "Warning"), ("error", "Error")],
                        default="warning",
                        max_length=20,
                    ),
                ),
                ("page_number", models.PositiveIntegerField(blank=True, null=True)),
                ("code", models.CharField(blank=True, max_length=80)),
                ("message", models.TextField()),
                ("raw_payload", models.JSONField(blank=True, default=dict)),
                (
                    "job",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="issues", to="corpus.importjob"),
                ),
            ],
            options={
                "ordering": ["created_at", "id"],
            },
        ),
        migrations.AddIndex(
            model_name="source",
            index=models.Index(fields=["author", "year"], name="corpus_sour_author_8e8d50_idx"),
        ),
        migrations.AddIndex(
            model_name="source",
            index=models.Index(fields=["source_type", "genre"], name="corpus_sour_source__0b30b1_idx"),
        ),
        migrations.AddIndex(
            model_name="importjob",
            index=models.Index(fields=["status", "created_at"], name="corpus_impo_status_24d53f_idx"),
        ),
        migrations.AddIndex(
            model_name="importjob",
            index=models.Index(fields=["input_sha256"], name="corpus_impo_input_s_7e9dd7_idx"),
        ),
        migrations.AddIndex(
            model_name="document",
            index=models.Index(fields=["source", "title"], name="corpus_docu_source__ec68fd_idx"),
        ),
        migrations.AddIndex(
            model_name="document",
            index=models.Index(fields=["file_sha256"], name="corpus_docu_file_sh_75a5f8_idx"),
        ),
        migrations.AddConstraint(
            model_name="page",
            constraint=models.UniqueConstraint(fields=("document", "page_number"), name="unique_page_per_document"),
        ),
        migrations.AddIndex(
            model_name="textunit",
            index=models.Index(fields=["document", "sequence"], name="cor_text_doc_seq_idx"),
        ),
        migrations.AddIndex(
            model_name="textunit",
            index=models.Index(fields=["is_approved_for_search", "review_status"], name="corpus_text_is_appr_7f1d7a_idx"),
        ),
        migrations.AddIndex(
            model_name="sentence",
            index=models.Index(fields=["document", "sequence"], name="cor_sent_doc_seq_idx"),
        ),
        migrations.AddIndex(
            model_name="sentence",
            index=models.Index(fields=["text_unit", "sequence"], name="corpus_sent_text_un_7a6afe_idx"),
        ),
        migrations.AddIndex(
            model_name="token",
            index=models.Index(fields=["normalized"], name="corpus_toke_normali_b24569_idx"),
        ),
        migrations.AddIndex(
            model_name="token",
            index=models.Index(fields=["normalized_unaccented"], name="corpus_toke_normali_f0cf01_idx"),
        ),
        migrations.AddIndex(
            model_name="token",
            index=models.Index(fields=["document", "sequence"], name="cor_tok_doc_seq_idx"),
        ),
        migrations.AddIndex(
            model_name="token",
            index=models.Index(fields=["sentence", "sentence_token_index"], name="corpus_toke_sentenc_b6dc71_idx"),
        ),
    ]
