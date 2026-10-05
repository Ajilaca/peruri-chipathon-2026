# ADR 0017: Memory and schedule phase between Phase 5 and Phase 6 (PENDING 19): scope S6-S9, rules, branch

- Status: Accepted
- Date: 2026-10-02
- Decided by: Jevan, Team J5 (chat 2026-10-02, answered the three ADR questions)

## Context
- ADR 0010 (Accepted): 50 MHz is a best-effort project target, not a Phase 5 gate; the C3-P6 critical path is the memory read
  (MEASURED: 21.292 ns of 29.345 ns, then `sub_mod` 4.348 ns and the DSP 3.705 ns,
  `evidence/phase05/baseline/c3p6_critical_path.md`). Phase 5 fixed schedule, memory, L and P.
- Phase 5 result (`docs/results/phase05.md`): arithmetic changes saved area (C4b-B 9,166-9,208 ALM vs C3-P6 10,484-10,516)
  but did not move Fmax beyond the seed spread; information compiles at 20.000 ns fail for C3-P6 (setup -2.059 ns) and C4b-B
  (-2.557 ns) (`evidence/phase05/closure/info_20ns.md`).
- The decision package (`evidence/phase05/baseline/decision_package.md`) lists the memory / pipeline levers
  with ESTIMATE costs; ADR 0012 sets the adoption rules (t_NTT and t_INTT at the median Fmax of seeds 1-6 better than the previous
  step, constant cycles, NTT-core ALM <= 12,573).
- PENDING #19 asks for the name and position of the phase that holds this work. The team instruction (2026-10-01, S5) asks for a
  "memory and schedule" phase after Phase 5 and before Phase 6, containing steps S6-S9.
- Working base for the steps below: C4b-B (Barrett). ADR 0013 (Barrett) is still Proposed (PENDING #23); if the team picks
  Montgomery instead, the base changes and the baseline numbers are re-measured.

## Options considered
(a) A separate phase between Phase 5 and Phase 6, with its own branch, test plan, result artifact and Approval gate
    (proposed name: "Phase 5M: memory and schedule"; numbering is the team's, e.g. "Phase 5.5"). Cost: one more phase in the roadmap and
    one more approval; benefit: the memory path is changed under the same evidence rules as every earlier phase, and Phase 6 starts
    from a measured base.
(b) A sub-phase inside Phase 6 (operation-level scheduling). Cost: mixes a kernel-level timing change with the operation-level
    schedule, so a result cannot be attributed to one change; Phase 6 already has its own scope.
(c) No such phase: stay at about 35 MHz and treat 50 MHz as unreachable. Cost: the project target of ADR 0010 is dropped
    without the measured steps that could reach it; no new RTL risk.

## Decision
Option (a) accepted 2026-10-02 by Jevan, Team J5: a separate phase between Phase 5 and Phase 6, with the content and rules below. The proposed name "Phase 5M: memory and schedule" is used as the working name (the answer chose option (a), whose text proposed it; the team may rename it). Working base: C4b-B (Barrett, ADR 0013 accepted).

Content (each step is one change, one test plan written before measuring, one STOP for the team):
| Step | Change | Rule |
|---|---|---|
| S6 | INTT without the scaling pass: halve in every layer (3303 = 2^-7 mod q, 7 layers), golden `intt_halving()` equal to `intt()` on 256 basis vectors, basis x (q-1), random and edge vectors; constants from a script; remove S_SCALE and the scaling multiplier | ADR with the equivalence argument; `half_mod` exhaustive over 3,329 values; INTT cycles = NTT cycles; negative control (one layer without halving) must fail |
| S7 | Split the memory read mux (decision package lever 1: P -> 7, no stall, +1 cycle) | hazard scoreboard plus negative control; ADR 0012 adoption |
| S8 | Write-path register (lever 4: P -> 8, one data-independent stall per transform) | ADR 0012 adoption plus a 20 ns information compile |
| S9 | M10K / synchronous-read study: documentation only, no RTL; port needs vs M10K, options (more 1R1W banks, two coefficients per word, double-pumping, schedule change), conflict-free evidence conditions, ESTIMATE-labelled ALM / M10K | the team chooses; no adoption rule (no RTL) |

Common rules: the mathematics stays locked (C1); every RTL file follows the project RTL rules; Verilator `-Wall` and slang lint; Verilator
and Icarus simulation; Quartus seeds 1-6 one at a time in the background; full CRG gate; a local commit per step, never a push by the
assistant; Approval boxes are ticked only by a team member. Proposed ordering rationale (INFERENCE): S6 removes a multiplier and a
pass (area, no memory change), S7 and S8 target the measured critical segment, S9 is the study that decides whether a larger
memory change is worth a separate phase.

Branch and approval: after the team approves, a new branch is created from the Phase 5 result (proposed name `phase5m-memory-schedule`,
or as the numbering decision dictates). This record does not create it.

## Consequences
- If accepted: PENDING #19 is closed; `docs/ROADMAP.md` gets the new phase (done-criteria, evidence folder, Approval gate) in a
  separate change; Phase 6 starts only after this phase's Approval.
- If rejected: S6-S9 are not started; 50 MHz stays a best-effort target without a planned path.
- The 12,573 ALM limit and the cycle rule of ADR 0012 stay in force; exceeding either needs a new team decision.
- Levers 1 and 4 together could cost up to about 1,300 ALM in the worst case of the measured per-stage range (ESTIMATE, decision
  package), against the measured margin; the measured result decides, not this estimate.

## Evidence
- `docs/decisions/0010-*.md`, `0012-*.md`, `0013-*.md`
- `evidence/phase05/baseline/c3p6_critical_path.md`, `decision_package.md`, `stall_cycles.txt`
- `evidence/phase05/closure/info_20ns.md`, `docs/results/phase05.md`

## Amendment note (2026-10-02, Jevan, Team J5; the decision above is unchanged)
The "full CRG gate" of the common rules is run as the Phase 0-5 regression once, at S8, on the final tree of S6-S8 (not after every step);
each step still runs its own specific tests, formal proofs and Quartus seeds. Details: `evidence/phase05m/test_plan.md`, Amendment A1.
