"""
Markup fixer + audit for ap90.txt (AP90).
Counterpart of PWG#175, PWK#113, and siblings.

AP90-specific notes:
  - Only 2 paired tag types: <ab> (46,066) and <ls> (43,892). Both balanced.
  - 1 trailing-space hit in <ls>.
  - 526 adjacent </ab> <ab> — mostly intentional, for review.
  - 5 <ab n="…"> with non-standard values ("Page", "Purāṇa", "Dhātupāṭha",
    "Hindi", "South(ern) Marāṭhā (Mahārāṣṭra)") — audit only.
  - 288 {{old -> new || …}} correction records present.
  - <lbinfo> is a self-opening structural tag (34,882), not a paired tag.

Inputs:
  ../../../csl-orig/v02/ap90/ap90.txt   (when run from ap90issues/markup_fix/)
  or argv[1] (any path)
Outputs: ap90_fixed.txt, markup_fix_changes.txt, markup_audit.txt
"""

import sys, re
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
if len(sys.argv) >= 3:
    PW_TXT, OUT_FIX = Path(sys.argv[1]), Path(sys.argv[2])
else:
    candidates = [HERE.parent.parent.parent / "csl-orig" / "v02" / "ap90" / "ap90.txt", HERE / "ap90.txt"]
    PW_TXT = next((p for p in candidates if p.exists()), candidates[0])
    OUT_FIX = HERE / "ap90_fixed.txt"
OUT_LOG, OUT_AUDIT = HERE / "markup_fix_changes.txt", HERE / "markup_audit.txt"

NEST_RX = re.compile(r"<ab(?P<oa>\b[^>]*)>(?P<pre>[^<]*)<ab(?P<ia>\b[^>]*)>(?P<inner>[^<]*)</ab>(?P<post>[^<]*)</ab>")

def fix_nested_ab(line):
    n = 0
    while True:
        m = NEST_RX.search(line)
        if not m: return line, n
        line = line[:m.start()] + f"<ab{m.group('oa')}>{m.group('pre')}{m.group('inner')}{m.group('post')}</ab>" + line[m.end():]
        n += 1

TRIM_TAGS = ["ab", "ls"]

def fix_trim_whitespace(line):
    n = 0
    for tag in TRIM_TAGS:
        p1 = re.compile(rf"(<{tag}\b[^>]*>)(\s+)([^<]*?)(\s*)(</{tag}>)")
        def _r1(m):
            nonlocal n
            inside = m.group(3).rstrip()
            if inside != m.group(2)+m.group(3)+m.group(4): n += 1
            return f"{m.group(1)}{inside}{m.group(5)}"
        line = p1.sub(_r1, line)
        p2 = re.compile(rf"(<{tag}\b[^>]*>)([^<]*?)(\s+)(</{tag}>)")
        def _r2(m):
            nonlocal n
            inside = m.group(2).rstrip(); n += 1
            return f"{m.group(1)}{inside}{m.group(4)}"
        line = p2.sub(_r2, line)
    return line, n

def _ls_nested_classify(line):
    inside, outside = [], []
    for m in re.finditer(r"<ls\b[^>]*>([^<]*<ls\b[^>]*>)", line):
        io = m.group(1).find("<ls"); ip = m.start(1)+(io if io>=0 else 0)
        pfx = line[:ip]
        (inside if pfx.rfind("{{") > pfx.rfind("}}") else outside).append(m)
    return outside, inside

AUDIT_CHECKS = [
    ("Adjacent </ab> <ab> — possibly intentional", re.compile(r"</ab>\s*<ab")),
    ("Nested <ls> outside a {{ … }} correction record", None),
    ("Nested <ls> INSIDE a {{ … }} correction record (informational)", None),
    ("<ab n=\"?\"> placeholder", re.compile(r'<ab\s+n="\?+">')),
    ("<ab n=\"\"> empty attribute", re.compile(r'<ab\s+n="">')),
    ("<ab n=\"…\"> non-standard expansion value", re.compile(r'<ab\s+n="(?!")[^"]{2,}">')),
    ("Empty content tag", re.compile(r"<(ls|ab)\b[^>]*></\1>")),
    ("{#…#} brace immediately followed by <ab>/<ls>", re.compile(r"#\}<(?:ab|ls)\b")),
    ("Malformed tag with unescaped <", re.compile(r'<[A-Za-z][A-Za-z0-9]*\s+[A-Za-z]+="[^"]*<[^"]*"\s*[^>]*>')),
]

