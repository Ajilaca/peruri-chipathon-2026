<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Phase 9M item 1 (9M-1): codec byte path of two bytes per cycle — test plan and adoption rule

Written 2026-10-04 before any 9M-1 RTL and before any 9M-1 measurement. Scope: ADR 0034 (Accepted, Faza Dzil), item 1. Baseline: the Phase 9 core C7-core as merged (main 49bebf7). Labels: MEASURED, ESTIMATE, INFERENCE, perhitungan tim. The mathematics is locked (C1): the bytes and coefficients are exactly those of Phase 9; only how many move per cycle changes.

## 1. Why (from `../../profile.md`, MEASURED in simulation)
Loading or storing a polynomial costs 391-393 cycles at d = 12 and 326-329 at d = 10 because the codec moves one byte per cycle (384 and 320 bytes), while the engine port moves one coefficient per cycle (256). With two bytes per cycle, every d is limited by the engine port (256 coefficients per polynomial).

## 2. Design (new files; Phase 9 files keep their behaviour)
| New file | Role | Difference from the Phase 9 module |
|---|---|---|
| `rtl/mlkem/mlkem_unpack2.sv` | ByteDecode_d + Decompress_d | input beat of 16 bits (byte 2i in bits 7:0, byte 2i+1 in bits 15:8), 32-bit bit buffer, a beat is taken when at most 16 bits remain after this cycle's coefficient; 16 d beats per polynomial |
| `rtl/mlkem/mlkem_pack2.sv` | Compress_d + ByteEncode_d | output beat of 16 bits when at least 16 bits are buffered, 32-bit buffer; 16 d beats; `beat_last_o` on beat 16 d - 1 |
| `rtl/mlkem/mlkem_wordbytes2.sv` | 64-bit words to 16-bit beats | four beats per word, same read-ahead as Phase 9 |
| `rtl/mlkem/mlkem_bytedst2.sv` | 16-bit beats to 64-bit words | four beats per word |
| `rtl/mlkem/mlkem_ldpoly2.sv`, `mlkem_stpoly2.sv` | load / store task | the Phase 9 tasks on the modules above; same ports |
| `rtl/mlkem/mlkem_codec2_top.sv` | test top | packer and unpacker side by side (as `mlkem_codec_top.sv`) |
`rtl/mlkem/mlkem_core.sv` gets one parameter `CODEC_W2` (default 0). At 0 it instantiates exactly the Phase 9 `mlkem_ldpoly` / `mlkem_stpoly`; at 1 the new ones. No other line of the core changes; the micro-program (ROM) does not change. Compress / Decompress use the same constants as Phase 9 (proved on all 3,329 inputs in 9a). No control depends on a data value.

## 3. Estimates written before measuring (ESTIMATE, from the profile and the design)
| Quantity | Phase 9 (MEASURED) | 9M-1 ESTIMATE |
|---|---|---|
| LDP / STP d = 12 (cycles) | 391 / 393 | about 263 / 265 |
| LDP / STP d = 10 | 326-327 / 329 | about 263 / 265 |
| LDP / STP d = 1 or 4 | 263 / 265 | unchanged |
| KeyGen, Encaps, Decaps with the profile inputs | 9,095 / 10,735 / 16,667 | about 8,330 / 10,160 / 15,520 (-8 %, -5 %, -7 %) |
| ALM (core, median seeds 1-6) | 17,620.5 | +100 to +500 |
| Registers / RAM blocks / DSP | 8,210-8,365 / 54 / 28 | about +100 / 54 / 28 |
| Fmax lowest slow corner, median | 49.280 MHz | 47-51 MHz (the codec is not on the critical path: INFERENCE) |

