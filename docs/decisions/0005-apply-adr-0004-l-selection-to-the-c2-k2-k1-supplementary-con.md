# ADR 0005: Apply ADR 0004 L-selection to the C2-K2-K1 supplementary configuration

- Status: Proposed
- Date: 2026-09-30
- Decided by: pending team decision

## Context
ADR 0004 (Accepted) fixes the Phase 3 lane-count criterion: minimise cycle count among the L values
whose Quartus ALM is within 25% of the device (10,478 ALM, ADR 0004 / 'perhitungan tim'). Applied to the C2 sweep
(`docs/results/result_phase3.md`), L=8 (MEASURED 11,446 ALM, `docs/evidence/quartus/C2-L8-20260929.md`) was disqualified and **L=4** is the reported
result (pending team sign-off).

The team then approved two supplementary optimisation experiments on C2, run as separate
configurations so the C2 baseline stays reproducible:
- K2 (`docs/evidence/phase03-multilane/k2_experiment_2026-09-30.md`): narrower sub-cycle counter.
  Valid but insufficient on its own (L=8: MEASURED 11,232 ALM, `docs/evidence/quartus/C2-L8-K2-20260930.md`).
- K1 (`docs/evidence/phase03-multilane/k1_experiment_2026-09-30.md`): one shared modular multiplier
  per butterfly instead of one per mode, on top of K2 (config C2-K2-K1). It changes the butterfly
  datapath, so it is outside the written Phase 3 implementation scope ("butterfly, arithmetic and
  memory as in Phase 2"); the team approved it as a supplementary experiment on that basis.

MEASURED C2-K2-K1 (Quartus, `docs/evidence/quartus/C2-K2-K1-L{1,2,4,8}-20260930.md`; same device/constraints/seed as C2; simulation bit-exact on two
simulators; cycle counts identical to C2):

| L | ALM | Within 10,478? | NTT / INTT cycles |
|---|---|---|---|
| 1 | 5,566 | yes | 897 / 1153 |
| 2 | 5,374 | yes | 449 / 705 |
| 4 | 6,775 | yes | 225 / 481 |
| 8 | 9,754 | yes (724 below) | 113 / 369 |

Applying ADR 0004's rule unchanged to this family gives **L=8** (lowest cycle count, within budget).
ADR 0004's secondary AT check still cannot run: no configuration meets timing at any clock.

Open items that bear on this decision (from the K1 record): the butterfly-equivalence formal proof
did not complete (simulation evidence only); the core formal gap for L>1 is unchanged; the fitter's
ALM packing varied by up to ~370 ALM (MEASURED, `k1_entity_breakdown_2026-09-30.txt`, K2-L1) between compiles of identical logic, versus a 724-ALM margin;
K1 lowers Fmax slightly at L=1/2/4 (MEASURED, same Quartus evidence files).

## Options considered
1. **Adopt C2-K2-K1 as the Phase 3 configuration family and select L=8** under ADR 0004's rule.
   Throughput: 8 butterflies/cycle, NTT 113 / INTT 369 cycles (MEASURED in simulation, `k1_cocotb_regression_2026-09-30.txt`). Cost: accepts a butterfly change
   outside the written Phase 3 scope, recorded here as a deliberate deviation; Phase 4 then starts
   from C2-K2-K1-L8.
2. **Adopt C2-K2-K1 but keep L=4** (e.g. for more ALM headroom for Keccak/sampler, or timing, which is
   worse at larger L). Contradicts ADR 0004's rule unless a new criterion is stated.
3. **Keep the C2 result (L=4) for Phase 3 and carry K1 into a later phase** (e.g. Phase 5, arithmetic
   optimisation). Keeps Phase 3 strictly within its written scope; L=8 is revisited later.
4. **Defer until the open formal items are closed** (butterfly equivalence via multiplier
   abstraction and/or exhaustive simulation; optionally a seed sweep for the ALM margin).

## Decision
<!-- Not decided. Fill in only from what the team actually decides. Until then L=4 (C2) remains the
     ADR 0004 result and L=8 (C2-K2-K1) is a candidate pending team approval. -->

## Consequences
<!-- To be written with the decision. Whatever is chosen: ADR 0004 itself is not edited;
     docs/results/result_phase3.md and docs/ROADMAP.md are updated only after the team decides. -->

## Evidence
- `docs/evidence/phase03-multilane/k1_experiment_2026-09-30.md`, `k1_entity_breakdown_2026-09-30.txt`,
  `k1_cocotb_regression_2026-09-30.txt`, `k1_formal_2026-09-30.txt`
- `docs/evidence/quartus/C2-K2-K1-L{1,2,4,8}-20260930.md`
- `docs/evidence/phase03-multilane/k2_experiment_2026-09-30.md`,
  `docs/evidence/quartus/C2-L{1,2,4,8}-K2-20260930.md`
- `docs/decisions/0004-phase-3-lane-count-l-selection-criterion.md`, `docs/results/result_phase3.md`
