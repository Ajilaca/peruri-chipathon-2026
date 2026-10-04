<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Phase 9F step S2: register after the Barrett reducer in the NTT/INTT core (P = 5 -> 6) — test plan and adoption rule

Written 2026-10-04 before any S2 RTL and before any S2 measurement. Scope: ADR 0036 (Accepted: S2 attacks the limit that S1 exposes) and the batch plan of chat 2026-10-04 (S2 belongs to Batch 2, taken over by Jevan in the same session; commits on the branch `phase9m-optimisation`). Baseline: **K1b** (`../9f1b/`, `mlkem_core3`: K0 sampler, K0 hash, two-byte codec, background hash). Labels: MEASURED, ESTIMATE, INFERENCE. Kernel-only static timing with virtual pins; not a board result.

## 1. Why (MEASURED: the worst paths of K1b at 15 ns, seed 1, `critical_paths_K1b-15_2026-10-04.md`; field-level breakdown recomputed 2026-10-04 from the archived database, raw report not stored)
298 of the 300 worst paths are in the NTT core / memory class (the other 2 are engine sequencer to sampler sponge at +2.420 ns). The single worst (slack +1.170 ns, 182 of the 300 paths share its shape) runs in **one clock cycle** from the last register of the Barrett reducer (`g_cut[2]`, the cut after the second subtraction) through four blocks of logic into the write data of an M10K bank:
1. the last Barrett step (`d3 = r - q`, select `p3`): the 13-bit subtraction chain plus the select, about 3.1 ns (6.5 to 9.6 ns on the path);
2. the butterfly add / subtract (`add_mod`, `sub_mod`: a 12-bit add chain plus the compare with q and the output select): about 4.3 ns (9.6 to 13.9 ns);
3. the write-data multiplexer of the bank (`g_bank[4].wd[*]`, two logic levels with long routing): about 4.0 ns (13.9 to 17.9 ns);
4. routing to the RAM write port and its setup: about 1.4 ns.
Other classes in the same compile, MEASURED: the mode register to the butterfly (+2.212 ns, 72 paths), the memory read select to the butterfly (+2.288 ns, 24 paths), the layer counter to the memory (+1.910 ns, 20 paths). So a cut between block 1 and block 2 moves the wall by about 1.2 to 1.5 ns in the best case (the next class at +1.9 ns), not more; the next wall after it is a different one (INFERENCE).
The Barrett module already supports a fourth cut: `REG_AFTER[3]` registers `p3`, the output of the final correction. The cuts in use are bits 0, 1, 2 (P = 5: read latency 2 plus three multiplier cuts). Setting bit 3 gives P = 6. **No new arithmetic, no new hardware structure: a parameter.**

## 2. Design (smallest safe change, a parameter first)
1. New wrapper `rtl/ntt/ntt_core_s10_p6.sv`: `ntt_core_s10` at `NUM_LANES = 8`, `RD_LAT = 2`, `MUL_REG` bits 0, 1, 2, 3 (P = 6). The core already derives `WrDly`, `Pipe`, the drain counter, the write delay of the memory (`WR_DELAY`), the delayed side operand (`u_side`, `Lat`) and the delayed host-write alignment from `MUL_REG`; no edit of `ntt_core_s10.sv`, `butterfly_m6.sv`, `modmul_barrett.sv`, `poly_mem_m10k.sv`.
2. Parameter `NTT_P6` (default 0) on `kpke_smp_top_s10` (a generate selects `ntt_core_s10_p5` or `ntt_core_s10_p6`) and on `mlkem_core3` (forwarded to the engine). At the default 0 the elaborated design is the K1b design (V8 checks cycles and the Quartus-relevant netlist inputs). `mlkem_core.sv` and `mlkem_core2.sv` are not edited.
3. The sequencer (`kpke_sched_smp`) depends on the NTT core only through the host read latency (`CORE_RDLAT = 2`, unchanged) and `busy`/`done`; it does not depend on `Pipe` (checked by reading the file, V6 checks by simulation).
4. Stall freedom (INFERENCE, `../ntt_pipeline_depth_analysis_2026-10-04.md`): the largest P without a stall at a layer boundary is 7 for L = 8; P = 6 stalls nowhere, so one transform takes 113 + 6 = **119 cycles** (118 at P = 5). The formal properties A, B, C (V5) and the bit-exact tests prove or measure this; nothing is assumed in the RTL.

## 3. Estimates written before measuring (ESTIMATE; K1b numbers are MEASURED)
| Quantity | K1b (MEASURED) | S2 ESTIMATE |
|---|---|---|
| NTT / INTT cycles per transform | 118 | 119 (+1) |
| Cycles KeyGen / Encaps / Decaps (profile inputs; 6 / 7 / 11 transforms) | 8,404 / 10,236 / 15,597 | 8,410 / 10,243 / 15,608 (+6 / +7 / +11) |
| ALM median at 40 ns | 14,335.0 | +0 to +250 |
| Registers (40 ns) | 8,211-8,258 (`../9f1b/selection_worksheet_2026-10-04.md`) | +250 to +450 (8 lanes x two 12-bit stages: reducer output and side operand, about 190; write-delay chain of the memory control for 16 ports, about 150) |
| RAM blocks / DSP | 54 / 28 | 54 / 28 |
| Fmax lowest slow corner at 15 ns, median of 6 seeds | 73.855 MHz | 76 to 80 MHz (the next classes sit 0.7 to 1.1 ns behind the worst path of K1b; skew and placement vary by seed) |
| Latency KeyGen / Encaps / Decaps at 15 ns (cycles / median Fmax) | 113.8 / 138.6 / 211.2 us | 104 to 111 / 127 to 135 / 194 to 206 us |
A result outside a range is stated as such in the report.

