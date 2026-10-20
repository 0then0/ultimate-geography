"""Read-only comparison of the supplied APKG with the editable RU build.

All imports and extraction use Anki in a disposable directory. The package is
never unzipped into the checkout, and its templates are never executed here.
"""

import argparse
import hashlib
import json
import tempfile
from pathlib import Path

from anki.collection import Collection
from anki.import_export_pb2 import ImportAnkiPackageOptions, ImportAnkiPackageRequest

ROOT = Path(__file__).resolve().parent.parent


def audit(package):
    expected = json.loads((ROOT / "doc/reference-audit.json").read_text(encoding="utf-8"))
    assert hashlib.sha256(package.read_bytes()).hexdigest() == expected["reference_sha256"], (
        "Different reference APKG"
    )
    deck = json.loads(
        (ROOT / "build/Ultimate Geography [RU]/deck.json").read_text(encoding="utf-8")
    )
    fields = [f["name"] for f in deck["note_models"][0]["flds"]]
    source = {n["guid"]: dict(zip(fields, n["fields"])) for n in deck["notes"]}
    allowed = {(d["country"], d["field"]): d for d in expected["intentional_field_differences"]}
    import csv

    with (ROOT / "src/data/guid.csv").open(newline="", encoding="utf-8") as f:
        names = {r["guid:ru"]: r["country"] for r in csv.DictReader(f)}
    differences = []
    with tempfile.TemporaryDirectory(prefix="ug-reference-") as tmp:
        c = Collection(str(Path(tmp) / "collection.anki2"))
        try:
            c.import_anki_package(
                ImportAnkiPackageRequest(
                    package_path=str(package.resolve()),
                    options=ImportAnkiPackageOptions(with_scheduling=True, with_deck_configs=True),
                )
            )
            assert c.note_count() == 319 and c.card_count() == 978
            imported = set()
            for nid in c.find_notes(""):
                note = c.get_note(nid)
                imported.add(note.guid)
                assert note.guid in source, f"Missing reference GUID: {note.guid}"
                for field, value in note.items():
                    actual = source[note.guid][field]
                    if value != actual:
                        entry = allowed[(names[note.guid], field)]
                        assert entry["reference"] == value and entry["source"] == actual, entry
                        differences.append((names[note.guid], field))
            assert len(differences) == len(allowed)
            assert {names[g] for g in source.keys() - imported} == set(
                expected["upstream_only_notes"]
            )
            assert not c.media.check().missing
        finally:
            c.close()
    print(
        f"Reference: all 319 GUIDs and 10 fields checked; {len(differences)} documented differences; four upstream-only notes retained."
    )


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("package", type=Path)
    audit(p.parse_args().package)
