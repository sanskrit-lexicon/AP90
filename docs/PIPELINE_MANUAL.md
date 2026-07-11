# AP90 pipelines — operator manual

_Created: 11-07-2026 · Last updated: 11-07-2026_

This is the **operator manual** for the AP90 repository: how the markup,
hyphenation, verb-identification, transcoding and issue-campaign pipelines for
Apte's 1890 *Sanskrit-English Dictionary* actually run — from the real
`redo.sh` files, not from their idealized readme summaries (two material
discrepancies between the two are corrected below).

Three documents describe this repo, with different jobs:

- **What the repo is** (history, issue typology, the verified apte_s2h usage
  example) — [README.md](https://github.com/sanskrit-lexicon/AP90/blob/master/README.md);
- **Code contract for AI/code sessions** —
  [CLAUDE.md](https://github.com/sanskrit-lexicon/AP90/blob/master/CLAUDE.md)
  (note: its abls and verbs01 step lists are idealized — see
  [the corrections](#two-corrections-to-the-existing-docs));
- **How to operate the pipelines** (this document) —
  [docs/PIPELINE_MANUAL.md](https://github.com/sanskrit-lexicon/AP90/blob/master/docs/PIPELINE_MANUAL.md).

Commands are quoted verbatim from the actual `redo*.sh` drivers and per-folder
readmes; scripts and paths verified on disk 11-07-2026. The apte_s2h pipeline
was previously live-verified byte-identical (05-07-2026, recorded in the
README); the others are transcription-verified — most are one-time campaigns
pinned to csl-orig commits.

## Cheat-sheet: the shared correction idiom

Everything here is the standard Cologne loop over the sibling
[csl-orig](https://github.com/sanskrit-lexicon/csl-orig)'s
`v02/ap90/ap90.txt` (never edited in place):

```sh
# 0. Snapshot, pinned by commit (record the hash in your readme)
git -C <csl-orig> show <hash>:v02/ap90/ap90.txt > ap90_0.txt

# 1. Generate a change file, then apply it — generator and applier are SEPARATE steps
python <generator>.py ap90_0.txt change_1.txt        # emits transactions
python updateByLine.py ap90_0.txt change_1.txt ap90_1.txt

# 2. Validate via csl-pywork, then deliver per the batched-PR rule
cp ap90_N.txt <csl-orig>/v02/ap90/ap90.txt
cd <csl-pywork>/v02 && sh generate_dict.sh ap90 ../../ap90 && sh xmlchk_xampp.sh ap90
```

Change-file format: paired `NNN old <text>` / `NNN new <text>` lines, `;`
comments — identical to every Cologne repo. Delivery: never push csl-orig
directly; queue and ship as one consolidated batch PR per the canonical
[correction workflow](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md).

**Ordering is commit-hash chaining.** The historical campaigns ran in a strict
sequence, each starting from the commit the previous one installed:
hyphen_deva (→ `29e18e69`) → abls Round 1 (`29e18e69` → `19c7ee9c`) → abls1
Round 2 (`19c7ee9c` → `37f98f8b`). Reproduce a campaign only against **its
own** pinned start commit.

## Two corrections to the existing docs

Verified against the scripts on 11-07-2026 — trust these over CLAUDE.md/README
prose:

1. **`markup/abls/redo.sh` is 12 invocations, not 8 steps.** `change0a.py`
   *generates* `change0a.txt` (256 transactions); it does not apply anything —
   a separate `updateByLine.py` call applies it, followed by a second
   `updateByLine.py` for the manual `change0b.txt`. CLAUDE.md collapses the
   generator and applier into one step. (Cosmetic defect: the script's final
   `echo` names `ap90_4.txt` while the last command writes `ap90_5.txt`.)
2. **`verbs01/redo.sh` runs 4 commands, not the documented 5** — the two MW
   verb-extraction commands are commented out, and `mwverb.py` /
   `mwverbs1.py` / `mwverbs*.txt` **do not exist in `verbs01/`** (they live
   only in `ap57_verbs01/`). `mwverbs1.txt` is consumed from the sibling
   [MWS](https://github.com/sanskrit-lexicon/MWS) repo
   (`../../MWS/mwverbs/mwverbs1.txt`). The redo also produces a sixth,
   undocumented output: `ap90_verb1_deva.txt` (Devanagari edition).

## Map of the workspaces

| Workspace | What it did | Issues | Status |
|---|---|---|---|
| [markup/hyphen_deva/](https://github.com/sanskrit-lexicon/AP90/tree/master/markup/hyphen_deva) | resolve 13,601 Devanagari end-of-line hyphens (3 staged passes + reversibility proofs) | [#8](https://github.com/sanskrit-lexicon/AP90/issues/8) | done; ran **first** in the chain |
| [markup/hyphen_eng/](https://github.com/sanskrit-lexicon/AP90/tree/master/markup/hyphen_eng) | resolve 26,749 English end-of-line hyphens (26,652 applied, 97 open questions) | [#7](https://github.com/sanskrit-lexicon/AP90/issues/7) | done |
| [markup/abls/](https://github.com/sanskrit-lexicon/AP90/tree/master/markup/abls) | Round 1 `<ab>`/`<ls>` abbreviation + literary-source markup | [#4](https://github.com/sanskrit-lexicon/AP90/issues/4)/[#9](https://github.com/sanskrit-lexicon/AP90/issues/9)/[#11](https://github.com/sanskrit-lexicon/AP90/issues/11)/[#24](https://github.com/sanskrit-lexicon/AP90/issues/24) | done |
| [markup/abls1/](https://github.com/sanskrit-lexicon/AP90/tree/master/markup/abls1) | Round 2 `<ls>` corrections (change6→change15) | [#11](https://github.com/sanskrit-lexicon/AP90/issues/11)/[#24](https://github.com/sanskrit-lexicon/AP90/issues/24)/[#30](https://github.com/sanskrit-lexicon/AP90/issues/30) | done; `filtercode/` is a non-runnable "sampling" |
| [markup/ap57_90_ls/](https://github.com/sanskrit-lexicon/AP90/tree/master/markup/ap57_90_ls) | AP57↔AP90 `<ls>` tooltip variant merge (data-only, no scripts) | [#23](https://github.com/sanskrit-lexicon/AP90/issues/23) | done; changes deliberately NOT in csl-corrections' printchange ledger |
| [verbs01/](https://github.com/sanskrit-lexicon/AP90/tree/master/verbs01) | 3,632 AP90 verb entries identified + mapped to MW | [#1](https://github.com/sanskrit-lexicon/AP90/issues/1)/[#2](https://github.com/sanskrit-lexicon/AP90/issues/2) | **re-runnable** (needs MWS sibling) |
| [ap57_verbs01/](https://github.com/sanskrit-lexicon/AP90/tree/master/ap57_verbs01) | same pipeline for AP57 (3,978 verbs) + AP57↔AP90 verb diff | [#2](https://github.com/sanskrit-lexicon/AP90/issues/2)/[#23](https://github.com/sanskrit-lexicon/AP90/issues/23) | **re-runnable, fully self-contained** |
| [apte_s2h/](https://github.com/sanskrit-lexicon/AP90/tree/master/apte_s2h) | 202-work Apte-Student abbreviation list, SLP1 → Devanagari/IAST | — | **re-runnable; live-verified byte-identical 05-07-2026** |
| [andhrabharati/](https://github.com/sanskrit-lexicon/AP90/tree/master/andhrabharati) | AndhraBharati re-digitization + abbreviation lists (data-only) | [#17](https://github.com/sanskrit-lexicon/AP90/issues/17) | ingested; `ap90ab_v2_suggest.txt` TODO list still unapplied |
| [compounds/AB_AP57/](https://github.com/sanskrit-lexicon/AP90/tree/master/compounds/AB_AP57) | parse 37,649 compounds out of AB's AP57 (36,589 entries) | [#5](https://github.com/sanskrit-lexicon/AP90/issues/5) | done |
| [issues/issue26/](https://github.com/sanskrit-lexicon/AP90/tree/master/issues/issue26) | Scott/Usha/Jim correction batch + alternate-headword promotion (+2,662 entries) | [#26](https://github.com/sanskrit-lexicon/AP90/issues/26) | **open**, multi-part |
| [issues/issue29/](https://github.com/sanskrit-lexicon/AP90/tree/master/issues/issue29) | activate `<ls>` link targets for AP90 (13 activated) | [#29](https://github.com/sanskrit-lexicon/AP90/issues/29) | **open**; cologne install + csl-lslink step = TODO |

The committed [issues/readme.txt](https://github.com/sanskrit-lexicon/AP90/blob/master/issues/readme.txt)
lists only these two folders — most campaign work in this repo predates the
`issues/` convention and lives in the topic directories above.

## Environment and prerequisites

- **Python 3**, stdlib only. `updateByLine.py` (164 lines) and
  `transcoder.py` (+ per-dir XML tables) are copy-vendored per workspace —
  frozen records, no shared module.
- **Git Bash / POSIX shell** for the `redo*.sh` drivers.
- **Sibling checkouts:** csl-orig (`v02/ap90/`, `v02/ap57/`, `v02/ap/`,
  `v02/mw/`), csl-pywork (`generate_dict.sh` + `xmlchk_xampp.sh` + the
  `distinctfiles/*/tooltip.txt` inputs), MWS (`mwverbs/mwverbs1.txt` for
  verbs01), csl-corrections (correction-form intake + printchange ledgers),
  csl-websanlexicon + csl-apidev (`basicadjust.php`, issue29), csl-lslink
  (link sqlite build), `AP90Scan`/`AP57Scan` (scan images).
- **Three path conventions coexist** — remap per workspace: `markup/*` uses
  bare `../ap90.txt` relatives; `verbs01/redo.sh` uses the two-root
  `../../../cologne/csl-orig/v02` layout; `issues/*` readmes use absolute
  `/c/xampp/htdocs/...`. None are parameterized.
- **Default branch is `master`** (not main) — a local stale `main` branch may
  exist in old checkouts; blob links and PRs target `master`.
- No secrets; no network access.

## Walkthrough 1 — markup Round 1 ([markup/abls/](https://github.com/sanskrit-lexicon/AP90/tree/master/markup/abls))

The real [redo.sh](https://github.com/sanskrit-lexicon/AP90/blob/master/markup/abls/redo.sh), verbatim:

```sh
python change0a.py ap90_0.txt change0a.txt              # GENERATES 256 transactions
python updateByLine.py ap90_0.txt change0a.txt ap90_0a.txt
python updateByLine.py ap90_0a.txt change0b.txt ap90_0b.txt   # manual edits
python abbrauth.py abbr_1.txt auth_1.txt abbrauth_1.txt       # 269 abbrevs+authors merged
python prep1.py ap90_0b.txt abbrauth_1.txt ap90_1.txt abbr_2.txt   # {%..%} -> <ab>
python prep2.py ap90_1.txt abbrauth_1.txt ap90_2.txt auth_2.txt    # Rv. 1.22.16 -> <ls>
python prep3.py ap90_2.txt auth_2.txt ap90_3.txt changes3.txt      # cross-line <ls>
python hyphen_eng1.py ap90_3.txt hyphen_eng.txt hyphen_eng_questions.txt
python updateByLine.py ap90_3.txt hyphen_eng.txt ap90_4.txt
python hyphen_deva1.py ap90_4.txt hyphen_deva.txt hyphen_deva_questions.txt
python updateByLine.py ap90_4.txt hyphen_deva.txt ap90_5.txt   # (script's echo says _4 — stale label)
```

Consumes `ap90_0.txt` (= csl-orig `29e18e69`) + the abbreviation/author lists
harvested from the ap90 header (`abbr_1.txt`, `auth_1.txt`; A.D./B.C. added
by hand); produces `ap90_5.txt`, installed as csl-orig `19c7ee9c`. Known
residue recorded in its readme: 15 type-2 duplicate abbreviations (`N.`,
`P.`, `U.`, `A.` …), bare `' A.'`/`' P'` cases, and one `Bhāv. P.` typo.
`change_misc*.py` are manual-assist generators — **not** part of the chain.

**Round 2** ([markup/abls1/](https://github.com/sanskrit-lexicon/AP90/tree/master/markup/abls1),
`redo2.sh`) is ten chained `updateByLine.py temp_ap90_N.txt changeN.txt
temp_ap90_N+1.txt` applications for `change6.txt`…`change15.txt` (numbering
continues Round 1's `_0.._5`), taking csl-orig `19c7ee9c` → `37f98f8b`. The
change files were built partly by hand and partly by the `filtercode/`
scripts, which the readme explicitly keeps as a non-runnable "sampling".
Stats regen: `python ls_summary1.py temp_ap90_15.txt tooltip.txt ls_summary1.txt`.

## Walkthrough 2 — hyphenation ([markup/hyphen_deva/](https://github.com/sanskrit-lexicon/AP90/tree/master/markup/hyphen_deva), [markup/hyphen_eng/](https://github.com/sanskrit-lexicon/AP90/tree/master/markup/hyphen_eng))

**Devanagari** (ran first of all campaigns): manual `changes0_edit.txt` (53) →
`spacechg.py` (986 space-boundary fixes; writes `changes0b.txt` — the
readme's `changes_0b.txt` spelling is wrong) → three staged hyphen passes
(`hyphen1.py` 1,232 + `<lbinfo n=.../>` markers; `hyphen2.py` 12,298;
`hyphen3.py` ~35 `{#--#}` cases), each applied via `updateByLine.py`, ending
in `ap90_3.txt`. Every stage has a **reversibility proof**
(`restore1/2/3.py`, `restore_hyphen2.py` — diff back to the input must be 0);
keep that discipline in any new hyphen work.

**English** (no redo.sh; the readme is the runbook):

```sh
python hyphen_eng.py ap90_0.txt hyphen_changes.txt hyphen_questions.txt  # 26,749 found / 26,652 resolved
python updateByLine.py ap90_0.txt hyphen_changes.txt ap90_1.txt
# reversibility proof via restore_hyphen_eng.py; then install:
cp ap90_1.txt ../ap90.txt
sh generate_dict.sh ap90 ../../AP90Scan/2020/
```

Open residue: 97 unresolved `-$` cases in `hyphen_questions.txt`; ~3,000
resolutions flagged `type=false` by English spell-check — a review pool, not
errors.

## Walkthrough 3 — the verb pipelines

**AP90** ([verbs01/redo.sh](https://github.com/sanskrit-lexicon/AP90/blob/master/verbs01/redo.sh),
the real 4 commands — see [correction #2](#two-corrections-to-the-existing-docs)):

```sh
orig="../../../cologne/csl-orig/v02"
mwverbs1="../../MWS/mwverbs/mwverbs1.txt"
python ap90_verb_filter.py ${orig}/ap90/ap90.txt ap90_verb_exclude.txt ap90_verb_include.txt ap90_verb_filter.txt
python ap90_verb_filter_map.py ap90_verb_filter.txt ${mwverbs1} ap90_verb_filter_map.txt
python verb1.py slp1 ${orig}/ap90/ap90.txt ap90_verb_filter_map.txt ap90_verb1.txt
python verb1.py deva ${orig}/ap90/ap90.txt ap90_verb_filter_map.txt ap90_verb1_deva.txt
```

Filter (pattern codes C = class-pada 3,338 · D = denominative 286 · P =
pada-only 8, with hand-curated include/exclude overrides) → MW mapping →
final reports. Recorded results: **3,632 verbs** (1,740 prefixed / 1,822
non-prefixed / 70 unmatched `mw=?`; 2,987 same spelling as MW, 575 differ).

**AP57** ([ap57_verbs01/redo.sh](https://github.com/sanskrit-lexicon/AP90/blob/master/ap57_verbs01/redo.sh))
is the **self-contained** variant: it *does* run `mwverb.py` + `mwverbs1.py`
locally (against sibling `mw.txt`), works from a local `temp_ap57.txt`
snapshot, adds pattern codes `€` (2,979 — AP57's literal euro-sign class-pada
sigil), `T` (' To ' English-definition verbs, 286) and `X` (include-list,
123), and ends with the unique `compare_filter_map.py` →
`ap57_ap90_compare.txt`: the AP57↔AP90 verb diff (**8 verbs only in AP90,
300 only in AP57**). Recorded results: **3,978 verbs** (1,926 / 1,954 / 98
unmatched).

## Walkthrough 4 — transcoding & data ingests

- **[apte_s2h/](https://github.com/sanskrit-lexicon/AP90/tree/master/apte_s2h)**
  (re-runnable, live-verified): `python transcode.py slp1 deva
  apte_s2h_works.txt apte_s2h_works_deva.txt` and `slp1 roman` for IAST —
  202 works each. Traps: period renders as lāghava-cihna `॰` (not daṇḍa) in
  Devanagari; `<X>` spans stay untranscoded English; IAST output capitalizes
  name words. The README's Usage section documents the byte-identical
  verification run.
- **[andhrabharati/](https://github.com/sanskrit-lexicon/AP90/tree/master/andhrabharati)**
  (data-only): AB's re-coded AP90 (`ap90ab.txt`, `ap90ab_v2.txt`) plus
  normalized abbreviation lists (`{X}` = normal abbrevs, `<X>` = literary
  sources). `ap90ab_v2_suggest.txt` is a still-open `* TODO` punch-list of
  abbreviation normalizations.
- **[compounds/AB_AP57/](https://github.com/sanskrit-lexicon/AP90/tree/master/compounds/AB_AP57)**:
  `deva_slp1.py deva slp1 AP57entries.txt AP57entries_slp1.txt` →
  `parseprep.py` (85,168 → 82,383 lines) → `parse.py` → `ap57b.txt` +
  pointer file: 36,589 entries, 4,365 with compounds, **37,649 compounds**.
  (Its readme says `AB57entries.txt`; the real file is `AP57entries.txt`.)

## Walkthrough 5 — the two open issue campaigns

**[issues/issue26/](https://github.com/sanskrit-lexicon/AP90/tree/master/issues/issue26)
(Scott's corrections, hard, open).** Four parts so far: (1) hand-edited
correction form → `diff_to_changes_dict.py` → `change_1.txt` (432), cases
bucketed into `case_*.txt`; (2) `LBdash.py` — the `({#--X#})` → `{#--(X)#}`
line-break defect, `change_2.txt` (1,790); (3) `althw_1.py` — 701
comma-separated alternate headwords promoted to real `<L>` entries (32,176 →
32,877); (4) `redo_4.sh`: census → `althw_2_prep.py` → `althw_2.py` → census
diff — **1,961 more alt-headword entries** (→ 34,838), powered by the
1,971-line hand-built dictionary `althw_2_man_1.py`, plus the `althw_2fix`
pass (2 print-changes). Known folder defects: `readme_althw_2.txt` has a
duplicated-argument command typo; Part 4's commit message says "althw_1";
several print-change debates spun off as issues
[#27](https://github.com/sanskrit-lexicon/AP90/issues/27)/[#28](https://github.com/sanskrit-lexicon/AP90/issues/28).

**[issues/issue29/](https://github.com/sanskrit-lexicon/AP90/tree/master/issues/issue29)
(link targets, open).** `lsextract_all.py` inventories `<ls>` refs for `ap`
and `ap90` against their csl-pywork tooltips; `lsdump_all.py` dumps the 330
tooltip contexts; `link_target_work_ap90.txt` (seeded from AP's issue19 list)
tracks **13 activated targets**. Delivery edits `basicadjust.php` in BOTH
csl-websanlexicon and csl-apidev; `redo_new.sh` intentionally restores the
websanlexicon copy but leaves csl-apidev revised (it echoes a WARNING to that
effect). **Still TODO:** the cologne install and the csl-lslink sqlite build
(`sh redo_one_xampp.sh ap90` → 18,741 links) — and `redo_new.sh` is an
un-repointed copy of AP's version (`cd .../AP/issues/issue29`, regenerates
dict `ap` not `ap90`). Fix those before trusting a run.

## Symptom → cause → cure

| Symptom | Cause | Cure |
|---|---|---|
| `verbs01`: `mwverb.py: No such file` | Running the documented 5-command block — those scripts exist only in `ap57_verbs01/` | Use the real 4-command `redo.sh`; ensure the sibling MWS checkout provides `mwverbs/mwverbs1.txt` |
| `verbs01/redo.sh`: csl-orig not found | It assumes the two-root `../../../cologne/csl-orig/v02` layout | Remap or symlink; other workspaces use different conventions (see Environment) |
| `updateByLine.py`: old-text mismatch | Wrong base snapshot — campaigns are commit-pinned and chained | Re-extract with `git show <the folder's recorded hash>:v02/ap90/ap90.txt` |
| A markup campaign "finds nothing" on current ap90.txt | It already landed (abls installed `19c7ee9c`, abls1 `37f98f8b`) | Expected; reproduce against the pinned start commit only |
| `redo_new.sh` (issue29) regenerates the wrong dictionary | It's an unre-pointed copy of AP's issue19 script (`ap`, and a `cd` into the AP repo) | Edit the `cd` and dict code to `ap90` first — flagged as an open defect |
| csl-apidev shows uncommitted `basicadjust.php` changes after issue29 work | `redo_new.sh` deliberately leaves it revised (prints a WARNING) | Intentional: that copy is the delivery; commit or discard consciously — see the fork-sync check skill |
| Devanagari output shows daṇḍa where the print has an abbreviation dot | Wrong transcode of the period | `apte_s2h/transcode.py` maps `.` → lāghava-cihna `॰` by design; check `<X>` English spans too |
| `€` in AP57 verb patterns looks like mojibake | It's a literal sigil AP57's digitization uses for class-pada verb forms (2,979 hits) | Leave it; it is load-bearing in `ap57_verb_filter.py` |
| Hyphen-fix output looks wrong for some English words | ~3,000 resolutions are flagged `type=false` (fail spell-check) in `hyphen_changes.txt` | That column is the review queue; the 97 `hyphen_questions.txt` cases are still open |
| You can't find round-2 change files 1–5 | `abls1` numbering continues Round 1's `ap90_0..5` | change6…change15 are the complete Round-2 set |
| Reproducing `changes0b.txt` per the hyphen_deva readme fails | Readme spells it `changes_0b.txt`; the script writes `changes0b.txt` | Trust the `redo.sh` spelling |

## Glossary

| Term | Meaning here |
|---|---|
| AP90 / AP57 | Apte's *Sanskrit-English Dictionary*, 1890 edition (code `ap90`) vs the revised 1957–59 edition (code `ap`, worked in the sibling [AP](https://github.com/sanskrit-lexicon/AP) repo; `ap57` snapshots here) |
| `<ab>` / `<ls>` | abbreviation / literary-source citation tags — the objects of the abls rounds and issue29's link targets |
| abbrauth | the merged abbreviation+author control list (`abbrauth_1.txt`, 269 rows) driving prep1–prep3 |
| lbinfo | `<lbinfo n=.../>` markers hyphen passes insert to preserve original line-break info |
| reversibility proof | each hyphen stage's `restore*.py` must diff back to its input with 0 lines — the campaign's safety property |
| pattern codes | verb-filter classes: C class-pada, D denominative, P pada-only (+ AP57's `€`, `T`, `X`) |
| lāghava-cihna | `॰` (U+0970), the Devanagari abbreviation sign the transcoder uses for `.` |
| AB / AndhraBharati | the independent re-digitization ingested in `andhrabharati/` |
| link target | a clickable `<ls>` → scanned-page mapping; 13 activated for AP90 so far (issue29) |
| commit-hash chaining | each campaign starts from the csl-orig commit the previous one installed — the repo's real ordering key |

## Maintainer appendix

### Invariants

1. **Campaigns are commit-pinned and chained** — every folder's readme records
   its start and install hashes; the chain order is hyphen_deva → abls →
   abls1.
2. **Generator ≠ applier** — change files are always produced by one script
   and applied by `updateByLine.py`; never fold the two together.
3. **Hyphen passes are reversible** — a `restore*.py` diff-to-zero accompanies
   every stage; new hyphen work must keep the proof.
4. **Entry-count checkpoints** for issue26's alt-headword promotion:
   32,176 → 32,877 (althw_1) → 34,838 (althw_2).
5. **apte_s2h is deterministic** — re-running reproduces the committed outputs
   byte-identically (verified 05-07-2026).

### Known traps and observed defects

1. **CLAUDE.md's two idealized step lists** (abls "8 steps", verbs01 "5
   commands") don't match the real `redo.sh` files — corrected above; fixing
   CLAUDE.md is metadoc backlog #2.
2. **issue29's `redo_new.sh` is un-repointed** (targets `ap`, `cd`s into the
   AP repo) and its cologne/csl-lslink delivery is TODO.
3. **issue26 folder defects**: duplicated argument in `readme_althw_2.txt`'s
   command, wrong commit message on Part 4, one benign ERROR line
   (kuraMgamaH) in althw_1's run.
4. **`ap57_90_ls` changes are deliberately absent from csl-corrections'
   printchange ledger** — a documented provenance gap, not an oversight.
5. **`andhrabharati/ap90ab_v2_suggest.txt`** is an unapplied TODO punch-list
   of abbreviation normalizations — open work, easy to miss.
6. **Vendored engine copies** (`updateByLine.py` ×4, `transcoder.py` ×4) are
   frozen per folder; fix forward in the newest copy.
7. **Stray committed artifact**: `apte_s2h/__pycache__/…​.pyc`.
8. **`redo.sh` stale echo** in abls (says `ap90_4.txt`, writes `ap90_5.txt`)
   and the hyphen_deva readme's `changes_0b.txt` misspelling — cosmetic, but
   they cost a newcomer real time.

Improvement backlog, provenance and revision history live in the companion
metadoc:
[docs/PIPELINE_MANUAL.meta.md](https://github.com/sanskrit-lexicon/AP90/blob/master/docs/PIPELINE_MANUAL.meta.md).

_Dr. Mārcis Gasūns_
