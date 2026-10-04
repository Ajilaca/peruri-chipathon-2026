<!-- claim-lint: skip-file (internal block report, not proposal text) -->
# Phase 9F step S2 report: register after the Barrett reducer in the NTT core (P = 5 -> 6, configuration K2)

- Status: **DONE** (STOP after the step, ADR 0036). Branch `phase9m-optimisation`, not committed at the time of writing. RTL: the parameter `P6` of `rtl/ntt/ntt_core_s10_p5.sv` (fourth multiplier cut, `MUL_REG` bit 3), forwarded by `NTT_P6` of `kpke_smp_top_s10` and `mlkem_core3`; all default 0 (amendment A1: no new wrapper file). Plan and rule: `test_plan_9s2.md` (written before the RTL and the compiles). Kernel-only static timing with virtual pins; not a system on the board. Twelve Quartus compiles, all `rc=0`; a first attempt of the 15 ns compiles in two parallel copies was killed by an editor crash and none of its output is used.

## 1. Result
**The rule of the plan adopts K2, but S2 gives no measurable Fmax gain.** The register works as designed: the reducer-to-memory path that limited K1b (+1.170 ns, 182 of the 300 worst paths) is at +2.349 ns in K2. But a different path was already behind it, the layer counter through the issue-stage address arithmetic to the memory ports (+1.910 ns in K1b, +1.404 ns in the K2 seed analysed), and it limits K2 now. Median Fmax at 15 ns: **74.125 MHz against 73.855 MHz of K1b (+0.27 MHz)**, inside the spread of the seeds (K2 3.38 MHz, K1b 2.94 MHz); K2's lowest seed 72.65 MHz is below K1b's highest 74.40 MHz. Latency at 15 ns is 0.2 % lower for all three operations (more cycles, equal Fmax): that is below the noise of the seeds and is **not reported as a gain**. Area is unchanged within the spread (ALM median -122.0 at 40 ns, -85.5 at 15 ns). The ESTIMATE of the plan (Fmax 76 to 80 MHz) was not met.

## 2. Parameters measured (MEASURED; `selection_worksheet_2026-10-04.md`, extracts `quartus_K2*_20261004.md`, `../9f1b/quartus_K1b*_20261004.md`)
| Parameter | K1b | K2 | Difference |
|---|---|---|---|
| ALM median, 40 ns, seeds 1-6 (min-max) | 14,335.0 (14,329-14,376) | 14,213.0 (14,171-14,235) | -122.0 |
| ALM median at 15 ns | 14,435.0 (14,390-14,459) | 14,349.5 (14,301-14,454) | -85.5 |
| Registers, 40 ns / 15 ns | 8,211-8,258 / 8,213-8,276 | 8,327-8,375 / 8,343-8,430 | about +120 |
| RAM blocks / DSP | 54 / 28 (53 at 15 ns) | 54 / 28 (53 at 15 ns) | 0 |
| Timing met at 40.000 ns | 6 of 6 | 6 of 6 | |
| Worst setup slack, 40 ns (all corners) | +18.043 ns | +20.136 ns | |
| **Timing met at 15.000 ns** | 6 of 6 | **6 of 6** | |
| Worst setup slack, 15 ns (all corners) | +1.007 ns | +1.236 ns | |
| **Fmax lowest slow corner at 15 ns**, median (min-max) | **73.855 MHz** (71.46-74.40) | **74.125 MHz** (72.65-76.03) | +0.270 MHz, inside the spread |
| Fmax at 40 ns, median | 51.730 MHz | 52.055 MHz | +0.325 MHz |
| Cycles per transform (NTT, INTT; core test) | 118 | 119 | +1 |
| Cycles KeyGen / Encaps / Decaps (profile inputs; simulation) | 8,404 / 10,236 / 15,597 | 8,416 / 10,250 / 15,619 | +12 / +14 / +22 |
| Latency at 15 ns (median Fmax; perhitungan tim) | 113.8 / 138.6 / 211.2 us | 113.5 / 138.3 / 210.7 us | -0.22 % / -0.23 % / -0.22 % |
| Latency at 15 ns (lowest Fmax of 6) | 117.6 / 143.2 / 218.3 us | 115.8 / 141.1 / 215.0 us | |
| Critical warnings per compile | 1 | 1 | the virtual-pin clock warning of every kernel-only compile |
Cycle detail: only the RUN count changes (+12 / +14 / +22 = 2 per transform for 6 / 7 / 11 transforms). INFERENCE for the cause (not measured separately): one cycle of the hold-off `hw_q` after the last host write before the start, and one cycle of the drain, both set by `Pipe`.

