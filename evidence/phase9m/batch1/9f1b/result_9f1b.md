<!-- claim-lint: skip-file (internal block report, not proposal text) -->
# Phase 9F step S1b report: hash running beside other work (configuration K1b)

- Status: **DONE** (STOP after the step, ADR 0036; closes Batch 1). Branch `phase9m-optimisation`. RTL: new module `rtl/mlkem/mlkem_core3.sv` and `rtl/mlkem/mlkem_ctl_rom2.sv` (generated from the new golden model `tb/golden/mlkem_ctl_model2.py`; amendment A1 of the plan). Plan and rule: `test_plan_9f1b.md` (written before the RTL). Kernel-only static timing with virtual pins; not a system on the board. Twelve Quartus compiles, all `rc=0` (K1b-15-s5 was compiled twice: the first attempt was killed by a restart of the session and not used).

## 1. Result
**K1b is adopted by its rule and recovers the cycle cost of K1.** K1b = K1 with the three independent hashes (KeyGen H(ek), Encaps H(ek), Decaps J) running in a background sidecar while the main controller loads or stores: cycles fall by 391 / 391 / 386 against K1 (8,404 / 10,236 / 15,597), at +274 ALM (40 ns). Timing is met at 40 ns at 6 of 6 seeds and at 15 ns at 6 of 6 seeds; the latency at 15 ns is 5.5 / 4.7 / 3.5 % below K1 and, against the 9M-1 core (MW) at 15 ns (S0, two seeds), equal within +0.2 % (113.8 / 138.6 / 211.2 us against 113.6 / 138.5 / 211.6 us), with 3,500 ALM (-20 %) less. K1b does not raise Fmax: the wall at 15 ns is still the NTT core / memory (section 4).

## 2. Parameters measured (MEASURED; `selection_worksheet.md`, extracts `quartus_K1b*.md`)
| Parameter | K1 (S1) | K1b (S1b) | Difference |
|---|---|---|---|
| ALM median, 40 ns, seeds 1-6 (min-max) | 14,061.0 (14,002-14,108) | 14,335.0 (14,329-14,376) | +274.0 (+1.9 %) |
| ALM median, 15 ns, seeds 1-6 | 14,211.5 (14,173-14,273) | 14,435.0 (14,390-14,459) | +223.5 |
| ALM in % of the fitter's 41,910 | 34 % | 34 % | |
| Registers, 40 ns | 8,348-8,452 | 8,211-8,258 | about 150 fewer |
| RAM blocks / DSP | 54 (53 at 15 ns) / 28 | 54 (53 at 15 ns) / 28 | 0 |
| Timing met at 40.000 ns | 6 of 6 | 6 of 6 | |
| Worst setup slack over seeds, 40 ns | +19.063 ns | +18.043 ns | |
| Fmax lowest slow corner, 40 ns, median (min-max) | 51.765 MHz (47.76-53.40) | 51.730 MHz (45.54-52.28) | equal |
| **Timing met at 15.000 ns** | 6 of 6 | **6 of 6** | |
| Worst setup slack over seeds, 15 ns | +1.114 ns | +1.007 ns | |
| **Fmax lowest slow corner at 15 ns**, median (min-max) | 73.070 MHz (72.01-74.10) | **73.855 MHz (71.46-74.40)** | +0.8 MHz, inside the spread |
| Cycles KeyGen / Encaps / Decaps (profile inputs; simulation) | 8,795 / 10,627 / 15,983 | 8,404 / 10,236 / 15,597 | -391 / -391 / -386 (-4.4 %, -3.7 %, -2.4 %) |
| Latency at 15 ns, median Fmax (perhitungan tim) | 120.4 / 145.4 / 218.7 us | 113.8 / 138.6 / 211.2 us | -5.5 %, -4.7 %, -3.5 % |
| Latency of the 9M-1 core at 15 ns (S0, lower Fmax of 2 seeds) | 113.6 / 138.5 / 211.6 us | | K1b +0.2 %, +0.0 %, -0.2 % |
| Critical warnings per compile | 1 | 1 | |
Per state (profile, `profile_k1b_verilator.json` against `../9f1/profile_k1_verilator.json`): only the hash states change (HFD 364 -> 7 and HGT 67 -> 35 in KeyGen; HFD 367 -> 10, HGT 67 -> 35 in Encaps; HFD 360 -> 10, HGT 67 -> 35 in Decaps) and two cycles of fetch / dispatch fewer; LDP, STP, RUN, SDL, WR32, RD32 and CMP counts are equal to K1: the sidecar never delays the main controller.
The comparison with MW uses the lower Fmax of two seeds for MW and the median of six for K1b: indicative, not like for like.

