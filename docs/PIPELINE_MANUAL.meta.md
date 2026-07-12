# PIPELINE_MANUAL.md — metadoc

_Created: 11-07-2026 · Last updated: 11-07-2026_

Companion record for
[docs/PIPELINE_MANUAL.md](https://github.com/sanskrit-lexicon/AP90/blob/master/docs/PIPELINE_MANUAL.md)
— purpose, provenance, improvement backlog and revision history of the manual
itself (not of the pipelines it documents).

## Purpose

Give a new operator/contributor a runnable understanding of AP90's pipeline
family — the markup rounds (abls/abls1), the hyphenation campaigns with their
reversibility proofs, the two verb pipelines (AP90 vs the self-contained
AP57 variant), the transcoding/ingest workspaces, and the two open issue
campaigns (#26 alt-headwords, #29 link targets) — **from the real `redo.sh`
files**, correcting the two idealized step lists in CLAUDE.md/README.

## Audience

- **Operators** re-running the verb pipelines or apte_s2h, or picking up the
  open issue26/issue29 work (cheat-sheet, walkthroughs 3/5, symptom table);
- **Maintainers** touching the markup/hyphen tooling (corrections section,
  appendix invariants + traps);
- **Historians** of the 2020-era markup/hyphenation chain (commit-hash
  chaining, walkthroughs 1–2).

## Provenance

- Authored 11-07-2026 by Fable 5 (`claude-fable-5`) executing handoff
  [H523-Fable_AP90_markup_verbs_pipeline_manual_10.07.26.md](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H523-Fable_AP90_markup_verbs_pipeline_manual_10.07.26.md)
  (manual-coverage census batch H501–H531).
- Modelled on the gold-standard operator manual
  [RussianRamayana Litpam-Indexator MANUAL.md](https://github.com/gasyoun/RussianRamayana/blob/main/Litpam-Indexator/docs/indesign-pipeline/MANUAL.md).
- Source material: the per-folder readmes and — decisively — the actual
  `redo*.sh` drivers across all 11 workspaces, surveyed by an Explore agent
  (Fable 5 `claude-fable-5` session, 11-07-2026) with first-hand reads of
  README/CLAUDE.md/issues. Two material doc-vs-code discrepancies found and
  corrected in the manual instead of propagated:
  1. `markup/abls/redo.sh` = 12 invocations (generator/applier separated),
     not CLAUDE.md's 8 steps;
  2. `verbs01/redo.sh` = 4 active commands with `mwverb.py`/`mwverbs1.py`
     absent from that folder (they live in `ap57_verbs01/`), `mwverbs1.txt`
     consumed from the sibling MWS repo, plus an undocumented Devanagari
     output.
- The apte_s2h byte-identical verification (05-07-2026) is inherited from the
  README's recorded run, not re-executed here.

## Ranked improvement backlog

| # | Item | Status |
|---|---|---|
| 1 | Re-point [issues/issue29/redo_new.sh](https://github.com/sanskrit-lexicon/AP90/blob/master/issues/issue29/redo_new.sh) to AP90 (it still `cd`s into the AP repo and regenerates dict `ap`) and finish the cologne + csl-lslink delivery TODOs | open |
| 2 | Fix [CLAUDE.md](https://github.com/sanskrit-lexicon/AP90/blob/master/CLAUDE.md)'s abls and verbs01 step lists to match the real `redo.sh` files, and point it at this manual | open |
| 3 | Triage [andhrabharati/ap90ab_v2_suggest.txt](https://github.com/sanskrit-lexicon/AP90/blob/master/andhrabharati/ap90ab_v2_suggest.txt) — the unapplied abbreviation-normalization TODO list (apply, or record won't-fix) | open |
| 4 | Live-verify the two re-runnable verb pipelines against current siblings and record fresh counts (apte_s2h already verified) | open |
| 5 | Work the review pools left by hyphen_eng: 97 open `hyphen_questions.txt` cases + the ~3,000 `type=false` spell-check flags | open |
| 6 | Clean cosmetic defects: abls `redo.sh` stale echo, hyphen_deva readme `changes_0b.txt` misspelling, issue26 readme duplicated-argument typo, committed `apte_s2h/__pycache__` | open |

## Known limitations

- **Transcription-verified, not re-executed** (except apte_s2h, inherited):
  the campaigns are commit-pinned, already landed, and mutate the sibling
  csl-orig tree. Backlog #4 upgrades the verb pipelines.
- issue26/issue29 are open campaigns — the manual describes their state as of
  11-07-2026; their folders' readmes remain the running logs.
- The three coexisting path conventions are remapped descriptively, not
  fixed; parameterization is upstream work in each folder.

## Related documents

- [README.md](https://github.com/sanskrit-lexicon/AP90/blob/master/README.md) — repo overview + the verified apte_s2h usage example
- [CLAUDE.md](https://github.com/sanskrit-lexicon/AP90/blob/master/CLAUDE.md) — code contract (with the two idealized lists this manual corrects)
- [DATA_DICTIONARY.md](https://github.com/sanskrit-lexicon/AP90/blob/master/DATA_DICTIONARY.md) — minimal tag table
- [csl-corrections correction workflow](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md) — the canonical delivery procedure
- Sibling census-batch manuals: [AP](https://github.com/sanskrit-lexicon/AP/blob/main/docs/PIPELINE_MANUAL.md) · [PWK](https://github.com/sanskrit-lexicon/PWK/blob/main/docs/PIPELINE_MANUAL.md) · [AMAR](https://github.com/sanskrit-lexicon/AMAR/blob/main/docs/CONVERSION_MANUAL.md)

## Revision history

| Date | Change | By |
|---|---|---|
| 11-07-2026 | Initial manual + this metadoc authored (H523); 11 workspaces surveyed (1 Explore agent + first-hand README/CLAUDE/issue reads); 2 doc-vs-code discrepancies corrected, 8 traps recorded | Fable 5 (`claude-fable-5`) |

_Dr. Mārcis Gasūns_
