# Validation record

## 2026-10-27: territorial flags and description corrections

This later local revision supersedes the earlier 982-card/550-media counts below.
All seven public decks now contain **323 notes, 996 cards and 564 media**:
219 country-to-capital, 219 capital-to-country, 235 flag-to-country and
323 map cards. The 14 added flags are Bermuda, British Virgin Islands, Turks and
Caicos Islands, Cayman Islands, Anguilla, Gibraltar, Guernsey, Isle of Man,
Jersey, American Samoa, Northern Mariana Islands, Sint Maarten, Falkland Islands
and Martinique. They reuse the existing notes/GUIDs and add only flag cards.
This is not an expansion into city flags or a claim to cover every regional flag.

Northern Ireland now explains its Union Flag status and distinguishes Belfast's
city flag. The same flag field remains empty to avoid an ambiguous UK duplicate.
Saint Lucia's layering is corrected in all seven languages, Vatican keys in
JA/PT-BR, and the Kanak/FLNKS caption explains its status for New Caledonia.
Decisions, sources and allowed migration field changes are recorded in
`flag-corrections.csv`. Pronunciation content and all note GUIDs are unchanged.

All 14 downloaded original SVGs match Wikimedia imageinfo SHA1 checksums. Source
pages, actual licenses, credited creators/collections and local SHA256 hashes
are recorded in `sources.csv` and `media-attribution.csv`. Jersey's source is the
public-domain Xrmap collection. The Northern Mariana Islands file is from the
CC0 Open Clip Art Library collection; an individual artist is not claimed.
All **241 flag SVG files** (including six masked/full pairs) parse and render,
with no missing files, scripts or external SVG references found in the audit.

Both Brain Brew recipes, source parity, all seven APKG exports and **11 tests**
passed using the same CPython 3.14.8 / Anki backend 26.9.3 environment. Migration
from each actual 2026.10.25 release was tested after a real scheduler review:
all old card rows and review events survive, exactly 14 new unreviewed flag cards
appear with the expected existing note GUIDs, and a second import adds none.
Only registered flag/explanation fields may change in the existing ten fields.
Combined installation in both language orders yields **2,261 notes / 6,972 cards**.
Ruff, Biome and Git whitespace checks pass. Original release ZIPs are retained.

Chrome 156.0.8078.48 / Playwright passed **56 scenarios** at **360, 393, 412
and 1920 CSS px**, light and dark: **111,552 card-side evaluations** and
**448 screenshots**, with no overflow, missing/distorted images, hidden notes or
excess map-panel width. An additional **84 focused screenshots** at 393 px cover
the corrected descriptions, Northern Ireland and the new Northern Mariana Islands
flag question/answer in every language and both themes. All 235 full flags were
also visually inspected in two contact sheets.
Reports: `build/qa/flag-validation.json`, `flag-release-verification.json`,
`layout-verification.json`, `flag-corrections-visual.json`,
`flag-fixed-audit.json` and `flag-change-boundaries.json`. The focused answers
were visually inspected in all seven languages and both themes. Native Anki GUI, AnkiDroid, AnkiMobile and
physical devices were not run. These are browser checks and native backend tests.

## 2026-10-27: pronunciation fields and bounded map panels

Source/build version: **2026.10.27**, locally generated and not published.
The seven original `build/Ultimate_Geography_2026.10.25_<LANG>.zip` files were
verified against their APKG manifests before work. They remain unchanged.

Both Brain Brew recipes, source validation and all seven native APKG exports
passed on **CPython 3.14.8**, with Anki backend **26.9.3** and Node.js **24.22.1**.
Ten regression tests passed, including UTF-8 checks, control-word
pronunciations and hint visibility for all four card types in every language.
Ruff lint/format, Biome format/check, lockfile and Git whitespace checks passed.
The earlier Python matrix below is historical; the new tests were run locally
on 3.14.8, not on all six interpreters. No dependencies were added or updated.

### Content and update integrity

`Country_Pronunciation` and `Capital_Pronunciation` are appended after the ten
existing fields. All seven retain **323 notes, 982 cards and 550 media**.
No missing/unused media, empty cards, template errors, personal scheduling,
review history or custom study presets were found in clean public imports.
Repeated imports, independent rebuilds and coexistence of all seven languages
passed; the combined collection contains **2,261 notes and 6,874 cards**.

