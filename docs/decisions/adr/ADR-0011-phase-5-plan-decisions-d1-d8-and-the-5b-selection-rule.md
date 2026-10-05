# ADR 0011: Phase 5 plan decisions D1-D8 and the 5b selection rule

- Status: Accepted
- Date: 2026-10-01
- Decided by: Faza Dzil, Team J5 (session 2026-10-01: "terima semua saran")

## Context
The Phase 5 test plan (`evidence/phase05/test_plan.md`, CRG-4) listed eight open questions (§13, D1–D8)
with a suggestion for each, and a proposed selection rule for sub-step 5b (§11) that must be fixed before any 5b
revision is compiled (as with ADR 0004 / ADR 0007). Phase 5's timing objective is ADR 0010. Starting point: C3-P6
(ADR 0009), MEASURED in `evidence/phase04/quartus_C3-P6.md` and
`evidence/phase05/baseline/c3p6_critical_path.md`.

## Options considered
For each item, the options are those of test plan §13 and §3; the suggestion was accepted in every case.

## Decision
| # | Decision |
|---|---|
| D1 | Every Phase 5 Quartus revision (C4a–C4d) uses `create_clock -period 40.000` on `clk_i`, as C3-P6. At the end, the final C4 configuration and C3-P6 are each compiled once more at 20.000 ns; those two results are information, not a gate (ADR 0010). |
| D2 | The NTT-core budget stays 12,573 ALM (ADR 0009). Compiles use Quartus defaults as in Phase 4 (comparable with C3-P6); a GHRD-settings compile of the final C4 is optional. DSP use is reported; no DSP limit is set. |
| D3 | Whether 5c and 5d are attempted is decided after the 5a / 5b results; the test plan keeps both plans (5c formal bound proof; 5d as a standalone unit, because `base_case_multiply.sv` is not part of C3-P6). |
| D4 | Reading (ii) of 5a: a q-specific fold reducer using q = 2^11 + 2^10 + 2^8 + 1 (2^12 ≡ 767 mod q, shift-and-add only, then a fixed number of conditional subtractions). 5b = Barrett and Montgomery, in both of which the multiplication by q is shift-and-add. |
| D5 | In Phase 5 no register moves between the memory path and the multiplier path; the multiplier path keeps exactly 3 registers (P = 6, cycles 119 / 375 unchanged). Exact positions inside each new reducer are written into the test plan before its compile. |
| D6 | Operand contract: a new reducer must equal (a·b) mod q for all a, b in [0, q) (exhaustive); behaviour for 12-bit operands ≥ q is measured and reported, not required. |
| D7 | Default fitter seed for every revision; seeds 1–6 for the two 5b candidates. |
| D8 | The 5b selection rule below. |

5b selection rule (D8).
1. Both candidates (Barrett, Montgomery) are built, verified and compiled at seeds 1–6 before the rule is applied.
2. A candidate qualifies only if all hold: correct per test plan §7 (both simulators, exhaustive reducer test,
   negative controls); NTT / INTT cycles exactly 119 / 375; ALM ≤ 12,573 (fitter "ALMs needed"); timing met at
   40.000 ns (non-negative setup and hold at every reported corner). Applied per seed; a candidate is a qualifier
   if it qualifies at every seed.
3. Metric: Fmax(c) = median over seeds 1–6 of the lowest slow-corner Fmax (values as printed). Cycles are equal by
   condition 2, so time per NTT is proportional to 1 / Fmax.
4. The higher Fmax wins, unless the other qualifier is within 5% of it (near tie). In a near tie the qualifier with
   the lower median ALM wins. If the medians of ALM also differ by less than 32 ALM (C3-P6 seed spread), the team
   decides; suggested tie-break Barrett (no Montgomery-form tables).
5. If no candidate qualifies, nothing is selected automatically; results are reported and the team decides.
6. The result of the rule is recorded in a separate ADR (the "choice by ADR" of the roadmap).

Stated before measuring (INFERENCE from the baseline path analysis): Fmax is likely to tie because the critical path
lies in the memory read path; the rule then reduces to ALM.

## Consequences
- The test plan is final with these answers (its §13 records them); Phase 5 RTL may start with 5a.
- Four Quartus revisions at the default seed (C4a, C4c, C4d, BCM-ref as applicable) plus 12 for 5b (seeds 1–6 × 2),
  plus 2 informational compiles at 20.000 ns; one at a time.
- Moving registers between memory and multiplier paths, P changes and stalls belong to the separate phase of
  ADR 0010 (rules in ADR 0012).

## Evidence
- `evidence/phase05/test_plan.md` (§3, §5, §7, §9, §11, §13)
- `evidence/phase05/baseline/c3p6_critical_path.md`
- `evidence/phase04/seed_sweep.md` (32-ALM seed spread of C3-P6)
- `docs/decisions/0006-*.md`, `0007-*.md`, `0009-*.md`, `0010-*.md`
