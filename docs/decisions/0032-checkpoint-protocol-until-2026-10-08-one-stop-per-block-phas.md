# ADR 0032: Checkpoint protocol until 2026-10-08: one STOP per block (Phase 9 and later)

- Status: Accepted
- Date: 2026-10-03
- Decided by: Jo, Team J5, chat 2026-10-03: 'b' (option B, one STOP per block), and 'jangan commit terlebih dahulu' (commits are made at the end of the work, grouped by block)

## Context
- PENDING #26: how often the assistant stops and waits for the team until the deadline (2026-10-08, evidence freeze 2026-10-07 night). The team has about 6-8 hours of attention per day (ADR 0019). In Phase 8 the team asked for 8b, 8c and 8d to be run without stopping (chat 2026-10-03); the question stayed open for later phases.

## Options considered
(A) a STOP after every step (ADR 0012 style): most control, most waiting. (B) one STOP per block: a report after each group of work. (C) no STOP until the end of the phase: least waiting, least control.

## Decision
(B), one STOP per block. Chat 2026-10-03 (Jo, Team J5): 'b'. The blocks of Phase 9 are the assistant's proposal and not part of the decision: 9a encode/decode and compress/decompress; 9b the FO pieces (re-encryption, constant-time comparison, implicit rejection); 9c the controller for KeyGen, Encaps and Decaps with all pinned ACVP groups and the Quartus compile. Chat 2026-10-03 (Jo): 'jangan commit terlebih dahulu': commits are made when the work is finished, grouped by block (not one commit per block-step during the work).

## Consequences
- After each block the assistant writes a short report and stops; the team says whether to continue. Within a block there is no stop. Each block still has its test plan and adoption rule written before RTL and before measuring.
- Unchanged by this decision: the assistant never ticks an Approval box, never pushes, never decides an open PENDING item (it records a Proposed ADR), and never commits the status documents without being told.
- Until the team says to commit, the work stays uncommitted in the working tree; a commit history made afterwards must follow the real order of the work (plan, golden, RTL, tests, evidence, ADR, result) and must not suggest a timing that did not happen.

## Evidence
- `docs/decisions/PENDING.md` #26; `docs/decisions/0019-*.md` (checkpoint context); `docs/decisions/0012-*.md`.
