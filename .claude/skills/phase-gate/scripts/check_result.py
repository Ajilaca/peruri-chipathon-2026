#!/usr/bin/env python3
"""Validate a phase result artifact (docs/results/result_phase<N>.md).

  check_result.py docs/results/result_phase0.md [--root .]
  check_result.py --selftest

Errors (exit 1): missing sections; a criterion status other than PASS/FAIL/MISSING; a PASS row
without an evidence item that exists (evidence = `path` in backticks, or `cmd: ...`); overall
Status DONE while any row is not PASS; DONE with placeholders left; DONE with an empty
Git commit. The approval checkbox is never ticked by this script or by Claude.
"""
import argparse, os, re, sys, tempfile

SECTIONS = ["Done-criteria", "What was produced", "Numbers", "Standards and sources pinned",
            "Coverage and limits", "Deviations, failures and open issues", "Decisions needed",
            "Claims made in this phase", "Reproduce", "Approval"]
STATUS_VALUES = {"DONE", "NOT DONE", "PARTIAL"}
ROW_VALUES = {"PASS", "FAIL", "MISSING"}
PLACEHOLDER = re.compile(r"<[^>\n]{2,}>|\bTODO\b|\bTBD\b|\.\.\.\]")


def headings(text):
    return [re.sub(r"^#+\s*\d*\.?\s*", "", l).strip() for l in text.splitlines() if l.startswith("#")]


def section_body(text, name):
    m = re.search(r"^#{1,3}\s*\d*\.?\s*" + re.escape(name) + r".*?$(.*?)(?=^#{1,3}\s|\Z)", text, re.M | re.S)
    return m.group(1) if m else ""


def table_rows(body):
    rows = []
    for l in body.splitlines():
        if l.strip().startswith("|") and not re.match(r"^\s*\|[\s:|-]+\|\s*$", l):
            cells = [c.strip() for c in l.strip().strip("|").split("|")]
            rows.append(cells)
    return rows[1:] if rows else []          # drop header row


def check(text, root):
    errs = []
    hs = headings(text)
    for s in SECTIONS:
        if not any(h.lower().startswith(s.lower()) for h in hs):
            errs.append(f"missing section: {s}")
    m = re.search(r"^- Status:\s*(.+?)\s*$", text, re.M)
    status = m.group(1).split("(")[0].strip().upper() if m else None
    if status not in STATUS_VALUES:
        errs.append(f"'- Status:' must be one of {sorted(STATUS_VALUES)} (found {status!r})")
    rows = table_rows(section_body(text, "Done-criteria"))
    if not rows:
        errs.append("Done-criteria table has no rows")
    all_pass = bool(rows)
    for r in rows:
        if len(r) < 4:
            errs.append(f"criterion row malformed: {r}"); all_pass = False; continue
        crit, evid, st = r[1], r[2], r[3].upper().strip("* ")
        if st not in ROW_VALUES:
            errs.append(f"criterion '{crit[:50]}': status must be PASS/FAIL/MISSING (found {st!r})"); all_pass = False; continue
        if st != "PASS":
            all_pass = False
            continue
        items = re.findall(r"`([^`]+)`", evid)
        if not items:
            errs.append(f"criterion '{crit[:50]}': PASS without evidence in backticks (path or `cmd: ...`)")
            continue
        for it in items:
            if it.startswith("cmd:"):
                continue
            if not os.path.exists(os.path.join(root, it)):
                errs.append(f"criterion '{crit[:50]}': evidence path does not exist: {it}")
    if status == "DONE":
        if not all_pass:
            errs.append("Status DONE but not every criterion is PASS")
        if PLACEHOLDER.search(text.replace("<!--", "").split("## 10")[0]):
            errs.append("Status DONE but placeholders (<...>, TODO, TBD) remain")
        gm = re.search(r"^- Git commit.*?:\s*(\S.*)$", text, re.M)
        if not gm or "<" in gm.group(1):
            errs.append("Status DONE but 'Git commit' is empty")
    if not re.search(r"^- \[[ xX]\] .*approv", text, re.M | re.I):
        errs.append("approval checkbox line missing (- [ ] Human approver ...)")
    return errs


GOOD = """# Result — Phase 0: Foundations
- Status: DONE
- Date (UTC): 2026-10-01
- Git commit (HEAD when verified): abc1234
## 1. Done-criteria
| # | Criterion | Evidence | Status |
|---|---|---|---|
| 1 | Params locked | `cmd: python3 check_params.py` | PASS |
| 2 | KAT | `docs/evidence/golden/kat.txt` | PASS |
## 2. What was produced
| path | purpose |
|---|---|
| tb/golden/params.py | constants |
## 3. Numbers
| quantity | value | label | evidence |
|---|---|---|---|
| KAT cases | 70 | MEASURED | `docs/evidence/golden/kat.txt` |
## 4. Standards and sources pinned
FIPS 203.
## 5. Coverage and limits
Sample vectors only.
## 6. Deviations, failures and open issues
None.
## 7. Decisions needed
None.
## 8. Claims made in this phase
None.
## 9. Reproduce
pytest
## 10. Approval
- [ ] Human approver (name, date): 
"""


def selftest():
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, "docs/evidence/golden"))
        open(os.path.join(d, "docs/evidence/golden/kat.txt"), "w").write("ok")
        assert check(GOOD, d) == [], check(GOOD, d)
        assert any("does not exist" in e for e in check(GOOD.replace("kat.txt`| PASS", "gone.txt` | PASS").replace("docs/evidence/golden/kat.txt` | PASS", "docs/evidence/golden/gone.txt` | PASS"), d))
        assert any("without evidence" in e for e in check(GOOD.replace("`docs/evidence/golden/kat.txt` | PASS", "we ran it | PASS"), d))
        assert any("not every criterion" in e for e in check(GOOD.replace("| PASS |\n## 2", "| MISSING |\n## 2"), d))
        assert any("placeholders" in e for e in check(GOOD.replace("Sample vectors only.", "TODO write this"), d))
        assert any("Git commit" in e for e in check(GOOD.replace("abc1234", "<sha>"), d))
        assert any("missing section" in e for e in check(GOOD.replace("## 8. Claims made in this phase", "## 8. Other"), d))
        assert any("approval checkbox" in e for e in check(GOOD.replace("- [ ] Human approver (name, date): ", "signed"), d))
        partial = GOOD.replace("Status: DONE", "Status: PARTIAL").replace("| PASS |\n## 2", "| MISSING |\n## 2")
        assert check(partial, d) == [], check(partial, d)      # PARTIAL with a MISSING row is honest, not an error
    print("selftest OK (check_result.py)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?")
    ap.add_argument("--root", default=".")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.file:
        ap.error("file required")
    if not os.path.exists(a.file):
        print(f"check_result: {a.file} not found"); return 2
    errs = check(open(a.file, encoding="utf-8").read(), a.root)
    for e in errs:
        print("ERROR:", e)
    print(f"\ncheck_result: {len(errs)} error(s)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
