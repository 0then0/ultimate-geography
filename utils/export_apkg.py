"""Export the existing Brain Brew localized builds using Anki's own backend.

Run with a Python environment containing Anki (see README). No user collection
is ever opened. Numeric model IDs are stable; note identity is the source GUID.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from anki.collection import Collection
from anki.import_export_pb2 import ExportAnkiPackageOptions, ExportLimit
from locales import CARD_COUNT, LANGUAGES, MODEL_IDS, RELEASE, SOURCE_EPOCH

ROOT = Path(__file__).resolve().parent.parent


def media_names(fields):
    return set(re.findall(r'<img\b[^>]*\bsrc=["\']([^"\']+)', "\n".join(fields), re.I))


def export(language, output):
    source = ROOT / "build" / f"Ultimate Geography [{language}]"
    deck = json.loads((source / "deck.json").read_text(encoding="utf-8"))
    model = deck["note_models"][0]
    assert len(model["tmpls"]) == 4, "Only standard decks are public APKG releases"
    referenced = set().union(*(media_names(n["fields"]) for n in deck["notes"]))
    for name in referenced:
        if Path(name).name != name or not (source / "media" / name).is_file():
            raise ValueError(f"Invalid or missing media: {name}")
    output.mkdir(parents=True, exist_ok=True)
    name = f"Ultimate_Geography_{RELEASE}_{language}"
    package = output / (name + ".apkg")
    with tempfile.TemporaryDirectory(prefix="ug-export-") as tmp:
        col = Collection(str(Path(tmp) / "collection.anki2"))
        try:
            nt = col.models.new(f"Ultimate Geography [{language}]")
            nt["css"] = model["css"]
            for field in model["flds"]:
                new = col.models.new_field(field["name"])
                new.update({k: field[k] for k in ("font", "size", "rtl")})
                # Modern Anki matches fields by persistent ID before name.
                # Preserve the two IDs already present in the reference; give
                # other fields stable IDs so successive builds merge cleanly.
                reference_ids = {"Flag_Note": -1449076526530861433, "Map_Note": 3882546672089731509}
                new["id"] = (
                    reference_ids[field["name"]]
                    if language == "RU" and field["name"] in reference_ids
                    else stable_id(language, "field", field["name"])
                )
                col.models.add_field(nt, new)
            for template in model["tmpls"]:
                new = col.models.new_template(template["name"])
                new.update({k: template[k] for k in ("qfmt", "afmt")})
                new["id"] = stable_id(language, "template", template["name"])
                col.models.add_template(nt, new)
            col.models.add_dict(nt)
            # Anki's add API requires id=0. Remap the otherwise empty model in
            # this scratch collection before any notes/cards exist, then reopen
            # to discard backend caches. This preserves the reference RU ID.
            assigned = col.models.by_name(nt["name"])["id"]
            for table, column in (("notetypes", "id"), ("fields", "ntid"), ("templates", "ntid")):
                col.db.execute(
                    f"update {table} set {column}=? where {column}=?", MODEL_IDS[language], assigned
                )
            col.close()
            col = Collection(str(Path(tmp) / "collection.anki2"))
            nt = col.models.get(MODEL_IDS[language])
            did = col.decks.add_normal_deck_with_name(f"Ultimate Geography [{language}]").id
            d = col.decks.get(did)
            d["desc"] = (
                f"Ultimate Geography multilingual fork. 323 notes, {CARD_COUNT} cards. "
                "Sources and licenses accompany this package in the release ZIP."
            )
            col.decks.update_dict(d)
            for note in deck["notes"]:
                n = col.new_note(nt)
                n.guid = note["guid"]
                n.fields = note["fields"]
                n.tags = note["tags"]
                col.add_note(n, did)
            for filename in sorted(referenced):
                shutil.copyfile(source / "media" / filename, Path(col.media.dir()) / filename)
            assert col.note_count() == 323 and col.card_count() == CARD_COUNT
            assert not col.get_empty_cards().notes
            assert col.db.scalar("select count(*) from revlog") == 0
            # Fixed source revision date allows ordinary Anki 'if newer' updates.
            epoch = int(os.environ.get("SOURCE_DATE_EPOCH", str(SOURCE_EPOCH)))
            col.db.execute("update notes set mod=?", epoch)
            col.db.execute("update notetypes set mtime_secs=?", epoch)
            col.export_anki_package(
                out_path=str(package),
                options=ExportAnkiPackageOptions(
                    with_scheduling=False, with_deck_configs=False, with_media=True, legacy=False
                ),
                limit=ExportLimit(deck_id=did),
            )
        finally:
            col.close()
    package_release(package)
    manifest = {
        "language": language,
        "notes": len(deck["notes"]),
        "cards": CARD_COUNT,
        "media": len(referenced),
        "content_sha256": hashlib.sha256(
            json.dumps(
                {"notes": deck["notes"], "model": model}, ensure_ascii=False, sort_keys=True
            ).encode()
        ).hexdigest(),
        "apkg_sha256": hashlib.sha256(package.read_bytes()).hexdigest(),
    }
    (output / (name + ".json")).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest))


def stable_id(language, kind, name):
    return int.from_bytes(
        hashlib.sha256(f"ultimate-geography/{language}/{kind}/{name}".encode()).digest()[:8],
        "big",
        signed=True,
    )


def package_release(package):
    """Refresh release documentation without changing the validated APKG."""
    files = [
        ROOT / "LICENSE.md",
        ROOT / "sources.csv",
        ROOT / "media-attribution.csv",
        ROOT / "README.md",
        ROOT / "README.ru.md",
        ROOT / "CONTRIBUTING.md",
        ROOT / "CHANGELOG.md",
        ROOT / "CODE_OF_CONDUCT.md",
        ROOT / "SECURITY.md",
        ROOT / "doc" / "content-sources.csv",
        ROOT / "doc" / "flag-corrections.csv",
        ROOT / "doc" / "icon.svg",
        ROOT / "doc" / "reference-audit.json",
        ROOT / "doc" / "VALIDATION.md",
        ROOT / "doc" / "PRONUNCIATION.md",
        ROOT / "doc" / "pronunciation-sources.csv",
        ROOT / "doc" / "pronunciation-coverage.csv",
        ROOT / "doc" / "pronunciation-rules.csv",
    ]
    with ZipFile(package.with_suffix(".zip"), "w", ZIP_DEFLATED) as z:
        z.write(package, package.name)
        for file in files:
            z.write(file, file.relative_to(ROOT).as_posix())
        for file in sorted((ROOT / "src" / "data").glob("*.csv")):
            z.write(file, file.relative_to(ROOT).as_posix())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--language", choices=LANGUAGES, action="append")
    parser.add_argument("--output", type=Path, default=ROOT / "build" / "releases")
    args = parser.parse_args()
    for language in args.language or LANGUAGES:
        export(language, args.output.resolve())


if __name__ == "__main__":
    main()
