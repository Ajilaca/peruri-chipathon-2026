<!-- claim-lint: skip-file (internal block report, not proposal text) -->
# Phase 9M item 1 (9M-1) report: two bytes per cycle on the codec path (`CODEC_W2`)

- Status: **DONE** (STOP after the item, ADR 0034). The work is on the branch `phase9m-optimisation` and is not committed (chat 2026-10-04: the work is reported first). The adoption rule of the plan is met; the acceptance is the team's (ADR 0035, Proposed).
- Date (UTC): 2026-10-04. Plan and rule: `test_plan_9m1.md` (written before the RTL; Amendment A1 records what was found or added). Simulation, formal and static timing only; nothing here is a board result.

## 1. What was changed
New files in `rtl/mlkem/`: `mlkem_pack2.sv`, `mlkem_unpack2.sv`, `mlkem_wordbytes2.sv`, `mlkem_bytedst2.sv`, `mlkem_ldpoly2.sv`, `mlkem_stpoly2.sv`, `mlkem_codec2_top.sv` (two bytes per beat, 32-bit buffers, same Compress / Decompress arithmetic). `mlkem_core.sv` got the parameter `CODEC_W2` (default 0 = the Phase 9 tasks, unchanged behaviour); at 1 it uses the new tasks. The micro-program (ROM), the engine and all Phase 6-8 files are unchanged (0 files differ from main).

## 2. Parameters measured and results
| Parameter | Phase 9 (baseline) | 9M-1 (`CODEC_W2 = 1`) | Source |
|---|---|---|---|
| Load / store of one polynomial, d = 12 (cycles) | 391 / 393 | 263 / 265 | `profile_w2_verilator.json`, `../../profile_verilator.json` |
| Load / store, d = 10 | 326-327 / 329 | 262-263 / 265 | same |
| Load / store, d = 1 or 4 | 263 / 265 | 263 / 265 (unchanged, limited by the engine port) | same |
| Codec alone: pack / unpack cycles per polynomial, d = 1, 4, 10, 12 | 261 / 261 / 325 / 389 and 259 / 259 / 323 / 387 | 261 / 261 / 261 / 261 and 259 / 259 / 259 / 259 | `cycles_*_pack2.json`, `cycles_*_unpack2.json` |
| KeyGen, Encaps, Decaps cycles (profile inputs) | 9,095 / 10,735 / 16,667 | 8,327 / 10,159 / 15,515 (-8.4 %, -5.4 %, -6.9 %) | profiles |
| Cycles over the ACVP vectors: KeyGen (25 seeds) | 9,035-9,076 | 8,267-8,308 | `cycles_*_core_w2.json`, `9c/cycles_*_core.json` |
| Cycles over the ACVP vectors: Encaps (25 ek) / Decaps (10 dk) | 10,664-10,727 / 16,601-16,663 | 10,088-10,151 / 15,449-15,511 | same |
| Encaps / Decaps with a fixed ek (constant) | 10,691 / 16,623 | 10,115 / 15,471 | same |
| ALM, median (min-max), seeds 1-6 | 17,620.5 (17,608-17,636) | 17,654.0 (17,641-17,683), +33.5 | `selection_worksheet.md` |
| ALM in % of the fitter's 41,910 | 42 % | 42 % | same |
| Registers | 8,210-8,365 | 8,189-8,376 | same |
| RAM blocks / block memory bits / DSP | 54 / 120,350 / 28 | 54 / 120,350 / 28 | same |
| Timing at 40.000 ns | met at every seed (worst setup 19.010 ns, worst hold 0.075 ns) | met at every seed (worst setup 18.655 ns, worst hold 0.077 ns) | same |
| Fmax, lowest slow corner, median (min-max) | 49.280 MHz (47.64-51.74) | 48.855 MHz (46.85-52.15), -0.425 | same |
| Information at 20.000 ns (seed 1) | met, +4.419 ns, 64.18 MHz, 17,650 ALM | met, +4.355 ns, 63.92 MHz, 17,808 ALM | `quartus_MW-20.md`, `9c/quartus_MC-20.md` |
| Latency at median Fmax (perhitungan tim; kernel-only static timing, not a board measurement), KeyGen / Encaps / Decaps | 184.6 / 217.8 / 338.2 us | 170.4 / 207.9 / 317.6 us | worksheet |
| Critical warnings per compile | 1 (virtual pin clock, as in all earlier kernel-only compiles) | 1 | extracts |

