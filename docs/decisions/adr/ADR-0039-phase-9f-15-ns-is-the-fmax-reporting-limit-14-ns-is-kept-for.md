# ADR 0039: Phase 9F: 15 ns is the Fmax reporting limit; 14 ns is kept for later consideration

- Status: Accepted
- Date: 2026-10-04
- Decided by: Faza Dzil (Team J5), chat 2026-10-04

## Context
ADR 0036 (Accepted, Faza Dzil) asked that Fmax be reported at a tighter constraint beside the 40 ns gate and named 15 ns. Step S0 (`evidence/phase9m/batch1/9f0/result_9f0.md`) measured the 9M-1 core at 16, 15, 14 and 13 ns: 15 and 14 ns are met at both seeds, 13 ns at one of two; the limit of that design lies between 13 and 14 ns. Step S1 measured K1 at 15 ns (met at 6 of 6 seeds, Fmax median 73.07 MHz, `batch1/9f1/result_9f1.md`); K1 was not compiled below 15 ns.

## Options considered
1. Report and compare at 15 ns only (six seeds per configuration), keep 14 ns as a later point.
2. Also sweep every configuration (K1, K1b, later steps) at 14, 13 ns and below until the first failure: 4-6 more compiles per configuration (ESTIMATE 2-3 hours each).

## Decision
Faza Dzil, chat 2026-10-04: "kita ambil 15 ns saja sebagai batas; 14 ns bisa jadi bahan pertimbangan karena pass namun bisa dikerjakan nanti".
- 15 ns is the constraint at which Fmax and latency are reported and compared in Phase 9F (six seeds per configuration, beside the 40 ns gate).
- 14 ns is kept for consideration: the 9M-1 core meets it at both seeds (S0); it is not measured for K1, K1b or later steps now and may be done later.
- No further sweep below 15 ns is started for K1b or the Batch 2 steps unless the team asks.

## Consequences
S1b (K1b) is compiled at 40 ns and 15 ns, six seeds each, as in the plan; its adoption rule uses the 15 ns result. The statement "timing met at 15 ns" needs all six seeds; 14 ns remains a statement for the 9M-1 core at two seeds only (S0), labelled as such. Latencies stay perhitungan tim from kernel-only static timing; no board claim.

## Evidence
`evidence/phase9m/batch1/9f0/result_9f0.md`, `evidence/phase9m/batch1/9f1/result_9f1.md`, `docs/decisions/adr/ADR-0036-phase-9f-fmax-plan-s0-s1-s2-latency-rule-and-reporting-at-a-.md`.
