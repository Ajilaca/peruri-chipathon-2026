# ADR 0026: Phase 8 sub-steps 8a, 8b, 8c and 8d all go ahead (supersedes the skip of 8a, 8c and 8d in ADR 0019 point 2)

- Status: Accepted
- Date: 2026-10-03
- Decided by: Jose, Team J5, chat 2026-10-03: '8a 8b 8c 8d dikerjakan , adr tolong diganti , approval fase 7 acc'

## Context
- ADR 0019 (Accepted 2026-10-02, Jevan) point 2 skipped Phase 6 and the Phase 8 sub-steps 8a (two rounds per cycle), 8c (matrix A on the fly) and 8d (overlap of Keccak with arithmetic) to reach a full ML-KEM before Thursday 2026-10-08. Phase 6 was reinstated by ADR 0024; the 8a/8c/8d part of the skip still stood.
- Phase 7 (Keccak K0) is done technically and its Approval box was ticked by Jose on 2026-10-03 (commit 1154a20, `docs/results/result_phase7.md`). K0 measured (seed 1, kernel-only): 3,572 ALM, 1,653 registers, 0 M10K, 0 DSP, 26 cycles per permutation in the sponge (24 busy), Fmax 56.99 MHz at 40 ns.
- The ROADMAP Phase 8 sub-steps are each "measured and reviewed separately": 8a two rounds per cycle (configuration C5), 8b streaming samplers (CBD from the PRF stream, SampleNTT from the XOF stream), 8c matrix A generated on the fly, 8d overlap of sampling with the kernel's arithmetic; 8b to 8d together form C6.
- Estimate given to the team on 2026-10-03 (ESTIMATE, from the pace of Phases 6 and 7): 8a about 4-6 h, 8b about 3-5 h, 8c and 8d about 6-10 h each; with Phase 9 (19-32 h) the total exceeds what fits before 2026-10-08. The risk is stated in the chat of 2026-10-03: tier T3 (full ML-KEM against ACVP) is the item most likely to be cut.

## Options considered
(a) Keep ADR 0019 as it stood: Phase 9 integration next, 8a/8c/8d only if time remains.
(b) Do all four sub-steps 8a, 8b, 8c, 8d (the team's choice).
(c) Do 8a and 8b only.

## Decision
Option (b), by Jose (Team J5): **8a, 8b, 8c and 8d are all to be done.** The skip of 8a, 8c and 8d in ADR 0019 point 2 is superseded (amendment note 5 of ADR 0019). Order: the ROADMAP order 8a, 8b, 8c, 8d, each with its own test plan and adoption rule or "no rule" statement written before measuring, each measured and reviewed separately (STOP after each sub-step by the suggested default of PENDING #26, which stays open). Everything else in ADR 0019 (reporting tiers, process lightening, evidence freeze Wednesday 2026-10-07 night) is unchanged.

## Consequences
- Dependencies recorded now, not decided: 8c needs the matrix entries to reach the pointwise unit from the sampler stream (the Phase 6 store holds the matrix in slots today); 8d needs a scheduler interface between the Phase 6 sequencer and the sampler (ROADMAP: "scheduler interface"); neither is built. They are designed in their own test plans, and if 8c or 8d proves infeasible in the time left that is reported as "not completed", never as a result (C3).
- Phase 9 (integration, tiers T2 and T3) moves behind the Phase 8 sub-steps unless the team reorders it; the schedule risk to T2/T3 before 2026-10-08 is the team's, stated here: the Phase 8 sub-steps estimated at 19-31 h (ESTIMATE) plus Phase 9 at 19-32 h do not fit the days left at 6-8 h per day. The team may stop or reorder at any STOP.
- 8a replaces K0's permutation core, so it has an adoption rule (ADR 0012 style, seeds 1-6 at 40 ns, K0 seeds 2-6 compiled for the baseline) written before measuring; K0 files stay unedited, 8a is new files.
- ROADMAP rows C5 and C6 (C6b, C6c, C6d) are filled as the sub-steps are measured. PENDING #25 and #26 remain open.

## Evidence
- Chat 2026-10-03 (quoted in the header); `docs/results/result_phase7.md` (Approval ticked, commit 1154a20); `docs/decisions/0019-minimal-path-to-a-full-ml-kem-768-core-before-thursday-2026-.md` point 2; `docs/ROADMAP.md` Phase 8.
