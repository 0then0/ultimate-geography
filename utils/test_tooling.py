"""Regression checks for release tooling; build and export RU/EN before running."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent.parent


class ToolingTests(unittest.TestCase):
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
            self.assertEqual(report["bilingual_both_orders"], {"notes": 646, "cards": 1964})
            for language in ["RU", "EN"]:
                self.assertTrue(
                    report["languages"][language][
                        "independent_rebuild_updates_fields_and_preserves_history"
                    ]
                )
            cards = json.loads((qa / "cards.json").read_text(encoding="utf-8"))
            self.assertEqual(len(cards), 3928)
            self.assertTrue(any(c["country"] == "Соединённые Штаты Америки" for c in cards))


if __name__ == "__main__":
    unittest.main()
