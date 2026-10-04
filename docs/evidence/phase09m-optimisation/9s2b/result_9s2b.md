<!-- claim-lint: skip-file (internal block report, not proposal text) -->
# Phase 9F step S2b report: registered issue address in the NTT/INTT core (configuration K3)

- Status: **DONE** (STOP after the step). Branch `phase9m-optimisation`, not committed at the time of writing. RTL: the parameter `AREG` (default 0) of `rtl/ntt/ntt_core_s10.sv`, forwarded by the wrapper `ntt_core_s10_p5`, `NTT_AR` of `kpke_smp_top_s10`, `kpke_smp_top_s10o` and `mlkem_core3` / `mlkem_core4` (all default 0). Plan and rule: `test_plan_9s2b.md` (written before the RTL and the compiles; amendment A1: the 40 ns gate stays; A2: three extra seeds chosen after the six). Baseline K2 (`../9s2/`, `NTT_P6 = 1`). Kernel-only static timing with virtual pins; not a system on the board. Fifteen Quartus compiles (six at 15 ns, six at 40 ns, three extra seeds at 15 ns), all `rc=0`, one at a time (a first parallel attempt was killed by an editor crash and none of its output is used; one run was stopped by mistake and restarted, see A1).

## 1. Result
**By the rule as written K3 is NOT adopted, but the data show a gain of the median.** The registered issue address works as designed: the `layer_q` to memory-port class of K2 (+1.404 ns) is gone from the 300 worst paths of the weakest seed. Median Fmax at 15 ns, six seeds: **77.555 MHz against 74.125 MHz of K2 (+3.430 MHz)**; five of six seeds of K3 (77.32-79.37 MHz) are above every seed of K2 (maximum 76.03 MHz). Rule item 5 (the gain larger than the larger seed spread, or the lowest seed of K3 above the highest of K2) is **not met as written**: the spread of K3 is 6.35 MHz, larger than the gain, and seed 4 (73.02 MHz) is below the highest seed of K2. The three extra seeds (amendment A2; chosen after seeing the result, reported beside it, none dropped) give a nine-seed median of 77.320 MHz (72.80-79.37), 6 of 9 seeds above the highest seed of K2. Latency at 15 ns (cycles / median Fmax, perhitungan tim): **108.5 / 132.2 / 201.4 us** against 113.5 / 138.3 / 210.7 us of K2 (-4.4 % for all three; the cycles are equal). The cause of the low seeds was found later in K4's path report: the term `start_go` of S2b (section 6, INFERENCE for K3 itself).

