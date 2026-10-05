# Phase result artifacts

One file per finished phase: `phase<NN>.md` (NN follows `docs/ROADMAP.md`; `phase05m` and `phase9m` for the sub-phases), made from
`TEMPLATE.md`. It is the single page a reviewer reads to decide "is this phase really done?".

- Facts only, from files in this repository. `PASS` needs evidence that exists.
- `python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase<NN>.md` must report 0 errors
  before you ask for approval.
- The approval box is ticked by a human. Not by Claude, not by a script.
- A phase that is honestly `PARTIAL` is fine; a `DONE` with missing evidence is not.
