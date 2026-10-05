# ADR 0012: Rules for timing work beyond Phase 5: cycle increase judged by measured time, 12,573-ALM limit kept

- Status: Accepted
- Date: 2026-10-01
- Decided by: Faza Dzil, Team J5 (session 2026-10-01)

## Context
ADR 0010 keeps 50 MHz as a best-effort target and moves work on the memory, P or the schedule to a separate phase or
sub-phase after 5a/5b. That work may need deeper pipelines with stalls (more cycles) and more registers (more ALM).
The team asked for data before setting limits; it is in
`evidence/phase05/baseline/decision_package.md` and `stall_cycles.txt`:
- MEASURED: C3-P6 NTT 119 / INTT 375 cycles at 34.19 MHz (lowest slow corner) → t_NTT 3.481 µs, t_INTT 10.968 µs
  (INFERENCE); C3-P6 10,484–10,516 ALM over seeds 1–6, margin to 12,573 about 2,060 ALM.
- perhitungan tim / ESTIMATE: P = 7 needs no stall (+1 cycle); P = 8 needs 1 stall (+3 cycles, 2.5 % NTT); P = 12
  needs +12 cycles (10.1 %); stall counts depend only on P, direction and the fixed address schedule, not on data.
- MEASURED Phase 4 stage costs: −27 / +743 / +66 ALM for P0→P2 / P2→P4 / P4→P6; cost depends on the position.

## Options considered
(a) Cycle increase: a fixed percentage limit (e.g. ≤ 5 % or ≤ 10 %), or a time-based rule.
(b) ALM: keep 12,573 as the limit for added registers, or review it.

## Decision
1. Cycle increase (a): an increase in NTT / INTT cycle counts is acceptable only if t_NTT and t_INTT computed with
   the actually measured Fmax (lowest slow-corner Fmax from a Quartus compile in this repository, same rule as
   ADR 0007) are both better than the C3-P6 baseline (3.481 µs / 10.968 µs), and the constant-cycle property
   still holds (CRG-7: identical cycle count for every input, both simulators). No fixed percentage limit. Hypothetical
   clocks (40 / 45 / 50 MHz) are never used for this check.
2. ALM (b): added registers may use the available room, but the NTT core total stays ≤ 12,573 ALM (fitter
   "ALMs needed", ADR 0009) as a hard limit. If a timing change needs more, it is not changed silently: it is
   brought to the team as a new decision.
3. The name and position of the phase that does this work remain open (PENDING #19).

## Consequences
- Any new cycle counts (replacing 119 / 375) are recorded in that phase's ADR together with the measured times.
- ALM saved by 5a / 5b counts as room for added registers within the same 12,573 limit.
- The 12,573 figure remains the NTT-core design budget, not a system budget; Keccak, samplers, controller,
  encode/compress, storage, bridge and SignalTap are NOT MEASURED.

## Evidence
- `evidence/phase05/baseline/decision_package.md`, `stall_cycles.txt`
- `evidence/phase04/quartus_C3-P6.md`, `seed_sweep.md`
- `docs/decisions/0007-*.md`, `0009-*.md`, `0010-*.md`
