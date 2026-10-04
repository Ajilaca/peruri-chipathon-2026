<!-- claim-lint: skip-file (internal block report, not proposal text) -->
# Phase 9M item 2 (9M-2) report: the core at 20.000 ns, seeds 1-6

- Status: **DONE** (STOP after the item, ADR 0034). Branch `phase9m-optimisation`, not committed. No RTL change: the sources are those of Phase 9 and of 9M-1. Plan and rule: `test_plan_9m2.md` (written before the compiles). Kernel-only static timing with virtual pins; not a system on the board.

## 1. Result
**Timing is met at 20.000 ns (50 MHz) at 6 of 6 seeds for both configurations** (Phase 9 core `CODEC_W2 = 0` and 9M-1 core `CODEC_W2 = 1`); the rule of the plan (all six seeds) is met, so the statement may be made with the label "kernel-only static timing". Seed 1 comes from the Phase 9 / 9M-1 evidence, seeds 2-6 are new (ten new compiles, one at a time, all `rc=0`).

## 2. Parameters measured (MEASURED, `selection_worksheet_2026-10-04.md`, extracts `quartus_*-20-s*_20261004.md`)
| Parameter | Phase 9 core at 20 ns | 9M-1 core at 20 ns | Phase 9 core at 40 ns (reference) |
|---|---|---|---|
| Timing met at 20.000 ns | 6 of 6 seeds | 6 of 6 seeds | (40 ns: 6 of 6) |
| Worst setup slack over seeds / worst hold slack | +3.730 ns (seed 4) / +0.077 ns | +4.184 ns (seed 5) / +0.080 ns | +19.010 / +0.075 ns |
| Fmax, lowest slow corner, median (min-max) | 63.645 MHz (61.46-64.66) | 63.990 MHz (63.23-66.54) | 49.280 MHz (47.64-51.74) |
| ALM, median (min-max) | 17,708.5 (17,650-17,780) | 17,779.5 (17,728-17,845) | 17,620.5 |
| ALM in % of the fitter's 41,910 | 42 % | 42 % | 42 % |
| Registers | 8,369-8,504 | 8,407-8,487 | 8,210-8,365 |
| RAM blocks / DSP | 54 / 28 | 54 / 28 | 54 / 28 |
| Critical warnings per compile | 1 (virtual pin clock, as in all earlier compiles) | 1 | 1 |
| Cycles, profile inputs (KeyGen / Encaps / Decaps; simulation) | 9,095 / 10,735 / 16,667 | 8,327 / 10,159 / 15,515 | same |
| Latency at the median Fmax of the 20 ns table (perhitungan tim) | 142.9 / 168.7 / 261.9 us | 130.1 / 158.8 / 242.5 us | at 40 ns median: 184.6 / 217.8 / 338.2 us |
The latencies at 20 ns are cycles divided by the lowest slow-corner Fmax reached when the fitter was asked for 20 ns. They are not a measurement of an operation on the board.

## 3. Estimates against measurements (written in the plan before the compiles)
- Timing met at most or all seeds: met at all 12 (6 + 6): inside. One or more failures were possible; none occurred.
- Lowest slow-corner Fmax 55-66 MHz: measured 61.46-66.54 MHz: inside.
- Worst setup slack +1 to +5 ns: measured +3.730 to +4.972 ns (per-seed worst): inside.
- ALM within +/- 1 % of the 40 ns median: +0.5 % (Phase 9 core, 17,708.5 against 17,620.5) and +0.7 % (9M-1 core, 17,779.5 against 17,654.0): inside.

## 4. Findings and limits
1. The lowest seed at 40 ns was below 50 MHz (47.64 MHz, Phase 9 core); at a 20 ns constraint every seed reaches at least 61.46 MHz. The difference comes from the fitter's effort under the tighter constraint, not from a change of the design (INFERENCE; the critical path was not examined).
2. The result is information, not a gate (ADR 0010); the DE10-Nano clock tree, I/O and the HPS are not in these compiles. No claim about the board.
3. 9M-1 against Phase 9 at 20 ns: ALM +71.0 (median), Fmax median +0.345 MHz, within the spread of the seeds; the cycle saving of 9M-1 is unchanged.
4. No process problem in this item: ten compiles, all successful, the first-time `generate` issue of 9M-1 does not recur.

## 5. What this does not show
No board result; no speed claim against software; kernel-only static timing with virtual pins at one constraint; constant time means cycle-count invariance only.

## 6. Files
`test_plan_9m2.md`, `selection_worksheet_2026-10-04.md`, the ten new Quartus extracts in this directory, `quartus/phase09m2_core/` (ten revisions, `run_20.sh`), `scripts/select_9m2.py`.
