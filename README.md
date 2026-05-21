# Nawat Corpus Concordance

A modern Nawat / Pipil concordance and lexicographic research application.

The project is designed around one core rule: raw source evidence is preserved, and every derived layer is kept separate. PDF extraction, corrected text, sentence/token segmentation, concordance search, dictionary entries, and future linguistic analyses all keep provenance.

## What Is Implemented

- Django + Django REST Framework backend.
- PostgreSQL-oriented relational schema with migrations and PostgreSQL search indexes for `unaccent` and `pg_trgm`.
- Source, document, page, curated text unit, sentence, token, citation, import job, and import issue models.
- Lexicon-ready models for entries, forms, senses, definitions, examples, and attestations.
- PDF extraction pipeline that stores raw page text without auto-polluting the searchable corpus.
- Token normalization and tokenization utilities with tests.
- KWIC concordance API:
  - `GET /api/sources`
  - `GET /api/sources/{id}`
  - `GET /api/search/concordance?q=...`
  - `GET /api/concordance/{token_id}`
  - `GET /api/dictionary/search?q=...`
  - `GET /api/entries/{id}`
- Next.js frontend with search, KWIC results, result context, source library, source detail, and dictionary shell.

## Repository Layout

```text
backend/       Django project, apps, migrations, ingestion, tests
frontend/      Next.js + Tailwind interface
data/          Local raw/processed data workspace, ignored by Git
docs/          Project notes and architecture docs
scripts/       Developer helper scripts
*.py, *.json   Legacy Nawacolex extraction scripts and lexicon artifacts
```

## Backend Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements-dev.txt
Copy-Item backend\.env.example backend\.env
```

Start PostgreSQL:

```powershell
docker compose up -d postgres
```

Run migrations and seed a tiny sample corpus:

```powershell
cd backend
python manage.py migrate
python manage.py seed_sample_data
python manage.py createsuperuser
python manage.py runserver 8000
```

The Django admin is at `http://localhost:8000/admin/`.

## Frontend Setup

Use Node.js 18.18 or newer. Next.js security fixes require at least that runtime.

```powershell
cd frontend
npm install
npm run dev
```

The app runs at `http://localhost:3000/`.

## Importing A PDF Source

Raw extraction only:

```powershell
cd backend
python manage.py import_pdf_source "D:\Documentos\Idiomas\Náhuat\masin ed ARK.pdf" `
  --source-slug king-schultze-2012 `
  --title "Tajtaketza Pal Ijtzalku" `
  --author "Alan R. King / Leonhard Schultze Jena" `
  --year 2012 `
  --citation "King, Alan R. 2012. Tajtaketza Pal Ijtzalku."
```

Curate explicit pages into the searchable corpus:

```powershell
python manage.py import_pdf_source "D:\Documentos\Idiomas\Náhuat\masin ed ARK.pdf" `
  --source-slug king-schultze-2012 `
  --title "Tajtaketza Pal Ijtzalku" `
  --author "Alan R. King / Leonhard Schultze Jena" `
  --year 2012 `
  --approve-pages 17 `
  --tokenize
```

This explicit `--approve-pages` step is intentional. The PDF contains introductions, permissions, questions, and notes that should not automatically enter the concordance.

## Importing Legacy Lexicon JSON

```powershell
cd backend
python manage.py import_raw_lexicon ..\raw_lexicon.json
```

The importer creates relational entries/forms/senses/definitions while preserving each legacy record payload.

## Tests

For local tests without PostgreSQL:

```powershell
cd backend
$env:DJANGO_SETTINGS_MODULE="nawacorpus.test_settings"
python manage.py test corpus.tests
```

## Design Notes

- Original orthography is never replaced by normalized text.
- `Page.raw_text` stores extraction output.
- `Page.corrected_text` stores manual page-level correction.
- `TextUnit.raw_text` / `TextUnit.corrected_text` represent curated corpus units.
- `Sentence` and `Token` are derived from approved text units.
- Future lemmatization and morphology should be stored as annotations/attestations, not as destructive edits to source text.
