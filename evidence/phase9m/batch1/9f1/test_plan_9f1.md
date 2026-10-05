<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Phase 9F step S1: K0 sponge in both places (hash instance and the sampler of the engine) - test plan and adoption rule

Written 2026-10-04 before any S1 RTL change and before any S1 compile. Scope: ADR 0036 (Accepted, Faza Dzil), step S1. Baseline: the 9M-1 core (`CODEC_W2 = 1`, C5 everywhere), report `../9m1/result_9m1.md`; the critical-path report `../../critical_paths_MW.md` (all 300 worst paths at 20 ns inside the two C5 permutations). Labels: MEASURED, ESTIMATE, INFERENCE, perhitungan tim. The mathematics is locked (C1): K0 and C5 compute the same Keccak-f[1600]; only the rounds per cycle differ.

## 1. What changes
- `rtl/mlkem/mlkem_core.sv`: one new parameter `SMP_C5` (default 1) passed to the engine's `CORE_R2` (now written as the constant `1'b1`). At the default the behaviour is exactly that of Phase 9 / 9M-1. The engine files (Phase 6-8, frozen) are not edited: `kpke_smp_top_s10`, `kpke_sched_smp` and `keccak_sampler` already have the parameter `CORE_R2` (K0 sampler verified in Phase 8b; the full sequencer with the K0 sampler was **not** run in Phases 8c/8d: that is what V2 and V3 add).
- Configuration K1: `HASH_C5 = 0`, `SMP_C5 = 0`, `CODEC_W2 = 1` (the hash instance K0 is item 3).

## 2. Estimates written before measuring (ESTIMATE; sources: 8b cycles per polynomial, 9b cycles per hash, area of 8b and 9b blocks)
| Quantity | MW (C5, MEASURED) | K1 ESTIMATE |
|---|---|---|
| Sampling cycles inside one operation (perhitungan tim, 8b: KeyGen 2,770 -> 3,168, Encaps and the re-encryption of Decaps 2,922 -> 3,332) | | +398 (KeyGen), +410 (Encaps, Decaps), partly hidden by the 8d overlap |
| Cycles KeyGen / Encaps / Decaps (profile inputs) | 8,327 / 10,159 / 15,515 | about 8,850 / 10,690 / 16,045 (hash +120 and sampling about +400 each, no hiding assumed) |
| ALM median | 17,654.0 | about 13,400 (hash instance -2,513 from 9b, sampler -1,739 from 8b; +/- 500) |
| Registers | 8,189-8,376 | about -1,000 to -1,500 |
| RAM blocks / DSP | 54 / 28 | 54 / 28 |
| Fmax at the 40 ns gate (lowest slow corner, median) | 48.855 MHz | 52-60 MHz (the Keccak permutations leave the critical list; the next limit is not identified) |
| Fmax at a 15 ns constraint (median, seeds 1-6) | not measured (S0 gives the baseline) | 62-70 MHz |
| Latency at the Fmax of the 15 ns constraint | MW at 20 ns: 8,327 / 10,159 / 15,515 cycles at 63.990 MHz = 130.1 / 158.8 / 242.5 us | about 126-143 / 153-172 / 229-259 us: the same as MW within the estimate range, not clearly lower |
The honest expectation: a higher Fmax and about 4,200 ALM less, with latency about equal to MW at 20 ns because the cycles grow (ADR 0036 point 2: the rule uses latency).

## 3. Tests (both simulators; repository RTL never mutated)
| # | Test | Pass condition |
|---|---|---|
| V1 | lint Verilator `-Wall` and slang of the core at `SMP_C5 = 0`, `HASH_C5 = 0`, `CODEC_W2 = 1` and at the defaults | 0 warnings, 0 errors |
| V2 | the Phase 8c/8d sequencer tests with the K0 sampler: `tb/smp/test_kpke_smp.py` (3 programs bit-exact, counters, constant cycles for fixed rho, PWMS stall coverage, STRESS) built with `CORE_R2 = 0` (env `KP_CORE_R2=0` in the runner) | all pass, both simulators; the stall classes are covered (the K0 sampler is slower: more waits in PWMS) |
| V3 | core at `SMP_C5 = 0`, `HASH_C5 = 0`, `CODEC_W2 = 1`: the whole 9c `core` target (ACVP keyGen 25, encapsulation 25, decapsulation 10, random cross-check, chain, protocol, constant cycles) | 100 % equal, both simulators |
| V4 | profile (`tb/mlkem/profile_core.py`, same inputs) at K1 | recorded; RUN, HFD and HGT states longer, every other state count equal to MW |
| V5 | control that the K0 sampler is really in use and tested: `nclen` at K1 | `test_acvp_encaps` fails, both simulators |
| V6 | formal: the sequencer proofs of 8c and 8d (F1-F5) at `CORE_R2 = 0` with the sampler protocol stub (the stub does not depend on the sponge: INFERENCE; run to show the proofs hold at the parameter value) and the 9c controller proof (independent of the parameter) | as 8c/8d, ALL AS EXPECTED |
| V7 | regression at the defaults: `scripts/test/phase9c_verify.sh` and a profile equal to the Phase 9 profile | PASS |
| V8 | Quartus: revision K1 seeds 1-6 at 40.000 ns (the gate) and K1-15 seeds 1-6 at 15.000 ns (information, ADR 0036 point 3), one at a time, kernel-only | extracts; timing at 40 ns met at every seed; at 15 ns: the number of seeds met and the Fmax reported |
| V9 | critical-path classification of K1 at the tightest constraint met (script `scripts/quartus/phase5m_top_paths.tcl` on a copy) | names the block that limits timing (input to S2) |

## 4. Parameters reported
ALM (median, min-max, % of the fitter's denominator, against the 20,000 budget), registers, RAM blocks, block memory bits, DSP, worst setup and hold slack, timing met per seed, Fmax lowest slow corner (median, min-max) at 40 ns and at 15 ns; cycles per operation (profile inputs and ACVP ranges); latency t = cycles / median Fmax at each constraint (perhitungan tim); ACVP counts; formal results; critical warnings; the limiting block.

## 5. Adoption rule (fixed before measuring; ADR 0036: by latency)
K1 is **adopted** as the high-Fmax / small-area configuration only if all hold:
1. V1-V7 pass as stated (any ACVP mismatch rejects it).
2. Timing met at 40.000 ns at every seed 1-6.
3. ALM median at most 20,000 (the budget).
4. For each of KeyGen, Encaps and Decaps, t = cycles / median Fmax at the 15 ns constraint (seeds 1-6, lowest slow corner) of K1 is at most 3 % above the latency of MW at its 20 ns result (`../9m2/selection_worksheet.md`: 130.1 / 158.8 / 242.5 us).
5. At 15 ns timing is met at every seed 1-6 **or** the failing seeds are named and the Fmax is reported for the seeds that meet it (the statement then reads "met at k of 6 seeds").
If item 4 fails but items 1-3 hold, K1 is reported as a **smaller, not faster** configuration and the team decides (ADR 0033 and 0035 list the choices); latency is never claimed lower than measured. The result is a Proposed ADR.

## 6. Not in this step
No S2 change (the next limit is only identified, V9); no board result; no clock claim for the DE10-Nano (a PLL decision belongs to Phase 10); constant time means cycle-count invariance only.

## 7. Amendment A1 (2026-10-04, written while building; nothing above is edited and the rule of section 5 is unchanged)
1. **New module instead of editing `mlkem_core.sv`:** section 1 said the parameter `SMP_C5` is added to `rtl/mlkem/mlkem_core.sv`. The S0 Quartus campaign (`quartus/phase09f0_core`, sources of `mlkem_core.sv`) was still compiling, and an edit would change what its later revisions read. The parameter is therefore added in a copy, `rtl/mlkem/mlkem_core2.sv` (module `mlkem_core2`; differences from `mlkem_core.sv`: the module name, the header comment, the parameter `SMP_C5` default 1, and `.CORE_R2(SMP_C5)` in the engine instance). At `SMP_C5 = 1` it is the same design as `mlkem_core`. Quartus revisions K1 use `mlkem_core2.sv`. S1b builds on this file (new ROM).
2. **Test scripts:** `tb/mlkem/run_core_tests.py` and `profile_core.py` take `CORE_TOP=mlkem_core2` and `CORE_SMP0=1`; `tb/smp/run_smp_tests.py` takes `KP_CORE_R2`. At the defaults they behave as before (V7 repeats the default regression).
3. **The default `mlkem_core.sv` stays unchanged**; the Phase 9 / 9M configurations are measured as before.
