# ADR 0005: Apply ADR 0004 L-selection to the C2-K2-K1 supplementary configuration

- Status: Accepted
- Date: 2026-09-30
- Decided by: Faza Dzil, Team J5

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

Open items that bear on this decision (from the K1 record): the fitter's
ALM packing varied by up to ~370 ALM (MEASURED, `k1_entity_breakdown_2026-09-30.txt`, K2-L1) between compiles of identical logic, versus a 724-ALM margin;
K1 lowers Fmax slightly at L=1/2/4 (MEASURED, same Quartus evidence files).
Closed since the first draft: `butterfly` vs `butterfly_shared` equivalence is established by a formal
proof with the multiplier abstracted (PASS, two negative controls FAIL) and by exhaustive simulation of
all 73,785,560,578 inputs (0 mismatches); see `k1_experiment_2026-09-30.md`, caveat 5.
Also closed: the core formal gap for L>1 was a harness artefact; C2-K2-K1 now PASSes k-induction at
L=1/2/4/8 for bank_overflow_o, the busy/done handshake and the counter ranges
(`formal_rerun_2026-09-30.md`).

## Options considered
1. **Adopt C2-K2-K1 as the Phase 3 configuration family and select L=8** under ADR 0004's rule.
   Throughput: 8 butterflies/cycle, NTT 113 / INTT 369 cycles (MEASURED in simulation, `k1_cocotb_regression_2026-09-30.txt`). Cost: accepts a butterfly change
   outside the written Phase 3 scope, recorded here as a deliberate deviation; Phase 4 then starts
   from C2-K2-K1-L8.
2. **Adopt C2-K2-K1 but keep L=4** (e.g. for more ALM headroom for Keccak/sampler, or timing, which is
   worse at larger L). Contradicts ADR 0004's rule unless a new criterion is stated.
3. **Keep the C2 result (L=4) for Phase 3 and carry K1 into a later phase** (e.g. Phase 5, arithmetic
   optimisation). Keeps Phase 3 strictly within its written scope; L=8 is revisited later.
4. **Defer** (e.g. until a seed sweep quantifies the ALM-packing margin).

## Decision
**Option 1.** The team adopts the optimised configuration **C2-K2-K1** as the Phase 3 configuration
family and, applying ADR 0004's rule to it unchanged, selects **L = 8** (MEASURED 9,754 ALM, within the
10,478 ALM budget; NTT 113 / INTT 369 cycles; 8 butterflies per cycle).

This is a deliberate, recorded deviation from the written Phase 3 implementation scope ("butterfly,
arithmetic and memory as in Phase 2"): K1 changes the butterfly datapath (one shared multiplier per
butterfly). The modular reduction method (`modmul_reduce.sv`) and every locked FIPS 203 parameter are
unchanged (ADR 0002 still holds). ADR 0004 itself is not edited; this record applies it.

## Consequences
- Phase 4 (pipelining) starts from **C2-K2-K1 at L = 8** (`rtl/ntt/ntt_core_c2_k2_k1.sv`,
  `rtl/ntt/butterfly_shared.sv`), not from C2 at L = 4. The earlier ADR 0004 result on the C2 family
  (L = 4, `docs/results/result_phase3.md` Section 3) is kept as the measured baseline comparison, not
  as the selected operating point.
- The C2, C2-K2 and C2-K2-K1 RTL and their evidence files all stay in the repository so the
  comparison remains reproducible.
- Accepted with these known limits, none of which this decision resolves: timing is not met for any
  configuration (Phase 4; no target-clock ADR yet); ADR 0004's secondary AT check still cannot run;
  the 724-ALM margin under the budget is larger than, but not far above, the largest fitter-packing
  swing observed (~370 ALM) and no seed sweep has been run; 0 M10K blocks are used.
- Any later change of the selected L or of the configuration family needs a new ADR.
- This decision does not tick the Approval box of `docs/results/result_phase3.md`; that remains a
  separate human sign-off.

## Evidence
- `docs/evidence/phase03-multilane/k1_experiment_2026-09-30.md`, `k1_entity_breakdown_2026-09-30.txt`,
  `k1_cocotb_regression_2026-09-30.txt`, `k1_formal_2026-09-30.txt`
- `docs/evidence/quartus/C2-K2-K1-L{1,2,4,8}-20260930.md`
- `docs/evidence/phase03-multilane/k2_experiment_2026-09-30.md`,
  `docs/evidence/quartus/C2-L{1,2,4,8}-K2-20260930.md`
- `docs/decisions/0004-phase-3-lane-count-l-selection-criterion.md`, `docs/results/result_phase3.md`
