from __future__ import annotations

from django.test import SimpleTestCase

from corpus.normalizers import normalize_text, normalize_token, query_normalizations, strip_diacritics


class NormalizationTests(SimpleTestCase):
    def test_preserves_search_relevant_punctuation_inside_tokens(self):
        self.assertEqual(normalize_token("Tiu-tiktait"), "tiu-tiktait")
        self.assertEqual(normalize_token("ka…"), "ka")

    def test_handles_case_apostrophes_and_accents(self):
        self.assertEqual(normalize_token("KÁ"), "ká")
        self.assertEqual(strip_diacritics("náhuat"), "nahuat")
        self.assertEqual(normalize_token("yaja’"), "yaja")
        self.assertEqual(normalize_token("muʼajkawki"), "mu'ajkawki")

    def test_query_normalizations_include_unaccented_form(self):
        payload = query_normalizations("Náhuat")
        self.assertEqual(payload["normalized"], "náhuat")
        self.assertEqual(payload["normalized_unaccented"], "nahuat")

    def test_text_normalization_compacts_whitespace(self):
        self.assertEqual(normalize_text("  Ashkan\n\tajwituk  "), "ashkan ajwituk")