## 2. Parameters measured (MEASURED; `selection_worksheet_2026-10-05.md`, extracts `quartus_K3*_20261004.md`, K2 from `../9s2/`)
| Parameter | K2 | K3 | Difference |
|---|---|---|---|
| Parameters | `NTT_P6 = 1`, `NTT_AR = 0` | `NTT_P6 = 1`, `NTT_AR = 1` | the issue-stage address (`j_r`, `jlen_r`: 8 lanes x 2 x 8 bits = 128 registers) is computed one cycle early and registered |
| ALM median, 40 ns, seeds 1-6 (min-max) | 14,213.0 (14,171-14,235) | 14,115.5 (14,081-14,153) | -97.5 |
| ALM median at 15 ns | 14,349.5 (14,301-14,454) | 14,293.0 (14,139-14,359) | -56.5 |
| Registers, 40 ns / 15 ns | 8,327-8,375 / 8,343-8,430 | 8,462-8,508 / 8,400-8,472 | about +40 to +135 |
| RAM blocks / DSP | 54 / 28 (53 at 15 ns) | 54 / 28 (53 at 15 ns) | 0 |
| Timing met at 40.000 ns | 6 of 6 | 6 of 6 | |
| Worst setup slack, 40 ns / 15 ns (all corners) | +20.136 ns / +1.236 ns | +20.302 ns / +1.305 ns | |
| **Timing met at 15.000 ns** | 6 of 6 | **6 of 6** (9 of 9 with the extra seeds) | |
| **Fmax lowest slow corner at 15 ns**, median (min-max) | **74.125 MHz** (72.65-76.03) | **77.555 MHz** (73.02-79.37); nine seeds 77.320 (72.80-79.37) | +3.430 MHz (six seeds) |
| Fmax at 40 ns, median | 52.055 MHz | 51.760 MHz | not used |
| Cycles per transform (NTT, INTT) | 119 | 119 | 0 |
| Cycles KeyGen / Encaps / Decaps (profile inputs) | 8,416 / 10,250 / 15,619 | 8,416 / 10,250 / 15,619 | 0 |
| Latency at 15 ns (median Fmax; perhitungan tim) | 113.5 / 138.3 / 210.7 us | 108.5 / 132.2 / 201.4 us | -4.42 % for all three |
| Latency at 15 ns (lowest Fmax of 6) | 115.8 / 141.1 / 215.0 us | 115.3 / 140.4 / 213.9 us | |
| Critical warnings per compile | 1 | 1 | the virtual-pin clock warning of every kernel-only compile |
Fmax of the K3 seeds at 15 ns: s1 77.71, s2 79.28, s3 77.40, s4 73.02, s5 77.32, s6 79.37, s7 77.03, s8 75.47, s9 72.80 MHz. Denominators of the fitter: 41,910 ALM, 553 RAM blocks, 112 DSP: K3 uses about 34 % of the ALMs, 28 DSP.

## 3. Tests (MEASURED; `sim_2026-10-05.md`, `formal_2026-10-05.md`)
| # | Result | Evidence |
|---|---|---|
| V1 lint | Verilator `-Wall` and slang of the wrapper, `kpke_smp_top_s10` and `mlkem_core3` at `NTT_AR` 0 and 1: no warning, no error (run during the build; output not stored as files) | this report |
| V2, V3 NTT core at P = 6 with `AREG = 1` | 6/6 bit-exact NTT and INTT, exactly 119 / 119 cycles, 0 stalls, Verilator and Icarus; control NC-A1 (`ncar`, the address taken one cycle late) fails as required on both | `sim_2026-10-05.md` |
| V4 formal | S10 control proof at P = 6 with `AREG = 1` (H, O, R, A, B, C): PASS (base case and induction); NC-O and NC-A FAIL as required | `formal_2026-10-05.md` |
| V5 sequencer tests, `NTT_P6 = 1`, `NTT_AR = 1` | 3/3 programs bit-exact, constant cycles; control `nchaz` fails as required; both simulators | `sim_2026-10-05.md` |
| V6 core K3 | ACVP keyGen 25, encapsulation 25, decapsulation 10 equal; 20 random cases equal; chain, protocol, constant cycles pass; Verilator 9/9 (with `nclen`, `ncoff`, `ncrom` as required), Icarus 7/7; cycles identical to K2 (Encaps 10,194, Decaps 15,563) | same |
| V7 default regression | `NTT_AR = 0` profile equals K2 and K1b; `run_s10_tests.py` default 13/13 with 118 / 118; `mlkem_core` defaults 6/6; formal of `mlkem_core3` (9f1b) still elaborates with the stub parameter | same, `../9s2/` |
| V8 Quartus | K3 seeds 1-6 at 40 ns, K3-15 seeds 1-6 at 15 ns, extra seeds 7-9 at 15 ns: all `rc=0`; met 6 of 6 at 40 ns and 9 of 9 at 15 ns | `quartus_K3*_20261004.md` |
| V9 critical paths of K3-15-s4 | worst +1.666 ns (slow 100 C): read-position delay to the Barrett reducer (144 paths) and side-operand delay to the M10K (126 paths); the K2 `layer_q` class is gone | `critical_paths_K3-15_2026-10-05.md` |

