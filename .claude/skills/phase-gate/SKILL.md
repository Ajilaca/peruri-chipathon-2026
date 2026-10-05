---
name: phase-gate
description: Check whether a roadmap phase is really finished (evidence exists for every done-criterion in docs/ROADMAP.md) before starting the next one, and report status honestly. Use when the user says a phase is done, asks "what is next", "are we ready for phase N", "status", or before starting RTL for a new block.
---

# phase-gate

Phases 0-5 are mandatory and sequential; Phase 6 is optional and only starts after Phase 5
is verified. A phase is **done** only when every done-criterion in `docs/ROADMAP.md` has
evidence a reviewer could open.

## Procedure

1. Read `docs/ROADMAP.md` and locate the phase (default: the lowest phase not yet done).
2. For each done-criterion, find its evidence (a path under `evidence/`, a passing test
   run you execute now, or a decision record). Run checks fresh; do not trust old output.
3. Report a table: `criterion | evidence path or command | PASS / FAIL / MISSING`.
   - No evidence = MISSING, never PASS.
   - A simulation-only result is labelled *simulation only*; it is not hardware validation.
4. If everything passes, **stop and ask the team to approve** the next phase. Do not start
   it on your own, and do not run `/rtl-agent-team:rat-auto-design` end to end.
5. If something fails, say what, why, and the smallest next step. Do not weaken a test,
   tolerance, or assertion to turn a row green.
6. Update the status line at the top of `docs/ROADMAP.md` only to reflect what you just
   verified, with the date and the evidence path.
7. **Result artifact.** When a phase is finished (or the user asks), create
   `docs/results/phase<NN>.md` from `docs/results/TEMPLATE.md` (N follows the
   roadmap, 0-6). Fill it only from evidence. Overall Status is DONE only if every criterion is PASS;
   otherwise PARTIAL or NOT DONE. Then validate:

   ```bash
   python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase<NN>.md
   ```

   Fix until 0 errors (never by editing the checker). **Leave the Approval box unticked**: a team member
   ticks it after reading the evidence.

## Also check at every gate

- `python3 .claude/skills/mlkem-guard/scripts/check_params.py` (locked parameters)
- `python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/proposal README.md`
- `docs/decisions/PENDING.md`: is a pending decision blocking the next phase?