## 3. Tests (MEASURED, simulation and formal; `sim_2026-10-04.md`, `formal_2026-10-04.md`)
| # | Result | Evidence |
|---|---|---|
| V1 lint | `verilator --lint-only -Wall` of `mlkem_core3` (K1b parameters) at `NTT_P6` 0 and 1 and of `kpke_smp_top_s10` at 1: rc 0, no warning; `slang`: 0 errors, 0 warnings (run during the build; output not stored as files) | this report |
| V2-V4 NTT core and memory at P = 6 | memory 4/4; core 6/6 bit-exact NTT and INTT, exactly 119 / 119 cycles, 0 stalls; controls NC-M and NC-W fail as required; Verilator and Icarus, 12/12 each | `sim_2026-10-04.md` |
| V5 formal | S10 control proof at P = 6 (H, O, R, A, B, C): PASS; NC-O and NC-A FAIL as required | `formal_2026-10-04.md` |
| V6 sequencer tests, `NTT_P6 = 1` | 3/3 programs bit-exact, constant cycles; control `nchaz` fails as required; both simulators | `sim_2026-10-04.md` |
| V7 core ACVP at K2 | keyGen 25, encapsulation 25, decapsulation 10 equal; 20 random cases equal; chain, protocol, constant cycles pass; Verilator 9/9 (with `nclen`, `ncoff`, `ncrom` controls as required), Icarus 7/7 | same |
| V8 default regression | `NTT_P6 = 0` profile 8,404 / 10,236 / 15,597 (= K1b); `mlkem_core` defaults 9,095 / 10,735 / 16,667 (= Phase 9); `run_s10_tests.py` default 13/13 with 118 / 118; `run_core_tests.py core` 6/6 (Verilator only) | same, `profile_*_2026-10-04.json` |
| V9 Quartus | K2 seeds 1-6 at 40 ns and K2-15 seeds 1-6 at 15 ns, all `rc=0`; met at 40 ns 6 of 6, at 15 ns 6 of 6 | `quartus_K2*_20261004.md` |
| V10 critical paths of K2-15-s5 | worst +1.404 ns: layer counter to the memory ports; reducer to memory now +2.349 ns | `critical_paths_K2-15_2026-10-04.md` |
Constant cycles (V7): Encaps 10,194 and Decaps 15,563 identical across the tested inputs (K1b 10,180 and 15,541); KeyGen over the ACVP seeds 8,344-8,397 (public rejection sampling of A, as before).

## 4. Rule of the plan (section 5), applied to files
1. V1-V8 pass: met.
2. Timing at 40 ns at every seed: met (6 of 6).
3. ALM median at most 20,000: met (14,213.0).
4. Latency of each operation lower than K1b at 15 ns (cycles / median Fmax): met by the numbers (-0.22 %, -0.23 %, -0.22 %).
5. Seeds met at 15 ns reported: 6 of 6 (K1b 6 of 6).
Statement required by the rule: the Fmax gain (+0.270 MHz) is **not** larger than the spread of the seeds, so it is not called a gain. The rule adopts; the evidence says the step is neutral. The team decides (Proposed ADR 0041).

## 5. Estimates against measurements (written in the plan before the measurements)
- Cycles per transform 119: **met** (measured 119 / 119). Cycles of the operations +6 / +7 / +11: **missed, measured +12 / +14 / +22** (the plan counted one cycle per transform; the hold-off and the drain each add one, INFERENCE).
- ALM +0 to +250: **missed in the other direction** (-122.0 at 40 ns, -85.5 at 15 ns; inside the spread of the seeds; the fitter removes the unused bits of the 37-bit reducer stage vector, INFERENCE). Registers +250 to +450: **not met** (about +120).
- Fmax at 15 ns 76 to 80 MHz: **missed, 74.125 MHz**. The plan said the next classes sit 0.7 to 1.1 ns behind the worst path of K1b; that held for the reducer path, but the layer counter class (+1.910 ns in K1b) was the first behind it and is now the wall, and in the K2 seeds it sits at +1.404 .. about +1.8 ns.
- Latency 104-111 / 127-135 / 194-206 us: **missed, 113.5 / 138.3 / 210.7 us**.

## 6. Findings
1. **The reducer-to-memory path is no longer the wall** (+1.170 -> +2.349 ns): the intended effect is real and measured at the path level.
2. **The next wall is the address path of the issue stage**: `layer_q` (and `mode_q`) through `log2len`, `len`, the shifts for block and position, and the bank map to the M10K address and write ports. It already existed in K1b at +1.910 ns. It is combinational arithmetic on values that change once per layer (every 16 cycles at L = 8), so it can be registered without a change of the schedule (INFERENCE; this is the candidate for a step S2b with its own plan and rule, not done here).
3. **Cost of S2:** +12 / +14 / +22 cycles (+0.14 % of KeyGen, Encaps and Decaps cycles) and about +120 registers; ALM unchanged.
4. S2 alone does not raise the Fmax of the design; whether it does together with S2b is not measured.

## 7. What this does not show
No board result; no speed claim against software; kernel-only static timing with virtual pins; seed noise of about 3 MHz limits any statement below that size; constant time means cycle-count invariance only; ACVP is simulation. One seed (K2-15-s5) was analysed for the paths.

## 8. Files
`test_plan_9s2.md` (with amendment A1), `selection_worksheet_2026-10-04.md`, `sim_2026-10-04.md`, `formal_2026-10-04.md`, `critical_paths_K2-15_2026-10-04.md`, `profile_k2_verilator_2026-10-04.json`, `profile_k1b_default_verilator_2026-10-04.json`, `profile_default_verilator_2026-10-04.json`, `cycles_*_k2_*.json`, twelve extracts `quartus_K2*_20261004.md`, `quartus/phase09s2_core/` (twelve revisions, `run_k2.sh`, `run_k2_15.sh`), `scripts/select_9s2.py`, `formal/run_formal_phase9s2.py`, `formal/phase09m-optimisation/9s2/`, changed test runners `tb/s10/run_s10_tests.py`, `tb/smp/run_smp_tests.py`, `tb/mlkem/run_core_tests.py`.