Each actual 2026.10.25 package was imported into a disposable collection, a card
was reviewed using Anki's scheduler, and the new package was imported twice.
All existing ten field values, GUIDs, card IDs, scheduling columns and review
events were preserved; new fields matched the editable CSVs. No duplicate or
renamed pronunciation fields were created. No real user profile was opened.
Reports: `build/qa/pronunciation-validation.json` and `release-verification.json`.

There are **3,262 nonempty pronunciation fields**: RU 538, EN 537, ES 499,
DE 541, FR 530, JA 122 and PT-BR 495. The audit covers **3,815 individual names**,
with **3,279 readings** and **536 documented exemptions**. All 534 previously
unresolved rows now have sourced decisions; none remains `unverified`. See
`PRONUNCIATION.md` for the distinction between target-language pronunciation,
local aliases, explicitly labelled foreign variants and orthographic exemptions.
No native-language editorial certification is claimed. The new regression tests
reject missing/stale/duplicate names, unresolved statuses, fake exemptions,
empty IPA and foreign hints without visible language labels.

### Rendering

Installed **Chrome 156.0.8078.48**, driven headlessly by Playwright, passed
**56 scenarios** at **360, 393, 412 and 1920 CSS px**, light and dark themes:
**109,984 card-side layout evaluations** and **448 screenshots**. No horizontal
overflow, broken/distorted images, hidden notes, oversized map panels or incorrect
mobile stacking were found. A separate focused run generated **126 screenshots**,
covering all four questions/answers with pronunciation examples at 393 px and
England's answer at 1920 px, for every language and both themes. After the
last source-language label and Timor-component clarifications, a focused follow-up
checked **38 affected card sides in 304 viewport/theme combinations**. No
overflow or clipped pronunciation text was found. This includes named Gulf
Arabic/Mandinka labels and the Māori/Irish local aliases. Report:
`build/qa/completion-label-verification.json`; screenshots: `completion-labels/`.

The strengthened desktop regression was also evaluated against every rendered
card side in all seven languages and both themes: **14 scenarios, 27,496
card-side evaluations**, with no excess empty width inside map panels. Its
report is `build/qa/map-panel-verification.json`.

The focused questions/answers were visually inspected in all seven languages,
including long names, Russian combining accents, IPA and Japanese glyphs.
England's desktop answer was inspected in EN/light and JA/dark. Across all seven
languages and both themes its map panel is **534 px**, image **500 px**, and
unused content width **0 px**, excluding the intentional padding and border.
The grid no longer assigns an unbounded `1fr` track to a 760 px limited image;
map panels follow intrinsic image dimensions. Their source media are unchanged.
Reports/screenshots: `build/qa/layout-verification.json`,
`pronunciation-visual-verification.json`, `pronunciation-screenshots/` and
`pronunciation-contact/`. Native Anki GUI, AnkiDroid, AnkiMobile and physical
phones were not run. These are browser viewport checks, not device/client tests.

## 2026-10-25: seven localized variants

Current source/build version: **2026.10.25**. Standard variants RU,
EN, ES, DE, FR, JA and PT-BR use the shared templates and explanation fields.
The following earlier sections retain the historical 2026-10-20 RU/EN results.

### Source and identity checks

All pre-existing GUID columns for all 323 notes were compared with commit
`b07fcd2` and remained unchanged. EN/RU field values are unchanged. DE/ES/FR
retain their existing note-model UUIDs and note GUIDs. JA and PT-BR have separate
GUID columns, model IDs and deck UUIDs; PT-BR is distinct from legacy PT.
The new regression test locks the five established language identity mappings.

All seven source outputs passed complete CSV-to-field comparison, template-field
validation, media SHA-256 and attribution checks. Each language contains
**323 notes, 982 cards and 550 media**, with 221 flag notes and 323 map notes.
No missing translations in required fields, empty cards or missing/unused media
were found. Primary-source HTML links are retained in the translated fields.

Both normal/extended and experimental Brain Brew recipes passed. APKG export,
repeat import, independent rebuild updates and review-history preservation
passed in disposable collections for every language. Installing all seven
languages in forward and reverse order, then updating all of them, produced
**2,261 notes and 6,874 cards** without overwriting other languages.

