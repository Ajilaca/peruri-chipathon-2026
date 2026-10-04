<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Phase 9F step S2b: registered issue address in the NTT/INTT core (address computed one cycle early) — test plan and adoption rule

Written 2026-10-04 before any S2b RTL and before any S2b measurement. Scope: S2b is the follow-up named in `../9s2/result_9s2.md` section 6 (Batch 2, Jevan, same session; commits on the branch `phase9m-optimisation`, not made yet). Baseline: **K2** (`../9s2/`, `mlkem_core3` with `NTT_P6 = 1`). Labels: MEASURED, ESTIMATE, INFERENCE. Kernel-only static timing with virtual pins; not a board result.

## 1. Why (MEASURED: the worst path of K2-15-s5, slack +1.404 ns at 100 C; `../9s2/critical_paths_K2-15_2026-10-04.md`; element-level reading of the same report, 2026-10-04)
55 of the 300 worst paths of K2 run from `layer_q` to the address and write ports of the M10K banks, the others in the first 144 are at +2.354 ns and more. The worst path is one clock cycle and has two halves of about equal length:
1. **Address arithmetic** (about 5 ns, `layer_q` to the adder outputs): decode of `log2len` from `layer_q` and `mode_q` (0.6 ns), the shifts `p >> log2len` and `block << (log2len+1)` (1 ns), the adders for `j` and `j + len` (about 3 ns).
2. **Bank decode and address multiplexer** (about 6 ns, adder outputs to the RAM address pins): the bank number of each port (`bank_r`, fanout 65), then for each bank the multiplexer that selects the address of the port that addresses it (two LUT levels with 1.6 ns and 1.7 ns of routing), then the RAM port.
Only the first half depends on the schedule counters. If the address of the **next** cycle is computed in the previous cycle and registered, the path splits at the adder outputs: both halves fit into one cycle with margin (the first half then starts at `t_q` / `layer_q` and ends at a register, about 5 ns plus the next-state logic of the counters, about 1.5 ns; the second half starts at the register, about 6.5 ns). That is a cut in the middle of the path, with **no extra cycle** because the registered address is the same value that is used in the same cycle today.
The classes behind it in the K2 seed, MEASURED: `mode_q` to the Barrett reducer (+2.354 ns, 144 paths), side-operand delay to the M10K (+2.102 ns, 45), the read-position delay to the reducer (+2.587 ns, 24), the reducer to the M10K (+2.349 ns, 18). So the best case for S2b is a wall at about +2.1 to +2.4 ns, about 0.7 to 1.0 ns better than the K2 seed analysed (INFERENCE).

## 2. Design (a parameter, as S2)
1. Parameter `AREG` (default 0, the K2 / K1b design) of `rtl/ntt/ntt_core_s10.sv`: when 1, the issue-stage addresses `j_lane` and `jlen_lane` of the transform (`state_q == S_RUN`) come from registers `j_q` and `jlen_q` that are loaded every cycle with the values the combinational arithmetic would produce **in the next cycle**: the same function evaluated on `layer_d`, `t_d` and the mode of the next cycle (`mode_i` in the cycle that starts a run, `mode_q` otherwise). The host path (single-address access of lane 0 outside a run, `host_addr_i`) stays combinational, so the host read latency (2) and the sequencer are untouched. Nothing else changes: enables, write controls, the zeta path, the memory and its write delay.
2. Parameter forwarding as in S2: `P6`-style parameter `AREG` of the wrapper `ntt_core_s10_p5`, `NTT_AR` of `kpke_smp_top_s10` and of `mlkem_core3` (all default 0), and the same extra parameter in the formal stub of the engine (`formal/phase09-integration/9c/stubs_9c.sv`; lesson of S2: the formal flows of `mlkem_core3` fail to elaborate without it).
3. **Equivalence argument (INFERENCE, checked by test):** with `AREG = 1` the address presented to the memory in every cycle of a run equals the address of `AREG = 0` in that cycle, so every request, write time, cycle count and result is unchanged. The cycle count per transform stays 119 (at P = 6). Any difference is a bug.
4. Cost (ESTIMATE): 8 lanes x two 8-bit address registers = 128 registers; no ALM change beyond routing.

