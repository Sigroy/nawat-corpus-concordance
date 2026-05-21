from __future__ import annotations

from django.test import SimpleTestCase

from corpus.tokenization import iter_tokens, split_sentences


class TokenizationTests(SimpleTestCase):
    def test_sentence_split_keeps_offsets(self):
        text = "Ashkan ajwituk ne tal. Inte waktuk."
        sentences = split_sentences(text)
        self.assertEqual([item.text for item in sentences], ["Ashkan ajwituk ne tal.", "Inte waktuk."])
        self.assertEqual(sentences[0].start, 0)
        self.assertEqual(text[sentences[1].start : sentences[1].end], "Inte waktuk.")

    def test_tokens_keep_original_and_normalized_layers(self):
        tokens = iter_tokens("Tiu-tiktait pal náhuat.")
        self.assertEqual([token.original for token in tokens], ["Tiu-tiktait", "pal", "náhuat"])
        self.assertEqual(tokens[0].normalized, "tiu-tiktait")
        self.assertEqual(tokens[2].normalized_unaccented, "nahuat")