Six regression tests passed on **CPython 3.10.22, 3.11.17, 3.12.15, 3.13.16,
3.14.8 and 3.15.0** (36 successful test executions), including non-UTF-8 locale
checks and Japanese/Brazilian exonym tests. Final PT-BR wording changes were
rebuilt and the complete six-test suite and seven-language imports passed again
on default Python 3.14.8. Original ZIP packaging also passed after export/QA.

### Display checks

Playwright 1.62.1 drove the installed **Google Chrome 156.0.8078.48**, headlessly,
using `UG_CHROMIUM_PATH=/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`.
No browser or project dependency was added. Node.js was 24.22.1; Anki backend was
26.9.3. The existing shared Node package directory was supplied through `NODE_PATH`.

The full seven-language run covered **56 scenarios**, all question/answer sides
at **360, 393, 412 and 1920 CSS px**, in both themes: **109,984 card-side layout
evaluations** and **448 screenshots**. All checks passed: no horizontal overflow,
failed or distorted images, hidden notes, or incorrect mobile stacking. PT-BR
was checked separately again after selecting Brazilian names and editing its
wording, covering all eight width/theme combinations and replacing its 64
screenshots. Japanese uses explicit `lang="ja"`, native CJK font fallbacks and
strict line breaking; PT-BR uses `lang="pt-BR"`.

Questions and answers of all four types were visually inspected for each new
language at 393 px in both themes, using long country names. Wide answer/map
layouts for the five new languages were also inspected at 1920 px in both themes.
Contact sheets and raw screenshots are under `build/qa/contact-sheets` and
`build/qa/screenshots`. The final PT-BR rerun has a separate
`build/qa/layout-verification-ptbr-final.json` report.

### Tooling, documentation and limitations

Biome formatting/checks, Ruff lint/format checks, `uv lock --check`, Git whitespace
checks and parsing of the workflow/issue-form YAML passed. `.gitattributes` keeps
source text at LF but disables text conversion for hash-bound `src/media` assets.
The issue forms, PR template, conduct/security policies and changelog were
validated locally before committing, pushing and preparing the 2026.10.25 release.
No remote repository settings were changed. The published 2026.10.20 artifacts
remain unchanged.

New explanation translations were machine-assisted and then corrected for
terminology, exonyms and Brazilian spelling. They have not been independently
copy-edited by native-language reviewers. Builds use committed CSV values and
never call a translation service.

The original reference `/Users/user/Desktop/Страны, Столицы, Флаги.apkg` is no
longer present. Its optional migration/audit could not be repeated: an initial
`--reference` attempt failed with a file-not-found error. Public package tests
were rerun successfully without it. Historical reference checks below remain
separate from the current checks. Interactive Anki/AnkiDroid/AnkiMobile clients,
physical devices, remote CI, and updates from old upstream DE/ES/FR APKGs were
not exercised. Log files and test reports are kept in ignored `build/qa/`.

RU/EN fork, checked locally on 2026-10-20. GitHub Actions itself was not run
remotely. The checks below use disposable resources.

## Review fixes and default Python 3.14

The two confirmed review findings were fixed: the upstream ZIP utility now skips
service directories such as `build/qa` and `build/releases`, and project JSON/CSV
reads and generated text reports explicitly use UTF-8. `.python-version` now
selects Python 3.14; a fresh `uv sync --locked --group export` selected CPython
3.14.8. The supported Python range and dependency lockfile remain unchanged.

Four regression tests in `utils/test_tooling.py` failed before the fixes and
passed afterwards on CPython 3.10.22, 3.11.17, 3.12.15, 3.13.16, 3.14.8 and
3.15.0 (24 successful test executions). They cover:

- Standard, extended and experimental ZIPs, unrelated service folders, repeated
  packaging and preservation of archived bytes.
- Source integrity under `LC_ALL=C`, `PYTHONCOERCECLOCALE=0`, `PYTHONUTF8=0`.
- Rejection of a wrong reference APKG for the intended hash-check reason under
  that same locale, rather than failure while decoding the audit JSON.
