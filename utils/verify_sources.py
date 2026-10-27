"""Offline checks for source integrity and Brain Brew localized output."""

import csv
import hashlib
import html
import json
import re
from pathlib import Path

from locales import CARD_COUNT, FLAG_COUNT, LANGUAGES, MEDIA_COUNT, field_column

ROOT = Path(__file__).resolve().parent.parent


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert all(None not in r and None not in r.values() for r in rows), path
        return rows


def pronunciation_names(value):
    """Split existing multi-capital fields, preserving Washington, D.C."""
    return [
        clean
        for part in re.split(r"<br\s*/?>|,(?!\s*D\.C\.)\s*|;\s*|、", value)
        if (clean := html.unescape(re.sub("<[^>]+>", "", part)).strip())
    ]


def verify_pronunciations(data, *, sources=None, coverage=None, rules=None):
    sources = read_csv(ROOT / "doc/pronunciation-sources.csv") if sources is None else sources
    coverage = read_csv(ROOT / "doc/pronunciation-coverage.csv") if coverage is None else coverage
    rules = read_csv(ROOT / "doc/pronunciation-rules.csv") if rules is None else rules
    rule_index = {r["rule"]: r for r in rules}
    statuses = {
        "dictionary",
        "dictionary-variant",
        "dictionary-stress",
        "component-dictionary",
        "composed-reading",
        "original-language",
        "source-language-reading",
        "kana-spelling",
        "single-syllable",
        "orthographic-rule",
        "ordinary-vocabulary",
    }
    audit = {(r["country"], r["field"], r["language"], r["name"]): r for r in coverage}
    assert len(audit) == len(coverage), "Duplicate pronunciation audit"
    expected = set()
    for field in ("country", "capital"):
        hints = {r["country"]: r for r in read_csv(data / f"{field}_pronunciation.csv")}
        for row in read_csv(data / f"{field}.csv"):
            for language in LANGUAGES:
                key = (row["country"], field, language)
                for name in pronunciation_names(row[field_column(field, language)]):
                    name_key = (*key, name)
                    expected.add(name_key)
                    assert name_key in audit, f"Missing pronunciation audit: {name_key}"
                    record = audit[name_key]
                    assert record["status"] in statuses, f"Unreviewed pronunciation: {name_key}"
                    assert record["reason"] and record["evidence"].startswith("https://"), name_key
                    if not record["hint"]:
                        rule = rule_index.get(record["rule"])
                        assert rule and language in rule["language"].split(), name_key
                        assert record["status"] in {
                            "kana-spelling",
                            "single-syllable",
                            "orthographic-rule",
                            "ordinary-vocabulary",
                        }, name_key
                        if record["status"] != "ordinary-vocabulary":
                            assert record["evidence"] == rule["source"], name_key
                        if record["status"] == "kana-spelling":
                            assert language == "JA" and re.fullmatch(
                                "[ぁ-ゖァ-ヺー・ 　=＝-]+", name
                            ), name_key
                        if record["status"] == "single-syllable":
                            assert (
                                language == "RU"
                                and len(re.findall("[аеёиоуыэюяАЕЁИОУЫЭЮЯ]", name)) == 1
                            ), name_key
                value = hints[row["country"]][field_column(field + " pronunciation", language)]
                for name in pronunciation_names(row[field_column(field, language)]):
                    assert audit[(*key, name)]["hint"] in value, (*key, name)
                cited = [r for r in sources if (r["country"], r["field"], r["language"]) == key]
                assert bool(value) == bool(cited), f"Unattributed pronunciation: {key}"
                for source in cited:
                    assert source["hint"] in value, key
                    assert source["hint"].strip("/[] "), f"Empty transcription: {key}"
                    assert source["source"].startswith("https://") and source["revision"], key
                    assert source["author"] and source["license"], key
                    assert source["reading_language"], key
                    if source["reading_language"].casefold() != language.casefold():
                        assert source["display_label"] and source["display_label"] in value, key
                        assert f"({source['reading_language']})" in source["display_label"], key
                if language == "RU":
                    assert (
                        not value
                        or "\u0301" in value
                        or "ё" in value
                        or any(r["display_label"] for r in cited)
                    ), key
    assert set(audit) == expected, "Stale pronunciation audit names"


def main():
    data = ROOT / "src/data"
    verify_pronunciations(data)
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
    for filename, expected in [("flag_note.csv", FLAG_COUNT), ("map_note.csv", 323)]:
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
            "Country_Pronunciation",
            "Capital_Pronunciation",
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
            "Country_Pronunciation": "country_pronunciation",
            "Capital_Pronunciation": "capital_pronunciation",
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
        assert expected_cards == CARD_COUNT
        for template in model["tmpls"]:
            for side in ("qfmt", "afmt"):
                text = template[side]
                assert not re.search(r"__[A-Z_]+__", text), text
                assert "<details" not in text.lower()
                assert set(re.findall(r"{{[#/^]?([^{}]+)}}", text)) <= set(names)
    print(
        f"Source checks passed: 323 notes, {CARD_COUNT} cards per language; GUIDs, translations, templates and all {MEDIA_COUNT} image attributions valid across 7 languages."
    )


if __name__ == "__main__":
    main()
