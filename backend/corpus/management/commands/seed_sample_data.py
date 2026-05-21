from __future__ import annotations

from django.core.management.base import BaseCommand

from corpus.ingestion import create_text_unit_from_page, tokenize_text_unit
from corpus.models import Document, Page, Source


class Command(BaseCommand):
    help = "Create a tiny approved sample corpus for local UI testing."

    def handle(self, *args, **options):
        source, _ = Source.objects.get_or_create(
            slug="king-schultze-2012-sample",
            defaults={
                "title": "Tajtaketza Pal Ijtzalku",
                "short_title": "Tajtaketza Pal Ijtzalku",
                "author": "Alan R. King / Leonhard Schultze Jena",
                "year": 2012,
                "source_type": "story",
                "genre": "oral narrative",
                "language_codes": "Nawat, Spanish",
                "citation": "King, Alan R. 2012. Tajtaketza Pal Ijtzalku.",
                "rights_notes": "Sample seed includes a tiny excerpt for local development only.",
            },
        )
        document, _ = Document.objects.get_or_create(
            source=source,
            title="Sample curated excerpt",
            defaults={"document_type": "manual_seed"},
        )
        page, _ = Page.objects.get_or_create(
            document=document,
            page_number=17,
            defaults={"raw_text": "Ashkan ajwituk ne tal. Nawat nemi nikan."},
        )
        if not document.text_units.exists():
            text_unit = create_text_unit_from_page(
                page=page,
                text=page.raw_text,
                sequence=1,
                heading="Sample excerpt",
                approve_for_search=True,
            )
            tokens = tokenize_text_unit(text_unit, force=True)
        else:
            tokens = document.tokens.count()
        self.stdout.write(self.style.SUCCESS(f"Sample data ready. Tokens: {tokens}."))