- Complete public import/reimport/rebuild/bilingual/history tests under that
  locale, plus valid UTF-8 QA JSON containing Russian country names. QA output
  is written to a temporary directory.

Reproduce after building and exporting the decks:

```sh
uv run --locked --group export python -m unittest discover -s utils -p 'test_*.py' -v
```

CI runs these tests after both build recipes and APKG export on every Python
version in its matrix. No test dependency or private reference is required.

Both build recipes, source integrity, APKG export and the real upstream ZIP
command also passed on default Python 3.14. Reference migration and the full
reference audit additionally passed with UTF-8 mode and locale coercion disabled,
using the supplied APKG only in disposable collections. Ruff, Biome,
`uv lock --check` and `git diff --check` passed. Logs and command exit codes are
in ignored `build/qa/review-fixes.log` and `review-fixes.json`.

The earlier review's Chromium checks remain applicable: these fixes do not change
card content, templates or CSS. Remote CI, real Anki client interfaces, and
migration from an old upstream EN APKG remain outside this local validation.

## Python 3.10–3.15 compatibility

After the initial uv migration, the full local check sequence was repeated on
standard GIL-enabled CPython **3.10.22, 3.11.17, 3.12.15, 3.13.16, 3.14.8 and
3.15.0**, using macOS arm64. All six versions passed. The supported range in
`pyproject.toml` is now `>=3.10,<3.16`; the initial default was Python 3.11 and is now Python 3.14.
Ruff targets Python 3.10 syntax. The flag helper's Python-3.11-only `typing.Self`
annotations were replaced with forward references to the existing classes.

The original ruamel.yaml.clib 0.2.12 failed to build on Python 3.15 because its
setup code imports the removed `ast.Str`. PyYAML was updated from 6.0.2 to 6.0.3
and ruamel.yaml.clib from 0.2.12 to 0.2.15. The rest of the existing dependencies
remain unchanged, except the universal lockfile selects Markdown 3.10.3 for Python
3.10 and keeps 3.11.2 for Python 3.11–3.15. Brain Brew remains 0.3.11 and Anki
backend remains 26.9.3. On macOS arm64, PyYAML and ruamel.yaml.clib built from
source on 3.15 using the available C toolchain; installation is not wheel-only.

Each interpreter had a separate disposable environment selected with
`UV_PROJECT_ENVIRONMENT=/private/tmp/ug-python-<version>` and
`uv run --locked --python <version> --group export`. Each ran:

- Ruff lint and formatting checks and byte compilation of all Python utilities.
- The flag helper with `--no-colour '#a00' '#f00'`; all returned the expected
  colour difference of 32.96.
- Both regular/extended and experimental Brain Brew build recipes.
- Full offline source/media integrity validation.
- RU/EN export, public import/update checks and reference migration/history checks.
- The complete ten-field reference audit, including all 39 documented differences.

Every interpreter produced the same RU/EN semantic hashes, also matching the
previous validated releases. Each language still contains 323 notes, 982 cards
and 550 media; both import orders, repeat imports, independent rebuild updates
and preservation of the reference's 978 existing cards and review event passed.
Raw per-version logs and results are in `build/qa/python-*.log` and
`build/qa/python-compatibility.json`. Biome, `uv lock --check` and
`git diff --check` also passed after the compatibility changes.

CI now has six mandatory Python jobs, with `fail-fast: false`, running the same
public builds/import checks on `ubuntu-latest`. The workflow YAML and matrix
selection were checked locally, but remote CI, Linux, Windows, PyPy and
free-threaded builds were not executed. No browser rerun was needed for this
change: templates, CSS and semantic deck content are unchanged from the reviewed
browser builds described below.

## Initial uv migration checks

The initial migration used uv 0.13.3, Python 3.11.17, Ruff 0.17.1, Biome 2.5.15,
Node.js 24.22.0 and npm 11.19.1. `uv.lock` preserves the five previous Brain Brew
dependency versions: brain-brew 0.3.11, PyYAML 6.0.2, ruamel.yaml 0.18.10,
ruamel.yaml.clib 0.2.12 and yamale 6.0.0. The optional `export` group installs
Anki backend 26.9.3 from PyPI in the same Python 3.11 environment.

All these commands completed successfully after the tooling migration:

