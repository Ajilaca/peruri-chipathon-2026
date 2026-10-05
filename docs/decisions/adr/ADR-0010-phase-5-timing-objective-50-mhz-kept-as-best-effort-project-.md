# ADR 0010: Phase 5 timing objective: 50 MHz kept as best-effort project target; ADR 0006 expectation corrected

- Status: Accepted
- Date: 2026-10-01
- Decided by: Faza Dzil, Team J5 (direction stated and confirmed in the session of 2026-10-01)

## Context
- ADR 0006 (Accepted) set 40.000 ns as the Phase 4 milestone and 20.000 ns (50 MHz) as the end goal "after Phase 5",
  and expected reaching 50 MHz to need the Phase 5 arithmetic work as well as pipelining. That expectation came
  from the P = 0 path breakdown, in which the divider (`%` in `modmul_reduce`) was about 44 ns
  (`evidence/phase04/k1_l8_worst_path_breakdown.md`).
- Phase 5 (`docs/ROADMAP.md`) keeps the schedule, the memory, L and P fixed; only `rtl/arith/` units change.
- New evidence on the selected C3-P6 (`evidence/phase05/baseline/c3p6_critical_path.md`):
  - MEASURED: the 300 worst setup paths (Slow 1100mV 100C, default seed, 40.000 ns) all start at the memory's
    slot-arbitration registers; the worst one (slack +10.753 ns) is memory read decode + read mux ≈ 21.3 ns, then the
    butterfly input `sub_mod(b, a)` ≈ 4.3 ns, then the DSP multiplier ≈ 3.7 ns. No reducer-internal path is among
    the 300; reducer segments have slack +23.6 to +24.5 ns.
  - INFERENCE: the memory read part alone is longer than 20 ns, so with memory, schedule, L and P fixed, Phase 5
    arithmetic changes cannot reach 20.000 ns. Removing the `sub_mod` entirely would leave that segment at about
    25 ns (ESTIMATE), about 40 MHz.

## Options considered
1. **Keep 50 MHz as the project target, best-effort, not a Phase 5 gate**; correct ADR 0006's expectation; do the
   work that touches memory / P / schedule as a separate phase or sub-phase after 5a/5b, with its own ADR and test
   plan.
2. Drop 50 MHz and fix the project clock at the met 40.000 ns (25 MHz, experimental target per ADR 0006).
3. Widen Phase 5's scope to include memory / P / schedule changes now. Conflicts with the roadmap's "schedule,
   memory, L and P stay fixed" and mixes arithmetic and memory effects in one set of measurements.

## Decision
1. **50 MHz (20.000 ns) stays the project's timing target, on a best-effort basis.** It is neither a guarantee nor a
   Phase 5 gate.
2. **ADR 0006's expectation is corrected:** reaching 50 MHz is not expected from Phase 5 arithmetic alone, because the
   critical path of C3-P6 lies in the memory read path (MEASURED, Context). ADR 0006's text is not changed; this ADR
   records the correction.
3. Work that changes the memory, P or the schedule (e.g. a register inside the read mux, P > 7 with stalls, a write-path
   register, synchronous-read memory) is done **as a separate phase or sub-phase after 5a/5b**, with its own ADR and
   test plan (selection rule written before measuring), bit-exact / constant-cycle / hazard re-verification (negative
   controls beyond the slack must still fail) and compiles at 20.000 ns with slack reported per segment.
   **Its name and position in the roadmap are still open** and will be decided by the team.
4. Phase 5 (5a–5d) proceeds as in the roadmap: arithmetic correct and measured; Fmax, slack and ALM reported against
   C3-P6. Phase 5 passes or fails on the roadmap's PASS criteria, not on 50 MHz.

## Consequences
- "50 MHz after Phase 5" is no longer the stated expectation anywhere it appears (ADR 0006 consequences,
  `HANDOFF.md`, result files, reports); new text must cite this ADR.
- A follow-up decision is needed for the memory / P / schedule phase (name, position, levers, acceptable cycle
  increase, ALM limit for added registers). Data prepared for it:
  `evidence/phase05/baseline/stall_cycles.txt` (stall cycles per P, perhitungan tim) and
  `evidence/phase05/baseline/decision_package.md`.
- The constant-cycle rule is unchanged; a later change of P may change the cycle counts (119 / 375), which would be
  recorded in its own ADR.
- No claim of 50 MHz may be made until a Quartus compile at 20.000 ns meets timing (CLAUDE.md §3).

## Evidence
- `evidence/phase05/baseline/c3p6_critical_path.md`, `c3p6_top300_path_classes_slow100.txt`
- `evidence/phase04/quartus_C3-P6.md`, `seed_sweep.md`
- `evidence/phase04/k1_l8_worst_path_breakdown.md`
- `docs/decisions/adr/ADR-0006-phase-4-target-clock.md`, `docs/decisions/adr/ADR-0009-phase-4-final-decision-l-8-p-6-c3-p6-and-a-30-alm-design-bud.md`
