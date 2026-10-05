<!-- claim-lint: skip-file (internal block report, not proposal text) -->
# Phase 9F step S0 report: the 9M-1 core under 16, 15 and 14 ns constraints

- Status: **DONE** (STOP after the step, ADR 0036). Branch `phase9m-optimisation`, not committed. **No RTL change**: the sources are those of the 9M-1 core (`quartus/phase09m1_core/MW.qsf`). Plan: `test_plan_9f0.md` (written before the compiles). Kernel-only static timing with virtual pins; not a system on the board. Eight compiles in the first sweep, two more in amendment A2 (section 8), all `rc=0`.

## 1. Result
**Timing is met at 16, 15 and 14 ns at both seeds with the Quartus defaults; the sweep did not find the limit of the design** (it ended at its tightest constraint, which was met). At 14 ns the lowest slow-corner Fmax is 75.31 MHz (seed 1) and 77.29 MHz (seed 2); at 15 ns 73.94 and 73.33 MHz. The high performance effort did **not** help at 14 ns (lower worst slack, 970-1,000 ALM and about 2,200 registers more). Two seeds only: this is a sweep to locate the limit, not the six-seed statement that ADR 0036 asks for at the final reporting constraint (that comes with S1).

## 2. Parameters measured (MEASURED, `selection_worksheet.md`, extracts `quartus_F*.md`, `quartus_H14-*.md`)
| Revision | Constraint | ALM | Registers | RAM blocks / DSP | Worst setup / hold (ns) | Fmax lowest slow corner (MHz) |
|---|---|---|---|---|---|---|
| F16-s1 / s2 | 16 ns | 17,980 / 17,888 | 8,635 / 8,575 | 53 / 28 | +1.992 / +2.075; +0.118 / +0.108 | 71.39 / 71.81 |
| F15-s1 / s2 | 15 ns | 17,971 / 17,926 | 8,719 / 8,700 | 53 / 28 | +1.475 / +1.363; +0.102 / +0.071 | 73.94 / 73.33 |
| F14-s1 / s2 | 14 ns | 17,907 / 17,889 | 8,770 / 8,669 | 53 / 28 | +0.721 / +1.062; +0.109 / +0.108 | 75.31 / 77.29 |
| H14-s1 / s2 (high performance effort) | 14 ns | 18,876 / 18,897 | 10,966 / 10,935 | 49 / 28 | +0.826 / +0.423; +0.090 / +0.107 | 75.91 / 73.65 |
Reference, same core at the other constraints (earlier items): 40 ns median Fmax 48.855 MHz, ALM 17,654.0 (`../9m1/selection_worksheet.md`); 20 ns median 63.990 MHz, ALM 17,779.5 (`../9m2/selection_worksheet.md`). Critical warnings: 1 per compile (the virtual-pin clock warning).
Latency at the lower Fmax of the two seeds (perhitungan tim; profile-input cycles of the 9M-1 core 8,327 / 10,159 / 15,515): 16 ns 116.6 / 142.3 / 217.3 us; 15 ns 113.6 / 138.5 / 211.6 us; 14 ns 110.6 / 134.9 / 206.0 us. Against the 20 ns table of 9M-2 (130.1 / 158.8 / 242.5 us) this is 15 % lower at 14 ns. These are static-timing figures, not a board measurement.

## 3. Critical-path classification (MEASURED, `critical_paths_F14_H14.md`)
At 14 ns, defaults: worst paths in the C5 Keccak permutation of the hash instance (+0.721 ns, 133 of 300 paths), then NTT core / memory / PWM (+1.055 ns, 84), then the sampler-sponge permutation (+1.266 ns, 83). With the high performance effort the two permutations lead (+0.423 and +0.453 ns). Within 0.55 ns three blocks share the limit: no single block dominates.

## 4. Estimates against measurements (written in the plan before the compiles)
- 16 ns met at both seeds: **met**. 15 ns met at one or both seeds: met at both.
- **14 ns not met at the default effort: wrong** (met at both seeds, slack +0.721 and +1.062 ns).
- High performance effort gains 0.3-1 ns at 14 ns: **not observed** (slack +0.826 / +0.423 ns against +0.721 / +1.062 for the defaults; the effort costs area and registers).
- ALM within +/- 3 % of 17,654: defaults inside (+1.3 % to +1.8 %); the high performance effort outside (+6.9 % to +7.0 %). Registers within +/- 3 %: **outside** (defaults +2.4 % to +4.7 % against 8,376 max; effort +30 %: fitter replication and retiming under a tight constraint: INFERENCE).
- RAM blocks 54 and DSP 28 unchanged: DSP unchanged; **RAM blocks 53 (defaults) and 49 (effort)**: the fitter packed memories differently under the constraint (INFERENCE, not examined).
- Earlier 20 ns INFERENCE "outside Keccak about 69 MHz": consistent with the 14 ns result only in that the NTT class (path about 12.9 ns here) is close behind Keccak; the 69 MHz figure itself was a lower bound from a relaxed compile, not a limit.

