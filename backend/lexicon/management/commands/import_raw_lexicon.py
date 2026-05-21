from __future__ import annotations

import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.text import slugify

from corpus.models import Source
from corpus.normalizers import normalize_token
from lexicon.models import Definition, Entry, Form, FormKind, Sense


FIELD_TO_LANGUAGE = {
    "gn": "es",
    "dn": "es",
    "rn": "es",
    "ge": "en",
    "de": "en",
    "re": "en",
    "gd": "de",
}

FORM_FIELDS = {
    "lx": FormKind.HEADWORD,
    "lz": FormKind.SOURCE_SPELLING,
    "va": FormKind.VARIANT,
    "if": FormKind.INFLECTED,
    "pl": FormKind.INFLECTED,
    "sg": FormKind.INFLECTED,
    "po": FormKind.INFLECTED,
    "se": FormKind.DERIVED,
}


class Command(BaseCommand):
    help = "Import the legacy raw_lexicon.json while preserving original marker payloads."

    def add_arguments(self, parser):
        parser.add_argument("json_path")
        parser.add_argument("--limit", type=int)

    @transaction.atomic
    def handle(self, *args, **options):
        json_path = Path(options["json_path"])
        if not json_path.exists():
            raise CommandError(f"JSON not found: {json_path}")

        payload = json.loads(json_path.read_text(encoding="utf-8"))
        sources_by_legacy_id: dict[str, Source] = {}
        for raw_source in payload.get("sources", []):
            legacy_id = raw_source.get("id", "")
            slug = slugify(legacy_id or raw_source.get("name", ""))[:150]
            source, _ = Source.objects.get_or_create(
                slug=slug,
                defaults={
                    "title": raw_source.get("name", legacy_id),
                    "short_title": raw_source.get("name", ""),
                    "citation": raw_source.get("bibliography", ""),
                    "publication_info": raw_source.get("bibliography", ""),
                    "source_type": "dictionary",
                    "legacy_source_id": legacy_id,
                    "metadata": raw_source,
                },
            )
            sources_by_legacy_id[legacy_id] = source

        imported = 0
        for lexicon in payload.get("lexicons", []):
            source = sources_by_legacy_id.get(lexicon.get("source_id", ""))
            for record in lexicon.get("records", []):
                if options["limit"] and imported >= options["limit"]:
                    break
                headword = record.get("headword") or (record.get("fields", {}).get("lx") or [""])[0]
                if not headword:
                    continue
                entry, _ = Entry.objects.get_or_create(
                    normalized_headword=normalize_token(headword, strip_accents=True),
                    defaults={
                        "headword": headword,
                        "part_of_speech": first_field(record, "ps"),
                        "legacy_payload": record,
                    },
                )
                if not entry.legacy_payload:
                    entry.legacy_payload = record
                    entry.save(update_fields=["legacy_payload", "updated_at"])

                import_forms(entry, source, record)
                import_senses(entry, source, record)
                imported += 1
            if options["limit"] and imported >= options["limit"]:
                break

        self.stdout.write(self.style.SUCCESS(f"Imported/merged {imported} legacy lexicon records."))


def first_field(record: dict, marker: str) -> str:
    values = record.get("fields", {}).get(marker) or []
    return values[0] if values else ""


def import_forms(entry: Entry, source: Source | None, record: dict) -> None:
    fields = record.get("fields", {})
    for marker, kind in FORM_FIELDS.items():
        for value in fields.get(marker, []):
            if not value:
                continue
            Form.objects.get_or_create(
                entry=entry,
                source=source,
                form=value,
                normalized_form=normalize_token(value, strip_accents=True),
                kind=kind,
                legacy_marker=marker,
                defaults={"legacy_payload": {"record_index": record.get("record_index"), "marker": marker}},
            )


def import_senses(entry: Entry, source: Source | None, record: dict) -> None:
    fields = record.get("fields", {})
    sense_numbers = fields.get("sn") or [""]
    sense = None
    for index, sense_number in enumerate(sense_numbers, start=1):
        sense, _ = Sense.objects.get_or_create(
            entry=entry,
            sense_number=sense_number or (str(index) if len(sense_numbers) > 1 else ""),
            defaults={
                "part_of_speech": first_field(record, "ps"),
                "legacy_payload": {"record_index": record.get("record_index"), "sense_number": sense_number},
            },
        )

    if sense is None:
        sense, _ = Sense.objects.get_or_create(entry=entry, sense_number="", defaults={"part_of_speech": first_field(record, "ps")})

    for marker, language in FIELD_TO_LANGUAGE.items():
        for text in fields.get(marker, []):
            if text:
                Definition.objects.get_or_create(
                    sense=sense,
                    source=source,
                    language=language,
                    text=text,
                    legacy_marker=marker,
                    defaults={"is_source_specific": source is not None},
                )
