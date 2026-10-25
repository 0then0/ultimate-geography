"""Offline checks for source integrity and Brain Brew localized output."""

import csv
import hashlib
import json
import re
from pathlib import Path

from locales import LANGUAGES, field_column

ROOT = Path(__file__).resolve().parent.parent


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert all(None not in r and None not in r.values() for r in rows), path
        return rows


def main():
    data = ROOT / "src/data"
    main_rows = read_csv(data / "main.csv")
    countries = {r["country"] for r in main_rows}
    assert len(countries) == len(main_rows) == 323
    for path in data.glob("*.csv"):
        rows = read_csv(path)
        keys = [r["country"] for r in rows]
        assert len(keys) == len(set(keys)), f"Duplicate country in {path}"
        assert set(keys) <= countries, path
    guids = read_csv(data / "guid.csv")
    seen = set()
    for language in LANGUAGES:
        values = {r[field_column("guid", language)] for r in guids}
        assert len(values) == 323 and "" not in values and not seen & values, language
        seen.update(values)
    for filename, expected in [("flag_note.csv", 221), ("map_note.csv", 323)]:
        rows = read_csv(data / filename)
        key = filename[:-4].replace("_", " ")
        assert len(rows) == expected
        for language in LANGUAGES:
            assert all(r[field_column(key, language)] for r in rows), (filename, language)
    sources = {r["File"]: r for r in read_csv(ROOT / "sources.csv")}
    attribution = {r["File"]: r for r in read_csv(ROOT / "media-attribution.csv")}
    images = {
        p.name: p
        for p in (ROOT / "src/media").rglob("*")
        if p.is_file() and not p.name.startswith("_")
    }
    assert set(images) == set(sources) == set(attribution), "Image/attribution mismatch"
    for name, path in images.items():
        assert attribution[name]["SHA256"] == hashlib.sha256(path.read_bytes()).hexdigest(), name
        assert attribution[name]["License"] == sources[name]["License"]
        if sources[name]["License"].startswith("CC BY"):
            assert attribution[name]["Author"] and attribution[name]["License URL"], name
    for language in LANGUAGES:
        build = ROOT / "build" / f"Ultimate Geography [{language}]"
        deck = json.loads((build / "deck.json").read_text(encoding="utf-8"))
        model = deck["note_models"][0]
        names = [f["name"] for f in model["flds"]]
        assert names == [
            "Country",
            "Country info",
            "Capital",
            "Capital info",
            "Capital hint",
            "Flag",
            "Flag similarity",
            "Map",
            "Flag_Note",
            "Map_Note",
        ]
        assert len(deck["notes"]) == 323 and len(model["tmpls"]) == 4
        assert [t["name"] for t in model["tmpls"]] == [
            "Country - Capital",
            "Capital - Country",
            "Flag - Country",
            "Map - Country",
        ]
        expected_cards = 0
        guid_column = field_column("guid", language)
        countries_by_guid = {r[guid_column]: r["country"] for r in guids}
        main_by_country = {r["country"]: r for r in main_rows}
        derivatives = {p.stem: {r["country"]: r for r in read_csv(p)} for p in data.glob("*.csv")}
        field_files = {
            "Country info": "country_info",
            "Capital": "capital",
            "Capital info": "capital_info",
            "Capital hint": "capital_hint",
            "Flag similarity": "flag_similarity",
            "Flag_Note": "flag_note",
            "Map_Note": "map_note",
        }
        for note in deck["notes"]:
            fields = dict(zip(names, note["fields"], strict=True))
            country = countries_by_guid[note["guid"]]
            expected_fields = {
                "Country": country,
                "Flag": main_by_country[country]["flag"],
                "Map": main_by_country[country]["map"],
            }
            if language != "EN":
                expected_fields["Country"] = derivatives["country"][country][
                    field_column("country", language)
                ]
            for field, filename in field_files.items():
                column = field_column(filename.replace("_", " "), language)
                expected_fields[field] = derivatives[filename].get(country, {}).get(column, "")
            assert fields == expected_fields, f"Stale or incorrect build: {language}/{country}"
            assert fields["Country"] and fields["Map"] and fields["Map_Note"]
            assert bool(fields["Flag"]) == bool(fields["Flag_Note"])
            expected_cards += (
                2 * bool(fields["Capital"]) + bool(fields["Flag"]) + bool(fields["Map"])
            )
            assert not {"UG::1", "UG::2"} & set(note["tags"])
            if language != "RU":
                assert not re.search("[А-Яа-яЁё]", " ".join(note["fields"])), fields["Country"]
            for name in re.findall(r'<img\b[^>]*src=["\']([^"\']+)', "\n".join(note["fields"])):
                assert name in images and (build / "media" / name).is_file(), name
        assert expected_cards == 982
        for template in model["tmpls"]:
            for side in ("qfmt", "afmt"):
                text = template[side]
                assert not re.search(r"__[A-Z_]+__", text), text
                assert "<details" not in text.lower()
                assert set(re.findall(r"{{[#/^]?([^{}]+)}}", text)) <= set(names)
    print(
        "Source checks passed: 323 notes, 982 cards per language; GUIDs, translations, templates and all 550 image attributions valid across 7 languages."
    )


if __name__ == "__main__":
    main()