## 4. Rule of the plan (section 5), applied to files
1. V1-V7 pass: met.
2. Timing at 40 ns at every seed: met (6 of 6).
3. ALM median at most 20,000: met (14,115.5).
4. Latency of each operation lower than K2 at 15 ns: met (-4.42 %, -4.42 %, -4.42 %).
5. Median gain (+3.430 MHz) larger than the larger spread (K3 6.35 MHz, K2 3.38 MHz), or the lowest seed of K3 above the highest of K2: **NOT met as written** (73.02 MHz is below 76.03 MHz).
6. Seeds met at 15 ns reported: 6 of 6 (K2: 6 of 6); 9 of 9 with the extra seeds.
Result of the rule: **not adopted** as written; K2 would stay. Amendment A2 adds, without changing the rule, that 5 of 6 seeds (6 of 9) are above every seed of K2 and the median is +3.4 MHz. The team decides (Proposed ADR 0042; K3 is also the base of the measurement of K4, ADR 0043).

## 5. Estimates against measurements (written in the plan before the measurements)
- Cycles per transform 119, operations equal to K2: **met**.
- ALM within +-150 of K2: **met** (-97.5 at 40 ns, -56.5 at 15 ns).
- Registers +100 to +200: **partly met**: +40 to +135 depending on the corner and constraint (the fitter shares some of the registers).
- Fmax 75 to 79 MHz, low confidence: **met** (77.555 MHz; the nine-seed median 77.320).
- Latency 107-112 / 130-137 / 198-208 us: **met** (108.5 / 132.2 / 201.4 us).

## 6. Findings
1. **The address path is fixed**: the `layer_q` to memory class (+1.404 ns in K2) is not among the 300 worst paths of the weakest K3 seed; the next wall is the read-position delay to the reducer (+1.666 ns) and the side operand to the M10K (+2.368 ns).
2. **A tail of low seeds** (seed 4 at 73.02, seed 8 at 75.47, seed 9 at 72.80 MHz beside six seeds at 77.0-79.4 MHz) keeps the rule from being met. INFERENCE (found in the K4 report, `../9i4/critical_paths_K4-15_2026-10-05.md`, not checked in the K3 seeds with a path report): the term `start_go` of the S2b logic makes the registered address depend on `host_we_i`, which the sequencer drives from `cnt_q != 0`; the path `cnt_q` -> `core_hwe_o` -> `mode_n` -> address adders -> `jlen_r` is the worst path of K4's weakest seed (+0.736 ns).
3. **Cost of S2b:** no extra cycle, about +40 to +135 registers, ALM equal within the spread; no RAM block or DSP.
4. The gain depends on S2 (the register after the reducer): K2 alone gave +0.27 MHz, K3 gives +3.43 MHz over K2 (+3.70 MHz over K1b).

## 7. What this does not show
No board result; no speed claim against software; kernel-only static timing with virtual pins; seed noise of 3 MHz (larger for K3) limits any statement below that size; the three extra seeds were chosen after the result; K2 has six seeds only; constant time means cycle-count invariance only; ACVP is simulation; the formal proof covers control and bank capacity, not the address values. One seed (K3-15-s4) was analysed for the paths.

## 8. Files
`test_plan_9s2b.md` (with amendments A1 and A2), `selection_worksheet_2026-10-05.md`, `sim_2026-10-05.md`, `formal_2026-10-05.md`, `critical_paths_K3-15_2026-10-05.md`, `profile_k3_verilator_2026-10-05.json`, `cycles_*_k3_2026-10-05.json`, fifteen extracts `quartus_K3*_20261004.md`, `quartus/phase09s2b_core/` (runners `run_k3.sh`, `run_k3_15.sh`, `run_k3_40.sh`, `run_k3_x.sh`), `scripts/select_9s2b.py`, `formal/run_formal_phase9s2b.py`, `formal/phase09m-optimisation/9s2b/`, the changed test runners.
