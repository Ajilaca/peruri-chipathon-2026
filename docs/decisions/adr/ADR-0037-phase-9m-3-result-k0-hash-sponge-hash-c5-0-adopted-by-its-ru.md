# ADR 0037: Phase 9M-3 result: K0 hash sponge (HASH_C5 = 0) adopted by its rule as the smaller option

- Status: Proposed
- Date: 2026-10-04
- Decided by: pending team decision

## Context
ADR 0034 (Accepted, Faza Dzil) made item 3 of Phase 9M the choice of the sponge of the hash instance (G, H, J): C5 (two rounds per cycle, ADR 0027, the Phase 9 default) or K0 (one round per cycle, Phase 7). The parameter `HASH_C5` already existed; item 3 changed no RTL. It was measured against the 9M-1 core under its own plan and rule (`evidence/phase9m/batch1/9m3/test_plan_9m3.md`, `result_9m3.md`). The rule was applied to files and is met. The sampler inside the K-PKE engine keeps its C5 sponge in both options.

## Options considered
1. Keep `HASH_C5 = 1` (C5, ADR 0027): 8,327 / 10,159 / 15,515 cycles (profile inputs, `CODEC_W2 = 1`), ALM median 17,654.0.
2. Use `HASH_C5 = 0` (K0): 8,447 / 10,279 / 15,635 cycles (+120 each, +1.44 % / +1.18 % / +0.77 %), ALM median 15,917.5 (-1,736.5), Fmax median 48.935 against 48.855 MHz, latency at the median Fmax +1.28 % / +1.02 % / +0.61 %, timing met at 40 ns at 6 of 6 seeds, ACVP 100 % on both simulators (MEASURED, simulation and kernel-only Quartus; `batch1/9m3/selection_worksheet.md`).

## Decision
Proposed, not decided. The rule of the plan says the numbers justify K0 (area saved at about 1 % latency); the team chooses. K0 is not a speed improvement: it frees about 1,700 ALM that the Fmax plan (ADR 0036) can spend. The default of `HASH_C5` stays 1 until an acceptance is recorded.

## Consequences
If accepted: the configuration of later steps (S1 onward) is `CODEC_W2 = 1`, `HASH_C5 = 0`, or K0 is superseded there by the S1 sampler work; ADR 0027 is not edited (a later ADR supersedes it if the team replaces C5 in the core). Latencies are perhitungan tim from kernel-only static timing. No board claim. If rejected: C5 stays, the K0 files remain a parameter.

## Evidence
`evidence/phase9m/batch1/9m3/result_9m3.md`, `selection_worksheet.md`, `formal.md`, `sim_verilator.md`, `sim_icarus.md`, `regression_default.md`, `quartus_MK*.md`; profiles `batch1/9m3/profile_k0_w2_verilator.json` and `batch1/9m1/profile_w2_verilator.json`.
