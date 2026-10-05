# ADR 0015: Phase 5d Karatsuba-style base case not attempted in Phase 5; move to Phase 6

- Status: Accepted
- Date: 2026-10-01
- Decided by: Jevan, Team J5 (chat 2026-10-02, answered the three ADR questions)

## Context
- ROADMAP Phase 5 lists 5d (optional): Karatsuba-style base-case multiplication, 4 modular multiplications instead of 5.
  ADR 0011 D3 left the attempt open until after 5a / 5b; the S3 instruction asks for a proposal only.
- Finding recorded in the test plan (`evidence/phase05/test_plan.md`, 5d): `rtl/ntt/base_case_multiply.sv` is
  **not part of the C3-P6 / C4 NTT core**. No core instantiates it; the C3 core does NTT / INTT only, so 5d cannot
  change the kernel that Phase 5 measures (the pointwise base-case product belongs to a later datapath).
- Phase 5 acceptance (ADR 0010, 0012) is judged on the NTT core: t_NTT and t_INTT at measured Fmax, ALM <= 12,573.
  A 5d unit changes neither of those quantities. The multiplier DSP count is a separate budget item (ADR 0013 records
  DSP 9 -> 18 for Barrett).
- The ROADMAP places Karatsuba-type work with the Phase 6 arithmetic items (pointwise multiplication in the full
  datapath).

## Options considered
(a) **Not attempted in Phase 5; moved to Phase 6** (where the base-case multiplier is part of a datapath that can be
    measured end to end). Cost: the C4 ablation row for 5d stays "not attempted" (allowed by the test plan:
    "or 'not attempted'"). No Phase 5 effort spent on a unit outside the measured core.
(b) Attempt now as a standalone unit `C4d` against a standalone compile of the frozen `base_case_multiply.sv`
    (`BCM-ref`), as the test plan describes. Cost: a new RTL unit, an exhaustive or bounded proof over
    (a0, a1, b0, b1, gamma), two extra Quartus compiles (seeds as the team decides); the result would be a standalone
    DSP / ALM comparison with no effect on t_NTT, t_INTT or the Phase 5 gate.

## Decision
Option (a) accepted 2026-10-02 by Jevan, Team J5: 5d is not attempted in Phase 5 and moves to Phase 6.

## Consequences
- If (a): C4 matrix row 5d = "not attempted in Phase 5 (ADR 0015)"; `phase05.md` states this; the Phase 6 plan
  carries the item (the team decides its position there).
- If (b): a test-plan section for `C4d` is executed with its own adoption rule fixed before measuring.
- The mathematics (C1) is untouched either way.

## Evidence
- `evidence/phase05/test_plan.md` (5d paragraph, sections on `C4d` / `BCM-ref`)
- `docs/decisions/adr/ADR-0011-phase-5-plan-decisions-d1-d8-and-the-5b-selection-rule.md` (D3)
- `docs/ROADMAP.md` (Phase 5 sub-steps)
