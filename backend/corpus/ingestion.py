from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from django.db import transaction
from django.utils import timezone

from .models import (
    Document,
    ImportIssue,
    ImportJob,
    ImportStatus,
    Page,
    ReviewStatus,
    Sentence,
    Source,
    TextUnit,
    TextUnitType,
    Token,
)
from .tokenization import iter_tokens, normalized_sentence_text, split_sentences


@dataclass(frozen=True)
class ExtractedPage:
    page_number: int
    text: str
    method: str = "pdfplumber"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def extract_pdf_pages(pdf_path: Path, *, page_numbers: Iterable[int] | None = None) -> list[ExtractedPage]:
    try:
        import pdfplumber
    except ImportError as exc:  # pragma: no cover - exercised only in incomplete environments
        raise RuntimeError("pdfplumber is required for PDF extraction") from exc

    allowed = set(page_numbers or [])
    pages: list[ExtractedPage] = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for index, page in enumerate(pdf.pages, start=1):
            if allowed and index not in allowed:
                continue
            text = page.extract_text(x_tolerance=2, y_tolerance=3) or ""
            pages.append(ExtractedPage(page_number=index, text=text.strip(), method="pdfplumber"))
    return pages


@transaction.atomic
def store_pdf_extraction(
    *,
    source: Source,
    pdf_path: Path,
    document_title: str | None = None,
    replace_raw: bool = False,
    page_numbers: Iterable[int] | None = None,
) -> ImportJob:
    file_hash = sha256_file(pdf_path)
    job = ImportJob.objects.create(
        source=source,
        status=ImportStatus.RUNNING,
        input_path=str(pdf_path),
        input_file_name=pdf_path.name,
        input_sha256=file_hash,
        importer="pdfplumber",
        options={"replace_raw": replace_raw, "page_numbers": list(page_numbers or [])},
        started_at=timezone.now(),
    )

    try:
        document, created = Document.objects.get_or_create(
            source=source,
            file_sha256=file_hash,
            defaults={
                "title": document_title or pdf_path.stem,
                "document_type": "pdf",
                "original_file_name": pdf_path.name,
                "import_job": job,
            },
        )
        if not created and document.import_job_id is None:
            document.import_job = job
            document.save(update_fields=["import_job", "updated_at"])

        extracted_pages = extract_pdf_pages(pdf_path, page_numbers=page_numbers)
        for extracted in extracted_pages:
            page, page_created = Page.objects.get_or_create(
                document=document,
                page_number=extracted.page_number,
                defaults={
                    "raw_text": extracted.text,
                    "extraction_method": extracted.method,
                },
            )
            if not page_created:
                has_curated_text = bool(page.corrected_text or page.is_reviewed or page.text_units.exists())
                if has_curated_text and not replace_raw:
                    ImportIssue.objects.create(
                        job=job,
                        severity="warning",
                        page_number=extracted.page_number,
                        code="raw_not_replaced",
                        message="Existing reviewed/corrected page was not overwritten.",
                    )
                    continue
                page.raw_text = extracted.text
                page.extraction_method = extracted.method
                page.save(update_fields=["raw_text", "extraction_method", "updated_at"])

        issue_count = job.issues.count()
        job.status = ImportStatus.COMPLETED_WITH_WARNINGS if issue_count else ImportStatus.COMPLETED
        job.completed_at = timezone.now()
        job.summary = f"Stored {len(extracted_pages)} raw PDF pages."
        job.save(update_fields=["status", "completed_at", "summary", "updated_at"])
        return job
    except Exception as exc:
        job.status = ImportStatus.FAILED
        job.completed_at = timezone.now()
        job.summary = str(exc)
        job.save(update_fields=["status", "completed_at", "summary", "updated_at"])
        raise


@transaction.atomic
def create_text_unit_from_page(
    *,
    page: Page,
    text: str,
    sequence: int,
    heading: str = "",
    approve_for_search: bool = False,
) -> TextUnit:
    return TextUnit.objects.create(
        document=page.document,
        page=page,
        unit_type=TextUnitType.PARAGRAPH,
        sequence=sequence,
        heading=heading,
        raw_text=text,
        review_status=ReviewStatus.APPROVED if approve_for_search else ReviewStatus.NEEDS_REVIEW,
        is_approved_for_search=approve_for_search,
    )


@transaction.atomic
def tokenize_text_unit(text_unit: TextUnit, *, force: bool = False) -> int:
    if text_unit.sentences.exists() and not force:
        return text_unit.tokens.count()

    if force:
        text_unit.sentences.all().delete()

    global_sequence = (
        Token.objects.filter(document=text_unit.document).order_by("-sequence").values_list("sequence", flat=True).first()
        or 0
    )
    created_tokens = 0
    for sentence_index, sentence_span in enumerate(split_sentences(text_unit.text), start=1):
        sentence = Sentence.objects.create(
            document=text_unit.document,
            page=text_unit.page,
            text_unit=text_unit,
            sequence=sentence_index,
            text=sentence_span.text,
            normalized_text=normalized_sentence_text(sentence_span.text),
            start_offset=sentence_span.start,
            end_offset=sentence_span.end,
        )
        for token_index, token_span in enumerate(
            iter_tokens(sentence_span.text, base_offset=sentence_span.start),
            start=1,
        ):
            global_sequence += 1
            Token.objects.create(
                document=text_unit.document,
                page=text_unit.page,
                text_unit=text_unit,
                sentence=sentence,
                sequence=global_sequence,
                sentence_token_index=token_index,
                original=token_span.original,
                lower=token_span.lower,
                normalized=token_span.normalized,
                normalized_unaccented=token_span.normalized_unaccented,
                start_offset=token_span.start,
                end_offset=token_span.end,
            )
            created_tokens += 1
    return created_tokens