## 3. Verification (all MEASURED)
| Test (plan section 4) | Result | Evidence |
|---|---|---|
| V1 lint (Verilator -Wall, slang), core at both parameter values, codec2 top | 0 warnings, 0 errors | run of 2026-10-04 (repeated after the `generate` fix) |
| V2 codec2: the 9a pack and unpack tests with two bytes per beat | pack 6/6 and unpack 7/7, bit-exact against the golden primitives, Verilator and Icarus | `cycles_*` files; logs of `tb/mlkem/run_codec2_tests.py` |
| V3 core with `CODEC_W2 = 1`: ACVP keyGen 25, encapsulation 25, decapsulation 10, random cross-check (20 cases), chain, protocol, constant cycles | 6/6 and 100 % equal, both simulators | `sim_verilator.md`, `sim_icarus.md` |
| V4 profile with `CODEC_W2 = 1` | section 2 | `profile_w2_verilator.json` |
| V5 negative controls NC-W-ORD, NC-W-CNT (codec2) and NC-W-CORE (core) | each fails the test named for it, both simulators | `sim_*.md` and the codec2 runner logs |
| V6 formal: pack2 and unpack2 (P1-P5, U1-U6) with controls; the 9c controller proof with `CODEC_W2 = 1` | all as expected (NC-P1 and NC-U1 UNKNOWN in the proof and FAIL in BMC at depth 300, as in 9a); controller proof PASS | `formal.md`; `mlkem_core_w2_safety.sby` (PASS by k-induction, run of 2026-10-04) |
| V7 regression at the default parameter | `phase9c_verify.sh` OVERALL PASS (ACVP 11/11 per simulator, 9a 17/17, 9b 23/23 with formal, frozen blocks 0 differing files); formal 9c ALL AS EXPECTED; the profile at the default equals the Phase 9 profile exactly | `regression_default.md` |
| V8 Quartus MW seeds 1-6 and MW-20 | section 2 | `quartus_MW*.md`, `selection_worksheet.md` |

## 4. Adoption rule (test plan section 6; fixed before measuring)
| Item | Result |
|---|---|
| 1 correctness (V1-V3, V5-V7) | met |
| 2 timing met at 40.000 ns at every seed | met |
| 3 t = cycles / median Fmax lower than Phase 9 for KeyGen, Encaps and Decaps | met (170.4 < 184.6, 207.9 < 217.8, 317.6 < 338.2 us) |
| 4 ALM median at most 1,000 above 17,620.5 | met (+33.5) |
**9M-1 is adopted by its rule.** The default of `CODEC_W2` stays 0 until the team accepts it (ADR 0035, Proposed).

## 5. Estimates against measurements (the estimates were written in the plan before measuring)
- Load / store cycles: estimated about 263 / 265 for d = 10 and 12; measured 263 / 265 (d = 10: 262-263): inside.
- KeyGen, Encaps, Decaps: estimated about 8,330 / 10,160 / 15,520; measured 8,327 / 10,159 / 15,515: inside.
- ALM: estimated +100 to +500; measured +33.5: **too high** (the two-byte modules are almost as small as the one-byte ones).
- Fmax: estimated 47-51 MHz; measured median 48.855: inside. The 0.425 MHz fall against Phase 9 is within the spread between seeds (46.85-52.15); that the codec is not on the critical path was an INFERENCE and the critical path was not examined here.

## 6. Findings and deviations (all in Amendment A1 of the plan)
1. The first Quartus compiles failed in seconds (Quartus 25.1 needs `generate` / `endgenerate` around the generate `if`); the output was not used; all seven revisions and the core simulations were rerun on the final file (my mistake, not a design problem).
2. A formal proof of the core with `CODEC_W2 = 1` was added after the plan; no cover runs for pack2 and unpack2 (the 9a modules have none either).
3. The Icarus runs of the whole core set take about an hour; the controls use a reduced vector set, as in 9c.

## 7. What this does not show
No board result and no comparison with software. The saving is limited to the polynomial loads and stores (about 6-8 % of the cycles); the engine (65-72 % of the cycles) is unchanged. Latencies in microseconds are kernel-only static timing divided into simulated cycles. Constant time means cycle-count invariance only; the cycles depend on the public ek or rho through the matrix sampling.

## 8. Decision for the team
ADR 0035 (Proposed): accept `CODEC_W2 = 1` as the configuration for the next Phase 9M items (item 2: 20 ns seeds; item 3: K0 hash; item 4: overlap with the engine). Nothing is decided here.
