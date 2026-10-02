# ADR 0019: Minimal path to a full ML-KEM-768 core before Thursday 2026-10-08 (supersedes ADR 0018 scope)

- Status: Accepted
- Date: 2026-10-02
- Decided by: Jevan, Team J5 (chat 2026-10-02: phases 8 and 9 must exist; option 'Jalur minimal ke ML-KEM penuh'; 6-8 h per day)

## Context
- ADR 0018 (Accepted 2026-10-02) planned: finish Phase 5M S6-S8, then Keccak K0, Section 3 of the proposal; Phases 8 and 9 not attempted.
- The team then said Phases 8 and 9 must be done, and chose the "minimal path to a full ML-KEM" option, with 6-8 hours per day of team attention.
- Deadline: Thursday 2026-10-08 (from Friday 2026-10-02; time of day not given; evidence freeze planned for Wednesday night).
- Estimates (ESTIMATE, low confidence; basis: step S6 took about 6 hours wall-clock): Keccak K0 8-14 h; baseline samplers 8-12 h; minimal full
  ML-KEM controller and integration 35-60 h; Section 3 of the proposal 6-10 h. Total about 57-96 h against six days. Success is **not
  guaranteed**; the tiers below keep partial results reportable.
- Known risks: (1) the polynomial storage of the whole KEM does not fit as flip-flop memory like the NTT core's (ADR 0009 budget is for the NTT
  core only; the full design must fit 41,910 ALM, fitter denominator), so storage of the other polynomials likely needs M10K; (2) the roadmap
  requires an ADR on whether the FIPS 203 input checks run in hardware or on the HPS before Phase 9 starts; (3) Decaps needs constant-cycle
  evidence for valid and rejected ciphertexts.

## Options considered
(a) **Minimal path**: stop Phase 5M after S6; skip Phase 6; skip the Phase 8 optimisations (8a two rounds per cycle, 8c matrix on the fly,
    8d overlap) and use baseline samplers; integrate a full ML-KEM-768 with the simplest controller; optimisations stay planned work.
(b) Parallel by block with other team members on separate branches (same scope as (a)). Not chosen in the answer, but compatible with (a) if
    members join; integration and verification stay under the same rules.
(c) Keep ADR 0018 (no Phases 8-9 before the deadline).

## Decision
Option (a), chosen by Jevan, Team J5. ADR 0018 is superseded by this record (its status header is updated; its text is unchanged).
1. **Phase 5M stops after S6.** S7, S8 and S9 are not done before the deadline (the work is kept in the roadmap as future work); ADR 0017
   stays Accepted, its scope is reduced by this record. The S6 report is still written and its verdict is the team's.
2. **Phase 6 is skipped** before the deadline (a trivial fixed operation order is used in the controller), recorded as a deviation from the
   roadmap's "approval of phase N before N+1".
3. **Order of work (each block: golden model first, lint Verilator -Wall + slang, both simulators, bit-exact tests, constant-cycle evidence where it
   applies):** Phase 7 Keccak K0 (SHA3-256/512, SHAKE128/256) -> baseline samplers (SampleNTT, SamplePolyCBD; non-streaming-optimised, from the K0
   stream) -> encode/decode and compress/decompress (no division) -> K-PKE KeyGen / Encrypt / Decrypt -> ML-KEM Encaps / Decaps with the FO
   transform, constant-time comparison and implicit rejection -> pinned NIST ACVP vectors.
4. **Reporting tiers** (a tier is only claimed when its evidence exists in `docs/evidence/`): T1 K0 and samplers bit-exact; T2 K-PKE KeyGen /
   Encrypt / Decrypt bit-exact; T3 full ML-KEM Encaps / Decaps against the ACVP vectors with constant-cycle evidence. A tier that is not reached is
   described in the proposal as not completed.
5. **Process lightening, without weakening any correctness check:** blocks that have no adoption rule use one Quartus compile (default seed, labelled
   single compile) instead of a seed sweep; formal proofs only where they are cheap and already patterned; the full Phase 0-5 regression runs once,
   on the final integrated tree, as in the spirit of Amendment A1 of the 5M test plan. Lint, both simulators, golden bit-exactness and the
   constant-cycle checks are not reduced.
6. Section 3 of the proposal is written in parallel from the repository's evidence only, under the claim rules; nothing is claimed beyond the tiers
   reached; evidence freeze Wednesday 2026-10-07 night.

## Consequences
- Two items must be decided by the team before the controller work reaches them: PENDING #25 (FIPS 203 input checks in hardware or on the HPS) and
  PENDING #26 (checkpoint protocol: fewer STOPs, see below).
- The proposal states measured results for NTT/INTT and for the tiers reached; optimisations (Phase 6, 8a, 8c, 8d, S7-S9) appear as planned work only.
- If resource overflow appears at integration, it becomes a team decision (ADR), not a silent change; the 12,573 ALM budget stays the NTT-core
  budget (ADR 0009, 0012).

## Evidence
- `docs/decisions/0017-*.md`, `0018-*.md`, `docs/ROADMAP.md` Phases 6-9, chat 2026-10-02.

## Amendment note (2026-10-02, Jevan, Team J5; the decision above is unchanged)
S7 and S8 of ADR 0017 are kept as **stretch work, not scheduled**: the team may reopen them only if time remains after tier T2 (K-PKE
KeyGen / Encrypt / Decrypt bit-exact) is reached, and only by a new explicit instruction. They would start from C4b-B on branch
`phase5m-memory-schedule` and follow the S6 pattern (test plan and adoption rule first, ADR 0012). Because they modify the memory and core
files, merging them after the integration work started requires the full Phase 0-5 regression (Amendment A1 of the 5M test plan) and a
re-run of the integrated tests; otherwise they stay unmerged as future work. The Fmax lever without RTL changes (Quartus performance settings,
Phase 4 evidence `ghrd_plus_c3p6_integration_2026-10-01.md`) is allowed for the final compile as an information result, labelled with its settings.
