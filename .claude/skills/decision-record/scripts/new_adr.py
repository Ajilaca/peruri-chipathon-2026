#!/usr/bin/env python3
"""Create the next numbered decision record in docs/decisions/adr/.

  new_adr.py "Title" [--status proposed|accepted] [--decided-by "names"] [--dir docs/decisions/adr]
  new_adr.py --selftest

An ADR may be `accepted` only with --decided-by (a human decision). Everything else is
`proposed`. This script never edits existing records.
"""
import argparse, datetime, os, re, sys, tempfile, unicodedata

TEMPLATE = """# ADR {num}: {title}

- Status: {status}
- Date: {date}
- Decided by: {decided}

## Context
<!-- Why is a decision needed? What constraints apply (CLAUDE.md, proposal, hardware)? -->

## Options considered
<!-- At least two, with the cost of each. Cite evidence paths or references. -->

## Decision
<!-- What was chosen. Only fill this in from what the team actually said. -->

## Consequences
<!-- What becomes easier or harder. What must be re-checked (claims, proposal text, measurements). -->

## Evidence
<!-- evidence/... paths or numbered proposal references. Label estimates as ESTIMATE. -->
"""


def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s[:60] or "decision"


def next_number(d):
    nums = [int(m.group(1)) for f in os.listdir(d) if (m := re.match(r"^(?:ADR-)?(\d{4})-", f))]
    return max(nums, default=0) + 1


def create(title, status, decided_by, d):
    if status == "accepted" and not decided_by:
        raise SystemExit("refused: 'accepted' needs --decided-by (a human team decision). Use 'proposed'.")
    os.makedirs(d, exist_ok=True)
    num = f"{next_number(d):04d}"
    path = os.path.join(d, f"ADR-{num}-{slugify(title)}.md")
    text = TEMPLATE.format(num=num, title=title, status=status.capitalize(),
                           date=datetime.date.today().isoformat(),
                           decided=decided_by or "pending team decision")
    with open(path, "x", encoding="utf-8") as f:
        f.write(text)
    return path


def selftest():
    with tempfile.TemporaryDirectory() as d:
        p1 = create("Choose DMA vs register I/O", "proposed", None, d)
        p2 = create("Reader-side or card-side accelerator?", "proposed", None, d)
        assert os.path.basename(p1).startswith("ADR-0001-") and os.path.basename(p2).startswith("ADR-0002-"), (p1, p2)
        try:
            create("x", "accepted", None, d); raise AssertionError("accepted without decider must be refused")
        except SystemExit as e:
            assert "refused" in str(e)
        p3 = create("Accepted example", "accepted", "team J5", d)
        assert "Decided by: team J5" in open(p3).read()
        assert slugify("Ünïcode & spaces!!") == "unicode-spaces"
    print("selftest OK (new_adr.py)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("title", nargs="?")
    ap.add_argument("--status", choices=["proposed", "accepted"], default="proposed")
    ap.add_argument("--decided-by")
    ap.add_argument("--dir", default="docs/decisions/adr")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.title:
        ap.error("title is required")
    print(create(a.title, a.status, a.decided_by, a.dir))


if __name__ == "__main__":
    sys.exit(main())
