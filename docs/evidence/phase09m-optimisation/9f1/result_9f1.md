<!-- claim-lint: skip-file (internal block report, not proposal text) -->
# Phase 9F step S1 report: K0 sampler and K0 hash (configuration K1)

- Status: **DONE** (STOP after the step, ADR 0036; S1b follows in the same batch, `../9f1b/`). Branch `phase9m-optimisation`, not committed. RTL: new module `rtl/mlkem/mlkem_core2.sv` (a copy of `mlkem_core.sv` with the parameter `SMP_C5`; amendment A1 of the plan). Plan and rule: `test_plan_9f1.md` (written before the RTL and the compiles). Kernel-only static timing with virtual pins; not a system on the board. Twelve Quartus compiles, all `rc=0`.

## 1. Result
**K1 is smaller, not clearly faster.** By the rule of the plan (section 5, fixed before measuring) K1 is adopted: tests pass, timing is met at 40 ns at 6 of 6 seeds, ALM median 14,061.0 is far below the 20,000 budget, and the latency at 15 ns is 7.5-9.8 % below the reference chosen in the plan (MW at 20 ns). **But** S0 later measured the 9M-1 core (MW) at 15 ns and found 73.6 MHz; against MW at the *same* 15 ns constraint K1 is **3-6 % slower** (more cycles, the same Fmax). The rule's reference was fixed before S0 existed; I report both and do not claim K1 faster. What K1 gives is **3,593 ALM less (-20 %)** with Fmax unchanged: the wall of the design is the NTT core / memory (section 4), not the Keccak permutations.

## 2. Parameters measured (MEASURED; `selection_worksheet_2026-10-04.md`, extracts `quartus_K1*_20261004.md`)
| Parameter | MW (9M-1: C5 sampler and hash) | K1 (K0 sampler and hash) | Difference |
|---|---|---|---|
| ALM median, 40 ns, seeds 1-6 (min-max) | 17,654.0 (17,641-17,683) | 14,061.0 (14,002-14,108) | -3,593.0 (-20.4 %) |
| ALM in % of the fitter's 41,910 | 42 % | 34 % | |
| Registers, 40 ns | 8,189-8,376 | 8,348-8,452 | about equal (K0 saves ALM, not registers) |
| RAM blocks / DSP, 40 ns | 54 / 28 | 54 / 28 | 0 |
| Timing met at 40.000 ns | 6 of 6 | 6 of 6 | |
| Worst setup slack over seeds, 40 ns | +18.655 ns | +19.063 ns | |
| Fmax lowest slow corner, 40 ns, median (min-max) | 48.855 MHz (46.85-52.15) | 51.765 MHz (47.76-53.40) | +2.9 MHz |
| ALM median at 15 ns | 17,948.5 (S0, 2 seeds) | 14,211.5 (14,173-14,273, 6 seeds) | -3,737.0 |
| RAM blocks at 15 ns | 53 | 53 | |
| **Timing met at 15.000 ns** | 2 of 2 seeds (S0) | **6 of 6 seeds** | |
| Worst setup slack at 15 ns | +1.363 ns | +1.114 ns | |
| **Fmax lowest slow corner at 15 ns**, median (min-max) | 73.635 MHz (73.33-73.94, 2 seeds) | **73.070 MHz (72.01-74.10, 6 seeds)** | -0.57 MHz, inside the spread |
| Cycles KeyGen / Encaps / Decaps (profile inputs; simulation) | 8,327 / 10,159 / 15,515 | 8,795 / 10,627 / 15,983 | +468 each (+5.6 %, +4.6 %, +3.0 %) |
| Latency at 15 ns (perhitungan tim; MW: lower Fmax of 2 seeds, K1: median of 6) | 113.6 / 138.5 / 211.6 us | 120.4 / 145.4 / 218.7 us | +6.0 %, +5.0 %, +3.4 % |
| Latency reference of the rule: MW at 20 ns (median of 6, 9M-2) | 130.1 / 158.8 / 242.5 us | K1 at 15 ns 120.4 / 145.4 / 218.7 us | -7.5 %, -8.4 %, -9.8 % |
| Critical warnings per compile | 1 | 1 | |
Cycle detail (profile, `profile_k1_verilator_2026-10-04.json` against the 9M-3 K0-hash profile): only RUN changes against the K0-hash core, +348 per operation; against MW the K0 hash adds +120 (HFD +96, HGT +24, 9M-3) and the K0 sampler +348 (the engine tests give +336: KeyGen 6,352 -> 6,688, Encrypt 7,653 -> 7,989; Decrypt unchanged).
Median Fmax at 15 ns for K1 is the median of six seeds, for MW the lower of two (S0): the comparison is indicative, not like for like.

