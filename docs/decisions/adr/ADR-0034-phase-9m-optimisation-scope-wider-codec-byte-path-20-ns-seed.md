# ADR 0034: Phase 9M optimisation scope: wider codec byte path, 20 ns seeds, K0 hash core, host-engine overlap; second sampler kept as an idea

- Status: Accepted
- Date: 2026-10-04
- Decided by: Faza Dzil (Team J5), chat 2026-10-04

## Context
Phase 9 (C7-core, `docs/results/phase09.md`, merged in PR #9) runs KeyGen, Encaps and Decaps of ML-KEM-768 in RTL; all pinned ACVP vectors pass in simulation. Jo closed Phase 9; Faza Dzil takes over optimisation and repository cleanup (chat 2026-10-04). Jo had said the proposal stops at Phase 9; Phases 10-12 stay pending (no board, PENDING #8).
A cycle profile of the core (`evidence/phase9m/profile.md`, MEASURED in simulation) shows where the cycles go: the K-PKE engine 65-72 %, loading polynomials into the engine 0-23 %, storing them 9-26 %, hashing and comparison about 3 %. Loading and storing a polynomial with d = 12 or d = 10 is limited by the one-byte-per-cycle path of the codec, not by the one-coefficient-per-cycle port of the engine.

## Options considered
Listed to Faza Dzil in chat 2026-10-04 (savings are ESTIMATE from the profile):
1. Wider codec byte path (two bytes per cycle): about 9 % of KeyGen, 6 % of Encaps, 7 % of Decaps; only Phase 9 files change; about one working day.
2. The core at a 20 ns constraint: already met at seed 1 (MC-20); seeds 1-6 make it a full measurement; no RTL change.
3. The K0 sponge for the hash instance: about 2,500 ALM less for about 120 more cycles per operation; a parameter (`HASH_C5`).
4. Overlap of polynomial loads and stores with the engine: up to 25-32 % in theory; needs the engine host port to work while the engine runs, i.e. a new variant of frozen Phase 6-8 files; about 2-4 working days, high risk.
5. A second sampler for the matrix A: about 900 cycles; a new engine variant and about 5,300 ALM more; about 2-3 working days, high risk.

## Decision
Faza Dzil, chat 2026-10-04: "kita kerjakan no 1 2 3 4 saja 5 kita simpan sebagai ide/solusi yang mungkin digunakan"; then "kerjakan 1 dulu kemudian stop dan lapor ke saya, parameter apa yang diukur, penggunaan resource dan seterusnya, lakukan untuk semuanya; kita bikin branch baru fase 9m optimasi".
- Items 1, 2, 3 and 4 are done in Phase 9M (branch `phase9m-optimisation`), one at a time, starting with item 1; after each item a report (parameters measured, resources, timing, cycles) and a STOP (as ADR 0032).
- Item 5 (second sampler) is kept as an idea for later work and is not implemented.
- Each item has its own test plan and adoption rule written before its RTL or measurement; the adoption of a result is recorded as a Proposed ADR for the team.

## Consequences
- Phase 9 files may change only as new variants or behind a parameter whose default keeps the Phase 9 behaviour; the Phase 9 tests are rerun at the default (regression). Frozen Phase 6-8 files are not edited (item 4 makes a new variant).
- The evidence freeze is Wednesday night 2026-10-07; item 4 (ESTIMATE 2-4 days) may not be finished by then. What is not finished and verified is reported as not done, not claimed.
- The Approval box of `docs/results/phase09.md` is still empty (2026-10-04); the team ticks it.

## Evidence
`evidence/phase9m/profile.md`, `docs/results/phase09.md`, `docs/decisions/adr/ADR-0033-phase-9-c7-core-as-built-ml-kem-768-in-simulation-acvp-100-p.md`.
