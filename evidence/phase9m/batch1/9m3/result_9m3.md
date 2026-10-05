<!-- claim-lint: skip-file (internal block report, not proposal text) -->
# Phase 9M item 3 (9M-3) report: the K0 sponge for the hash instance (`HASH_C5 = 0`)

- Status: **DONE** (STOP after the item, ADR 0034). Branch `phase9m-optimisation`, not committed. **No RTL change in this item**: the parameter `HASH_C5` already existed in Phase 9; only test scripts changed (`run_core_tests.py` reads `CORE_K0`, `profile_core.py` added). Plan and rule: `test_plan_9m3.md` (written before the measurements). Kernel-only static timing with virtual pins; not a system on the board.

## 1. Result
**Rule met (all four items): K0 is adopted by the rule as the smaller hash sponge.** ALM median 15,917.5 against 17,654.0 (-1,736.5), at the cost of +120 cycles per operation (+1.0 % to +1.4 % cycles; +0.6 % to +1.3 % latency at the median Fmax of each table). Timing at 40 ns is met at 6 of 6 seeds; ACVP 100 % on both simulators. The adoption of K0 against the C5 default (ADR 0027) stays with the team (Proposed ADR 0037).

## 2. Parameters measured (MEASURED; `selection_worksheet.md`, extracts `quartus_MK*.md`, `../9m1/quartus_MW*.md`)
| Parameter | MW (C5 hash, `CODEC_W2 = 1`) | MK (K0 hash, `CODEC_W2 = 1`) | Difference |
|---|---|---|---|
| ALM, median (min-max), seeds 1-6 at 40 ns | 17,654.0 (17,641-17,683) | 15,917.5 (15,899-15,940) | -1,736.5 (-9.8 %) |
| ALM in % of the fitter's 41,910 | 42 % | 38 % | |
| Registers | 8,189-8,376 | 8,230-8,382 | about equal (K0 has fewer sponge registers, but the registers of the rest differ by seed) |
| RAM blocks / DSP | 54 / 28 | 54 / 28 | 0 |
| Timing met at 40.000 ns | 6 of 6 | 6 of 6 | |
| Worst setup slack over seeds / hold | +18.655 ns / +0.077 ns | +18.934 ns / +0.080 ns | |
| Fmax, lowest slow corner, median (min-max) | 48.855 MHz (46.85-52.15) | 48.935 MHz (47.47-49.39) | +0.080 MHz, inside the spread of the seeds |
| Cycles, profile inputs (KeyGen / Encaps / Decaps; simulation) | 8,327 / 10,159 / 15,515 | 8,447 / 10,279 / 15,635 | +120 each (+1.44 %, +1.18 %, +0.77 %) |
| Latency at the median Fmax of the 40 ns table (perhitungan tim) | 170.4 / 207.9 / 317.6 us | 172.6 / 210.1 / 319.5 us | +1.28 %, +1.02 %, +0.61 % |
| Information, seed 1 at 20.000 ns (MW-20, MK-20) | ALM 17,808; setup +4.355 ns; Fmax 63.92 MHz | ALM 16,007; setup +4.003 ns; Fmax 62.51 MHz | one seed only, not a statement |
| Critical warnings per compile | 1 | 1 | the virtual-pin clock warning of every kernel-only compile |
Per micro-operation (profile, `profile_k0_w2_verilator.json` against `../9m1/profile_w2_verilator.json`): only HFD and HGT change, by +96 and +24 cycles in every operation; every other state count and every other micro-operation count is equal. Example KeyGen: `HFD 0 144 148` 263 -> 359, `HGT 3 4` 25 -> 37.

