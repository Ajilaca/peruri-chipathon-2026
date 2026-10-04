# ADR 0038: Phase 9F S1 result: K0 sampler and K0 hash (K1) adopted by its rule as a smaller configuration, not a faster one

- Status: Proposed
- Date: 2026-10-04
- Decided by: pending team decision

## Context
ADR 0036 (Accepted, Faza Dzil) made S1 the step after S0: the K0 Keccak sponge (one round per cycle) in both places, the hash instance and the sampler of the K-PKE engine, to remove the C5 permutations from the critical paths. S1 was built in the new module `rtl/mlkem/mlkem_core2.sv` (parameter `SMP_C5`), verified and measured under its own plan and rule (`docs/evidence/phase09m-optimisation/9f1/test_plan_9f1.md`, `result_9f1.md`). The rule was applied to files and is met. Step S0 (`9f0/result_9f0.md`), measured later, shows that the 9M-1 core already meets 14 ns (75.3 MHz lowest slow corner) and fails at 13 ns in the NTT core / memory class together with the C5 permutations.

## Options considered
1. Keep the 9M-1 core (C5 sampler and C5 hash, `SMP_C5 = 1`, `HASH_C5 = 1`): 8,327 / 10,159 / 15,515 cycles, ALM median 17,654.0 (40 ns), Fmax lowest slow corner 73.6 MHz at 15 ns (S0, two seeds), latency at 15 ns 113.6 / 138.5 / 211.6 us.
2. Use K1 (`SMP_C5 = 0`, `HASH_C5 = 0`): 8,795 / 10,627 / 15,983 cycles (+468 each), ALM median 14,061.0 (-3,593, -20 %), Fmax median 73.07 MHz at 15 ns (six seeds, all met), latency at 15 ns 120.4 / 145.4 / 218.7 us (+6.0 %, +5.0 %, +3.4 % against option 1 at the same constraint); timing met at 40 ns at 6 of 6 seeds; ACVP 100 % on both simulators (MEASURED, simulation and kernel-only Quartus; `9f1/selection_worksheet_2026-10-04.md`). At 15 ns all 300 worst paths of K1 are in the NTT core / memory / PWM class.

## Decision
Proposed, not decided. The rule of the plan adopts option 2 (it compares with MW at 20 ns, fixed before S0); against MW at the same constraint K1 is slower by 3-6 %. K1 frees about 3,600 ALM and does not raise Fmax. The team chooses; the S1b result (`9f1b/`) recovers about 390 cycles of the 468.

## Consequences
If accepted: later steps use `SMP_C5 = 0`, `HASH_C5 = 0` as the base; ADR 0027 is not edited (a later ADR supersedes it where the team replaces C5). S2 targets the NTT core / memory class. Latencies are perhitungan tim from kernel-only static timing. No board claim. If rejected: the C5 core stays; `mlkem_core2.sv` remains with its parameter.

## Evidence
`docs/evidence/phase09m-optimisation/9f1/result_9f1.md`, `selection_worksheet_2026-10-04.md`, `sim_verilator_2026-10-04.md`, `sim_icarus_2026-10-04.md`, `formal_2026-10-04.md`, `critical_paths_K1-15_2026-10-04.md`, `quartus_K1*_20261004.md`; `docs/evidence/phase09m-optimisation/9f0/result_9f0.md` (S0).
