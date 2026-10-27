"""Regression checks for release tooling; build and export all supported languages before running."""

import copy
import csv
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from locales import CARD_COUNT, LANGUAGES

ROOT = Path(__file__).resolve().parent.parent


class ToolingTests(unittest.TestCase):
    def test_territorial_flags_and_corrections(self):
        from verify_sources import read_csv

        main = {r["country"]: r for r in read_csv(ROOT / "src/data/main.csv")}
        notes = {r["country"]: r for r in read_csv(ROOT / "src/data/flag_note.csv")}
        corrections = read_csv(ROOT / "doc/flag-corrections.csv")
        added = [r["country"] for r in corrections if "Flag" in r["fields"].split("|")]
        self.assertEqual(len(added), 14)
        self.assertEqual(sum(bool(r["flag"]) for r in main.values()), 235)
        for country in added:
            self.assertTrue(main[country]["flag"], country)
            for language in LANGUAGES:
                key = "flag note" + ("" if language == "EN" else ":" + language.lower())
                self.assertTrue(notes[country][key], (country, language))
        # A city flag must not become an ambiguous territory-identification card.
        self.assertEqual(main["Northern Ireland"]["flag"], "")
        info = next(
            r
            for r in read_csv(ROOT / "src/data/country_info.csv")
            if r["country"] == "Northern Ireland"
        )
        for language in LANGUAGES:
            key = "country info" + ("" if language == "EN" else ":" + language.lower())
            self.assertIn("<br>", info[key])
        self.assertNotIn("teclas", notes["Vatican City"]["flag note:pt-br"])
        self.assertNotIn("十字キー", notes["Vatican City"]["flag note:ja"])
        self.assertIn("chaves", notes["Vatican City"]["flag note:pt-br"])
        self.assertIn("鍵", notes["Vatican City"]["flag note:ja"])
        self.assertIn("in front of the black", notes["Saint Lucia"]["flag note"])
        for language in LANGUAGES:
            key = "flag note" + ("" if language == "EN" else ":" + language.lower())
            self.assertIn("FLNKS", notes["New Caledonia"][key])

    def test_complete_pronunciation_audit(self):
        from verify_sources import read_csv, verify_pronunciations

        coverage = read_csv(ROOT / "doc/pronunciation-coverage.csv")
        sources = read_csv(ROOT / "doc/pronunciation-sources.csv")
        verify_pronunciations(ROOT / "src/data", coverage=coverage, sources=sources)
        self.assertEqual(len(coverage), 3815)
        for defect in ("missing", "stale", "duplicate", "unreviewed", "fake-exemption"):
            with self.subTest(defect=defect):
                changed = copy.deepcopy(coverage)
                if defect == "missing":
                    changed.pop()
                elif defect == "duplicate":
                    changed.append(changed[0])
                elif defect == "stale":
                    changed[0]["name"] = "Nonexistent place"
                elif defect == "unreviewed":
                    changed[0]["status"] = "unverified"
                else:
                    changed[0].update(hint="", status="orthographic-rule", rule="JA-KANA")
                with self.assertRaises(AssertionError):
                    verify_pronunciations(ROOT / "src/data", coverage=changed, sources=sources)

    def test_foreign_pronunciation_requires_visible_language(self):
        from verify_sources import read_csv, verify_pronunciations

        sources = read_csv(ROOT / "doc/pronunciation-sources.csv")
        foreign = next(r for r in sources if r["display_label"])
        self.assertIn(f"({foreign['reading_language']})", foreign["display_label"])
        for defect in ("label", "hint"):
            changed = copy.deepcopy(sources)
            target = next(r for r in changed if r["display_label"])
            target["display_label" if defect == "label" else "hint"] = (
                "" if defect == "label" else "//"
            )
            with self.subTest(defect=defect), self.assertRaises(AssertionError):
                verify_pronunciations(ROOT / "src/data", sources=changed)

    def test_pronunciation_control_words(self):
        with (ROOT / "src/data/country_pronunciation.csv").open(encoding="utf-8", newline="") as f:
            countries = {r["country"]: r for r in csv.DictReader(f)}
        # Protect against dictionary templates resolving a placeholder page
        # instead of their geographic entry, and against losing combining marks.
        self.assertEqual(countries["Russia"]["country pronunciation:ru"], "Росси́я")
        self.assertEqual(countries["Japan"]["country pronunciation:ja"], "にほん")
        self.assertIn("ɪŋ", countries["England"]["country pronunciation"])
        self.assertIn("ɲ", countries["Spain"]["country pronunciation:es"])
        self.assertNotIn("api", countries["Spain"]["country pronunciation:es"])
        self.assertIn("ɐ", countries["England"]["country pronunciation:pt-br"])
        self.assertNotEqual(countries["England"]["country pronunciation:pt-br"], "/aˈpi/")
        with (ROOT / "src/data/capital_pronunciation.csv").open(encoding="utf-8", newline="") as f:
            capitals = {r["country"]: r for r in csv.DictReader(f)}
        # A local alias is a different word, not an IPA reading of the exonym.
        self.assertIn("Te Whanganui-a-Tara", capitals["New Zealand"]["capital pronunciation:pt-br"])
        self.assertIn("Béal Feirste", capitals["Northern Ireland"]["capital pronunciation:pt-br"])
        self.assertIn("árabe del Golfo", countries["Kuwait"]["country pronunciation:es"])
        self.assertIn("mandinka", capitals["The Gambia"]["capital pronunciation:es"])
        self.assertTrue(countries["Timor Sea"]["country pronunciation"].startswith("Timor: "))
        self.assertIn(" · Timor:", countries["Timor Sea"]["country pronunciation:fr"])

    def test_pronunciations_follow_visible_names(self):
        from anki.collection import Collection
        from export_apkg import RELEASE
        from verify_release import import_package

        for language in LANGUAGES:
            with self.subTest(language=language), tempfile.TemporaryDirectory() as tmp:
                c = Collection(str(Path(tmp) / "collection.anki2"))
                try:
                    import_package(
                        c,
                        ROOT / "build/releases" / f"Ultimate_Geography_{RELEASE}_{language}.apkg",
                    )
                    tested = set()
                    for nid in c.find_notes(""):
                        note = c.get_note(nid)
                        if not note["Country_Pronunciation"] or not note["Capital_Pronunciation"]:
                            continue
                        if not note["Flag"]:
                            continue
                        for card in note.cards():
                            front = card.question()
                            back = card.answer()
                            count = front.count('<div class="ug-pronunciation">')
                            self.assertEqual(count, 1 if card.ord < 2 else 0)
                            self.assertIn(note["Country_Pronunciation"], back)
                            self.assertIn(note["Capital_Pronunciation"], back)
                            tested.add(card.ord)
                        if len(tested) == 4:
                            break
                    self.assertEqual(tested, {0, 1, 2, 3})
                finally:
                    c.close()

    def run_python(self, *args, cwd=ROOT):
        # Exercise UTF-8 files with Python's UTF-8 mode and locale coercion off.
        env = dict(
            os.environ,
            LC_ALL="C",
            LANG="C",
            PYTHONUTF8="0",
            PYTHONCOERCECLOCALE="0",
            PYTHONIOENCODING="utf-8",
        )
        return subprocess.run(
            [sys.executable, "-B", *map(str, args)],
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    def assert_success(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_existing_note_identities_are_preserved(self):
        # These are the five established language identities before adding JA/PT-BR.
        expected = {
            "RU": "add78b038a2baef2a543ade99e835bc04ed160abd251f7e8260fcffd4a6cb08f",
            "EN": "add3b4622985631f0ac68ba2511250de7f268375b551cd00895110d82a0cda42",
            "ES": "3f35b5dc358e53b9c21fc9e544b08ffb37c4cbc22fac157bd5950b7e4bfe0e22",
            "DE": "a418bb57dc4c6b6dd442010272bda6263126c49828fd10ffce4c4ac8a0694327",
            "FR": "2a1c3200e3ae42bbd8c80b4f85ae43a970963f9f27625dc711b97a34c127c0f4",
        }
        with (ROOT / "src/data/guid.csv").open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        for language, digest in expected.items():
            column = "guid" if language == "EN" else "guid:" + language.lower()
            actual = hashlib.sha256(
                json.dumps(
                    {r["country"]: r[column] for r in rows},
                    ensure_ascii=False,
                    sort_keys=True,
                ).encode()
            ).hexdigest()
            self.assertEqual(actual, digest, language)
        portuguese = {r["guid:pt"] for r in rows}
        brazilian = {r["guid:pt-br"] for r in rows}
        self.assertFalse(portuguese & brazilian)

    def test_local_exonyms_and_brazilian_variant_selection(self):
        with (ROOT / "src/data/country.csv").open(encoding="utf-8", newline="") as f:
            countries = {r["country"]: r for r in csv.DictReader(f)}
        with (ROOT / "src/data/capital.csv").open(encoding="utf-8", newline="") as f:
            capitals = {r["country"]: r for r in csv.DictReader(f)}
        for country, expected in {
            "Jordan": "ヨルダン",
            "Java": "ジャワ島",
            "English Channel": "イギリス海峡",
        }.items():
            self.assertEqual(countries[country]["country:ja"], expected)
        self.assertEqual(countries["North Macedonia"]["country:pt-br"], "Macedônia do Norte")
        self.assertEqual(countries["Egypt"]["country:pt-br"], "Egito")
        self.assertEqual(countries["Bangladesh"]["country:pt-br"], "Bangladesh")
        self.assertEqual(capitals["Russia"]["capital:pt-br"], "Moscou")
        self.assertEqual(capitals["Netherlands"]["capital:pt-br"], "Amsterdã")
        for path in (ROOT / "src/data").glob("*.csv"):
            with path.open(encoding="utf-8", newline="") as f:
                for row in csv.DictReader(f):
                    for column, value in row.items():
                        if column.endswith(":pt-br"):
                            self.assertNotIn("(BR)", value, (path.name, row["country"]))
                            self.assertNotIn("(PT)", value, (path.name, row["country"]))
                            for spelling in ["Polónia", "Roménia", "Irão", "Bangladexe"]:
                                self.assertNotIn(spelling, value, (path.name, row["country"]))

    def test_zip_ignores_service_folders_and_preserves_deck_files(self):
        with tempfile.TemporaryDirectory(prefix="ug-zip-test-") as tmp:
            root = Path(tmp)
            header = root / "src/headers/desc.html"
            header.parent.mkdir(parents=True)
            header.write_text("Колода Ultimate Geography v42.1", encoding="utf-8")
            variants = {
                "Ultimate Geography [RU]": "RU",
                "Ultimate Geography [EN] [Extended]": "EN_EXTENDED",
                "Ultimate Geography [EN] [Experimental]": "EN_EXPERIMENTAL",
            }
            payload = "Флаг и карта".encode("utf-8")
            for folder in [*variants, "qa", "releases", "unrelated"]:
                path = root / "build" / folder / "media/flag.svg"
                path.parent.mkdir(parents=True)
                path.write_bytes(payload)
            for _ in range(2):
                result = self.run_python(ROOT / "utils/zip_decks.py", cwd=root)
                self.assert_success(result)
                self.assertEqual(
                    {p.name for p in (root / "build").glob("*.zip")},
                    {f"Ultimate_Geography_v42.1_{suffix}.zip" for suffix in variants.values()},
                )
                for folder, suffix in variants.items():
                    with ZipFile(root / "build" / f"Ultimate_Geography_v42.1_{suffix}.zip") as z:
                        self.assertIsNone(z.testzip())
                        self.assertEqual(z.read(f"{folder}/media/flag.svg"), payload)
            for folder in ["qa", "releases", "unrelated"]:
                self.assertEqual((root / "build" / folder / "media/flag.svg").read_bytes(), payload)

    def test_source_integrity_with_non_utf8_locale(self):
        result = self.run_python(ROOT / "utils/verify_sources.py")
        self.assert_success(result)
        self.assertIn("Source checks passed: 323 notes", result.stdout)

    def test_reference_audit_rejects_wrong_package_with_non_utf8_locale(self):
        with tempfile.TemporaryDirectory(prefix="ug-audit-test-") as tmp:
            package = Path(tmp) / "wrong.apkg"
            package.write_bytes(b"not the supplied reference")
            result = self.run_python(ROOT / "utils/audit_reference.py", package)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Different reference APKG", result.stderr)
            self.assertNotIn("UnicodeDecodeError", result.stderr)

    def test_release_imports_and_utf8_reports_with_non_utf8_locale(self):
        with tempfile.TemporaryDirectory(prefix="ug-release-test-") as tmp:
            qa = Path(tmp) / "qa"
            code = (
                "import sys; from pathlib import Path; "
                "sys.path.insert(0, sys.argv[1]); import verify_release; "
                "verify_release.QA = Path(sys.argv[2]); verify_release.verify()"
            )
            result = self.run_python("-c", code, ROOT / "utils", qa)
            self.assert_success(result)
            report = json.loads((qa / "release-verification.json").read_text(encoding="utf-8"))
            self.assertEqual(
                report["bilingual_both_orders"], {"notes": 646, "cards": (2 * CARD_COUNT)}
            )
            for language in LANGUAGES:
                self.assertTrue(
                    report["languages"][language][
                        "independent_rebuild_updates_fields_and_preserves_history"
                    ]
                )
            self.assertEqual(
                report["multilingual_both_orders"],
                {"notes": 323 * len(LANGUAGES), "cards": CARD_COUNT * len(LANGUAGES)},
            )
            cards = json.loads((qa / "cards.json").read_text(encoding="utf-8"))
            self.assertEqual(len(cards), (2 * CARD_COUNT) * len(LANGUAGES))
            self.assertTrue(any(c["country"] == "Соединённые Штаты Америки" for c in cards))


if __name__ == "__main__":
    unittest.main()
