# AP90 — Apte's Sanskrit-English Dictionary (1890)

_Created: 14-03-2020 · Last updated: 05-07-2026_

Research and correction work on **Apte's Sanskrit-English Dictionary of
1890** — 27 issue-tracked correction campaigns, a verb-identification
pipeline that mapped 3,632 AP90 verb entries to Monier-Williams, and a full
literary-source-abbreviation transcoding pipeline — part of the
[sanskrit-lexicon](https://github.com/sanskrit-lexicon) project.

---

## Why this repo exists

The canonical source text ([`ap90.txt`](https://github.com/sanskrit-lexicon/csl-orig/blob/main/v02/ap90/ap90.txt))
lives in the sibling `csl-orig` repo and is never edited directly. This repo
is where the actual correction and enrichment engineering happens: markup
normalization pipelines (five sequential `prep*.py` steps for `<ls>`
citation markup alone), a dedicated verb-identification pipeline
cross-referencing MW, transliteration tooling for Apte's abbreviation
lists, and per-issue working files for the 27 tracked corrections.

---

## Contents

| Directory | Description |
|---|---|
| [`verbs01/`](https://github.com/sanskrit-lexicon/AP90/tree/master/verbs01) | Verb identification and correlation with MW dictionary |
| [`ap57_verbs01/`](https://github.com/sanskrit-lexicon/AP90/tree/master/ap57_verbs01) | Same pipeline for the smaller Apte AP57 |
| [`markup/abls/`](https://github.com/sanskrit-lexicon/AP90/tree/master/markup/abls) | Literary source (`<ls>`) abbreviation markup — round 1 |
| [`markup/abls1/`](https://github.com/sanskrit-lexicon/AP90/tree/master/markup/abls1) | Further `<ls>` markup corrections — round 2 |
| [`markup/hyphen_deva/`](https://github.com/sanskrit-lexicon/AP90/tree/master/markup/hyphen_deva) | Devanagari hyphenation fixes |
| [`markup/hyphen_eng/`](https://github.com/sanskrit-lexicon/AP90/tree/master/markup/hyphen_eng) | English hyphenation fixes |
| [`markup/ap57_90_ls/`](https://github.com/sanskrit-lexicon/AP90/tree/master/markup/ap57_90_ls) | AP57 vs AP90 literary source comparison |
| [`apte_s2h/`](https://github.com/sanskrit-lexicon/AP90/tree/master/apte_s2h) | Apte abbreviation transcoding (SLP1 → IAST/Devanagari) — see [Usage](#usage-transcoding-apte-abbreviations-verified-runnable) below |
| [`andhrabharati/`](https://github.com/sanskrit-lexicon/AP90/tree/master/andhrabharati) | Andhra Bharati cross-reference for abbreviations |
| [`compounds/AB_AP57/`](https://github.com/sanskrit-lexicon/AP90/tree/master/compounds/AB_AP57) | AP57 compound entry parsing |
| [`issues/`](https://github.com/sanskrit-lexicon/AP90/tree/master/issues) | Per-issue correction workflows |

---

## Usage: transcoding Apte abbreviations (verified runnable)

[`apte_s2h/`](https://github.com/sanskrit-lexicon/AP90/tree/master/apte_s2h)
holds a transliteration of the Apte Student edition's Sanskrit-to-Hindi
abbreviation list (202 works, e.g. `a. pu. : agni purARa`), and
[`apte_s2h/transcode.py`](https://github.com/sanskrit-lexicon/AP90/blob/master/apte_s2h/transcode.py)
converts it between transliteration schemes using the shared XML-driven
`transcoder` module bundled in [`apte_s2h/transcoder/`](https://github.com/sanskrit-lexicon/AP90/tree/master/apte_s2h/transcoder).

This is fully self-contained — all inputs live in the repo — and was
executed directly, in this checkout, against
[`apte_s2h/apte_s2h_works.txt`](https://github.com/sanskrit-lexicon/AP90/blob/master/apte_s2h/apte_s2h_works.txt)
(05-07-2026):

```sh
cd apte_s2h
python transcode.py slp1 deva apte_s2h_works.txt apte_s2h_works_deva_test.txt
```

Output:

```
202 Works read from apte_s2h_works.txt
202 records written to apte_s2h_works_deva_test.txt
```

First lines of the result:

```
अ॰ पु॰ : अग्नि पुराण
अ॰ श॰ : अन्यापदेश शतक
अ॰ सं : अगस्त्य संहिता
अथर्व॰ : अथर्व वेद
```

This was diffed programmatically against the already-committed
[`apte_s2h/apte_s2h_works_deva.txt`](https://github.com/sanskrit-lexicon/AP90/blob/master/apte_s2h/apte_s2h_works_deva.txt)
and found **byte-identical** (4,302 characters both sides) — confirming the
script and its committed output are in sync, not stale.

The same script also produces IAST:

```sh
python transcode.py slp1 roman apte_s2h_works.txt apte_s2h_works_iast.txt
```

Per [`apte_s2h/readme.md`](https://github.com/sanskrit-lexicon/AP90/blob/master/apte_s2h/readme.md):
the period becomes the Devanagari abbreviation sign (lāghava-cihna, `॰`)
rather than daṇḍa when transcoding to `deva`; `<X>` marks English text `X`
left untranscoded; and IAST output capitalizes abbreviation/name-field
words.

---

## Markup pipeline (`markup/abls/`)

Sequential steps driven by `redo.sh`, per [`CLAUDE.md`](https://github.com/sanskrit-lexicon/AP90/blob/master/CLAUDE.md):

1. `change0a.py` — regex replacements for known abbreviation patterns
2. `updateByLine.py` — apply manual `change0b.txt` edits
3. `abbrauth.py abbr_1.txt auth_1.txt` — merge abbreviations and authors into `abbrauth_1.txt`
4. `prep1.py` — mark general abbreviations (`{%..%}` → `<ab>...</ab>`)
5. `prep2.py` — mark literary sources (`Rv. 1. 22. 16` → `<ls>Rv. 1. 22. 16</ls>`)
6. `prep3.py` — complete cross-line `<ls>` markup
7. `hyphen_eng1.py` + `updateByLine.py` — fix English hyphenation at line boundaries
8. `hyphen_deva1.py` + `updateByLine.py` — fix Devanagari hyphenation at line boundaries

## Verb pipeline (`verbs01/`)

Sequential steps driven by `redo.sh`:

```sh
python mwverb.py mw ../../mw/mw.txt mwverbs.txt
python mwverbs1.py mwverbs.txt mwverbs1.txt
python ap90_verb_filter.py ../ap90.txt ap90_verb_exclude.txt ap90_verb_include.txt ap90_verb_filter.txt
python ap90_verb_filter_map.py ap90_verb_filter.txt mwverbs1.txt ap90_verb_filter_map.txt
python verb1.py slp1 ../ap90.txt ap90_verb_filter_map.txt ap90_verb1.txt
```

This needs `ap90.txt` (from the sibling `csl-orig` checkout) and `mw.txt`
(from the sibling `mw` repo) — both outside this repo's own tree, so it is
documented here as the real pipeline definition rather than independently
re-executed. Output: 3,632 verb entries identified — 1,740 prefixed, 1,822
non-prefixed, 70 unmatched.

## The general `updateByLine.py` correction pattern

Used across `markup/*/` for applying change files, same as every other
Cologne dictionary repo:

```sh
python updateByLine.py <input_file> <changein_file> <output_file>
```

Change file format: paired `NNN old <original>` / `NNN new <replacement>`
lines; `;` prefix for comments.

---

## Timeline

| Year | Work |
|---|---|
| 2020 | Verb identification (`verbs01/`): 3,632 AP90 verb entries mapped to MW |
| 2020–2021 | Literary source markup pipeline (`markup/abls/`), 5-step `prep*.py` chain |
| 2021 | Round 2 markup corrections (`markup/abls1/`) via filter scripts |
| 2021 | Devanagari and English hyphenation fixes (`markup/hyphen_*`) |
| 2022 | Andhra Bharati abbreviation cross-reference (`andhrabharati/`) |
| 2022–2025 | Text corrections, encoding fixes, ongoing markup issues |

---

## Projects & Milestones

| Milestone | Project | Total | Open | Closed |
|---|---|---|---|---|
| Dictionary to Book (1) | Project 1 | 1 | 1 | 0 |
| Digitization Quality (2) | Project 2 | 10 | 3 | 7 |
| Structured Data (3) | Project 3 | 11 | 7 | 4 |
| Major Enhancements (4) | Project 4 | 5 | 4 | 1 |
| **Total** | | **27** | **15** | **12** |

## Issue Typology

### Solved (12 closed)

| # | Type | Severity | Summary |
|---|---|---|---|
| #4 | markup | medium | `<ls>` markup batch corrections |
| #5 | content-enhancement | minor | Display upgrade |
| #7 | encoding | minor | Character rendering fix |
| #8 | encoding | minor | Character rendering fix |
| #9 | markup | minor | XML tag normalisation |
| #13 | encoding | minor | SLP1 transcoding fix |
| #18 | text-correction | minor | German/English definition correction |
| #19 | markup | minor | XML tag normalisation |
| #20 | text-correction | minor | Definition correction |
| #22 | encoding | minor | Character rendering fix |
| #24 | markup | medium | `<ls>` markup batch corrections |
| #25 | text-correction | minor | Definition correction |

### Open (15 open)

| # | Type | Severity | Summary |
|---|---|---|---|
| #1 | content-enhancement | medium | Verb markup integration |
| #2 | content-enhancement | medium | Bibliography enhancements |
| #3 | content-enhancement | minor | Display upgrade |
| #6 | bug | minor | Broken link or XML error |
| #11 | markup | medium | `<ls>` markup corrections |
| #12 | link-target | medium | `<ls>` click-through to PDF pages |
| #14 | markup | minor | XML tag normalisation |
| #15 | markup | minor | XML tag normalisation |
| #16 | markup | minor | XML tag normalisation |
| #17 | content-enhancement | medium | Major display upgrade |
| #21 | text-correction | minor | Definition correction |
| #23 | markup | medium | `<ls>` markup batch corrections |
| #26 | text-correction | medium | Batch definition corrections |
| #27 | question | minor | Editorial question |
| #28 | question | minor | Editorial question |

---

## Labels

**Type** (one per issue): `link-target` · `link-splitting` · `markup` · `text-correction` · `content-enhancement` · `encoding` · `scan-quality` · `bug` · `question`

**Severity** (one per issue): `minor` · `medium` · `hard`

---

## Contributors

[sanskrit-lexicon](https://github.com/sanskrit-lexicon) project.

---

_Dr. Mārcis Gasūns_
