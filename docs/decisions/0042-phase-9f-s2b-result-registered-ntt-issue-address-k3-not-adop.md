# ADR 0042: Phase 9F S2b result: registered NTT issue address (K3) not adopted by its rule as written, Fmax median +3.4 MHz with a tail of low seeds

- Status: Proposed
- Date: 2026-10-05
- Decided by: pending team decision

## Context
ADR 0041 (Proposed) reported S2 (register after the Barrett reducer, K2) as neutral and named the layer-counter address path as the next wall. S2b registers the issue-stage address of the NTT core (parameter `AREG` / `NTT_AR`, default 0), computed one cycle early from the next-state values; it was verified and measured under its own plan and rule (`docs/evidence/phase09m-optimisation/9s2b/test_plan_9s2b.md`, `result_9s2b.md`; amendment A1: the 40 ns gate stays; amendment A2: three additional 15 ns seeds, chosen after the first six). The rule of the plan was fixed before measuring and tightened after S2: a gain inside the seed noise is not adopted. ADR 0039 (Accepted, Faza Dzil) fixed 15 ns as the reporting limit.

## Options considered
1. Keep K2 (ADR 0041, `NTT_AR = 0`): Fmax median 74.125 MHz at 15 ns (six seeds, 72.65-76.03), latency at 15 ns 113.5 / 138.3 / 210.7 us.
2. Use K3 (`NTT_AR = 1`): same cycles (8,416 / 10,250 / 15,619); Fmax median 77.555 MHz at six seeds (73.02-79.37; +3.43 MHz), latency 108.5 / 132.2 / 201.4 us (-4.4 %); at nine seeds median 77.320 MHz (72.80-79.37), six of nine seeds above the highest seed of K2; timing met at 6 of 6 seeds at 15 ns and at 6 of 6 at 40 ns; ALM median 14,115.5 at 40 ns (-97.5), 14,293.0 at 15 ns (-56.5), registers about +40 to +135 (MEASURED, `9s2b/selection_worksheet_2026-10-05.md`). The seeds are bimodal: six at 77.0 to 79.4 MHz and three at 72.8 to 75.5 MHz. A path analysis of K4 (same S2b logic) finds the cause of the low end: the term `start_go` of S2b puts the sequencer counter, through the host write enable, into the cone of the registered address (INFERENCE for the K3 seeds, MEASURED in K4-15-s6).

## Decision
Proposed, not decided. **By the rule as written K3 is not adopted** (item 5: the gain of the median, +3.43 MHz, is smaller than the spread of the seeds of K3, 6.35 MHz, and the lowest seed of K3 is below the highest seed of K2). Items 1-4 and 6 are met. The evidence points to a real gain of about 3 MHz with a tail of low seeds; it is not hidden here that the rule says no. The team decides whether to accept K3 (it is the base of the K4 measurement in ADR 0043), or to reject it.

## Consequences
If accepted: the base is `mlkem_core3` / `mlkem_core4` with `NTT_P6 = 1`, `NTT_AR = 1`; S2 (ADR 0041) is part of it. If rejected: K2 or K1b stays (parameters at their defaults; the item 4 results of ADR 0043 are relative to K3 and would have to be remeasured on the other base). Latencies are perhitungan tim from kernel-only static timing; seed noise is about 3 MHz and larger for K3. No board claim. ADR 0041 is not edited.

## Evidence
`docs/evidence/phase09m-optimisation/9s2b/result_9s2b.md`, `selection_worksheet_2026-10-05.md`, `sim_2026-10-05.md`, `formal_2026-10-05.md`, `critical_paths_K3-15_2026-10-05.md`, `quartus_K3*_2026100*.md`; `docs/evidence/phase09m-optimisation/9i4/critical_paths_K4-15_2026-10-05.md`; `docs/decisions/0041-phase-9f-s2-result-register-after-the-barrett-reducer-k2-ado.md`, `0039-phase-9f-15-ns-is-the-fmax-reporting-limit-14-ns-is-kept-for.md`.