## 4. Tests (both simulators, Verilator and Icarus; negative controls on copies, the repository RTL is never mutated)
| # | Test | Pass condition |
|---|---|---|
| V1 | lint Verilator `-Wall` and slang of the core with `CODEC_W2 = 1` and of the codec2 top | 0 warnings, 0 errors |
| V2 | codec2: the 9a pack and unpack tests on `mlkem_codec2_top` with two bytes per beat (exhaustive Compress / Decompress, all 12-bit values, special and random polynomials for d = 1, 4, 10, 12, valid / ready patterns always, random, runs, start while busy ignored, held output, constant cycles) | bit-exact against the unmodified golden `primitives`, both simulators |
| V3 | core with `CODEC_W2 = 1`: the whole Phase 9c `core` target (ACVP keyGen 25, encapsulation 25, decapsulation 10; random cross-check; chain; protocol; constant cycles) | 100 % equal, both simulators |
| V4 | profile with `CODEC_W2 = 1` (same inputs as `../../profile.md`) | recorded; KeyGen, Encaps, Decaps each fewer cycles than Phase 9 |
| V5 | negative controls: NC-W-ORD (the two bytes of a pack beat swapped) -> V2 pack must FAIL; NC-W-CNT (unpack takes a beat when 20 bits remain) -> V2 unpack must FAIL; NC-W-CORE (`mlkem_ldpoly2` writes the coefficient index + 1) -> V3 ACVP must FAIL | each fails as required |
| V6 | formal: pack2 and unpack2 properties as 9a (P1 counts with 16 d beats, P2 held beat, P3 idle, P4 bit balance with 16 bits per beat, P5 pipeline count; U-properties likewise), with controls; core formal of 9c with `CODEC_W2 = 1` is not needed (the load / store tasks are stubs there and keep their protocol) | proofs PASS, controls FAIL, covers reached |
| V7 | regression: the Phase 9 scripts (9a, 9b, 9c) at the default parameter; no Phase 6-8 file differs from main | PASS |
| V8 | Quartus: revision MW (core, `CODEC_W2 = 1`), seeds 1-6 at 40.000 ns, one at a time, kernel-only as MC | evidence extracts; timing met or the failure documented |

## 5. Parameters reported (for Faza Dzil, from the reports and logs)
ALM (median, min-max, % of the fitter's denominator), registers, RAM blocks, block memory bits, DSP, worst setup and hold slack, timing met per seed, Fmax lowest slow corner (median, min-max); cycles per operation (profile inputs and ACVP ranges), per micro-operation; latency t = cycles / median Fmax (perhitungan tim); ACVP counts per simulator; constant-cycle results; formal results; critical warnings.

## 6. Adoption rule (fixed before measuring; not changed afterwards)
9M-1 is **adopted** (as the configuration for the next 9M items) if all hold:
1. V1-V3, V5-V7 pass as stated (correctness first; any ACVP mismatch rejects it).
2. Timing met at 40.000 ns at every seed 1-6 (V8).
3. For each of KeyGen, Encaps and Decaps (profile inputs), t = cycles / median Fmax of MW is lower than t of Phase 9 (cycles of `../../profile.md` / 49.280 MHz).
4. ALM median of MW is at most 1,000 above 17,620.5 (well inside the device; a larger cost would mean the design is not what section 2 describes).
Otherwise it is **not adopted** and the core stays at `CODEC_W2 = 0`. The result is recorded as a Proposed ADR; the team accepts it.

## 7. Not in this item
The 20 ns seeds (item 2), the K0 hash (item 3) and the overlap with the engine (item 4) are separate items with their own plans. No board result; no speed claim against software; constant-time means cycle-count invariance only.

## 8. Amendment A1 (2026-10-04, written after the runs; nothing above is edited and the rule of section 6 is unchanged)
1. **Quartus syntax (my mistake, not a design change):** the first MW compiles stopped within seconds with Quartus error 10170 (the generate `if` in `mlkem_core.sv` was written without `generate` / `endgenerate`; Verilator, slang and both simulators accept it, Quartus 25.1 does not). Their output was never used. The two generate blocks were wrapped in `generate` ... `endgenerate` (no logic change), lint was repeated (0 warnings, 0 errors, both parameter values), and the core simulations of V3 and V5 and all seven Quartus revisions were rerun on the final file. The first Icarus run on the earlier file was stopped by its process id and restarted.
2. **Added after the plan:** `formal/phase09m-optimisation/9m1/mlkem_core_w2_safety.sby` proves the 9c controller properties (E1 and S1-S7) with the core at `CODEC_W2 = 1` (stubs `stubs_9m1.sv`); section 4 V6 said this was not needed. The 9c proofs at the default parameter were rerun (V7) because the core now has generate blocks and `mlkem_core_formal_top.sv` selects the task instances by a macro.
3. **Not done:** V6 mentioned covers for pack2 and unpack2; the 9a proofs of the one-byte modules have none either, so none were written. Reachability is shown by the simulations (every run ends with done_o and the right output).
4. **Estimates against measurement:** see `result_9m1.md` (the cycle estimate was close; the ALM estimate of +100 to +500 was too high, the measured median is +33.5).
