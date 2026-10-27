# Pronunciation hints

Names keep their ordinary spelling. Two optional fields are appended after the
existing ten fields: `Country_Pronunciation` and `Capital_Pronunciation`.
They do not generate cards or change note GUIDs. Editable hints live in
`src/data/country_pronunciation.csv` and `capital_pronunciation.csv`.
Builds work offline and never call a dictionary or speech service.

Russian hints use an acute accent after the stressed vowel; `ё` already indicates
stress. English, German, Spanish and Brazilian Portuguese use IPA where sourced.
Portuguese dictionary stress classifications can instead supply a syllabic guide
with the tonic syllable in capitals; this does not infer regional vowel quality. `ˈ` comes
**before** the syllable with primary stress, `ˌ` before secondary stress.
A dictionary may supply more than one acceptable pronunciation; a hint is not
intended to prohibit regional variants. IPA presented as Brazilian must be identified as Brazilian by its source.
A Portuguese reading without Brazilian provenance is explicitly labelled Portuguese. French IPA describes sounds without inventing lexical
stress. Japanese kana readings clarify kanji; they are not pitch-accent notation.
Katakana already spells out a reading, including long vowels and small kana.

Questions show only pronunciation of the name already visible. Flag and map
questions never disclose the answer's name or pronunciation. Answer-side hints
and explanations remain visible without expanding a control.

## Sources, coverage and attribution

`pronunciation-sources.csv` records the language, source spelling, displayed hint,
dictionary page/revision (or a dated snapshot) and access date for each dictionary-derived hint.
Wiktionary and Wikipedia contributors retain authorship; linked page histories
identify them. Wikipedia lead-name stress marks supplement Russian dictionary
entries where the source explicitly marks that same spelling.
Extracted pronunciations, selection and arrangement in the two pronunciation CSVs
are provided under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Changes consist of selecting a variant, stripping dictionary markup, combining
separately cited words where recorded, and adding Russian stress to the existing
spelling. Individual reading/pronunciation facts also reference Cambridge
Dictionary, Duden, Dictionary.com/Collins/Random House, Forvo phonetic spellings and
Shogakukan’s Digital Daijisen on Kotobank, where listed. Their dictionary prose,
audio and illustrations are not redistributed or relicensed. Source authorship
and the distinction from CC-licensed Wiktionary data are recorded per entry.
No dictionary audio is redistributed. The license includes a disclaimer
of warranties; see its [legal code](https://creativecommons.org/licenses/by-sa/4.0/legalcode.en).

This applies to the new pronunciation data. The existing Unlicense and individual
image licenses remain applicable to their respective material.

`pronunciation-coverage.csv` audits **3,815 individual names** in all seven public
languages, including ordinary names and each component of multi-capital fields.
All 534 previously unresolved decisions are now recorded. Each row includes its
status, displayed hint, reasoning, evidence, rule (for exemptions) and reading
language. There are **3,279 name readings** in **3,262 nonempty fields**. The
remaining **536 rows** are explained exemptions: 423 kana spellings, four Russian
monosyllables, 91 reviewed Spanish/Portuguese orthographic cases and 18 ordinary
vocabulary cases with linked dictionary readings. No row remains `unverified`.

The audit includes 118 local-name readings and 94 additional explicitly labelled
source-language variants. Another 38 Portuguese syllabic stress guides label the
source language without asserting Brazilian vowel quality. A foreign-language
reading is not a claim about how speakers of the deck language pronounce that
name. Labels retain the actual language code and distinguish local names from
other attested variants. For example, the Māori name **Te Whanganui-a-Tara** is
not transcribed as though it were the English word **Wellington**. No artificial
French word stress or Japanese pitch accent is generated. This is complete
coverage of editorial decisions, not native-editor certification or a claim that
every entry has a target-language IPA transcription.

`pronunciation-rules.csv` records the rules and primary references used for
exemptions. Spanish rules are not applied blindly to unadapted foreign names;
Portuguese nasal tildes are not treated as stress marks. Ordinary vocabulary
exemptions cite readings for their lexical components in the audit itself.
Source-language fallbacks always have a visible localized language label. Native
IPA can refer to a local alias rather than to the exonym in the heading.

The offline validator rejects missing, duplicate and stale audit names, unresolved
statuses, unsupported exemptions, empty transcriptions and foreign-language
sources whose language label is absent from the displayed field. Unit tests
exercise those rejection paths and ensure flag/map questions never reveal hints.
These checks verify structural integrity and documented provenance. They cannot
prove that every dictionary variant is the preferred pronunciation for every
speaker; no independent native-speaker review was performed.

When editing a hint, update its source and coverage records. Keep geographic names
and GUIDs intact. Verify source/build parity and render all seven languages at the
widths and themes documented in `VALIDATION.md`.

Some Japanese readings are assembled from separately cited geographic affixes
and the original kana. These have method `composed-reading`; they do not claim
that the dictionary supplies that full compound or its pitch accent.
