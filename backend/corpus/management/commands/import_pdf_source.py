from __future__ import annotations

from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from corpus.ingestion import create_text_unit_from_page, store_pdf_extraction, tokenize_text_unit
from corpus.models import Page, Source


class Command(BaseCommand):
    help = "Extract PDF pages into raw page storage, optionally curating explicit pages for concordance search."

    def add_arguments(self, parser):
        parser.add_argument("pdf_path")
        parser.add_argument("--source-slug", required=True)
        parser.add_argument("--title", required=True)
        parser.add_argument("--author", default="")
        parser.add_argument("--year", type=int)
        parser.add_argument("--citation", default="")
        parser.add_argument("--source-type", default="story")
        parser.add_argument("--document-title", default="")
        parser.add_argument("--replace-raw", action="store_true")
        parser.add_argument(
            "--approve-pages",
            default="",
            help="Comma-separated page numbers to create approved text units from whole page text.",
        )
        parser.add_argument("--tokenize", action="store_true")

    def handle(self, *args, **options):
        pdf_path = Path(options["pdf_path"])
        if not pdf_path.exists():
            raise CommandError(f"PDF not found: {pdf_path}")

        source, _ = Source.objects.get_or_create(
            slug=options["source_slug"],
            defaults={
                "title": options["title"],
                "author": options["author"],
                "year": options["year"],
                "citation": options["citation"],
                "source_type": options["source_type"],
            },
        )
        job = store_pdf_extraction(
            source=source,
            pdf_path=pdf_path,
            document_title=options["document_title"] or options["title"],
            replace_raw=options["replace_raw"],
        )

        approved_pages = [int(item.strip()) for item in options["approve_pages"].split(",") if item.strip()]
        token_count = 0
        for page_number in approved_pages:
            page = Page.objects.get(document__source=source, document__file_sha256=job.input_sha256, page_number=page_number)
            text_unit = create_text_unit_from_page(
                page=page,
                text=page.display_text,
                sequence=page_number,
                heading=f"Page {page_number}",
                approve_for_search=True,
            )
            if options["tokenize"]:
                token_count += tokenize_text_unit(text_unit, force=True)

        self.stdout.write(
            self.style.SUCCESS(
                f"{job.status}: {job.summary} Approved pages: {len(approved_pages)}. Tokens: {token_count}."
            )
        )