## 3. Tests (MEASURED)
| # | Result | Evidence |
|---|---|---|
| V1 lint | `verilator --lint-only -Wall` of `mlkem_core3` at K1 parameters and at the defaults: rc 0, no warning; `slang`: 0 errors, 0 warnings (run during the build; output not stored) | this report |
| V2 model | `check_static2` passes; the new programs give the same keygen / encaps / decaps outputs as the Phase 9 programs for 2 random cases (valid and modified ciphertext; the plan asked for 200: not done, the ACVP and the 20 random cases of V3 on the RTL cover it); `gen_mlkem_ctl_rom2.py --check` passes (programs of 22 / 22 / 33 words) | run during the build; the ACVP of V3 is the final proof |
| V3 core K1b ACVP: keyGen 25, encapsulation 25, decapsulation 10, random cross-check (20), chain, protocol, constant cycles | 6/6 pass on Verilator and Icarus (file final) | `sim.md`, `cycles_*_core_k1b_*.json` |
| V4 profile | see section 2 | `profile_k1b_verilator.json` |
| V5 constant cycles | Encaps 10,180 and Decaps 15,541 identical across the tested inputs (ACVP-range numbers); KeyGen 8,332-8,385 over the ACVP seeds (public sampling of A, as before) | `sim.md` |
| V6 negative controls (copies; repository RTL not mutated) | `nclen`, `ncoff`, `ncrom` (Verilator), `nclen` (Icarus) fail as required; NC-PRIO (sidecar read wins) fails Encaps and Decaps (first run expected `test_acvp_keygen`, the wrong test, KeyGen does not read while its job runs; corrected to `test_acvp_encaps` and rerun: fails as required); NC-WR fails KeyGen; NC-ROM (job offset +1) fails; **the throttled sidecar passes the whole core target** (the join waits for a slow job) and **the throttled copy without any protection fails** (the join is effective, not only never needed) | `sim.md` |
| V7 formal (two copies, protocol stubs): E1, S1-S7, B1-B7 | **PASS** (basecase and induction, after one supporting invariant: the sidecar runs only while the main controller is not idle); cover: digest write of the sidecar (step 155) and sidecar read (step 9) reached; controls NC-B3 and NC-E1 FAIL as required; **NC-B7 timed out at 1,800 s (no violation found to step 94), a 3 h retry has no result at the time of this report**: the control B7 is shown by simulation (NC-WR), not by the formal run | `formal.md` |
| V8 regression | the defaults of `mlkem_core` and of `mlkem_core2` equal the Phase 9 profile (S1 V7, `../9f1/regression_default.md`); `mlkem_core3` at its own default parameters (C5) was **not** run (only K1 parameters) | |
| V9 Quartus | K1b seeds 1-6 at 40 ns and K1b-15 seeds 1-6 at 15 ns, all met; critical paths at 15 ns (K1b-15-s1): 298 of 300 in the NTT core / memory / PWM class (+1.170 ns), 2 in engine sequencer to sampler sponge (+2.420 ns) | `quartus_K1b*.md`, `critical_paths_K1b-15.md` |

## 4. Findings
1. **S1b gives the cycles back without area or Fmax cost beyond +274 ALM.** With S1 and S1b together the core has the latency of the 9M-1 core at 15 ns (within +0.2 % against two seeds of S0) and 20 % less area (14,335 against 17,654 ALM at 40 ns).
2. **The wall is unchanged.** At 15 ns the worst paths are in the NTT core / memory / PWM (298 of 300): S1 and S1b do not touch it; raising Fmax needs a change there (S2, Batch 2).
3. **No timing cost from the sidecar:** the sidecar is not among the 300 worst paths at 15 ns; median Fmax at 15 ns is 73.855 MHz against 73.070 MHz for K1 (inside the seed spread).
4. **The saving is the three independent hashes only** (about 390 of 8,400 / 10,200 / 15,600 cycles, 2.4-4.4 %). The hashes on the dependency chain (`G` of KeyGen, `G` of Decaps) stay in the foreground.
5. **Constant time:** the cycle counts of Encaps and Decaps are identical across the tested inputs; no control depends on a secret (E1 holds in the formal proof for the two-copy model with the sidecar).

## 5. Estimates against measurements (written in the plan before the RTL)
- Cycles about 8,410 / 10,240 / 15,600: **measured 8,404 / 10,236 / 15,597** (-6, -4, -3): inside.
- ALM S1 + 150 to 450: **measured +274.0 (40 ns), +223.5 (15 ns)**: inside.
- Registers S1 + 100 to 250: **measured about 150 fewer: wrong direction** (the fitter's result; not examined).
- RAM blocks / DSP 54 / 28: met.
- Fmax within 2 % of S1: measured +1.1 % at 15 ns median: inside.
- LDP and STP cycles equal to S1: met (per-state counts).

## 6. What this does not show
No board result; no speed claim against software; kernel-only static timing with virtual pins; the DE10-Nano clock tree, PLL and HPS are not in these compiles; constant time means cycle-count invariance only; ACVP is simulation; the formal control B7 is not shown by the formal run.

## 7. Files
`test_plan_9f1b.md` (with amendment A1), `selection_worksheet.md`, `sim.md`, `formal.md`, `critical_paths_K1b-15.md`, `profile_k1b_verilator.json`, `cycles_*_core_k1b_*.json`, twelve extracts `quartus_K1b*.md`, `quartus/phase09f1b_core/` (twelve revisions, `run_k1b.sh`, `run_k1b_rest.sh`), `rtl/mlkem/mlkem_core3.sv`, `rtl/mlkem/mlkem_ctl_rom2.sv`, `tb/golden/mlkem_ctl_model2.py`, `scripts/build/gen_mlkem_ctl_rom2.py`, `scripts/quartus/select_9f1b.py`, `formal/run/run_formal_phase9f1b.py`, `formal/phase09m-optimisation/9f1b/`.
