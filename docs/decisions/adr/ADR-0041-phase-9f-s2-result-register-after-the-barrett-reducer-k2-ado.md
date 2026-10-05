# ADR 0041: Phase 9F S2 result: register after the Barrett reducer (K2) adopted by its rule, no measurable Fmax gain

- Status: Accepted
- Date: 2026-10-04
- Decided by: Jo (Team J5), 2026-10-05

## Context
ADR 0036 (Accepted, Faza Dzil) listed S2 as the step that attacks the limit S1 exposes; ADR 0040 (Proposed) names the NTT core / memory as the wall of K1b at 15 ns. S2 adds the fourth multiplier cut (the register after the final Barrett correction, P = 5 -> 6) by the parameter `NTT_P6` (default 0), verified and measured under its own plan and rule (`evidence/phase9m/batch2/9s2/test_plan_9s2.md`, `result_9s2.md`). The rule was applied to files and is met. ADR 0039 (Accepted, Faza Dzil) fixed 15 ns as the reporting limit.

## Options considered
1. Keep K1b (ADR 0040, `NTT_P6 = 0`): 8,404 / 10,236 / 15,597 cycles, ALM median 14,335.0 (40 ns), Fmax median 73.855 MHz at 15 ns, latency at 15 ns 113.8 / 138.6 / 211.2 us.
2. Use K2 (`NTT_P6 = 1`): 8,416 / 10,250 / 15,619 cycles (+12 / +14 / +22), ALM median 14,213.0 (-122.0), registers about +120, Fmax median 74.125 MHz at 15 ns (+0.270 MHz, inside the seed spread of 3.38 / 2.94 MHz), latency at 15 ns 113.5 / 138.3 / 210.7 us (-0.2 %, below the noise of the seeds); timing met at 6 of 6 seeds at 40 ns and at 15 ns; ACVP 100 % on both simulators; formal control proof at P = 6 PASS (MEASURED, simulation, formal and kernel-only Quartus; `batch2/9s2/selection_worksheet.md`). The reducer-to-memory path moved from +1.170 to +2.349 ns, but the layer-counter address path (+1.910 ns in K1b) now limits at +1.404 ns in the seed analysed.

## Decision
Accepted by Jo (Team J5) on 2026-10-05 on the team's instruction to approve; the text below is the proposal as written. The rule of the plan adopts option 2; the evidence says S2 is neutral for Fmax and latency (the plan's ESTIMATE of 76 to 80 MHz was not met). The team accepts or rejects it; S2 has value mainly as the first half of a step S2b (registering the per-layer address arithmetic), which is not planned or built yet.

## Consequences
If accepted: the base for the next steps is `mlkem_core3` with `SMP_C5 = 0`, `HASH_C5 = 0`, `CODEC_W2 = 1`, `NTT_P6 = 1`; the NTT cycles per transform are 119; the wall at 15 ns is the issue-stage address path (`layer_q` to the memory ports), a candidate for S2b. If rejected: K1b stays (the default parameter value, no code to remove). Latencies are perhitungan tim from kernel-only static timing; seed noise is about 3 MHz. No board claim. ADR 0040 is not edited.

## Evidence
`evidence/phase9m/batch2/9s2/result_9s2.md`, `selection_worksheet.md`, `sim.md`, `formal.md`, `critical_paths_K2-15.md`, `quartus_K2*.md`; `evidence/phase9m/batch1/9f1b/` (reference K1b); `docs/decisions/adr/ADR-0036-phase-9f-fmax-plan-s0-s1-s2-latency-rule-and-reporting-at-a-.md`, `ADR-0039-phase-9f-15-ns-is-the-fmax-reporting-limit-14-ns-is-kept-for.md`, `ADR-0040-phase-9f-s1b-result-background-hash-k1b-adopted-by-its-rule-.md`.
