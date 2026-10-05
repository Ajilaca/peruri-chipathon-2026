# ADR 0035: Phase 9M-1 result: two-byte codec path (CODEC_W2) adopted by its rule

- Status: Accepted
- Date: 2026-10-04
- Decided by: Jo (Team J5), 2026-10-05

## Context
ADR 0034 (Accepted, Faza Dzil) made item 1 of Phase 9M the first step: loading and storing polynomials is limited by a one-byte-per-cycle codec path at d = 12 and d = 10 (`evidence/phase9m/profile.md`). Item 1 was built, verified and measured under its own plan and rule (`evidence/phase9m/batch1/9m1/test_plan_9m1.md`, `result_9m1.md`). The rule was applied to files and is met. The default of the core parameter `CODEC_W2` is still 0 (the Phase 9 behaviour).

## Options considered
1. Keep `CODEC_W2 = 0` (Phase 9 as merged): no change; 9,095 / 10,735 / 16,667 cycles (profile inputs).
2. Use `CODEC_W2 = 1` as the configuration of the later Phase 9M items: 8,327 / 10,159 / 15,515 cycles (-8.4 %, -5.4 %, -6.9 %), ALM median 17,654.0 against 17,620.5 (+33.5), Fmax median 48.855 against 49.280 MHz, timing met at 40 ns at every seed, ACVP 100 % on both simulators (MEASURED, simulation and kernel-only Quartus; `batch1/9m1/selection_worksheet.md`).

## Decision
Accepted by Jo (Team J5) on 2026-10-05 on the team's instruction to approve; the text below is the proposal as written. The rule of the plan adopts option 2; the team accepts or rejects it. Until an acceptance is recorded, the default stays 0 and nothing in the proposal depends on it.

## Consequences
If accepted: items 2, 3 and 4 of Phase 9M are measured on `CODEC_W2 = 1`; the Phase 9 numbers (`phase09.md`) stay as they are and the new numbers carry their own evidence paths. Latencies are perhitungan tim from kernel-only static timing. No board claim. If rejected: the core stays at the Phase 9 configuration and the files remain as an unused parameter.

## Evidence
`evidence/phase9m/batch1/9m1/result_9m1.md`, `selection_worksheet.md`, `formal.md`, `sim_verilator.md`, `sim_icarus.md`, `regression_default.md`, `quartus_MW*.md`; profiles `evidence/phase9m/profile_verilator.json` and `batch1/9m1/profile_w2_verilator.json`.
