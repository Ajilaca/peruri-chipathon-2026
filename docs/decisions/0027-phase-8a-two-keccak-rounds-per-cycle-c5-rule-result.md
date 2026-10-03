# ADR 0027: Phase 8a: two Keccak rounds per cycle (C5) - rule result

- Status: Proposed
- Date: 2026-10-03
- Decided by: pending team decision

## Context
- ADR 0026 (Accepted, Jose): sub-steps 8a, 8b, 8c, 8d all go ahead. 8a replaces the K0 permutation core (Phase 7) by one that computes two rounds per cycle (configuration C5). Test plan and adoption rule were written and committed before any 8a RTL and before any 8a measurement (`docs/evidence/phase08-keccak-stream/8a/test_plan_8a.md`, commit 9bdbad6).
- New files only: `rtl/keccak/keccak_f1600_r2.sv`, `keccak_sponge_r2.sv`; the K0 RTL is unedited. The K0 test files gained environment parameters whose defaults reproduce K0; the K0 verification was rerun as the regression and passes.

## Options considered
(a) Adopt C5 as the Keccak permutation core for 8b-8d and Phase 9. (b) Keep K0 (one round per cycle). (c) Other.

## Decision
Result of the pre-fixed rule (`scripts/select_8a.py`, no tolerance): **C5 is adopted by the rule** (all conditions PASS). Acceptance as the configuration is the team's (C5): this record stays Proposed.

## Consequences
- MEASURED (Quartus, seeds 1-6, 40.000 ns; `docs/evidence/phase08-keccak-stream/8a/selection_worksheet_2026-10-03.md`): ALM 6,152-6,169 (median 6,167.0; K0 3,558-3,572, median 3,566.5), registers 1,652 (K0 1,653), 0 M10K, 0 DSP; timing met at every seed; median lowest-slow-corner Fmax **50.655 MHz** (range 47.38-51.67) against K0's **67.675 MHz** (56.99-70.39).
- A permutation is 14 cycles in the sponge instead of 26 (12 busy instead of 24); t per permutation at the median Fmax is 14 / 50.655 = 0.2764 us against 26 / 67.675 = 0.3842 us (-28 %, perhitungan tim). A whole call shrinks by less (H(ek) 1184 B: 281 cycles against 389).
- Keccak cycles of one ML-KEM-768 operation (perhitungan tim from the measured formula): about 1,510 / 1,550 / 1,542 (KeyGen / Encaps / Decaps, median over 200 rho) against about 2,026 / 2,078 / 2,070 with K0, nothing overlapped.
- Cost: +73 % ALM (about +2,600 ALM); the Fmax of the permutation core drops by 25 %, so a system whose critical path is the Keccak core would lose that much Fmax; at present the NTT core (S10: median 44.320 MHz at 40 ns) is slower than C5's median, so the whole design is not limited by C5 (INFERENCE; no system compile yet).
- Information (seed 1, 20.000 ns, not part of the rule): C5-20 6,178 ALM, worst setup +4.591 ns (met), Fmax 64.90 MHz; K0-20 3,573 ALM, +6.893 ns, 76.30 MHz.
- Correction recorded for Phase 7: the K0 figure 56.99 MHz in `result_phase7.md` was seed 1 and the lowest of six; the median over seeds 1-6 is 67.675 MHz (K0 seeds 2-6 were compiled for this rule).
- Verification: both simulators, all 24 rounds compared (state per cycle and the first-round output), 12 busy cycles for every state, 306 cycle points equal to the formula with p = 14, three negative controls fail, formal K1-K5 PASS with NC-K1 and NC-K4 failing. Critical Warning 15725 (virtual pin clock) only, at every compile; nothing waived.
- Not covered: hardware, a system-level compile with the Keccak core and the NTT core together, other constraints.

## Evidence
- `docs/evidence/phase08-keccak-stream/8a/` (test plan, verify, formal, cycles, selection worksheet, `quartus_C5[-s2..s6]_20261003.md`, `quartus_C5-20_20261003.md`), `docs/evidence/phase07-keccak/quartus_K0[-s2..s6]_20261003.md` (baseline), `scripts/select_8a.py`.