## 4. Tests (both simulators; the repository RTL is never mutated, controls run on copies)
| # | Test | Pass condition |
|---|---|---|
| V1 | lint: Verilator `-Wall` and slang of `ntt_core_s10_p6`, `kpke_smp_top_s10` at `NTT_P6` 0 and 1, `mlkem_core3` at K1b and at `NTT_P6 = 1` | 0 warnings, 0 errors |
| V2 | NTT core unit test (`tb/s10/run_s10_tests.py`, new target `s10p6`: the S10 core test with `C3_WRDLY = 4`) | bit-exact NTT and INTT against the golden model, cycles exactly 119 / 119, Verilator and Icarus |
| V3 | memory unit test at `WR_DELAY = 4` (new target `mem6`) | pass, both simulators |
| V4 | negative controls on copies for P = 6: NC-M (bank map without the XOR bit) and NC-W (write control one cycle short) | bit-exact NTT and INTT must FAIL |
| V5 | formal: the S10 control proof (properties H, O, R, A, B, C) with P = 6 (a copy of the formal top with `P = 6`, depth 9), and its negative control (F_SKEW) | proofs PASS, control FAIL as required |
| V6 | K-PKE sequencer tests with `NTT_P6 = 1` (`KP_VAR = 2`, K0 sampler): three programs bit-exact, constant cycles for fixed rho, stall coverage | 3/3 pass, both simulators |
| V7 | core `mlkem_core3` with `NTT_P6 = 1`: the whole `core` target (ACVP keyGen 25, encapsulation 25, decapsulation 10, random cross-check, chain, protocol, constant cycles) and the profile | 100 % equal, both simulators; cycles as section 3 (+6 / +7 / +11 against K1b, only the RUN count and the NTT-bound states change); Encaps and Decaps cycle counts identical across inputs |
| V8 | regression at the defaults: `NTT_P6 = 0` gives the K1b profile (8,404 / 10,236 / 15,597) and the S10 target (`s10`, `ncm`, `ncw`, `mem`, `p6`) passes with 118 / 118; the default profile of `mlkem_core` is unchanged (9,095 / 10,735 / 16,667) | PASS |
| V9 | Quartus K2 (K1b + `NTT_P6 = 1`) seeds 1-6 at 40.000 ns (the gate) and K2-15 seeds 1-6 at 15.000 ns (ADR 0036 point 3), one compile at a time per project; no constraint below 15 ns (ADR 0039) | extracts; timing met at 40 ns at every seed; at 15 ns the number of seeds met and the Fmax of each seed |
| V10 | critical paths of the best-slack seed at 15 ns, classified as in S1 (`classify_paths_9f.py`) plus the field-level breakdown of the worst path | recorded: which block is the next wall |
Order: V1-V8 first (fast gates); V9 only for the final design of the step.

## 5. Adoption rule (fixed before measuring; ADR 0036: by latency at 15 ns)
S2 is **adopted** on top of K1b only if all hold:
1. V1-V8 pass as stated (any ACVP mismatch rejects it).
2. Timing met at 40.000 ns at every seed 1-6.
3. ALM median at most 20,000 (the budget).
4. For each of KeyGen, Encaps and Decaps, t = cycles / median Fmax at the 15 ns constraint (lowest slow corner, seeds 1-6) of K2 is lower than that of K1b (113.8 / 138.6 / 211.2 us).
5. The number of seeds that meet 15 ns is reported; if K2 meets fewer seeds than K1b (6 of 6) the rule is applied to the seeds that meet it in both and the difference is stated.
Whether the Fmax gain is larger than the spread of the seeds is stated (K1b: 72.0 to 74.1 MHz class of spread); a gain inside the spread is reported as such and is not called a gain. Otherwise S2 is reported as not adopted and K1b stays. The result is a Proposed ADR.

## 6. Not in this step
No change to the arithmetic, the schedule or the memory map; no second sampler (S3); no overlap with the engine (item 4); no constraint below 15 ns; no board result; constant time means cycle-count invariance only. If V10 shows a next wall that a further small change could move (for example duplicated mode register per lane, a read-select register), it is **proposed in the report as S2b with its own plan and rule**, not done under this plan.

## 7. Amendment A1 (2026-10-04, written while building; nothing above is edited and the rule of section 5 is unchanged)
1. **No new wrapper file.** Section 2 items 1 and 2 name `rtl/ntt/ntt_core_s10_p6.sv` and a generate in `kpke_smp_top_s10`. A new module would have required every file list that elaborates the engine (simulation runners, formal `.sby` files, Quartus `.qsf` files of 9c, 9M, 9F) to be edited. Instead the existing wrapper `rtl/ntt/ntt_core_s10_p5.sv` gets a parameter `P6` (default 0 = the P = 5 design, unchanged), `kpke_smp_top_s10` gets `NTT_P6` (default 0) and forwards it, `mlkem_core3` gets `NTT_P6` (default 0). The module name `ntt_core_s10_p5` stays at P = 6 (documented in its header).
2. **V1 is run for `NTT_P6` 0 and 1** on every file list in use (Verilator and slang on the test top levels); V8 confirms that the default netlist inputs and the cycle counts are those of K1b.
