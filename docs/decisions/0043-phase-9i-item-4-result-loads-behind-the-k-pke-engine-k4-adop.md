# ADR 0043: Phase 9I item 4 result: loads behind the K-PKE engine (K4) adopted by its rule, Encaps -639 and Decaps -2,630 cycles

- Status: Proposed
- Date: 2026-10-05
- Decided by: pending team decision

## Context
ADR 0034 listed item 4 (overlap of polynomial loads with the engine) as the largest remaining cycle saving ("needs the engine host port to work while the engine runs, i.e. a new variant of frozen Phase 6-8 files; high risk"). It was built as a new variant (`mlkem_core4`, `kpke_sched_smp4`, `kpke_smp_top_s10o`, `mlkem_ldpoly2o`, `mlkem_ctl_rom3`; the Phase 6-8 files and `mlkem_core3` are not edited) and verified and measured under its own plan and rule (`docs/evidence/phase09m-optimisation/9i4/test_plan_9i4.md`, `result_9i4.md`). The base of the measurement is K3 (ADR 0042, Proposed); the K3 parameters (`NTT_P6 = 1`, `NTT_AR = 1`) are the parameters of K4.

## Options considered
1. Keep K3 (`mlkem_core3`): 8,416 / 10,250 / 15,619 cycles; Fmax median 77.555 MHz at 15 ns; latency 108.5 / 132.2 / 201.4 us; ALM median 14,115.5 (40 ns) and 14,293.0 (15 ns).
2. Use K4 (`mlkem_core4`): 8,416 / 9,611 / 12,989 cycles (KeyGen equal, Encaps -639, Decaps -2,630); Fmax median 76.665 MHz at 15 ns (six seeds 69.43-80.99; -0.89 MHz, inside the spread); latency at 15 ns 109.8 / 125.4 / 169.4 us (+1.2 %, -5.1 %, -15.9 % against K3); ALM median 14,222.0 (40 ns, +106.5) and 14,480.0 (15 ns, +187.0); timing met at 6 of 6 seeds at 40 ns and at 15 ns (MEASURED, `9i4/selection_worksheet_2026-10-05.md`). ACVP 100 % on both simulators; negative controls as required, including a throttled host port that must pass with the interlock and fail without it; formal: safety (E1, S1-S7, B1-B7) PASS and cover PASS, NC-JOIN4 FAIL as required, **but P1 (bounded) and NC-E1-4 timed out and have no formal result** (`formal_2026-10-05.md`).

## Decision
Proposed, not decided. The rule of the plan adopts option 2. The team accepts or rejects it. The worst path of the K4 seed with the smallest slack is a path of S2b (ADR 0042), not of item 4; the low seed (69.43 MHz) belongs to that path. If K3 (ADR 0042) is rejected, K4 must be remeasured on the other base: the cycle savings do not depend on the NTT parameters, the Fmax does.

## Consequences
If accepted: the base is `mlkem_core4` with the K3 parameters; the controller has the micro-operations RUNS and RUNJ, the engine variant grants the host write port while it runs and starts an operation only after every slot it uses is loaded; KeyGen is unchanged (its stores stay in series); stores are not overlapped (a possible later step). `mlkem_core4` requires `CODEC_W2 = 1`. If rejected: `mlkem_core3` stays; `mlkem_core4` and its files remain unused. Latencies are perhitungan tim from kernel-only static timing. No board claim; constant time means cycle-count invariance only.

## Evidence
`docs/evidence/phase09m-optimisation/9i4/result_9i4.md`, `selection_worksheet_2026-10-05.md`, `sim_2026-10-05.md`, `formal_2026-10-05.md`, `critical_paths_K4-15_2026-10-05.md`, `profile_k4_verilator_2026-10-05.json`, `quartus_K4*_2026100*.md`; `docs/decisions/0042-phase-9f-s2b-result-registered-ntt-issue-address-k3-not-adop.md`, `0034-*.md`, `0039-*.md`.
