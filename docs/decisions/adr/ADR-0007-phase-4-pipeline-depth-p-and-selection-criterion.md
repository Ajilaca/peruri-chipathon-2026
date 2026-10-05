# ADR 0007: Phase 4 pipeline depth P and selection criterion

- Status: Accepted
- Amended 2026-10-01 by ADR 0009: candidate condition 3 uses 12,573 ALM (30%) instead of 10,478 ALM; rule,
  candidate set and other conditions unchanged. The text below is kept unchanged as the record of 2026-09-30.
- Date: 2026-09-30
- Decided by: Faza Dzil, Team J5

## Context
Phase 4 (`docs/ROADMAP.md`) pipelines the butterfly of the selected configuration, C2-K2-K1 at L = 8
(ADR 0005), as configuration C3: "pipeline depth P as a parameter over a small documented set; hazard
handling between NTT layers (stall or schedule), with the stall cost counted. No arithmetic changes;
no layer merging." The PASS criteria ask for an ADR for the chosen P. As with ADR 0004 for L, the set
of P values and the rule for choosing among them are to be fixed **before** anything is measured.

**Definition proposed.** P = the number of register stages on the path of one butterfly from the
cycle its addresses are issued to the cycle its results are written to memory. P = 0 is today's
C2-K2-K1: read, compute and write in one cycle. A butterfly issued at cycle t writes at cycle t + P.

Facts available today (no new compile was run for this ADR):
- MEASURED worst path of the P = 0 starting point, by block
  (`evidence/phase04/k1_l8_worst_path_breakdown.md`): 129.6 ns data delay =
  address generation about 5 ns, **memory access (bank slot arbitration across 16 ports, read mux)
  about 57 ns**, butterfly pre/post logic about 5 ns, multiplier about 4 ns, **divider (`%` in
  `modmul_reduce`) about 44 ns**, write path about 9 ns.
  Candidate register positions that follow from it: (c1) after address generation / bank mapping,
  (c2) inside the memory access path, (c3) after memory read, (c4) between multiplier and divider,
  (c5) inside the divider chain, (c6) before the memory write.
- Hazards, from an exhaustive check of the existing lane schedule
  (`evidence/phase04/layer_boundary_slack.txt`, perhitungan tim): inside a
  layer every address is read and written exactly once, so there is no read-after-write hazard within
  a layer for any P. At a layer boundary the next layer must not read an address whose write is still
  in the pipeline; for L = 8 the tightest boundary has 7 cycles of slack in both directions, so
  **P ≤ 7 needs no stall at any layer boundary** with the schedule unchanged. P > 7 would need stall
  cycles or a changed schedule.
- ALM: C2-K2-K1-L8 is at 9,754 ALM, 724 below ADR 0004's 10,478 ALM budget; fitter packing alone was
  seen to move totals by up to about 370 ALM (`k1_experiment.md`, caveat 1).

Consequences of pipelining that hold for every option below:
- **Latency / cycles.** For P ≤ 7 (no boundary stalls): NTT = 7 × 16 sub-cycles + P cycles to drain
  the pipeline + the existing overhead, i.e. 113 + P cycles (ESTIMATE from the FSM structure, to be
  measured in simulation). INTT additionally has the 256-cycle ×3303 scaling pass (369 cycles today);
  it grows by P for the drain, and by more if the scaling pass reuses a pipelined multiplier. Cycle
  counts stay data-independent (constant-time requirement) and are re-measured per P.
- **Throughput.** What matters is time per transform = cycles(P) / Fmax(P). A deeper pipeline adds a
  few cycles (about 1–6% at L = 8 for P ≤ 7) and is worth it only if Fmax rises by more than that.
- **Resources.** Each stage that carries the datapath registers 2 × 12 data bits and 2 × 8 write-address
  bits per lane, about 320 flip-flops per stage at L = 8 (ESTIMATE from signal widths; stages on the
  address side carry less, stages inside the divider carry the partial remainder per lane). Registers
  often pack into ALMs already in use, but that is not guaranteed; the 724-ALM margin can be consumed.
- **Memory ports.** Today each port reads and writes the same address in the same cycle. With P > 0 a
  cycle carries the reads of one set of butterflies and the writes of an earlier set, so a bank sees up
  to 2 reads and 2 writes of different addresses per cycle. The flip-flop memory can serve that, but
  `poly_mem_multiport` needs separate read and write addressing (a new variant file; the C2 memory stays
  frozen), and the Phase 2/3 "at most 2 accesses per bank per cycle" proof then applies to reads and to
  writes separately, not as one 2-port budget. A registered read (c3) is also the precondition for M10K
  inference, but 2R + 2W per bank does not map onto one true-dual-port M10K; M10K remains a separate
  question (not decided here).
