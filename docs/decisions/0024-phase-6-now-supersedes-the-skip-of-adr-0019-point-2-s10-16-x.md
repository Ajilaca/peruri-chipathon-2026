# ADR 0024: Phase 6 now (supersedes the skip of ADR 0019 point 2); S10 (16 x 1R1W M10K memory) inside Phase 6 afterwards

- Status: Accepted
- Date: 2026-10-03
- Decided by: Jevan, Team J5, chat 2026-10-03: 'fase 6 dulu aja' and 'kemudian kerjakan s10 di fase 6 saja'

## Context
- ADR 0019 (Accepted) point 2 skipped Phase 6 before the deadline (a trivial fixed operation order in the controller instead). The team (Jevan) asked on 2026-10-03 to do Phase 6 first, and then S10 inside Phase 6.
- S10 = option A of ADR 0022 (Proposed): 16 x 1R1W M10K banks with the conflict-free map `bank = (a1^a2^a3^a4, a7, a6, a5)`, `offset = a[3:0]`, crossbars, no slot arbitration. It targets Fmax; Phase 6 itself does not (docs/ROADMAP.md Phase 6).
- Phase 6 scope (ROADMAP): scheduler for the K-PKE arithmetic of KeyGen, Encrypt and Decrypt; transforms counted and equal to the reproduced reference (KeyGen 6 NTT / 0 INTT / 9 pointwise products, Encaps 3 / 4 / 12, Decaps 6 / 5 / 15, `tb/golden/op_counts.py`); inputs (matrix, noise) injected by the testbench; no Keccak or samplers in hardware.

## Options considered
(a) Keep ADR 0019's order (Keccak K0 next, Phase 6 skipped). (b) Phase 6 now, S10 afterwards in the same phase (chosen). (c) S10 first.

## Decision
Option (b), decided by Jevan (chat 2026-10-03). Working assumptions stated by the assistant, not decided by the team (the team may overrule them): NTT/INTT core base for Phase 6 = S7 (measured best, ADR 0021 is still Proposed; the scheduler uses the core only through its host port, so the core can be exchanged); full ROADMAP scope for Phase 6. S10 follows after the Phase 6 verdict with its own test plan and the ADR 0012 rule (compared with S7). The time estimate the team gave (done "this morning") is not matched by the assistant's ESTIMATE of 10-14 hours for both (basis: the S6-S8 work of 2026-10-02/03).

## Consequences
- ADR 0019 point 2 ("Phase 6 is skipped") is superseded by this record (ADR 0019 stays Accepted otherwise; amendment note 4 added there). Phase 7 (Keccak) and later blocks move after Phase 6 and S10.
- Branch `phase6-scheduling`. Phase 6 Approval (a team member) is needed before Phase 7 (ROADMAP); Phase 5M Approval is still empty.
- Fmax is not expected to rise in Phase 6 (INFERENCE); the Fmax effect of S10 is NOT MEASURED.
- The deadline risk (2026-10-08) of Keccak, samplers and the full ML-KEM path rises; it is the team's.

## Evidence
- Chat 2026-10-03; `docs/ROADMAP.md` Phase 6; `docs/decisions/0019-*.md`; `docs/decisions/0022-*.md`; `tb/golden/op_counts.py` (counts reproduced).
