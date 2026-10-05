# ADR 0006: Phase 4 target clock

- Status: Accepted
- Expectation corrected 2026-10-01 by ADR 0010: 50 MHz stays the project target on a best-effort basis but is
  not expected from Phase 5 arithmetic alone (C3-P6 critical path lies in the memory read path). The text below is
  kept unchanged as the record of 2026-09-30.
- Date: 2026-09-30
- Decided by: Faza Dzil, Team J5

## Context
`docs/ROADMAP.md` ("Measurement protocol") requires a target clock to be recorded as an ADR at the
Phase 1 gate. That ADR was never written: Phases 1, 2 and 3 were all compiled with a provisional
`create_clock -period 20.000` (50 MHz) and approved as documented baselines with timing not met
(`docs/results/phase01.md`, `phase02.md`, `phase03.md`).

Phase 4's goal is to raise Fmax by pipelining the butterfly. Without a target there is no definition
of "enough", and ADR 0004's secondary AT check cannot run.

MEASURED starting point, configuration C2-K2-K1 at L = 8 (ADR 0005), provisional 20.000 ns clock
(`evidence/quartus/C2-K2-K1-L8.md`):
- Fmax 7.68 MHz (Slow 100C), worst setup slack −110.494 ns; hold is met.
- Worst path, by block (`evidence/phase04/k1_l8_worst_path_breakdown.md`):
  data delay 129.6 ns, of which the memory access path (bank slot arbitration, read mux) is about
  57 ns, the divider (`%` in `modmul_reduce`) about 44 ns, address generation about 5 ns, multiplier
  about 4 ns, write path about 9 ns.

ESTIMATE from those segment lengths (ignores register overhead and re-routing; bounds expectations,
does not predict Fmax): an even split needs about 7 pipeline stages for 20 ns and about 4 for 40 ns;
any period below about 57 ns needs a register inside the memory access path, and below about 44 ns
also one inside the divider chain.