- **Verification.** New RTL files only (C2, C2-K2 and C2-K2-K1 stay frozen); bit-exact against the golden
  model on both simulators for every P; dedicated tests at layer boundaries; constant cycle count; the
  formal `bank_overflow_o` property restated for separate read and write schedules.

## Options considered
### A. Which P values to build and measure
1. **P ∈ {0, 1, 2, 3}, registers at block boundaries only** (c1, c3, c4, c6; none inside the memory
   access path or the divider).
   For: smallest RTL change; clearly within "no arithmetic changes"; 4 Quartus revisions.
   Against: by the path breakdown the clock period cannot go below the longest single block, about
   57 ns (about 17 MHz, ESTIMATE) — about 2× the current Fmax at best, far from 50 MHz and short of
   25 MHz.
2. **P ∈ {0, 2, 4, 6}, registers also inside the memory access path (c2) and the divider (c5).**
   For: the only kind of set that can approach 20–40 ns by the estimate; all values ≤ 7, so no
   boundary stalls; 4 revisions.
   Against: larger RTL change (memory variant with staged slot arbitration; the `%` written as explicit
   staged logic or an instantiated divider with pipeline stages). Needs a team ruling that registers
   inside the reduction — same method, same results, exhaustively checked against `modmul_reduce` — are
   not an "arithmetic change" in the ROADMAP's sense. More registers, so more ALM-budget risk.
3. **P ∈ {0, 1, 2, 4, 7}: a wider sweep up to the largest stall-free depth.**
   For: shows the whole curve, including where returns diminish.
   Against: 5 revisions (about 16 minutes each at L = 8) and 5 RTL variants to verify; P = 7 sits
   exactly at the hazard limit, so its boundary tests carry the most risk.
4. **Retiming-assisted: add P plain register stages at one boundary and let Quartus move them.**
   For: minimal RTL; cut positions chosen by the tool.
   Against: results are tool-dependent and harder to explain; whether Quartus Prime Lite 25.1std retimes
   across the inferred divider and the DSP block on this device has not been tried — it would need a
   trial compile before anything is planned around it.

Exact register positions for each P are part of the Phase 4 test plan (CRG-4), whichever set is chosen.

### B. How to choose P once measured
1. **Smallest P that meets the ADR 0006 target clock** (timing met at all corners), among P that are
   bit-exact, constant-cycle and within the ALM budget. If no P meets it: report, select nothing, the
   team decides. Needs ADR 0006 to set an absolute target.
2. **Minimum time per NTT, cycles(P) / Fmax(P)** (Slow-corner Fmax from the Fmax Summary panel), among P
   that are bit-exact, constant-cycle and within the ALM budget; INTT reported alongside; near-ties go
   to the smaller P. Works without an absolute target, but quotes latency at a measured Fmax rather than
   at a constrained clock.
3. **Highest Fmax within the ALM budget.** Simple; ignores the added cycles.

*First-draft suggestion, superseded by the Decision below:* B.1 as the primary rule if ADR 0006 fixed an
absolute target, B.2 otherwise. The team chose B.2, with "timing met at 40.000 ns" as a condition for
being a candidate (see Decision).

## Decision
**P set: option A.2 — P ∈ {0, 2, 4, 6}.**
- Register stages are allowed inside the memory access path and inside the divider, as well as at
  block boundaries.
- The mathematical function must not change: every P produces bit-for-bit the same NTT/INTT results
  as the golden model (and as P = 0). Pipelining may change timing and latency only. No change to q,
  the reduction method's results, the twiddle values or any other FIPS 203 quantity (ADR 0002).
- P = 0 is the C2-K2-K1 L = 8 configuration, **re-compiled** with the Phase 4 constraint of ADR 0006
  so that all four revisions share one constraint and seed.

**Selection rule: option B.2 — minimum time per NTT — applied to qualified candidates only.**

*Step 1 — measure everything.* All four P values are built, verified and compiled before the rule is
applied; nothing is selected from a partial sweep.

*Step 2 — candidate set.* A value of P is a candidate only if **all four** hold:
  1. bit-exact: PASS (both simulators, against the golden model);
  2. constant cycle count: PASS;
  3. ALM ≤ 10,478 (Quartus fitter);
  4. timing met at 40.000 ns (the ADR 0006 Phase 4 milestone): non-negative worst setup slack **and**
     non-negative worst hold slack at every corner the Timing Analyzer reports.

