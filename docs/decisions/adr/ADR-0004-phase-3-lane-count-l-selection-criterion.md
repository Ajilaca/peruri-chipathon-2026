# ADR 0004: Phase 3 lane-count (L) selection criterion

- Status: Accepted
- Amended 2026-10-01 by ADR 0009: the 25% / 10,478 ALM value below is superseded for the NTT core from Phase 4
  on by a 30% / 12,573 ALM design budget. The text below is kept unchanged as the record of the 2026-09-29 decision.
- Date: 2026-09-29
- Decided by: Faza Dzil, Team J5

## Context
`docs/ROADMAP.md` Phase 3 sweeps lane count L in {1, 2, 4, 8} over the Phase 2 banked
memory (config C2-L1..C2-L8), measuring ALM, registers, M10K, DSP, Fmax and cycle counts
for each. The Phase 3 spec requires: "The selection criterion (for example, lowest AT
within a stated resource budget) is written into an ADR before the sweep is measured."
This record exists to fix that criterion *before* the four Quartus compiles run, so the
choice of L is not made by eyeballing the comparison table after the fact.

Two prior conditions affect this decision and must be named, not hidden:
1. Phase 1 (C0) and Phase 2 (C1) both FAILED timing (CRG-9) at the provisional 20.000 ns
   clock; there is still no target-clock ADR. Any area x delay (AT) figure computed from
   an unmet-timing Fmax is only a relative comparison across L, not an absolute claim the
   design meets any real clock target.
2. Phase 2's M10K goal was not achieved (0/553 M10K; async-read limitation). If this is
   still unresolved when the L sweep runs, all four L configs will also show 0 M10K, and
   ALM usage will scale with L largely through LUT-based memory replication rather than
   block-RAM banking. That changes what "resource budget" means for this sweep and should
   be decided together with this ADR, not silently absorbed into it.

## Options considered
The Phase 3 spec's own example is "lowest AT within a stated resource budget." Concretely,
for team J5 to decide:

1. Lowest AT (Area x Time) product, no fixed budget - for each L, AT = ALM_used x
   (1 / Fmax_measured). Pick the L with the smallest AT. Simple, single-number ranking;
   but on a Cyclone V 5CSEBA6U23I7 (41,910 ALM datasheet ceiling) a large L could still win
   on AT while eating an impractical fraction of the device, leaving no headroom for
   Keccak, the sampler, or protocol logic sharing the same fabric.
2. Lowest AT within a stated ALM budget (e.g. reserve X% of 41,910 ALM for the NTT/INTT
   block; disqualify any L exceeding it, then rank the rest by AT). Matches the spec's
   own example. Requires the team to state the budget percentage now, as part of this ADR,
   not as a post-hoc filter.
3. Highest throughput (lowest total cycles for NTT+INTT+pointwise) within the same ALM
   budget, ignoring Fmax differences across L (since none of C0-C1 meet timing yet, a
   throughput-in-cycles metric is arguably more honest than an Fmax-weighted one right now).
4. Keep L configurable, defer the choice - ship all four configs, expose L as a
   synthesis-time parameter, and let Phase 4+ (pipelining) or the final proposal pick per
   context. Satisfies "keeping L configurable" allowed by the Phase 3 PASS criteria, but
   defers a decision the spec asked to be fixed before measuring.

None of these have been measured yet (no Quartus C2-L* evidence exists at time of writing);
this ADR is about the *rule*, not the *result*.

## Decision
Two-stage criterion, in priority order:

1. Primary - minimize cycle count, subject to an ALM budget of 25% of the target
   device (5CSEBA6U23I7, 41,910 ALM datasheet ceiling) -> budget = 10,478 ALM. Any
   L whose Quartus C2-L<n> compile exceeds 10,478 ALM is disqualified regardless of its
   cycle count. Among the remaining (in-budget) L values, the one with the lowest total
   cycle count (NTT + INTT + pointwise product, from cocotb, cycle-identical requirement
   from Phase 2 still applies within each L) wins. This is option 3 from the list above,
   chosen because C0/C1 timing is still unmet, so cycles are the more honest metric
   right now than an Fmax-weighted AT product.
2. Secondary - informational only, does not auto-override the primary pick. Once a
   timing-valid constrained clock exists (i.e. once the target-clock ADR lands and a
   config actually meets timing), re-evaluate the primary-selected L's AT product
   (ALM x 1/Fmax) against the same 10,478 ALM budget, for the record. If this secondary
   evaluation suggests a different L would have been better on AT, that is not applied
   automatically - changing the selected L after this ADR requires an explicit new ADR
   (or an update to this one) stating why.

If no L fits within the 10,478 ALM budget, or if Phase 2's M10K goal (async-read
limitation, `docs/results/phase02.md`) is still unresolved when the sweep runs
(all L configs then compete on LUT-based memory replication rather than block-RAM
banking), that is reported as a finding in `docs/results/phase03.md`, not silently
absorbed - this ADR does not pre-decide what happens if the budget is infeasible.

## Consequences
- The Phase 3 sweep must run all four L in {1,2,4,8} through Quartus and cocotb
  regardless of the primary criterion outcome (PASS criteria require all four measured
  and compared), then apply the ALM-budget filter and cycle-count ranking to pick one.
- `docs/results/phase03.md` must show: the ALM budget value (10,478), which L
  values passed/failed the budget, the cycle counts for the in-budget candidates, the
  selected L, and - once timing is valid at some later phase - the secondary AT
  re-evaluation, explicitly marked as informational.
- Any future change of the selected L must cite this ADR and either supersede it or add
  a follow-up ADR; it must not be a silent change in `docs/ROADMAP.md` alone.
- This does not resolve PENDING #3 (DMA vs memory-mapped transfer) or the missing
  target-clock ADR; both remain open and are referenced, not decided, here.

## Evidence
Phase 3 spec (pasted by team, 2026-09-29, `docs/ROADMAP.md` Phase 3 section).
Phase 1/2 timing status: `docs/results/phase01.md`, `docs/results/phase02.md`.