## 3. Estimates written before measuring (ESTIMATE; K2 numbers are MEASURED)
| Quantity | K2 (MEASURED) | S2b ESTIMATE |
|---|---|---|
| Cycles per transform (NTT, INTT) | 119 | 119 (no change) |
| Cycles KeyGen / Encaps / Decaps | 8,416 / 10,250 / 15,619 | equal |
| ALM median at 40 ns | 14,213.0 | within +-150 |
| Registers (40 ns) | 8,327-8,375 | +100 to +200 |
| RAM blocks / DSP | 54 / 28 | 54 / 28 |
| Fmax lowest slow corner at 15 ns, median of 6 seeds | 74.125 MHz | 75 to 79 MHz. **Low confidence:** the plan of S2 estimated 76 to 80 MHz and measured 74.1 because the next class was only 0.2 ns behind; here the classes behind the worst are 0.7 to 1.0 ns behind (INFERENCE), only 300 paths of one seed are known, and the seed noise is about 3 MHz |
| Latency at 15 ns, KeyGen / Encaps / Decaps (cycles / median Fmax) | 113.5 / 138.3 / 210.7 us | 107 to 112 / 130 to 137 / 198 to 208 us |
A result outside a range is stated as such in the report.

## 4. Tests (both simulators; repository RTL never mutated, controls on copies)
| # | Test | Pass condition |
|---|---|---|
| V1 | lint: Verilator `-Wall` and slang of `ntt_core_s10_p5` (`AREG` 0 and 1), `kpke_smp_top_s10`, `mlkem_core3` at K2 with `NTT_AR` 0 and 1 | 0 warnings, 0 errors |
| V2 | NTT core unit test at P = 6 with `AREG = 1` (new target `s10p6a` of `tb/s10/run_s10_tests.py`) | bit-exact NTT and INTT, cycles exactly 119 / 119, 0 stalls, Verilator and Icarus |
| V3 | control NC-A1: a copy in which the registered address is taken one cycle too late (the register is loaded from the values of the current cycle) | bit-exact NTT and INTT must FAIL |
| V4 | formal: S10 control proof at P = 6 with `AREG = 1` (properties H, O, R, A, B, C; a copy of the S2 formal top), and its negative controls NC-O, NC-A | proofs PASS, controls FAIL as required |
| V5 | K-PKE sequencer tests with `NTT_P6 = 1`, `NTT_AR = 1` (`KP_VAR = 2`, K0 sampler) | 3/3 pass, both simulators |
| V6 | core `mlkem_core3` at `NTT_P6 = 1`, `NTT_AR = 1`: the whole `core` target and the profile | 100 % equal; cycles **identical to K2** (8,416 / 10,250 / 15,619); Encaps and Decaps identical across inputs; Verilator and Icarus |
| V7 | regression at the defaults: `AREG = 0` profile equals K2 and K1b profiles (8,416 / 10,250 / 15,619 at `NTT_P6 = 1`, 8,404 / 10,236 / 15,597 at 0); `run_s10_tests.py` default (118) and `s10p6` (119) targets pass; formal of `mlkem_core3` (9f1b proofs) still elaborates and passes with the stub change | PASS |
| V8 | Quartus K3 (K2 + `NTT_AR = 1`) seeds 1-6 at 40.000 ns (gate) and K3-15 seeds 1-6 at 15.000 ns, one compile at a time (RAM limit of the machine: at least 2 GB free), no constraint below 15 ns (ADR 0039) | extracts; timing met at 40 ns at every seed; at 15 ns the number of seeds met and the Fmax of each seed |
| V9 | critical paths of the smallest-slack seed at 15 ns, classified as in S2, plus the element-level reading of the worst path | recorded: which block is the next wall |

