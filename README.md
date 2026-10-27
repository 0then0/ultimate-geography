<p align="left"><img src="doc/icon.svg" alt="Study cards with a globe, capital marker and flag" width="128" height="128"></p>

# Ultimate Geography · Multilingual

![7 languages](https://img.shields.io/badge/languages-7-23465a)
![323 notes per language](https://img.shields.io/badge/notes-323%20per%20language-57939a)
![996 cards per language](https://img.shields.io/badge/cards-996%20per%20language-57939a)
[![Original content: Unlicense](https://img.shields.io/badge/content-Unlicense-blue)](LICENSE.md)
[![Pronunciation data: CC BY-SA 4.0](https://img.shields.io/badge/pronunciation-CC_BY--SA_4.0-blue)](doc/PRONUNCIATION.md)
[![Media: individual licenses](https://img.shields.io/badge/media-individual%20licenses-lightgrey)](sources.csv)

[Русская документация](README.ru.md)

An editable geography deck for Anki in **Russian (RU), English (EN), Spanish (ES),
German (DE), French (FR), Japanese (JA) and Brazilian Portuguese (PT-BR)**, based on
[anki-geo/ultimate-geography](https://github.com/anki-geo/ultimate-geography).
This fork incorporates a corrected Russian reference APKG,
localizes its explanations, and retains the upstream CSV/Brain Brew workflow.
It is an independent fork, not an official upstream release.

Each language has **323 notes and 996 cards**, using the original four directions:
country → capital, capital → country, flag → country, and map → geographical
feature. No new directions or categories were added. Four map-only notes already
in upstream are absent from the supplied reference; they are retained here.

The fork adds 235 flag descriptions and 323 map explanations, precise distinctions
between capitals and seats of government, and the reference's left-aligned,
responsive layout. Extra information is always visible on the answer. Standalone
map panels have a bounded width. Personal priority decks, grading rules and study
settings from the reference are excluded. See [the migration audit](doc/reference-audit.json)
and [dated primary sources](doc/content-sources.csv) for deliberate differences.
English, Spanish, German and French retain their established upstream names and
note GUIDs. Japanese and Brazilian Portuguese have separate identities; upstream
European Portuguese (`PT`) remains available as a separate legacy variant.
[Release 2026.10.27](https://github.com/0then0/ultimate-geography/releases/tag/v2026.10.27)
contains all seven languages; the earlier 2026.10.20 release contains RU/EN only.
See [CHANGELOG.md](CHANGELOG.md).

## Pronunciation in the current source revision

The 2026.10.27 release appends optional country/capital pronunciation fields.
Russian uses stress marks, other languages use sourced IPA or explicit stress
guides, and Japanese adds kana readings for kanji. Foreign readings state their
actual language; French hints do not invent lexical stress. Ordinary name
spellings and existing GUIDs are unchanged. Hints appear only next to a name that
is already shown. The map/image panels now follow the image width instead of
stretching into the remaining desktop space.

See [pronunciation rules and attribution](doc/PRONUNCIATION.md), the per-entry
[source register](doc/pronunciation-sources.csv) and the full
[coverage audit](doc/pronunciation-coverage.csv). All **3,815 individual names** have a sourced reading or a documented,
rule-backed exemption. There are **3,262 nonempty hint fields**; the audit
distinguishes target-language readings from explicitly labelled foreign variants. The source CSVs and audit registers accompany the release ZIPs.

## Flag coverage

The current sources add 14 territorial flags to existing notes, with one new
flag-to-territory card each. Note GUIDs and existing cards are retained.
Northern Ireland explains the Union Flag status; Belfast’s city flag is not
used as a territorial flag. Saint Lucia’s triangle layering and Vatican key
translations are corrected. The New Caledonia caption identifies the Kanak/FLNKS
flag and distinguishes it from the French national flag.
See the [dated correction register](doc/flag-corrections.csv). This does not
introduce city flags or claim complete coverage of every regional flag.

## Install

Download the release ZIP for your language when available, extract it, and import its `.apkg` via
Anki's **File → Import**. Images are included; CrowdAnki is not needed for APKG.
Keep the ZIP's `LICENSE.md`, `sources.csv` and `media-attribution.csv` when sharing
or repackaging it. Share the ZIP as the complete distribution.

All seven APKGs can coexist in one collection. Each language has disjoint note
GUIDs, a separate note type and its own deck, such as `Ultimate Geography [JA]`
or `Ultimate Geography [PT-BR]`. Use the same language when updating.

## Update an existing deck

Synchronise and make an Anki backup first. Import the same language's new APKG;
choose **Update notes: Always**, **Update note types: Always**, and enable
**Merge note types** when migrating from the supplied corrected Russian deck.
Leave **Import learning progress** and **Import deck presets** off. The original
Russian model ID and all language GUIDs are retained. Existing cards keep their
IDs and review history; new notes start without progress. Existing cards may
remain in their old subdecks, which can be reorganised in the browser.

Do not delete the old notes before updating. Locally edited field content and
card styling can be overwritten by the update; back it up separately. A model
whose identity or field names were manually changed requires separate migration.
The supplied reference's custom model is renamed to `Ultimate Geography [RU]`.

CrowdAnki remains available: run `uv run --locked python utils/generate_and_build.py recipes/source_to_anki.yaml`, then import the corresponding
`build/Ultimate Geography [RU]` or `[EN]` folder with CrowdAnki. The RU CrowdAnki
deck has a separate UUID so it no longer shares the EN deck identity. Do not
alternate APKG and CrowdAnki upgrade methods without a backup and inspection of
their import logs; APKG import/merge is the migration path tested in this fork.

## Build from editable sources

Requires [uv](https://docs.astral.sh/uv/) and **CPython 3.10–3.15** (standard GIL
builds). `.python-version` selects 3.14 by default. `pyproject.toml` and `uv.lock`
replace Pipenv. uv manages the project's `.venv`; there is no need to activate it
manually.

```sh
uv sync --locked
uv run --locked python utils/generate_and_build.py recipes/source_to_anki.yaml
uv run --locked python utils/generate_and_build.py 'recipes/source_to_anki_[experimental].yaml'
uv run --locked python utils/verify_sources.py
```

To select another supported version for all commands in the current shell, set
`export UV_PYTHON=3.15` before syncing/running. A single command can instead use
`uv run --locked --python 3.15 --group export python utils/export_apkg.py`.
The lockfile covers all six versions; Markdown 3.10.3 is selected on Python 3.10,
and 3.11.2 on newer Python. PyYAML 6.0.3 and ruamel.yaml.clib 0.2.15 replace their
older versions for Python 3.15 compatibility. On the tested macOS system those two
packages build from source on 3.15, requiring a C compiler and Python development
headers. Brain Brew remains at 0.3.11. CI runs both build recipes and APKG tests
on every supported Python version. See [validation results](doc/VALIDATION.md)
for the exact locally tested interpreters and platforms.

The first build generates all upstream standard and extended CrowdAnki variants;
the second preserves the experimental build. Only standard variants of the seven
supported languages are packaged for this fork's public APKG releases. Edit CSVs in `src/data`, shared
templates in `src/note_models/templates/shared`, labels in
`src/note_models/translations.csv`, and styling in `src/note_models/style_shared.css`.
Generated templates and `build/` are ignored by Git. The remaining legacy upstream
languages retain their original templates and styling. New fields are appended after the eight upstream
fields.

The optional `export` dependency group pins **Anki backend 26.9.3** in the same
selected Python environment throughout 3.10–3.15. No desktop Anki installation
or `PYTHONPATH` is needed:

```sh
uv run --locked --group export python utils/export_apkg.py
# Or export one language after building:
uv run --locked --group export python utils/export_apkg.py --language JA
uv run --locked --group export python utils/verify_release.py
uv run --locked --group export python utils/audit_reference.py '/path/to/reference.apkg'
```

For the reference upgrade/history regression test, pass
`--reference '/path/to/reference.apkg'` to `verify_release.py`. CI runs the public
package tests without the private reference file. `uv sync --locked --group export`
installs the build, lint and export dependencies together in advance.

Outputs: `build/releases/Ultimate_Geography_2026.10.27_<LANG>.apkg` for
`RU`, `EN`, `ES`, `DE`, `FR`, `JA` and `PT-BR`, corresponding
ZIPs with licenses and attribution, and JSON manifests with package and semantic
content hashes. `SOURCE_DATE_EPOCH` sets the source modification date for a new
release (default: 2026-10-27 UTC); advance it when publishing changed content.
Anki assigns fresh internal database IDs and ZIP metadata during export, so APKG
bytes may differ between builds. GUIDs, fields, templates and semantic hashes are
reproducible. The reference APKG is needed only for the optional comparison audit,
never for building. Public packages are made in temporary collections, with media
included and scheduling and deck presets explicitly excluded.

## Formatting and linting

Ruff is pinned in the default `dev` dependency group. It checks Python utilities
for basic errors and import ordering, and formats them with four-space indentation
and a 100-character line width:

```sh
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked ruff check --fix .
uv run --locked ruff format .
```

Biome is pinned in `package-lock.json`. With Node.js 24 and npm:

```sh
npm ci --ignore-scripts
npm run check
npm run format
```

Biome checks owned JavaScript (`utils/*.cjs`), note-model CSS and JSON configuration
and documentation. Its explicit file list excludes HTML/Anki templates (including
the significant `--` separator), CSV, YAML, Markdown, SVG, third-party media,
generated templates and `build/`. CSV integrity remains covered by
`verify_sources.py`. CSS-only exceptions retain Anki’s intentional cascade order
and `!important` reviewer overrides. CI checks formatting without rewriting files. Dependabot
checks uv, npm and GitHub Actions monthly with grouped, bounded pull requests.

Browser QA still uses an existing Playwright/Chromium installation; Playwright is
not added as a project dependency:

```sh
node utils/verify_layout.cjs
```

Set `UG_CHROMIUM_PATH` for an existing Chromium outside Playwright's default cache,
and `NODE_PATH` for an existing shared Node package directory if needed. The script
opens Anki-rendered HTML from `verify_release.py` and writes measurements and
screenshots to `build/qa/`; it does not download packages or browsers.

## Validation and compatibility

After building the decks and exporting all seven APKGs, run the regression suite:

```sh
uv run --locked --group export python -m unittest discover -s utils -p 'test_*.py' -v
```

The standard-library tests check ZIP packaging alongside `build/qa` and
`build/releases`, UTF-8 input/output under a non-UTF-8 locale, rejection of an
unexpected reference package, and public import/update/history preservation.
They use temporary archives and Anki collections and require no private reference.
The import checks also install all seven languages together in both orders.
CI runs the suite on every Python version in the compatibility matrix.

See [the validation record](doc/VALIDATION.md) for exact versions, commands, import
results and browser viewport checks. Backend import tests are not a claim of
interactive testing in Anki desktop, AnkiDroid, AnkiMobile or on a physical phone.
Verified tooling: Anki backend **26.9.3** and Chromium **156.0.8078.4**.

## License and attribution

The original deck content, code, templates and project icon are **Unlicense**, as in
upstream. Images are excluded from that dedication and retain their original
licenses. [sources.csv](sources.csv) preserves upstream source links, licenses and
modification notes; [media-attribution.csv](media-attribution.csv) supplements it
with creator metadata retrieved from those source pages. No package-only image
with uncertain revision provenance is substituted for an upstream asset.
The label `kaiu` in the supplied model is not evidence of separate authorship or
an additional third-party license. No Apache-2.0 claim is made for this fork.

[CONTRIBUTING.md](CONTRIBUTING.md) describes the data model, translation workflow
and validation commands. [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) covers participation;
[SECURITY.md](SECURITY.md) explains vulnerability reporting. Use the issue forms
for reproducible bugs or sourced content corrections.

Project text files use UTF-8/LF, enforced through `.editorconfig` and
`.gitattributes`; binary media retain their exact bytes. Biome formats supported
JavaScript/CSS/JSON files; Ruff formats Python. CSV, YAML, Markdown and Anki HTML
are intentionally outside Biome's supported/safe formatting scope.
Use the distribution-specific commands and counts above for this fork.

The new pronunciation CSVs and their selection/arrangement are **CC BY-SA 4.0**;
see [their attribution and source distinctions](doc/PRONUNCIATION.md). Preserve
these notices and the pronunciation source/coverage registers when sharing builds.
