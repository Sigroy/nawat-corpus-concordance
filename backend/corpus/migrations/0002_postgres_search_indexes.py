from __future__ import annotations

from django.db import migrations


def install_postgres_search(apps, schema_editor) -> None:  # noqa: ANN001
    if schema_editor.connection.vendor != "postgresql":
        return

    statements = [
        "CREATE EXTENSION IF NOT EXISTS unaccent",
        "CREATE EXTENSION IF NOT EXISTS pg_trgm",
        (
            "CREATE INDEX IF NOT EXISTS corpus_token_original_trgm_idx "
            "ON corpus_token USING gin (original gin_trgm_ops)"
        ),
        (
            "CREATE INDEX IF NOT EXISTS corpus_token_normalized_trgm_idx "
            "ON corpus_token USING gin (normalized gin_trgm_ops)"
        ),
        (
            "CREATE INDEX IF NOT EXISTS corpus_token_unaccented_trgm_idx "
            "ON corpus_token USING gin (normalized_unaccented gin_trgm_ops)"
        ),
        (
            "CREATE INDEX IF NOT EXISTS corpus_sentence_normalized_trgm_idx "
            "ON corpus_sentence USING gin (normalized_text gin_trgm_ops)"
        ),
    ]
    with schema_editor.connection.cursor() as cursor:
        for statement in statements:
            cursor.execute(statement)


def uninstall_postgres_search(apps, schema_editor) -> None:  # noqa: ANN001
    if schema_editor.connection.vendor != "postgresql":
        return

    statements = [
        "DROP INDEX IF EXISTS corpus_sentence_normalized_trgm_idx",
        "DROP INDEX IF EXISTS corpus_token_unaccented_trgm_idx",
        "DROP INDEX IF EXISTS corpus_token_normalized_trgm_idx",
        "DROP INDEX IF EXISTS corpus_token_original_trgm_idx",
    ]
    with schema_editor.connection.cursor() as cursor:
        for statement in statements:
            cursor.execute(statement)


class Migration(migrations.Migration):
    dependencies = [
        ("corpus", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(install_postgres_search, uninstall_postgres_search),
    ]