def main():
    print(f"Reading {PW_TXT} …", flush=True)
    lines = PW_TXT.read_text(encoding="utf-8").splitlines()
    print(f"  {len(lines):,} lines", flush=True)
    out_lines, fix_log, tot_nested, tot_trim = [], [], 0, 0
    audit_hits = {label: [] for label, _ in AUDIT_CHECKS}
    for lineno, line in enumerate(lines, 1):
        orig = line
        line, n1 = fix_nested_ab(line); line, n2 = fix_trim_whitespace(line)
        tot_nested += n1; tot_trim += n2
        if line != orig: fix_log.append((lineno, orig, line))
        out_lines.append(line)
        outside_hits, inside_hits = _ls_nested_classify(orig)
        for m in outside_hits:
            s,e = max(0,m.start()-40), min(len(orig),m.end()+40)
            audit_hits["Nested <ls> outside a {{ … }} correction record"].append((lineno, orig[s:e].replace("\t"," ")))
        for m in inside_hits:
            s,e = max(0,m.start()-40), min(len(orig),m.end()+40)
            audit_hits["Nested <ls> INSIDE a {{ … }} correction record (informational)"].append((lineno, orig[s:e].replace("\t"," ")))
        for label, pat in AUDIT_CHECKS:
            if pat is None: continue
            for m in pat.finditer(orig):
                s,e = max(0,m.start()-40), min(len(orig),m.end()+40)
                audit_hits[label].append((lineno, orig[s:e].replace("\t"," ")))
                if len(audit_hits[label]) >= 5000: break
        if lineno % 100000 == 0: print(f"  {lineno:,}/{len(lines):,}", flush=True)
    print(f"nested <ab>: {tot_nested}  whitespace: {tot_trim}  changed: {len(fix_log)}", flush=True)
    with OUT_FIX.open("w", encoding="utf-8", newline="\n") as f:
        for line in out_lines: f.write(line+"\n")
    with OUT_LOG.open("w", encoding="utf-8") as f:
        f.write(f"; markup_fix log for ap90.txt\n; nested <ab>: {tot_nested}\n; whitespace: {tot_trim}\n; changed: {len(fix_log)}\n;\n")
        for ln,old,new in fix_log: f.write(f"{ln} old {old}\n{ln} new {new}\n")
    with OUT_AUDIT.open("w", encoding="utf-8") as f:
        f.write("AP90 markup audit — findings requiring a human decision\n" + "="*60 + "\n\n")
        f.write("Generated by 08_markup_fix.py against ap90.txt.\n")
        f.write("Only 2 paired tag types: <ab> and <ls>. Both balanced.\n\n")
        f.write("WHAT THIS FIXER AUTO-CORRECTS\n" + "-"*44 + "\n")
        f.write("  - Nested <ab> (guard for future overlay passes)\n")
        f.write("  - Whitespace inside <ab> and <ls>\n\n")
        f.write("WHAT NEEDS HUMAN ATTENTION\n" + "-"*44 + "\n")
        f.write("  1. Adjacent </ab> <ab> — 526 within-line cases; verify intentional.\n")
        f.write("  2. <ab n=\"…\"> non-standard values (5 occurrences): \"Page\", \"Purāṇa\",\n")
        f.write("     \"Dhātupāṭha\", \"Hindi\", \"South(ern) Marāṭhā (Mahārāṣṭra)\".\n")
        f.write("  3. 288 correction records present; nested tags inside are format.\n\n")
        f.write("AUTOMATED CHECKS BELOW\n" + "-"*44 + "\n\n")
        for label, _ in AUDIT_CHECKS:
            hits = audit_hits[label]
            f.write(f"## {label}\n   matches: {len(hits)} (showing up to 200)\n")
            for ln, snippet in hits[:200]: f.write(f"   L{ln}: {snippet}\n")
            f.write("\n")
    print("DONE", flush=True)

if __name__ == "__main__":
    main()