```sh
uv lock --check
uv sync --locked --group export
npm ci --ignore-scripts
uv run --locked ruff check .
uv run --locked ruff format --check .
npm run check
uv run --locked python utils/generate_and_build.py recipes/source_to_anki.yaml
uv run --locked python utils/generate_and_build.py 'recipes/source_to_anki_[experimental].yaml'
uv run --locked python utils/verify_sources.py
uv run --locked --group export python utils/export_apkg.py
uv run --locked --group export python utils/verify_release.py --reference '/path/to/reference.apkg'
uv run --locked --group export python utils/audit_reference.py '/path/to/reference.apkg'
node utils/verify_layout.cjs
```

The actual reference path was `/Users/user/Desktop/Страны, Столицы, Флаги.apkg`.
Local uv/npm caches used disposable directories because the global caches were
not writable; npm installation also disabled audit/funding output. Both normal
and experimental Brain Brew recipes passed. Ruff checks all seven Python utilities.
Biome checks only owned JavaScript, note-model CSS and JSON files. It excludes
Anki HTML templates, generated outputs and data CSVs. CSS-specific exceptions
preserve the intentional Anki cascade and `!important` overrides.

Browser QA uses Playwright 1.62.1 with existing Chromium 156.0.8078.4.
The local environment used
`NODE_PATH=/Users/user/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules`
and
`UG_CHROMIUM_PATH=/Users/user/Library/Caches/ms-playwright/chromium-1248/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing`.
No browser was downloaded. Playwright is not a project dependency.

Before the migration, equivalent builds and integrity checks also passed under
Pipenv 2026.10.1 with Python 3.11.17; export/import checks used the installed macOS
Anki backend 26.9.3 under Python 3.13.16. Those were historical checks. Pipenv's
manifest and lockfile have now been replaced by `pyproject.toml` and `uv.lock`;
current builds and exports no longer require application-bundled Python packages.

## Data, media and identities

The reference contains 319 notes and 978 cards. All 319 Russian GUIDs matched the
source; no name-based identity replacement was needed. All ten fields were
compared. There are exactly 39 documented differences: 32 equivalent image-tag
normalisations, two replacements of personal grading instructions with factual
flag comparisons, one conversion of an accepted short answer to a capital alias,
and four map-note clarifications. See `reference-audit.json` for the full values
and reasons. All 221 flag explanations were retained verbatim in Russian.

The source already included another four map-only notes: Strait of Malacca,
Strait of Hormuz, Strait of Gibraltar and Gulf of Oman. They were retained with
explanations in both languages. Each release therefore has **323 notes, 982 cards**:
219 country–capital, 219 capital–country, 221 flag–country and 323 map–country.
Combined RU/EN: **646 notes and 1,964 cards**. `main.csv` and all GUID columns in
`guid.csv` are unchanged from the starting checkout.

`verify_sources.py` compares every generated RU/EN field against the CSV values,
checks disjoint GUIDs, card counts, field schema, template field references,
complete translations and attribution hashes. It detects an old build left over
from a failed Brain Brew run.

Each APKG imports **550 media files**. There are no missing or unused media in a
clean release import, no empty cards, no unresolved template fields and no template
rendering errors. Every included image has an exact filename match in `sources.csv`
and a SHA-256-bound entry in `media-attribution.csv`. Two missing `.png` suffixes
and three missing ShareAlike license indications in upstream attribution were
corrected against source records. Source pages provide no creator name for eight
public-domain flags; those author cells are left blank, rather than invented.
Their origin and public-domain status are documented by their linked source pages.

All upstream image bytes are retained. The 134 differing package SVGs have no
supplied revision-level provenance and include older variants; none is silently
substituted into the release. Upstream attribution remains attached to the exact
upstream assets. No unresolved-origin package-only image is included.

## Import and update tests

Tests use disposable collections and never open the user's active Anki profile.

- Clean RU and EN imports each produce 323 notes and 982 new cards, zero review
  events, no scheduled/learning/suspended cards and only Anki's factory preset.
  Public export sets `with_scheduling=False` and `with_deck_configs=False`.
- Reimporting each APKG adds no notes/cards and preserves existing card IDs and
  all scheduling columns.
