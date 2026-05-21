from __future__ import annotations

from django.test import TestCase

from corpus.ingestion import create_text_unit_from_page, tokenize_text_unit
from corpus.models import Document, Page, Source
from corpus.search import concordance_results


class IngestionSearchTests(TestCase):
    def setUp(self):
        self.source = Source.objects.create(
            slug="sample",
            title="Sample Source",
            author="Test Author",
            year=2026,
            citation="Test Author 2026",
        )
        self.document = Document.objects.create(source=self.source, title="Sample Document")
        self.page = Page.objects.create(
            document=self.document,
            page_number=1,
            raw_text="Ashkan ajwituk ne tal. Náhuat nemi nikan.",
            corrected_text="Ashkan ajwituk ne tal. Nawat nemi nikan.",
        )

    def test_raw_and_corrected_text_are_kept_separate(self):
        text_unit = create_text_unit_from_page(
            page=self.page,
            text=self.page.corrected_text,
            sequence=1,
            approve_for_search=True,
        )
        self.assertIn("Náhuat", self.page.raw_text)
        self.assertIn("Nawat", text_unit.raw_text)

    def test_tokenize_and_search_returns_kwic(self):
        text_unit = create_text_unit_from_page(
            page=self.page,
            text=self.page.corrected_text,
            sequence=1,
            approve_for_search=True,
        )
        tokenize_text_unit(text_unit, force=True)
        results = concordance_results("náwat")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].match, "Nawat")
        self.assertEqual(results[0].right_context, "nemi nikan")
        self.assertIn("p. 1", results[0].citation)
