from __future__ import annotations

from django.db import models
from django.utils.text import slugify


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SourceType(models.TextChoices):
    GRAMMAR = "grammar", "Grammar"
    DICTIONARY = "dictionary", "Dictionary"
    STORY = "story", "Story"
    BIBLE = "bible", "Bible translation"
    FIELD_NOTES = "field_notes", "Field notes"
    TEXTBOOK = "textbook", "Textbook"
    ARTICLE = "article", "Article"
    OTHER = "other", "Other"


class Source(TimestampedModel):
    slug = models.SlugField(max_length=160, unique=True)
    title = models.CharField(max_length=500)
    short_title = models.CharField(max_length=180, blank=True)
    author = models.CharField(max_length=255, blank=True)
    year = models.IntegerField(null=True, blank=True)
    publication_info = models.TextField(blank=True)
    source_type = models.CharField(
        max_length=40,
        choices=SourceType.choices,
        default=SourceType.OTHER,
    )
    genre = models.CharField(max_length=120, blank=True)
    language_codes = models.CharField(
        max_length=120,
        blank=True,
        help_text="Comma-separated language labels/codes represented in the source.",
    )
    rights_notes = models.TextField(blank=True)
    permissions_url = models.URLField(blank=True)
    citation = models.TextField(blank=True)
    external_url = models.URLField(blank=True)
    editorial_notes = models.TextField(blank=True)
    legacy_source_id = models.CharField(max_length=120, blank=True, db_index=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["author", "year", "title"]
        indexes = [
            models.Index(fields=["author", "year"], name="corpus_sour_author_8e8d50_idx"),
            models.Index(fields=["source_type", "genre"], name="corpus_sour_source__0b30b1_idx"),
        ]

    def save(self, *args: object, **kwargs: object) -> None:
        if not self.slug:
            base = self.short_title or self.title
            if self.year:
                base = f"{base}-{self.year}"
            self.slug = slugify(base)[:150]
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        if self.year and self.author:
            return f"{self.author} ({self.year}) - {self.title}"
        return self.short_title or self.title


class ImportStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    RUNNING = "running", "Running"
    COMPLETED = "completed", "Completed"
    COMPLETED_WITH_WARNINGS = "completed_with_warnings", "Completed with warnings"
    FAILED = "failed", "Failed"


class ImportJob(TimestampedModel):
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name="import_jobs")
    status = models.CharField(
        max_length=40,
        choices=ImportStatus.choices,
        default=ImportStatus.PENDING,
    )
    input_path = models.TextField(blank=True)
    input_file_name = models.CharField(max_length=255, blank=True)
    input_sha256 = models.CharField(max_length=64, blank=True, db_index=True)
    importer = models.CharField(max_length=120, default="manual")
    options = models.JSONField(default=dict, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    summary = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "created_at"], name="corpus_impo_status_24d53f_idx"),
            models.Index(fields=["input_sha256"], name="corpus_impo_input_s_7e9dd7_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.source} import {self.created_at:%Y-%m-%d %H:%M}"


class ImportIssue(TimestampedModel):
    job = models.ForeignKey(ImportJob, on_delete=models.CASCADE, related_name="issues")
    severity = models.CharField(
        max_length=20,
        choices=[("info", "Info"), ("warning", "Warning"), ("error", "Error")],
        default="warning",
    )
    page_number = models.PositiveIntegerField(null=True, blank=True)
    code = models.CharField(max_length=80, blank=True)
    message = models.TextField()
    raw_payload = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["created_at", "id"]

    def __str__(self) -> str:
        location = f" page {self.page_number}" if self.page_number else ""
        return f"{self.severity}{location}: {self.message[:80]}"


class Document(TimestampedModel):
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name="documents")
    import_job = models.ForeignKey(
        ImportJob,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="documents",
    )
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    document_type = models.CharField(max_length=80, default="pdf")
    original_file_name = models.CharField(max_length=255, blank=True)
    file_sha256 = models.CharField(max_length=64, blank=True, db_index=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["source", "title"]
        indexes = [
            models.Index(fields=["source", "title"], name="corpus_docu_source__ec68fd_idx"),
            models.Index(fields=["file_sha256"], name="corpus_docu_file_sh_75a5f8_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.title} ({self.source})"


class Page(TimestampedModel):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="pages")
    page_number = models.PositiveIntegerField()
    label = models.CharField(max_length=80, blank=True)
    raw_text = models.TextField(blank=True)
    corrected_text = models.TextField(blank=True)
    extraction_method = models.CharField(max_length=80, default="pdfplumber")
    extraction_confidence = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_reviewed = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["document", "page_number"]
        constraints = [
            models.UniqueConstraint(fields=["document", "page_number"], name="unique_page_per_document")
        ]

    @property
    def display_text(self) -> str:
        return self.corrected_text or self.raw_text

    def __str__(self) -> str:
        return f"{self.document.title} p. {self.page_number}"


class TextUnitType(models.TextChoices):
    SECTION = "section", "Section"
    PARAGRAPH = "paragraph", "Paragraph"
    EXCERPT = "excerpt", "Excerpt"
    NOTE = "note", "Note"


class ReviewStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    NEEDS_REVIEW = "needs_review", "Needs review"
    REVIEWED = "reviewed", "Reviewed"
    APPROVED = "approved", "Approved for corpus"


class TextUnit(TimestampedModel):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="text_units")
    page = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="text_units",
    )
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
    )
    unit_type = models.CharField(
        max_length=40,
        choices=TextUnitType.choices,
        default=TextUnitType.PARAGRAPH,
    )
    sequence = models.PositiveIntegerField(default=1)
    heading = models.CharField(max_length=255, blank=True)
    raw_text = models.TextField(blank=True)
    corrected_text = models.TextField(blank=True)
    review_status = models.CharField(
        max_length=40,
        choices=ReviewStatus.choices,
        default=ReviewStatus.NEEDS_REVIEW,
    )
    is_approved_for_search = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["document", "sequence", "id"]
        indexes = [
            models.Index(fields=["document", "sequence"], name="cor_text_doc_seq_idx"),
            models.Index(fields=["is_approved_for_search", "review_status"], name="corpus_text_is_appr_7f1d7a_idx"),
        ]

    @property
    def text(self) -> str:
        return self.corrected_text or self.raw_text

    def __str__(self) -> str:
        label = self.heading or self.text[:60]
        return f"{self.document.title}: {label}"