- Independently rebuilding each APKG yields the same semantic content hash.
  After making a local field edit and answering a card with Anki's scheduler,
  importing that rebuild restores source content, preserves the review event and
  every scheduling column, and adds no duplicates. Field and template IDs are
  stable across builds. APKG ZIP bytes need not be identical.
- Installing RU then EN, and EN then RU, followed by reimporting both versions,
  produces 646 notes and 1,964 cards with both languages' complete content intact.
- The supplied corrected reference is imported with its scheduling in a temporary
  collection. A real scheduler answer creates a review record. Updating to the RU
  release preserves all 978 existing card IDs, all their scheduling values and
  that review record; exactly four new map cards are added. All fields are checked
  after import, including the two persistent reference field IDs. No duplicate
  `Flag_Note+` or `Map_Note+` fields are created.
- Anki may rename an incoming image when the old reference has different bytes
  under the same filename. Tests compare the resulting image bytes with the
  expected source image; they do not confuse that safe rename with data loss.

The migration was tested with note-type merging and unconditional note/note-type
updates, scheduling/preset import disabled for the public packages. Existing local
field/template edits may be overwritten as documented in the READMEs. Migration
from arbitrarily renamed fields, altered GUIDs or other unknown note types was
not tested. CrowdAnki's GUI import and alternating CrowdAnki/APKG updates were
not exercised; the upstream CrowdAnki build process remains available.

## Browser verification

All **1,964 question/answer sides per language** were checked at widths **360,
393, 412 and 1920 CSS pixels**, in light and dark themes: 16 complete-content
scenarios, or 31,424 card-side layout evaluations. No horizontal overflow, failed
images, hidden explanatory notes or stretched images were found. The image check
accounts for `object-fit: contain`, including the taller 500×421 maps of the UK
constituent countries. Flag/map grids are vertical on all three narrow widths.
A separate narrow 360px container within each viewport was checked with the
`mobile` and `night_mode` classes.

**128 screenshots** cover both sides of all four card types in both languages,
all widths and both themes, using United States of America as a long-name case.
All 16 contact sheets were visually inspected. After the uv/Ruff/Biome migration,
all 31,424 evaluations and 128 screenshots were regenerated successfully; all
16 contact sheets were byte-identical to the inspected versions. Full-resolution screenshots and
contact sheets remain in `build/qa/screenshots/` and `build/qa/contact-sheets/`.
The original wide, left-aligned appearance is preserved, the extra notes are
visible, images retain their proportions, and standalone map panels are bounded.

This is Chromium browser verification plus Anki backend testing. The interactive
Anki desktop application, AnkiDroid, AnkiMobile, Pixel 8 and other physical devices
were **not** run for these checks.

## Distribution and changed source groups

Release ZIPs contain the validated APKG, original `LICENSE.md`, `sources.csv`,
`media-attribution.csv`, both READMEs, this record, the reference audit, dated content
sources, the icon, CONTRIBUTING and editable data CSVs. The content remains
Unlicense; images retain their individual licenses. Generated builds are ignored
by Git. No pull request or release publication was performed; source changes
are committed and pushed separately from the ignored release packages.

Changed editable source groups:

- `src/data/{country,country_info,capital,capital_info,capital_hint,flag_similarity}.csv`;
  new `flag_note.csv` and `map_note.csv`.
- Four shared templates under `src/note_models/templates/ru-en/`,
  `src/note_models/style_ru_en.css`, `translations.csv`,
  `src/headers/desc_fork_en.html`, `desc_ru.html`, and template generation in
  `utils/generate_and_build.py`.
- All four existing forward/reverse recipe files; new offline source checks,
  APKG export/import regression checks, reference audit and browser QA scripts
  under `utils/`.
- `README.md`, `README.ru.md`, `CONTRIBUTING.md`, `doc/icon.svg`,
  `doc/content-sources.csv`, `doc/reference-audit.json`, `sources.csv` and
  `media-attribution.csv`.
- CI installs locked uv/npm dependencies and runs Ruff, Biome, source integrity,
  both build recipes and APKG export/import checks. Dependabot checks uv, npm and
  GitHub Actions monthly with grouped, bounded pull requests. `.gitignore` excludes
  environments, tool caches, Node dependencies and generated builds.
