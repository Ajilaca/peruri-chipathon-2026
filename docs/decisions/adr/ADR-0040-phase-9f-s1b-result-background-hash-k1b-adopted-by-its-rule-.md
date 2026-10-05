# ADR 0040: Phase 9F S1b result: background hash (K1b) adopted by its rule, recovers the cycle cost of K1

- Status: Proposed
- Date: 2026-10-04
- Decided by: pending team decision

## Context
ADR 0036 (Accepted, Faza Dzil) listed S1b after S1: let the hashes that do not depend on the work next to them (KeyGen `H(ek)`, Encaps `H(ek)`, Decaps `J`) run in a background sidecar. S1b was built in the new module `rtl/mlkem/mlkem_core3.sv` with the programs of `rtl/mlkem/mlkem_ctl_rom2.sv` (generated from `tb/golden/mlkem_ctl_model2.py`), verified and measured under its own plan and rule (`evidence/phase9m/batch1/9f1b/test_plan_9f1b.md`, `result_9f1b.md`). The rule was applied to files and is met. ADR 0039 (Accepted, Faza Dzil) fixed 15 ns as the reporting limit.

## Options considered
1. Keep K1 (ADR 0038, `mlkem_core2`): 8,795 / 10,627 / 15,983 cycles, ALM median 14,061.0 (40 ns), Fmax median 73.070 MHz at 15 ns, latency at 15 ns 120.4 / 145.4 / 218.7 us.
2. Use K1b (`mlkem_core3`): 8,404 / 10,236 / 15,597 cycles (-391 / -391 / -386), ALM median 14,335.0 (+274.0), Fmax median 73.855 MHz at 15 ns (6 of 6 seeds met; 40 ns met at 6 of 6), latency at 15 ns 113.8 / 138.6 / 211.2 us (-5.5 %, -4.7 %, -3.5 % against K1; +0.2 %, +0.0 %, -0.2 % against the 9M-1 core at 15 ns, two seeds of S0); ACVP 100 % on both simulators; negative controls as required including a throttled sidecar that must pass and one without protection that must fail (MEASURED, simulation, formal and kernel-only Quartus; `batch1/9f1b/selection_worksheet.md`).

## Decision
Proposed, not decided. The rule of the plan adopts option 2. The formal control NC-B7 was not demonstrated by the formal run (timeout; retry without result at the time of the report); it is demonstrated by simulation (NC-WR). The team accepts or rejects it.

## Consequences
If accepted: the base for Batch 2 (S2, S3, item 4) is `mlkem_core3` with `SMP_C5 = 0`, `HASH_C5 = 0`, `CODEC_W2 = 1`; the wall at 15 ns is the NTT core / memory (298 of the 300 worst paths), so S2 targets that class. ADR 0027 is not edited. Latencies are perhitungan tim from kernel-only static timing. No board claim. If rejected: K1 (ADR 0038) or the 9M-1 core stays the base; `mlkem_core3.sv` remains.

## Evidence
`evidence/phase9m/batch1/9f1b/result_9f1b.md`, `selection_worksheet.md`, `sim.md`, `formal.md`, `critical_paths_K1b-15.md`, `quartus_K1b*.md`; `evidence/phase9m/batch1/9f1/result_9f1.md`; `docs/decisions/adr/ADR-0038-phase-9f-s1-result-k0-sampler-and-k0-hash-k1-adopted-by-its-.md`, `ADR-0039-phase-9f-15-ns-is-the-fmax-reporting-limit-14-ns-is-kept-for.md`.
