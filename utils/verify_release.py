"""Exercise public APKGs with Anki in disposable collections; render QA HTML."""

import argparse
import csv
import hashlib
import html
import importlib.metadata
import json
import re
import tempfile
from pathlib import Path

from anki.collection import Collection
from anki.import_export_pb2 import ImportAnkiPackageOptions, ImportAnkiPackageRequest
from anki.scheduler_pb2 import CardAnswer
from export_apkg import RELEASE, ROOT, export, media_names

QA = ROOT / "build" / "qa"
PACKAGES = ROOT / "build" / "releases"


def import_package(c, path, scheduling=False):
    result = c.import_anki_package(
        ImportAnkiPackageRequest(
            package_path=str(path.resolve()),
            options=ImportAnkiPackageOptions(
                merge_notetypes=True,
                update_notes=1,
                update_notetypes=1,
                with_scheduling=scheduling,
                with_deck_configs=False,
            ),
        )
    )
    c.models._clear_cache()
    return result


def verify_content(c, language):
    deck = json.loads(
        (ROOT / "build" / f"Ultimate Geography [{language}]" / "deck.json").read_text(
            encoding="utf-8"
        )
    )
    names = [f["name"] for f in deck["note_models"][0]["flds"]]
    actual = {c.get_note(nid).guid: c.get_note(nid) for nid in c.find_notes("")}
    # Anki preserves older media by renaming conflicting imported filenames.
    # Accept a renamed image only if its bytes match the expected source asset.
    source_media = ROOT / "build" / f"Ultimate Geography [{language}]" / "media"
    for note in deck["notes"]:
        n = actual[note["guid"]]
        expected = dict(zip(names, note["fields"]))
        content = dict(n.items())
        assert content.keys() == expected.keys(), (note["guid"], content.keys())
        for field in ("Flag", "Map"):
            before = re.findall(r'src="([^"]+)"', expected[field])
            after = re.findall(r'src="([^"]+)"', content[field])
            assert len(before) == len(after)
            for source, imported in zip(before, after):
                assert (source_media / source).read_bytes() == (
                    Path(c.media.dir()) / imported
                ).read_bytes()
                content[field] = content[field].replace(f'src="{imported}"', f'src="{source}"')
        assert content == expected, (note["guid"], content)
        assert set(n.tags) == set(note["tags"])
    return deck


def snapshot(c):
    # Includes every scheduling column, card identity and review event.
    return {
        "cards": c.db.all(
            "select id,nid,ord,type,queue,due,ivl,factor,reps,lapses,left,odue,odid,flags,data from cards order by id"
        ),
        "revlog": c.db.all("select * from revlog order by id"),
    }


def validate_sources():
    with (ROOT / "sources.csv").open(newline="", encoding="utf-8") as f:
        sources = {r["File"]: r for r in csv.DictReader(f)}
    with (ROOT / "media-attribution.csv").open(newline="", encoding="utf-8") as f:
        attribution = {r["File"]: r for r in csv.DictReader(f)}
    for lang in ("RU", "EN"):
        j = json.loads(
            (ROOT / "build" / f"Ultimate Geography [{lang}]" / "deck.json").read_text(
                encoding="utf-8"
            )
        )
        media = set().union(*(media_names(n["fields"]) for n in j["notes"]))
        assert len(media) == 550
        for name in media:
            assert name in sources and name in attribution, name
            row = attribution[name]
            p = ROOT / "build" / f"Ultimate Geography [{lang}]" / "media" / name
            assert row["SHA256"] == hashlib.sha256(p.read_bytes()).hexdigest(), name
            if sources[name]["License"].startswith("CC BY"):
                assert row["Author"] and row["License URL"], name


def render_cards(c, language):
    target = QA / "html" / language
    target.mkdir(parents=True, exist_ok=True)
    entries = []
    for cid in c.find_cards(""):
        card = c.get_card(cid)
        n = card.note()
        for side, rendered in [("question", card.question()), ("answer", card.answer())]:
            assert "{{" not in rendered and "Template error" not in rendered, (cid, side)
            assert "<details" not in rendered.lower()
            assert rendered.strip()
            # Anki rendering includes the CSS; retain it verbatim.
            path = target / f"{cid}-{side}.html"
            doc = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            doc += f'<base href="{html.escape(Path(c.media.dir()).as_uri())}/"></head><body class="card">{rendered}</body></html>'
            # Copy media to a durable QA directory before closing the collection.
            doc = doc.replace(Path(c.media.dir()).as_uri(), (QA / "media").as_uri())
            path.write_text(doc, encoding="utf-8")
            entries.append(
                {
                    "country": n["Country"],
                    "type": card.ord,
                    "side": side,
                    "path": str(path),
                    "language": language,
                }
            )
    import shutil

    (QA / "media").mkdir(exist_ok=True)
    for f in Path(c.media.dir()).iterdir():
        if f.is_file():
            shutil.copyfile(f, QA / "media" / f.name)
    return entries