## 5. Findings and limits
1. The limit of the C5 core is not 50-64 MHz as the 20 ns compiles suggested; at tighter constraints the fitter reaches 73-77 MHz (lowest slow corner) at about the same ALM. The 20 ns compile was a loose constraint, not the limit.
2. The limit lies below 14 ns. To find it the sweep needs 13, 12, 11 ns (a decision for Faza Dzil: six more compiles at two seeds, ESTIMATE about 3 hours of machine time with other compiles running); this is not done.
3. S1 consequence (INFERENCE): K0 in place of C5 removes the permutation classes; the NTT / memory path is within about 0.33 ns of the hash permutation at 14 ns, so S1 may gain little Fmax and will mainly save area. S1 measures this.
4. The SDC files of this step (`C-16.sdc`, `C-15.sdc`, `C-14.sdc`) have no `set_false_path -from [get_ports {rst_ni}]`, whereas `C.sdc` and `C-20.sdc` of Phase 9 have it (my omission, not intended; the plan said "same form as C-20.sdc"). The input `rst_ni` has no input delay in either file, so its paths are not constrained in either case (INFERENCE, not tested by a compile with the line). The S1 compiles at 15 ns (K1-15) use the same SDC form as this step so that they stay comparable.
5. Two seeds per constraint; the lower-Fmax-of-two figure is not a median.

## 6. What this does not show
No board result; no speed claim against software; kernel-only static timing with virtual pins; the DE10-Nano clock tree, PLL and the HPS are not in these compiles (a PLL decision belongs to Phase 10); constant time means cycle-count invariance only.

## 7. Files
`test_plan_9f0.md`, `selection_worksheet.md`, `critical_paths_F14_H14.md`, eight Quartus extracts, `quartus/phase09f0_core/` (eight revisions, `run_f0.sh`), `scripts/quartus/select_9f0.py`, `scripts/quartus/classify_paths_9f.py`.

## 8. Amendment A2 result: the extended sweep (Faza Dzil, chat 2026-10-04: "check sampai fail; jika pada 10 ns masih pass kita stop di sana")
Rule and estimates are in `test_plan_9f0.md` section 7 (written before the runs). Run by `quartus/phase09f0_core/run_f0x.sh`: 13 ns, seeds 1 and 2 (defaults), then it stopped because one seed failed (log `quartus/phase09f0_core/f0x_status.log`).
| Revision | Constraint | ALM | Registers | RAM blocks / DSP | Worst setup / hold (ns, all corners) | Timing met | Fmax lowest slow corner (MHz) | Critical warnings |
|---|---|---|---|---|---|---|---|---|
| F13-s1 | 13 ns | 17,900 | 8,807 | 53 / 28 | +0.227 / +0.112 | **yes** | 78.29 | 1 |
| F13-s2 | 13 ns | 17,891 | 8,873 | 53 / 28 | -0.213 / +0.100 (slow 100 C setup: -0.185) | **NO** | 75.68 | 3 |
(Exact values: `selection_worksheet.md`, `quartus_F13-s1.md`, `quartus_F13-s2.md`.)
- **Result: 13 ns is met at 1 of 2 seeds; the limit of the 9M-1 core lies between 13 and 14 ns** (14 ns met at both seeds, 13 ns at one). The 10 ns stop rule was not reached.
- **Critical paths at 13 ns** (`critical_paths_F14_H14.md`, added section): the failing seed fails in **NTT core / memory / PWM** (-0.185 ns, 171 of 300 paths), with the hash-instance Keccak permutation also negative (-0.030 ns); in the passing seed the hash permutation leads (+0.227 ns) and the NTT class follows (+0.571 ns). So at the limit the NTT / memory path and the C5 permutations fail together: the wall is about 13.2 ns (about 75 MHz), not the permutation alone.
- **Estimate against measurement:** 13 ns met at both seeds: wrong (one seed fails); first failure at 12 or 11 ns: wrong (13 ns); the stated ALM growth up to +3 % and registers up to +10 %: ALM +1.3 % to +1.4 % over 17,654 (17,891-17,900), registers 8,807 / 8,873 (+5.1 % / +5.9 % over the 40 ns maximum 8,376): inside.
- **Consequence for S1 (INFERENCE):** replacing the C5 permutations by K0 removes the permutation classes but not the NTT / memory class, which is at the wall within 0.2 ns of them; S1 can gain at most a few percent of Fmax at this limit. The S1 compiles at 15 ns (section 9 of `../9f1/result_9f1.md`) show how the area saving and the Fmax behave.
- Limits of the statement: two seeds per constraint; one run per seed; the wall differs by seed (seed 2 fails by 0.185 ns, seed 1 passes by 0.227 ns), so the limit has a spread of the order of the seed-to-seed slack difference (about 0.4 ns).
- **Critical warnings (triage, CLAUDE.md rule 10):** F13-s1 has the one of every kernel-only compile (15725, the clock port is fed by a virtual pin; accepted). F13-s2 has two more, `332148 Timing requirements not met` (printed by the fitter and by the timing analyzer for the failing setup slack of -0.213 ns): they are the failing result itself, not a tool problem; the failure is reported, not waived.