## 3. Tests (MEASURED, simulation and formal)
| # | Result | Evidence |
|---|---|---|
| V1 lint | `verilator --lint-only -Wall -GHASH_C5=0 -GCODEC_W2=1 --top-module mlkem_core` (file list of `MK.qsf`): rc 0, no warning line; `slang --top mlkem_core -G HASH_C5=0 -G CODEC_W2=1`: 0 errors, 0 warnings (run 2026-10-04 at the time of this report; output not stored as a file) | this report |
| V2 core ACVP, `CORE_K0=1 CORE_W2=1` | keyGen 25, encapsulation 25, decapsulation 10 equal; random cross-check, chain, protocol, constant cycles pass; Verilator and Icarus 6/6 | `sim_verilator.md`, `sim_icarus.md` |
| V3 profile | only HFD / HGT change (section 2) | `profile_k0_w2_verilator.json` |
| V4 control `nclen` | `test_acvp_encaps` fails as required, both simulators (TOTAL 7/7 as expected) | the two sim files |
| V5 formal hash wrapper H1-H5, `CORE_R2 = 0`, protocol stub | proofs PASS, reachability PASS, two negative controls FAIL as required; INFERENCE: that the real K0 sponge follows the stub protocol rests on the Phase 7 proofs and the simulations of V2 | `formal.md` |
| V6 default regression | `run_core_tests.py verilator core` 6/6 pass at the defaults; default profile equal to the Phase 9 profile (9,095 / 10,735 / 16,667) | `regression_default.md` |
| V7 Quartus | MK seeds 1-6 at 40 ns and MK-20 all `rc=0`, timing met at all six seeds | `quartus_MK*.md` |
Constant cycles: Encaps 10,235 and Decaps 15,591 identical across the inputs tested in V2 (ACVP-range numbers, not the profile inputs); KeyGen over the ACVP seeds 8,387-8,428 (the KeyGen spread comes from the public rejection sampling of A, as in Phase 9).

## 4. Rule of the plan (section 5), applied to files
1. V1-V6 pass: met (V6: see section 3).
2. Timing at 40 ns at every seed: met (6 of 6).
3. ALM median at least 1,500 below MW: met (-1,736.5).
4. Latency of each operation at most 2 % above MW (cycles / median Fmax): met (+1.28 %, +1.02 %, +0.61 %).

## 5. Estimates against measurements (written in the plan before the measurements)
- Cycles +120: **measured exactly +120** in all three operations.
- ALM 2,000-2,800 fewer: **measured 1,736.5 fewer: outside the estimate** (too high; the 9b difference of the hash instance, about 2,500 ALM, was between the wrappers alone; inside the full core the fitter shares and trims differently: INFERENCE, not examined).
- Registers 300-700 fewer: **not met** (range 8,230-8,382 against 8,189-8,376: about equal).
- Fmax median 47-53 MHz: measured 48.935 MHz: inside. Timing at 40 ns at all seeds: met.
- RAM blocks / DSP unchanged: met.

## 6. Findings and limits
1. K0 cost: +120 cycles of 8,327-15,515 (about 1 %) for 1,736.5 ALM (about 10 % of the core): it is the cheaper option in area per cycle. It is not a speed improvement; it frees area. Under the Fmax plan (ADR 0036) that area can be spent on S1/S2.
2. At 20 ns (seed 1 only) MK has 62.51 MHz against 63.92 MHz of MW: information; the critical path is inside the C5 sampler sponge and the C5 hash permutation (`../../critical_paths_MW.md`), so removing the hash C5 leaves the sampler C5 as the wall (INFERENCE; S1 replaces it).
3. The Phase 9 default core with K0 (`CODEC_W2 = 0`, `HASH_C5 = 0`) was not measured (plan section 1); the effects of the two parameters are assumed additive (INFERENCE).
4. The sampler inside the K-PKE engine keeps its own C5 sponge; `HASH_C5` does not touch it.

## 7. What this does not show
No board result; no speed claim against software; kernel-only static timing with virtual pins; constant time means cycle-count invariance only; ACVP is simulation.

## 8. Files
`test_plan_9m3.md`, `selection_worksheet.md`, `sim_verilator.md`, `sim_icarus.md`, `formal.md`, `regression_default.md`, `cycles_*_core_k0.json`, `profile_k0_w2_verilator.json`, seven Quartus extracts `quartus_MK*.md`, `quartus/phase09m3_core/` (seven revisions, `run_mk.sh`), `scripts/quartus/select_9m3.py`, `formal/run/run_formal_phase9m3.py`, `formal/phase09m-optimisation/9m3/`.
