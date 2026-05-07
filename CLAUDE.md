# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **AP90 Sanskrit Dictionary Data Processing** repository — part of the [sanskrit-lexicon](https://github.com/sanskrit-lexicon) project. It contains scripts and data for correcting and enriching the AP90 (Apte's Sanskrit-English Dictionary of 1890).

The primary input is `ap90.txt` (located in `csl-orig/v02/ap90/ap90.txt`, a sibling repo not tracked here). All processing reads from or produces corrections to that file.

## Architecture

| Directory | Purpose |
|---|---|
| `verbs01/` | AP90 verb identification and correlation with MW dictionary |
| `ap57_verbs01/` | Same pipeline for the smaller Apte AP57 dictionary |
| `markup/abls/` | Round 1: literary source (`<ls>`) abbreviation markup pipeline |
| `markup/abls1/` | Round 2: further `<ls>` markup corrections via filter scripts |
| `markup/hyphen_deva/` | Devanagari hyphenation corrections at line boundaries |
| `markup/hyphen_eng/` | English hyphenation corrections at line boundaries |
| `markup/ap57_90_ls/` | AP57 vs AP90 literary source comparison and tooltip sync |
| `apte_s2h/` | Apte abbreviation list: SLP1 → IAST/Devanagari transcoding |
| `andhrabharati/` | Andhra Bharati cross-reference for AP90 abbreviations |
| `compounds/AB_AP57/` | AP57 compound entry parsing |
| `issues/` | Per-issue correction workflows (`issueNNN/` pattern) |

### Markup Pipeline (`markup/abls/`)

Sequential steps driven by `redo.sh`:
1. `change0a.py` — regex replacements for known abbreviation patterns
2. `updateByLine.py` — apply manual `change0b.txt` edits
3. `abbrauth.py abbr_1.txt auth_1.txt` — merge abbreviations and authors into `abbrauth_1.txt`
4. `prep1.py` — mark general abbreviations (`{%..%}` → `<ab>...</ab>`)
5. `prep2.py` — mark literary sources (`Rv. 1. 22. 16` → `<ls>Rv. 1. 22. 16</ls>`)
6. `prep3.py` — complete cross-line `<ls>` markup
7. `hyphen_eng1.py` + `updateByLine.py` — fix English hyphenation at line boundaries
8. `hyphen_deva1.py` + `updateByLine.py` — fix Devanagari hyphenation at line boundaries

### Verb Pipeline (`verbs01/`)

Sequential steps driven by `redo.sh`:
```
python mwverb.py mw ../../mw/mw.txt mwverbs.txt
python mwverbs1.py mwverbs.txt mwverbs1.txt
python ap90_verb_filter.py ../ap90.txt ap90_verb_exclude.txt ap90_verb_include.txt ap90_verb_filter.txt
python ap90_verb_filter_map.py ap90_verb_filter.txt mwverbs1.txt ap90_verb_filter_map.txt
python verb1.py slp1 ../ap90.txt ap90_verb_filter_map.txt ap90_verb1.txt
```
Output: 3,632 verb entries identified, 1,740 prefixed, 1,822 non-prefixed, 70 unmatched.

### `updateByLine.py` Pattern

Used across `markup/*/` for applying change files:
```sh
python updateByLine.py <input_file> <changein_file> <output_file>
```
Change file format: paired `NNN old <original>` / `NNN new <replacement>` lines; `;` prefix for comments.

## Dependencies

- **Python 3**
- **ap90.txt** — in sibling directory `../../csl-orig/v02/ap90/ap90.txt` (relative to working dirs)
- **mw.txt** — in sibling repo for the verb pipeline cross-reference

## GitHub Issue Conventions

### Milestones and projects

Every issue belongs to exactly one milestone, which mirrors an org-level kanban project:

| Milestone | Project | Scope |
|---|---|---|
| Dictionary to Book (1) | Project 1 | Link targets and link splitting |
| Digitization Quality (2) | Project 2 | Scan quality, encoding, bug fixes, text corrections |
| Structured Data (3) | Project 3 | Markup normalisation, structured data, editorial questions |
| Major Enhancements (4) | Project 4 | Large new content: verb markup, bibliography, Cologne material |

### Type labels

Every issue has exactly one type label:

| Label | When to use |
|---|---|
| `link-target` | Building a click-through from a `<ls>` abbreviation to scanned PDF pages |
| `link-splitting` | Splitting combined `SOURCE N,N` refs into individual per-page links |
| `markup` | Normalising XML tag content or structure (`<ls>`, `<ab>`, etc.) |
| `text-correction` | Corrections to English definitions or Sanskrit headwords |
| `content-enhancement` | New material, display upgrades, or structural additions beyond correction |
| `encoding` | SLP1/IAST transcoding, character rendering, hyphen/dash normalisation |
| `scan-quality` | Replacing blurry, skewed, or missing scan pages |
| `bug` | Broken links, XML structure errors, or broken download files |
| `question` | Scholarly or editorial questions requiring research before any code change |

### Severity labels

Every issue also has exactly one severity label:

| Label | When to use |
|---|---|
| `minor` | Targeted, self-contained fix — a handful of lines or a single file |
| `medium` | Standard unit of work — one markup pass, a batch of text corrections |
| `hard` | Large effort spanning many sources, files, or dictionaries |
