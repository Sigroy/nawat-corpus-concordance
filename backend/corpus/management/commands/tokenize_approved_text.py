from __future__ import annotations

from django.core.management.base import BaseCommand

from corpus.ingestion import tokenize_text_unit
from corpus.models import TextUnit


class Command(BaseCommand):
    help = "Tokenize approved text units for concordance search."

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true")

    def handle(self, *args, **options):
        total = 0
        for text_unit in TextUnit.objects.filter(is_approved_for_search=True).order_by("document_id", "sequence"):
            total += tokenize_text_unit(text_unit, force=options["force"])
        self.stdout.write(self.style.SUCCESS(f"Tokenization complete. Tokens available: {total}."))