def verify(reference=None):
    QA.mkdir(parents=True, exist_ok=True)
    validate_sources()
    entries = []
    results = {"anki_backend": importlib.metadata.version("anki"), "languages": {}}
    for language in ("RU", "EN"):
        package = PACKAGES / f"Ultimate_Geography_{RELEASE}_{language}.apkg"
        with tempfile.TemporaryDirectory(prefix="ug-verify-") as tmp:
            c = Collection(str(Path(tmp) / "collection.anki2"))
            try:
                r = import_package(c, package)
                assert len(r.log.new) == 323 and c.note_count() == 323 and c.card_count() == 982
                assert not c.get_empty_cards().notes
                report = c.media.check()
                assert not report.missing and not report.unused, report
                assert not c.db.scalar("select count(*) from revlog")
                assert not c.db.scalar(
                    "select count(*) from cards where type!=0 or queue!=0 or reps!=0 or lapses!=0 or ivl!=0"
                )
                # No imported custom presets: only Anki's factory default.
                assert len(c.decks.all_config()) == 1
                verify_content(c, language)
                entries.extend(render_cards(c, language))
                before = snapshot(c)
                import_package(c, package)
                assert c.note_count() == 323 and c.card_count() == 982
                assert snapshot(c) == before
                verify_content(c, language)
                # A newly built package has different internal database IDs.
                # It must still update the same notes, fields and cards.
                rebuilt_dir = Path(tmp) / "rebuilt"
                export(language, rebuilt_dir)
                original_manifest = json.loads(
                    package.with_suffix(".json").read_text(encoding="utf-8")
                )
                rebuilt_manifest = json.loads(
                    (rebuilt_dir / package.with_suffix(".json").name).read_text(encoding="utf-8")
                )
                assert original_manifest["content_sha256"] == rebuilt_manifest["content_sha256"]
                edited = c.get_note(c.find_notes("")[0])
                edited["Country info"] += " local edit for update regression test"
                c.update_note(edited)
                c.decks.select(
                    next(
                        d.id
                        for d in c.decks.all_names_and_ids()
                        if d.name == f"Ultimate Geography [{language}]"
                    )
                )
                queued = c.sched.get_queued_cards().cards[0]
                reviewed = c.get_card(queued.card.id)
                reviewed.start_timer()
                c.sched.answer_card(
                    c.sched.build_answer(
                        card=reviewed, states=queued.states, rating=CardAnswer.GOOD
                    )
                )
                studied = snapshot(c)
                import_package(c, rebuilt_dir / package.name)
                assert snapshot(c) == studied
                assert c.note_count() == 323 and c.card_count() == 982
                verify_content(c, language)
                results["languages"][language] = {
                    "notes": 323,
                    "cards": 982,
                    "media": 550,
                    "empty_cards": 0,
                    "missing_media": 0,
                    "review_events": 0,
                    "repeat_import_preserved_cards": True,
                    "independent_rebuild_updates_fields_and_preserves_history": True,
                }
            finally:
                c.close()
    # Both import orders, followed by repeated updates of both languages.
    for order in [("RU", "EN"), ("EN", "RU")]:
        with tempfile.TemporaryDirectory(prefix="ug-bilingual-") as tmp:
            c = Collection(str(Path(tmp) / "collection.anki2"))
            try:
                for lang in order + order:
                    import_package(c, PACKAGES / f"Ultimate_Geography_{RELEASE}_{lang}.apkg")
                assert c.note_count() == 646 and c.card_count() == 1964
                verify_content(c, "RU")
                verify_content(c, "EN")
            finally:
                c.close()
    results["bilingual_both_orders"] = {"notes": 646, "cards": 1964}
    if reference:
        with tempfile.TemporaryDirectory(prefix="ug-migration-") as tmp:
            c = Collection(str(Path(tmp) / "collection.anki2"))
            try:
                import_package(c, reference, scheduling=True)
                assert c.note_count() == 319 and c.card_count() == 978
                # Add a genuine review using Anki's scheduler, even if the input
                # happens to contain no history. Never touch the user's profile.
                c.decks.select(
                    next(d.id for d in c.decks.all_names_and_ids() if "1-Важные" in d.name)
                )
                queued = c.sched.get_queued_cards().cards[0]
                card = c.get_card(queued.card.id)
                card.start_timer()
                answer = c.sched.build_answer(
                    card=card, states=queued.states, rating=CardAnswer.GOOD
                )
                c.sched.answer_card(answer)
                before = snapshot(c)
                assert before["revlog"]
                import_package(c, PACKAGES / f"Ultimate_Geography_{RELEASE}_RU.apkg")
                assert c.note_count() == 323 and c.card_count() == 982
                after = snapshot(c)
                old_ids = {row[0] for row in before["cards"]}
                assert [row for row in after["cards"] if row[0] in old_ids] == before["cards"]
                assert after["revlog"] == before["revlog"]
                verify_content(c, "RU")
                results["reference_upgrade"] = {
                    "existing_cards_preserved": 978,
                    "new_cards": 4,
                    "review_events_preserved": len(before["revlog"]),
                }
            finally:
                c.close()
    (QA / "cards.json").write_text(
        json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (QA / "release-verification.json").write_text(
        json.dumps(results, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--reference", type=Path)
    verify(p.parse_args().reference)
