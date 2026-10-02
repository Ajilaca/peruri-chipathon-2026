# ADR 0018: Scope and order until the Thursday 2026-10-08 deadline: finish 5M, then Keccak baseline, defer Phase 6, write proposal Section 3

- Status: Superseded by 0019
- Date: 2026-10-02
- Decided by: Jevan, Team J5 (chat 2026-10-02: deadline answer and strategy option 'Selesaikan Fase 5M lalu Keccak baseline')

## Context
- The team has until **Thursday 2026-10-08** (counted from Friday 2026-10-02; the time of day was not given, so a Wednesday-night freeze is
  planned to be safe). The deliverable named in the chat is the **complete proposal, including Section 3 (pages 4-6)**, which was not written
  before (CLAUDE.md C4: "do not write it until asked"; the team has now asked by naming it as the deadline deliverable).
- Remaining work on the roadmap, ESTIMATE (low confidence, basis: step S6 took about 6 hours wall-clock): Phase 5M S6-S9 about 12-13 hours
  from 2026-10-02 evening; Phase 6 12-20 h; Phase 7 8-14 h; Phase 8 30-50 h; Phase 9 45-80 h. Phases 6-9 together (95-165 h) do not fit in six
  days; Phase 10 is blocked by the missing board (PENDING #8).
- Measured so far: C4b-B NTT/INTT core, kernel-only Quartus and simulation evidence (`docs/results/result_phase5.md`); S6 measured, its
  verdict pending (see ADR 0019 once written).

## Options considered
(a) **Finish Phase 5M (S6-S8, S9 as a document if time allows), then the Phase 7 Keccak baseline (K0); write Section 3 in parallel.**
    Two measured blocks (NTT/INTT and Keccak) at the deadline. Cost: Phase 6, 8, 9 not done; Phase 7 starts without Phase 6.
(b) **Stop Phase 5M after S6, go to Keccak now.** Same two blocks, earlier Keccak start, more slack for the proposal; S7-S8 (Fmax work) dropped.
(c) **No new RTL; spend all time on the proposal and the evidence summary.** Lowest risk for the document; no new measured block.

## Decision
Option (a) chosen by Jevan, Team J5, with Section 3 of the proposal to be written. Consequences the team accepted by choosing it:
1. Phase 5M continues in order S6, S7, S8, with S9 only as a document and only if time allows; each step still stops for the team.
2. **Phase 6 is deferred (not done before the deadline).** Phase 7 (Keccak K0, `docs/ROADMAP.md`) starts after S8 without Phase 6's approval.
   This deviates from the roadmap's "approval of phase N before N+1" and is recorded here; Phase 6 stays on the roadmap as future work.
3. **Phases 8, 9, 10 and 11 are not attempted before the deadline** and are described in the proposal as planned work only, with no result claimed.
4. Section 3 of the proposal (pages 4-6) is written from the repository's evidence only, under the claim rules (C2, C3, C8, `/proposal-claims`);
   numbers are traced in `docs/proposal/CLAIMS_REGISTER.md`. Nothing is claimed for the full ML-KEM, for speed-up versus software, for power,
   or for hardware validation.
5. Freeze: no new measurement is added to the proposal after Wednesday 2026-10-07 night; later results go to the repository only.

## Consequences
- Plan (ESTIMATE, may slip; ADR 0012 adoption rules and the one-change-per-step rule are unchanged): Fri 10-02 evening S6 report; Sat S7;
  Sun-Mon S8 (with the one full regression, Amendment A1 of the 5M test plan); Mon-Tue Phase 7 (K0); Tue-Wed proposal Section 3 and the claim
  check; Thu final review and submission. If S8 is not adopted or runs late, Phase 7 starts anyway and S8's result is reported as measured.
- If Phase 7 does not finish, K0 is reported as "not completed" and the proposal says so; a partial Keccak is not presented as a result.
- Any claim in the proposal about Keccak is allowed only after K0 has a passing test log and a Quartus report in `docs/evidence/`.

## Evidence
- `docs/ROADMAP.md` (Phases 6-10), `docs/decisions/0017-*.md`, `docs/results/result_phase5.md`, chat 2026-10-02.
