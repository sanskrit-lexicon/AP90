### Location

Counterpart of https://github.com/sanskrit-lexicon/PWG/issues/175 (PWG) and https://github.com/sanskrit-lexicon/PWK/issues/113 (PWK) for `ap90.txt`.

I ran the same two-job recipe over `csl-orig/v02/ap90/ap90.txt`: auto-fix the few things with a single safe resolution; audit everything else with line refs. Added `08_markup_fix.py` plus outputs to a new `issues/markup_fix/` folder on the branch `markup-fix-audit`.

@funderburkjim @Andhrabharati — would value a look at the 5 `<ls n="…"></ls>` empty-body entries and the 499 within-line adjacent `</ab> <ab>` cases.

## Markup fixer + audit for `ap90.txt`

### What it auto-fixes

| Pattern | Result |
|---|---|
| `<ab><ab>N.</ab> of town</ab>` | `<ab>N. of town</ab>` |
| `<ls>K. 1. 2. </ls>` | `<ls>K. 1. 2.</ls>` |
| `<ab> m. </ab>` | `<ab>m.</ab>` |

Whitespace trimming applies to the 2 paired tags in `ap90.txt`: `<ab>` and `<ls>`. Output goes to `ap90_fixed.txt`; change log in `markup_fix_changes.txt`.

### Closing-tag inventory in current `ap90.txt`

| Tag | Count |
|---|---:|
| `</ab>` | 46,066 |
| `</ls>` | 43,892 |

No self-closing tags. Both tags balanced. `<lbinfo>` (47,034 occurrences) is a self-opening structural tag, not a paired tag.

### What it found in current `ap90.txt`

- **0** nested `<ab>` — clean.
- **1** whitespace trim — applied: trailing space removed from one `<ls>` tag.
- **5** `<ab n="…">` attributes with non-standard values ("Page", "Purāṇa", "Dhātupāṭha", "Hindi", "South(ern) Marāṭhā (Mahārāṣṭra)") — audit only.
- **5** `<ls n="…"></ls>` empty-body entries — these are an **intentional structural pattern**: `<ls n="R. 11."></ls> <lbinfo n="ls:3.+53"/>` encodes line-break information. Not a markup bug, but worth confirming the pattern is well-formed.
- **0** nested `<ls>` — clean. (288 `{{old → new || …}}` correction records present.)
- **0** boundary collisions.
- **499** within-line adjacent `</ab> <ab>` — listed in `markup_audit.txt` for verification (526 total including cross-line). Spot checks show mostly intentional pairs.

### Broader cleanup checklist (in `markup_audit.txt`)

1. **Adjacent `</ab> <ab>`** (499 within-line) — verify each pair is intentional.
2. **`<ab n="…">` non-standard values** (5 occurrences) — confirm or standardise.
3. **`<ls n="…"></ls>` empty body** (5 occurrences) — confirm the `<lbinfo>` line-break pattern is consistent across the file.
4. **Nested `<ab>` / `<ls>` guards** — 0; retained for re-run safety.

### Usage

```
cd issues/markup_fix
python 08_markup_fix.py                        # uses csl-orig/v02/ap90/ap90.txt by default
python 08_markup_fix.py IN.txt OUT.txt         # custom paths
```

### Summary

`ap90.txt` uses 2 paired tag types, both balanced. One auto-fix applied (trailing space in `<ls>`). Non-trivial findings: 499 within-line adjacent `</ab> <ab>` pairs, 5 non-standard `<ab n="…">` values, and 5 empty `<ls n="…"></ls>` entries (intentional line-break pattern). Zero boundary collisions and zero nested tags.

### Severity

`minor`