## 5. Adoption rule (fixed before measuring; ADR 0036: by latency at 15 ns; tightened after S2: a gain inside the seed noise is not adopted)
S2b is **adopted** on top of K2 only if all hold:
1. V1-V7 pass as stated (any ACVP mismatch rejects it).
2. Timing met at 40.000 ns at every seed 1-6.
3. ALM median at most 20,000.
4. For each of KeyGen, Encaps and Decaps, t = cycles / median Fmax at the 15 ns constraint (lowest slow corner, seeds 1-6) of K3 is lower than that of K2 (113.5 / 138.3 / 210.7 us).
5. The median Fmax gain over K2 (74.125 MHz) is **larger than the larger spread of the seeds** of K2 (3.38 MHz) and K3, **or** the lowest seed of K3 is above the highest seed of K2 (76.03 MHz); a gain inside the noise is reported as neutral and S2b is then **not adopted** (the S2 lesson).
6. The number of seeds met at 15 ns is reported.
Otherwise S2b is reported as not adopted and K2 stays. The result is a Proposed ADR.

## 6. Not in this step
No change to the arithmetic, the schedule, the memory map or the bank map; no change to the host path or the sequencer; no second sampler (S3); no overlap with the engine (item 4); no constraint below 15 ns; no board result. If V9 shows a next wall that a further small change could move, it is only proposed in the report. Constant time means cycle-count invariance only.

## 7. Amendment A1 (2026-10-04, before any S2b measurement; nothing above is edited)
1. **The 40 ns gate stays.** A proposal to skip the 40 ns compiles was made and withdrawn the same day (Jevan, chat 2026-10-04: "kita test aja di 40ns gapapa"): sections 4 (V8) and 5 (items 2 and 3) apply as written, six compiles at 40.000 ns (`K3`, `K3-s2` .. `K3-s6`) after the six at 15.000 ns.
2. **Decision for the batch (Jevan, same chat):** after S2b the work goes to item 4 (overlap of load / store with the engine). If S2b, like S2, gives no effect beyond the seed noise, S2 and S2b are to be removed (what exactly is deleted is confirmed with the team before anything is deleted; the evidence of the negative result is kept unless the team says otherwise).
3. **Run note:** the first runner `run_k3.sh` (15 ns first, then 40 ns) was stopped after K3-15-s1 (rc 0) by mistake of the operator while K3-15-s2 was running; the rest runs under `run_k3_15.sh` (K3-15-s3 .. s6, K3-15-s2 finished beside it) and then `run_k3_40.sh` (the six 40 ns revisions). Same compiles, same order of results, one at a time.

## 8. Amendment A2 (2026-10-04, written AFTER the six 15 ns seeds were measured; the rule of section 5 is not changed)
The six 15 ns seeds gave K3 median 77.555 MHz against 74.125 MHz of K2 (+3.430 MHz), five of six seeds of K3 (77.32-79.37 MHz) above every seed of K2 (maximum 76.03 MHz) and one seed (seed 4, 73.02 MHz) below; the spread of K3 (6.35 MHz) is larger than the gain, so item 5 of section 5 is **not met as written**. At the request of Jevan (chat 2026-10-04: "setelah 40ns selesai jalankan 3 seed tambahan") three further seeds (7, 8, 9) of K3 at 15.000 ns are compiled after the 40 ns compiles (`K3-15-s7` .. `K3-15-s9`, `run_k3_x.sh`). They are **additional information chosen after seeing the result**: the formal outcome of the rule stays "not met as written" with the six seeds; the nine-seed statistics (median, spread, how many seeds are above the highest seed of K2) are reported beside it, and no seed is dropped or replaced. K2 has six seeds only; the comparison of nine against six is stated as such. Adoption stays a decision of the team (Proposed ADR).
