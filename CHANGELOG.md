# Changelog

This changelog records changes to this independent Ultimate Geography fork.
Dates use `YYYY-MM-DD`. Unreleased work is not part of a published package until
it appears in a tagged GitHub release.

## 2026.10.25 (2026-10-25)

- Add the shared responsive interface and flag/map explanations to Spanish,
  German and French while retaining their existing note GUIDs.
- Add Japanese and Brazilian Portuguese (`PT-BR`) with separate note, model and
  deck identities. Existing European Portuguese (`PT`) remains available.
- Build and validate seven public language variants: RU, EN, ES, DE, FR, JA and
  PT-BR; verify repeated imports and simultaneous installation.
- Add language markup, Japanese line breaking and CJK font fallbacks.
- Add contributor, security, issue and pull-request guidance; configure line
  endings, editor defaults, generated-file exclusions and read-only CI access.

## 2026.10.20 (2026-10-20)

First public release of the fork, based on upstream commit `6725c0f` and the
corrected Russian reference APKG.

- Ship RU/EN variants with 323 notes, 982 cards and 550 media files each.
- Add 221 flag descriptions, 323 map explanations and dated sources for
  significant geographical corrections.
- Preserve per-language GUIDs and verify updates retain review history.
- Adopt responsive light/dark card templates with always-visible explanations.
- Retain Unlicense for content/code and the original image licenses; include
  author attribution and source links in release archives.
- Add native APKG export, semantic manifests, import/layout checks, uv, Ruff,
  Biome and monthly grouped Dependabot updates.
- Support CPython 3.10–3.15; select Python 3.14 by default.
- Fix packaging alongside generated QA/release folders and UTF-8 handling under
  non-UTF-8 locales; add four regression tests across the Python matrix.
