<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Phase 9M item 2 (9M-2): the core at 20.000 ns, seeds 1-6 - test plan and rule

Written 2026-10-04 before any 9M-2 compile. Scope: ADR 0034 (Accepted, Faza Dzil), item 2 ("lanjut 2", chat 2026-10-04). No RTL change. Labels: MEASURED, ESTIMATE, INFERENCE, perhitungan tim.

## 1. Why
Phase 9 measured the core at a constraint of 40.000 ns (the gate of Phases 5-9) and, as information, at 20.000 ns for seed 1 only (MC-20: met, +4.419 ns). One seed is not a trend. This item compiles seeds 2-6 at 20.000 ns, so that "timing met at 20 ns" can be stated with the same seeds 1-6 as the 40 ns result, and a latency at 20 ns can be quoted (perhitungan tim). 20.000 ns is 50 MHz, the clock of the DE10-Nano; as in Phases 5-9 it is kernel-only static timing with virtual pins, not a system on the board (ADR 0010: information, not a gate).

## 2. Configurations (one project directory `quartus/phase09m2_core`, revisions run one at a time)
| Revision | Core | Seed |
|---|---|---|
| MC-20-s2 ... MC-20-s6 | Phase 9 core, `CODEC_W2 = 0`, `HASH_C5 = 1` (same sources as `quartus/phase09c_core/MC-20.qsf`) | 2-6 |
| MW-20-s2 ... MW-20-s6 | 9M-1 core, `CODEC_W2 = 1` (same sources as `quartus/phase09m1_core/MW-20.qsf`) | 2-6 |
Seed 1 of both is taken from the existing evidence (`evidence/phase09/9c/quartus_MC-20.md`, `evidence/phase9m/batch1/9m1/quartus_MW-20.md`); the settings are identical (Quartus defaults, `C-20.sdc`), only the seed differs. The Phase 9 core is measured because ADR 0035 (9M-1) is not accepted yet; the 9M-1 core because it is the candidate base for items 3 and 4.

## 3. Estimates written before measuring (ESTIMATE)
At 40 ns the lowest slow-corner Fmax of seeds 1-6 was 47.64-51.74 MHz (MC) and 46.85-52.15 MHz (MW), i.e. some seeds were below 50 MHz when the constraint was 40 ns. Under a 20 ns constraint the fitter works harder (MC-20 seed 1: 64.18 MHz, MW-20 seed 1: 63.92 MHz). ESTIMATE: timing is met at 20.000 ns at most or all seeds, lowest slow-corner Fmax 55-66 MHz, worst setup slack +1 to +5 ns; ALM within +/- 1 % of the 40 ns median; one or more seeds may fail. A failure is reported as MEASURED, not hidden.

## 4. Measured parameters
Per revision: ALM, registers, RAM blocks, block memory bits, DSP, worst setup and hold slack (all corners), timing met yes / no, lowest slow-corner Fmax, critical warnings (from the extract, `.claude/skills/quartus-report/scripts/extract_quartus_report.py`). Per configuration: median, minimum and maximum over seeds 1-6; the number of seeds that meet 20.000 ns. Latency at 20 ns: t = cycles / Fmax with the cycles of the profile inputs (Phase 9: 9,095 / 10,735 / 16,667; 9M-1: 8,327 / 10,159 / 15,515) and the median lowest slow-corner Fmax of the configuration (perhitungan tim, not a board measurement). Note: a core that meets a 20 ns constraint is not clocked faster by this fact; the figure that may be quoted is "meets 50 MHz (20 ns) in kernel-only static timing".

## 5. Rule (fixed before measuring)
Information, not an adoption between candidates. The statement "the core meets timing at 20.000 ns" is made for a configuration only if worst setup and hold slack are non-negative at all six seeds; otherwise the statement is "met at k of 6 seeds" with the failing seeds named. No run is repeated with other settings to turn a failing seed green.

## 6. Procedure
`quartus/phase09m2_core/run_20.sh` compiles the ten revisions strictly one at a time (they share one .qpf; the script restores the .qpf the tool rewrites), logs `compile_<rev>.log`; extracts with the `quartus-report` script; `scripts/quartus/select_9m2.py` writes `selection_worksheet_<date>.md` from the extracts. No simulation or formal run is needed (no RTL change; the RTL files are those of 9M-1, verified there).