## 3. Tests (MEASURED)
| # | Result | Evidence |
|---|---|---|
| V1 lint | `verilator --lint-only -Wall` of `mlkem_core2` at K1 and at the defaults: rc 0, no warning; `slang`: 0 errors, 0 warnings (run during the build; output not stored) | this report |
| V2 sequencer tests with the K0 sampler (`KP_VAR=2 KP_CORE_R2=0`): 3 programs bit-exact, constant cycles for fixed rho, stall coverage | 3/3 pass on Verilator and Icarus | `sim_verilator_2026-10-04.md`, `sim_icarus_2026-10-04.md`, `cycles_smp_v2_*` |
| V3 core ACVP at K1: keyGen 25, encapsulation 25, decapsulation 10, random cross-check (20), chain, protocol, constant cycles | 6/6 pass on Verilator and Icarus | same files |
| V4 profile | only RUN longer; every other state count equal to the K0-hash core | `profile_k1_verilator_2026-10-04.json` |
| V5 control `nclen` at K1 | `test_acvp_encaps` fails as required, both simulators | same files |
| V6 formal: Phase 8d sequencer proof at `CORE_R2 = 0` | PASS, control NC-F2 FAIL as required; **weak:** the sampler is a protocol stub that ignores `CORE_R2`; the real K0 sampler is covered by V2 / V3 and by the Phase 8b proofs (INFERENCE) | `formal_2026-10-04.md` |
| V7 regression at the defaults | `run_core_tests.py verilator core` 6/6 pass; the default profiles of `mlkem_core` and of `mlkem_core2` (SMP_C5 = 1, HASH_C5 = 1, CODEC_W2 = 0) equal the Phase 9 profile (9,095 / 10,735 / 16,667); Verilator only (the Phase 9 scripts `phase9c_verify.sh` were not rerun: no Phase 9 RTL file changed in S1) | `regression_default_2026-10-04.md` |
| V8 Quartus | K1 seeds 1-6 at 40 ns and K1-15 seeds 1-6 at 15 ns, all `rc=0`; 40 ns met at 6 of 6, 15 ns met at 6 of 6 | `quartus_K1*_20261004.md` |
| V9 critical paths of K1 at 15 ns (K1-15-s4, smallest slack) | all 300 worst paths in the NTT core / memory / PWM class (+1.114 .. +2.447 ns) | `critical_paths_K1-15_2026-10-04.md` |
Constant cycles (V3): Encaps 10,571 and Decaps 15,927 identical across the tested inputs (ACVP-range numbers); KeyGen over the ACVP seeds 8,723-8,776 (public rejection sampling of A, as before).

## 4. Findings
1. **The C5 permutations were not the only wall.** With K0 in both places no Keccak path is among the 300 worst at 15 ns; the worst paths are all in the NTT core / memory / PWM class (S0 had shown it within 0.2 ns of the permutations at 13 ns). So Fmax stays about 73 MHz (lowest slow corner at 15 ns) and S1 pays +468 cycles for the area it saves.
2. **Area:** -3,593 ALM (-20 %) at 40 ns. Registers do not fall. With S1 the core uses 34 % of the device instead of 42 %.
3. **What this does for the plan (ADR 0036):** S1 made room (ALM 14,061 of the 20,000 budget) but did not raise Fmax. The next Fmax lever is the NTT / memory class (S2); S1b gives back about 390 cycles per operation (`../9f1b/`).
4. **Honest reading of the rule:** the rule says adopt; the S0 comparison says K1 is a smaller configuration with 3-6 % more latency than MW at the same constraint. The team decides (ADR 0033, 0035, 0037 list the related choices).

## 5. Estimates against measurements (written in the plan before the measurements)
- Cycles about 8,850 / 10,690 / 16,045: **measured 8,795 / 10,627 / 15,983** (-0.6 %, -0.6 %, -0.4 %): inside the ESTIMATE's accuracy.
- Sampling cycles +398 / +410 / +410: measured +348 (RUN): lower than estimated (partly hidden by the overlap of 8d).
- ALM about 13,400 +/- 500: **measured 14,061: outside** (161 above the upper bound); the saving of the two sponges together was about 3,590, not about 4,250.
- Registers -1,000 to -1,500: **not met** (about equal).
- Fmax at 40 ns 52-60 MHz: 51.765 MHz: just below the range. Fmax at 15 ns 62-70 MHz: **73.07 MHz: above the range** (S0 had shown that the base core already reaches 73.6 MHz).
- Latency at 15 ns 126-143 / 153-172 / 229-259 us: measured 120.4 / 145.4 / 218.7 us: KeyGen and Decaps below the range, Encaps inside.
- Timing at 40 ns met at every seed: met. RAM blocks 54 and DSP 28: met at 40 ns (53 at 15 ns, as in S0).

## 6. What this does not show
No board result; no speed claim against software; kernel-only static timing with virtual pins; the DE10-Nano clock tree, PLL and HPS are not in these compiles; constant time means cycle-count invariance only; ACVP is simulation.

## 7. Files
`test_plan_9f1.md` (with amendment A1), `selection_worksheet_2026-10-04.md`, `sim_verilator_2026-10-04.md`, `sim_icarus_2026-10-04.md`, `formal_2026-10-04.md`, `regression_default_2026-10-04.md`, `critical_paths_K1-15_2026-10-04.md`, `profile_k1_verilator_2026-10-04.json`, `cycles_*_k1_*.json`, twelve extracts `quartus_K1*_20261004.md`, `quartus/phase09f1_core/` (twelve revisions, `run_k1.sh`), `scripts/select_9f1.py`, `scripts/classify_paths_9f.py`, `formal/run_formal_phase9f1.py`, `formal/phase09m-optimisation/9f1/`.