Clock sources: what is actually documented.
- *Board, 50 MHz - sourced.* Intel's DE10-Nano reference design (GHRD), repository
  <https://github.com/intel/de10-nano-hardware>, commit `9b5fc81654c61922b625607d007933a69b5fdb52`
  (2022-08-04): `hdl_src/top.v` declares the FPGA inputs `fpga_clk1_50`, `fpga_clk2_50`,
  `fpga_clk3_50`, and `hdl_src/soc_system_timing.sdc` constrains the design with
  `# 50MHz board input clock` / `create_clock -period 20 [get_ports fpga_clk1_50]`. So a 50 MHz clock
  input to the FPGA fabric exists on the board. (Pin locations are not recorded here; when needed they
  come from Terasic's documentation or that GHRD, never from memory - CLAUDE.md §6.2.)
- *Board, 25 MHz to the FPGA fabric - not sourced.* No document checked for this ADR shows a 25 MHz
  clock input to the fabric. Terasic's *DE10-Nano User Manual* could not be retrieved while writing
  this record (download mirrors refused automated access or had an expired certificate), so nothing
  is claimed from it; it should be read and cited before any board-level clock plan is written.
- *Device.* The fitter reports 6 PLLs on this device (e.g. "Total PLLs 0 / 6" in
  `evidence/quartus/C2-K2-K1-L8.md`), so a 25 MHz clock could be derived from the 50 MHz
  input. That would be a design choice with its own spec and `.sdc` entry (CLAUDE.md §3 rule 7); no
  such clock plan exists yet.
- *Project.* No project specification defines a clock for the accelerator. Every compile so far is a
  kernel-only compile with `clk_i` as a virtual pin and a `create_clock` period chosen by the team; the
  HPS-to-FPGA interface clock is undecided (PENDING #3, #7). No board is attached (PENDING #8), so
  every Fmax is a Quartus number, not a hardware measurement.

Consequently: 50 MHz is the frequency of a real board clock input but is not a stated system
requirement of this project; 25 MHz has no hardware or system requirement behind it at all.

Constraint-comparability note: the fitter is timing-driven, so changing the SDC period changes
placement and the reported numbers. Whatever period is chosen, the P = 0 reference (C2-K2-K1-L8)
has to be re-compiled at that period so every Phase 4 row shares one constraint; the Phase 1–3 rows
stay as measured at 20.000 ns.

## Options considered
1. Keep 20.000 ns (50 MHz) as the absolute target.
   Criterion: timing met (non-negative setup and hold slack, all corners) at 20 ns.
   For: no constraint change, so Phase 4 rows are directly comparable with Phases 1–3; the most
   demanding and therefore most informative target.
   Against: needs about a 6.5× Fmax increase; by the estimate above that means about 7 stages with
   registers inside both the memory access path and the divider. May not be reachable in Phase 4
   alone (arithmetic optimisation, which shortens the divider, is Phase 5), in which case Phase 4
   ends "timing not met" again by definition.
2. Set a lower absolute target, e.g. 40.000 ns (25 MHz).
   Criterion: timing met at 40 ns.
   For: by the estimate about 4 stages; a target Phase 4 can plausibly meet, giving the first
   timing-valid configuration and unblocking ADR 0004's AT check.
   Against: requires a clock the design does not yet have a source for (a PLL-derived clock would
   have to be defined in the spec and `.sdc`, CLAUDE.md rule 7); the P = 0 reference must be
   re-compiled at 40 ns; the value 25 MHz is a convenience, not derived from a system requirement.
3. No absolute target in Phase 4 (relative criterion only).
   Keep 20.000 ns as the constraint, report Fmax per P, and judge Phase 4 by the ADR 0007 criterion
   (for example latency in ns at each P's own Fmax). Fix the absolute target after Phase 5.
   For: no unsupported number is committed to; no re-compile of references; honest about what is
   known today.
   Against: the ROADMAP's missing target-clock ADR stays open; CRG-9 stays FAIL for Phase 4 by
   construction; "never state a latency without its clock" means latencies must be quoted at each
   configuration's measured Fmax, which is not a clock the design is constrained to.
4. Two-tier: a Phase 4 milestone plus a stated end goal.
   For example: end goal 20 ns (50 MHz) after Phase 5; Phase 4 milestone 40 ns (25 MHz), or "at least
   N× the P = 0 Fmax". Phase 4 passes or fails against the milestone; the end goal is recorded but not
   gated here.
   For: separates what pipelining alone should deliver from what needs arithmetic work.
   Against: two numbers to keep consistent; needs a decision on which period the Phase 4 compiles are
   constrained to (the milestone period makes Phase 4 self-consistent, the end-goal period keeps
   comparability with Phases 1–3).

Any option that names a frequency other than the provisional 50 MHz needs its source stated
(board oscillator, PLL setting, or HPS bridge clock) in the spec and `.sdc` before RTL depends on it.

## Decision
Option 4, two-tier.
1. Phase 4 milestone: 40.000 ns (25 MHz). This is an experimental target chosen to give Phase 4
   a reachable, checkable goal. It is not a hardware requirement and not a system requirement: no
   25 MHz clock to the fabric is documented for the board and no project specification asks for it
   (see "Clock sources" above).
2. End goal: 20.000 ns (50 MHz), after Phase 5. Recorded as the direction of travel; it corresponds
   to the board's documented 50 MHz FPGA clock input. It is not a Phase 4 gate.
3. One constraint for the whole of Phase 4. Every Phase 4 Quartus revision - including the P = 0
   reference (C2-K2-K1 at L = 8, re-compiled) - uses the same SDC, `create_clock -period 40.000` on
   `clk_i`, with the same device, seed and virtual-pin method as before.
4. ADR 0004 is not changed.

## Consequences
- "Timing met" in Phase 4 (CRG-9) means non-negative worst setup and hold slack at all corners at
  40.000 ns. Fmax is still reported for every revision; whether a revision would also meet 20.000 ns
  is reported as information only.
- The P = 0 reference must be re-compiled at 40.000 ns. Phase 4 rows are then comparable with each
  other; they are not directly comparable with the Phase 1–3 rows, which stay as measured at the
  provisional 20.000 ns and are not re-measured. The ablation matrix has to state the constraint of
  each row.
- If a Phase 4 revision meets timing at 40 ns, ADR 0004's secondary (informational) AT check becomes
  runnable for the first time; by ADR 0004 it still does not change the selected L without a new ADR.
- Latencies are quoted with their clock (ROADMAP measurement protocol): at 40.000 ns only for revisions
  that meet it; otherwise at the revision's measured Fmax, labelled as such.
- Before the accelerator is connected on a board, a clock plan is still needed (which board input, PLL
  settings if 25 MHz or any derived clock is used, relationship to the HPS bridge clock, reset per
  domain) with a cited source - this ADR does not provide it.
- Reaching 50 MHz is expected to need the Phase 5 arithmetic work as well as pipelining (ESTIMATE in
  Context); if Phase 4 meets 40 ns but not 20 ns, that is the planned outcome, not a failure.

## Evidence
- Intel DE10-Nano GHRD: <https://github.com/intel/de10-nano-hardware> at commit
  `9b5fc81654c61922b625607d007933a69b5fdb52`, files `hdl_src/top.v`, `hdl_src/soc_system_timing.sdc`
  (read 2026-09-30)
- `evidence/quartus/C2-K2-K1-L8.md`
- `evidence/phase04/k1_l8_worst_path_breakdown.md`
- `evidence/phase01/quartus_C0_timing_analysis.md`
- `docs/ROADMAP.md` (Measurement protocol; Phase 4), `docs/decisions/adr/ADR-0004-phase-3-lane-count-l-selection-criterion.md`,
  `docs/decisions/adr/ADR-0005-apply-adr-0004-l-selection-to-the-c2-k2-k1-supplementary-con.md`
