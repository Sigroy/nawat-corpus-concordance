# Architecture Notes

## Backend

Django is used because this project needs durable relational data, migrations, admin/editor workflows, and strong provenance. Django REST Framework exposes read APIs for the Next.js frontend.

The schema separates:

- source metadata;
- document/file identity;
- raw extracted pages;
- curated text units;
- sentence/token derivations;
- citations and import issues;
- lexicon entries/forms/senses/definitions;
- attestations linking corpus tokens to lexical analysis.

PostgreSQL is the primary database target. Migration `corpus.0002_postgres_search_indexes` installs `unaccent` and `pg_trgm` and adds trigram indexes when the database vendor is PostgreSQL. It no-ops under SQLite for local tests.

## Frontend

The Next.js app presents the usable concordance as the first screen. The KWIC view uses stable columns for left context, match, right context, and source. Result detail fetches the sentence, paragraph, tokens, page, and citation.

## Ingestion Policy

PDF import stores raw pages first. Text only enters concordance search after explicit curation through Django admin or the `--approve-pages` command option.

This avoids contaminating search results with prefaces, permissions, glossaries, exercises, footnotes, and editorial material.

## Lexicon Policy

Legacy SFM/MDF-like data is preserved in `legacy_payload` fields during import. The first relational import is intentionally conservative: entries, forms, senses, and definitions are created, but uncertain morphological analysis is not invented.