*Step 3 — the quantity compared.*
- cycles_NTT(P): the NTT cycle count measured in simulation (start to done; the same count on both
  simulators and for every input, by condition 2).
- Fmax(P): the **lowest** Fmax among the slow-corner results that the Timing Analyzer's Fmax Summary
  actually reports for `clk_i` in that revision, i.e.

      Fmax(P) = min over every slow corner c reported of  Fmax_c(P)

  (in the compiles so far the reported slow corners are Slow 1100mV 100C and Slow 1100mV −40C; no
  corner is assumed that the report does not contain). This is chosen as the worst-case slow-corner
  value: the clock the design can run at must hold at the slowest of the slow corners, so the more
  pessimistic figure is the one used. Values are taken as printed in the report, in MHz.
- Time per NTT, in microseconds (cycles divided by MHz):

      t_NTT(P) = cycles_NTT(P) / Fmax(P)

- Reported alongside for every P, candidate or not, but **not** used for the selection:

      t_INTT(P) = cycles_INTT(P) / Fmax(P)

*Step 4 — selection with the near-tie rule.* Let C be the candidate set and

      t_min = min over P in C of t_NTT(P)
      d(P)  = ( t_NTT(P) − t_min ) / t_min          for P in C

  A candidate is in a **near-tie** with the best one when d(P) ≤ 0.05 (its time per NTT is at most 5%
  above the global minimum t_min over the candidate set; candidates are not compared pairwise). The selected depth is the smallest such P:

      P_selected = min { P in C : d(P) ≤ 0.05 }      (equivalently  t_NTT(P) ≤ 1.05 × t_min)

  So the candidate with the minimum t_NTT is selected unless a smaller P is within 5% of it, in which
  case the smaller P is selected. The comparison uses the unrounded quotients.

*If C is empty* (no P satisfies all four conditions), no P is selected automatically: all measured
results are reported and the team is asked for a decision.

## Consequences
- The rule is now consistent with ADR 0006: a P that does not meet timing at 40.000 ns cannot be
  selected, so a selected P always meets the Phase 4 milestone (CRG-9 PASS for that revision).
- P = 0 is measured and reported as the reference but is not expected to be a candidate: the starting
  point's Fmax is 7.68 MHz at the provisional constraint (MEASURED,
  `evidence/quartus/C2-K2-K1-L8.md`), far below the 25 MHz that 40.000 ns requires.
- If no P satisfies the four conditions — for example no P ∈ {2, 4, 6} meets 40.000 ns, or every P > 0
  exceeds 10,478 ALM — nothing is selected; the measurements are reported and the team decides. Both
  are real possibilities: the path estimate suggests about 4 stages are needed for 40 ns, and the
  724-ALM margin of the starting point is not far above the observed fitter-packing swing (about
  370 ALM).
- Because registers may go inside the divider, the `%` in `modmul_reduce.sv` has to be replaced, in a
  new file, by a staged form that can hold registers. `modmul_reduce.sv`, `butterfly.sv`,
  `butterfly_shared.sv`, `poly_mem_multiport.sv` and the C2 / C2-K2 / C2-K2-K1 cores stay frozen; the
  staged reducer must be shown equal to `modmul_reduce` for every a, b in [0, q) (3329² = 11,082,241
  input pairs, small enough to check exhaustively) before it is used.
- Because registers may go inside the memory access path, a new memory variant with separate read and
  write addressing is needed (Context, "Memory ports"); the bank-capacity property is re-proven for the
  read schedule and the write schedule separately.
- All chosen depths are ≤ 7, so by the schedule analysis no stall is needed at layer boundaries; the
  expected cycle counts (NTT about 113 + P) are an ESTIMATE until measured, and the measured stall count
  is reported per P as the ROADMAP requires.
- Four Quartus revisions at L = 8 (about 16 minutes each on this machine, from the Phase 3 compiles),
  named after the configuration IDs to be added to the ablation matrix.
- The exact register positions for P = 2, 4, 6, the hazard tests at layer boundaries and the
  equivalence checks are fixed in the Phase 4 test plan (CRG-4), written after this ADR is accepted and
  before any RTL.
- Options A.1, A.3, A.4 and B.1, B.3 above are not pursued.

## Evidence
- `evidence/phase04/k1_l8_worst_path_breakdown.md`
- `evidence/phase04/layer_boundary_slack.txt` (`scripts/test/pipeline_hazard_slack.py`)
- `evidence/quartus/C2-K2-K1-L8.md`, `evidence/phase03/k1_experiment.md`
- `docs/ROADMAP.md` (Phase 4), `docs/decisions/adr/ADR-0006-phase-4-target-clock.md`
