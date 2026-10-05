# ADR 0036: Phase 9F Fmax plan S0-S1-S2: latency rule and reporting at a 15 ns constraint beside 40 ns

- Status: Accepted
- Date: 2026-10-04
- Decided by: Faza Dzil (Team J5), chat 2026-10-04

## Context
Faza Dzil asked for a plan to raise Fmax with an ALM budget of 20,000 (chat 2026-10-04). The critical paths of the 9M-1 core were measured (`evidence/phase9m/critical_paths_MW.md`, MEASURED): at 20 ns all 300 worst setup paths lie inside the two C5 Keccak-f[1600] permutations (195 in the hash instance, 105 in the sampler sponge of the engine; worst slack +4.355 ns); outside them the design would allow about 69 MHz (INFERENCE). ADR 0010 had named the memory read as the critical path of Phase 5; that is no longer the limit of the full core. K0 (one round per cycle) is faster as a block (67.7 MHz median at 40 ns, 76.3 MHz at 20 ns, MEASURED Phase 7 and 8a) but adds cycles. The reported Fmax depends on the constraint (48.9 MHz at 40 ns, 64.0 MHz at 20 ns, same design).

## Options considered
Plan proposed in chat 2026-10-04 (all savings and Fmax values are ESTIMATE): S0 a sweep of the constraint (18, 16, 15 ns; seeds 1-2) and the Quartus high-performance effort on the 9M-1 core, no RTL change; S1 K0 sponge in both places (hash instance and the sampler of the engine), about 13,200-13,800 ALM, Fmax about 65-72 MHz at a 15 ns constraint, cycles about +450 per operation; S2 attack the next limit found after S1 (hash output to the register file, or the NTT memory read), +100 to +800 ALM; S3 (optional, after the freeze) a second K0 sampler (item 5). Options not taken: reporting Fmax only at 40 ns (hides the real limit); judging by Fmax alone (K0 adds cycles, so a higher Fmax need not give a lower latency).

## Decision
Faza Dzil, chat 2026-10-04 (answering three questions): "saya setuju semua".
1. The order S0 -> S1 (-> S2 conditional on what S1 shows) is agreed; S3 stays an idea for later work.
2. The adoption rule of the Fmax steps is based on latency, t = cycles / Fmax, for KeyGen, Encaps and Decaps, not on Fmax alone.
3. Fmax is reported at a 15 ns constraint beside the 40 ns gate (seeds 1-6, kernel-only static timing, labelled as such). This is a change of the reporting policy: the 40 ns result stays the gate of Phases 5-9 (ADR 0011 D1, ADR 0017); the 15 ns figure is information (as the 20 ns figure, ADR 0010) and is never presented as a board clock.

## Consequences
Every step has its own test plan and rule written before its RTL or compile, the same verification as items 1-3 (ACVP 100 % on both simulators, constant cycles, formal, Quartus seeds 1-6), and a Proposed ADR for its adoption; the team accepts. The ALM budget of 20,000 is a limit of the plan (the 9M-1 core uses 17,654 ALM, median). Before freeze (2026-10-07) S0 and S1 are the target; S2 only if S1 exposes a simple limit. No claim about a board clock: a core that meets 15 ns in kernel-only static timing is not clocked faster by that fact, and the DE10-Nano system clock needs a PLL decision in Phase 10 (not part of this plan). Items 4 and 5 of ADR 0034 stay later work.

## Evidence
`evidence/phase9m/critical_paths_MW.md`, `evidence/phase9m/batch1/9m2/result_9m2.md` (20 ns, seeds 1-6), `evidence/phase08/8a/` and `evidence/phase07/` (K0 and C5 blocks), `docs/decisions/0010-*` and `0034-*`.