class Sentence(TimestampedModel):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="sentences")
    page = models.ForeignKey(Page, null=True, blank=True, on_delete=models.SET_NULL, related_name="sentences")
    text_unit = models.ForeignKey(TextUnit, on_delete=models.CASCADE, related_name="sentences")
    sequence = models.PositiveIntegerField()
    text = models.TextField()
    normalized_text = models.TextField(db_index=True)
    start_offset = models.PositiveIntegerField(default=0)
    end_offset = models.PositiveIntegerField(default=0)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["document", "text_unit", "sequence"]
        indexes = [
            models.Index(fields=["document", "sequence"], name="cor_sent_doc_seq_idx"),
            models.Index(fields=["text_unit", "sequence"], name="corpus_sent_text_un_7a6afe_idx"),
        ]

    def __str__(self) -> str:
        return self.text[:100]


class Token(TimestampedModel):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="tokens")
    page = models.ForeignKey(Page, null=True, blank=True, on_delete=models.SET_NULL, related_name="tokens")
    text_unit = models.ForeignKey(TextUnit, on_delete=models.CASCADE, related_name="tokens")
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE, related_name="tokens")
    sequence = models.PositiveIntegerField()
    sentence_token_index = models.PositiveIntegerField()
    original = models.CharField(max_length=255)
    lower = models.CharField(max_length=255, db_index=True)
    normalized = models.CharField(max_length=255, db_index=True)
    normalized_unaccented = models.CharField(max_length=255, db_index=True)
    start_offset = models.PositiveIntegerField(default=0)
    end_offset = models.PositiveIntegerField(default=0)
    is_word = models.BooleanField(default=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["document", "sequence"]
        indexes = [
            models.Index(fields=["normalized"], name="corpus_toke_normali_b24569_idx"),
            models.Index(fields=["normalized_unaccented"], name="corpus_toke_normali_f0cf01_idx"),
            models.Index(fields=["document", "sequence"], name="cor_tok_doc_seq_idx"),
            models.Index(fields=["sentence", "sentence_token_index"], name="corpus_toke_sentenc_b6dc71_idx"),
        ]

    def __str__(self) -> str:
        return self.original


class SourceCitation(TimestampedModel):
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name="citations")
    document = models.ForeignKey(
        Document,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="citations",
    )
    page = models.ForeignKey(Page, null=True, blank=True, on_delete=models.SET_NULL, related_name="citations")
    text_unit = models.ForeignKey(
        TextUnit,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="citations",
    )
    sentence = models.ForeignKey(
        Sentence,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="citations",
    )
    label = models.CharField(max_length=255, blank=True)
    locator = models.CharField(max_length=120, blank=True)
    citation_text = models.TextField()
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["source", "document", "locator", "id"]

    def __str__(self) -> str:
        return self.label or self.citation_text[:100]
