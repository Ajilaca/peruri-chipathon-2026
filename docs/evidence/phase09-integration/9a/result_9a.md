<!-- claim-lint: skip-file (internal block report, not proposal text) -->
# Phase 9a block report: coefficient <-> byte codec (`mlkem_pack`, `mlkem_unpack`)

- Status: **DONE** (STOP after the block, ADR 0032). This is a block checkpoint, not the phase result: `docs/results/result_phase9.md` comes at the end of Phase 9 and its Approval box is the team's.
- Date (UTC): 2026-10-03. The work is in the working tree and not committed (chat 2026-10-03: commits are made when the work is finished).
- Plan and rule: `test_plan_9a.md` (written before the RTL; Amendment A1 records the findings below). Block plan: `../phase9_plan.md`. Simulation results are simulation only; nothing here is a board result.

## 1. Result
Two small streaming blocks, both exact against the unmodified golden `primitives` (`compress`, `decompress`, `byte_encode`, `byte_decode`): `rtl/mlkem/mlkem_pack.sv` (256 coefficients -> Compress_d -> ByteEncode_d, `32 d` bytes) and `rtl/mlkem/mlkem_unpack.sv` (`32 d` bytes -> ByteDecode_d -> Decompress_d, 256 coefficients), d in {1, 4, 10, 12}, plus the wrapper `rtl/mlkem/mlkem_codec_top.sv`. Compress and Decompress contain no division and no data-dependent control (constants proved on the whole input domain of 3,329 values).

## 2. Verification (MEASURED, simulation and formal; `verify_2026-10-03.md`, `formal_2026-10-03.md`)
| Test | Result |
|---|---|
| V1 lint: Verilator `-Wall` and slang on pack, unpack and the wrapper | 0 warnings, 0 errors |
| V2 golden codec model vs unmodified golden primitives (all x for compress, all y for decompress, all 4,096 12-bit values) | 7 passed |
| V3-V7 cocotb, Icarus and Verilator: random and special polynomials, 9 back-pressure / gap mode pairs, exhaustive compress (every x, d = 1, 4, 10), exhaustive decompress (every y) and every 12-bit value, round trip, start / dsel while busy ignored, reset mid-run, constant cycles | 13/13 on each simulator |
| V8 negative controls (NC-RND, NC-ORD, NC-MOD, NC-CNT) | each fails the test named for it, on both simulators (4/4 each) |
| V9 formal (SymbiYosys, yosys-slang): P1-P5 for the packer, U1-U6 for the unpacker | both PASS (basecase and induction); controls NC-P2 and NC-U6 FAIL; NC-P1 and NC-U1 give UNKNOWN in the proof (violation beyond depth 40) and FAIL in BMC at depth 300 |
| V11 cycles per polynomial, always-ready sink, no gaps (identical for every data value of one d) | pack 261 / 261 / 325 / 389 and unpack 259 / 259 / 323 / 387 for d = 1 / 4 / 10 / 12 |

## 3. Quartus (MEASURED, kernel-only, virtual pins, 25.1std Lite, `selection_worksheet_2026-10-03.md`, `quartus_CD*_20261003.md`)
- Seeds 1-6 at 40.000 ns: ALM 298-299 (median 299.0), registers 192-193, DSP 2, block memory 0 bits, **timing met at every seed** (worst setup 30.046 ns, worst hold 0.166 ns); Fmax lowest slow corner median 105.630 MHz (100.46-110.38).
- Information: CD-20 (20.000 ns, seed 1): timing met (worst setup 10.952 ns), Fmax 110.52 MHz.
- Warnings: Critical Warning 15725 (clock port fed by a virtual pin) in every compile, as in all earlier kernel-only compiles; nothing waived.

## 4. Findings and deviations (all in Amendment A1 of the test plan)
1. A void control (NC-CNT) caused by a driver that never offered more than the exact count: fixed in the driver before the final runs; the early runs are not evidence.
2. X values from unreset data registers read by the driver: handled in the driver (resolved value required whenever valid). RTL unchanged.
3. A formal draft contained a tautology placeholder in P4; replaced by the exact bit-balance equation before the first proof run. The first packer proof run failed its induction until the "DUT counters equal black-box counters" invariants were added; the final proofs take 17 s (packer) and 12 s (unpacker).
4. ESTIMATE misses: pack and unpack cycles for d = 1 and 4 (estimated about 36 / 132 and 256 / 128, measured 261 / 261 and 259 / 259): the small d are bound by the input of one coefficient per cycle. d = 10 and 12 matched (bound by the byte stream).
5. The expectation of two formal controls was changed from "FAIL" to "UNKNOWN in the proof, FAIL in BMC at depth 300" after the first run showed UNKNOWN, with the Phase 3 control NC-B as precedent; the properties were not weakened.

## 5. What this does not show
No board result. The codec has no memory interface yet (9c). Values outside [0, q-1] at the packer input are outside its domain and are not tested. Cycle invariance is shown in simulation, not on hardware. Nothing about side channels.

## 6. Cost for the budget of 9c
The tb port moves one coefficient per cycle (256 per polynomial); the packer needs 389 cycles per d = 12 polynomial. ESTIMATE (perhitungan tim) of the encoding time in a KeyGen: the 6 polynomials of t_hat and s_hat at d = 12 are about 6 x 389 = 2,334 cycles if not overlapped, against 6,344 cycles of the K-PKE KeyGen arithmetic (8d, MEASURED): that is a cost to decide in 9c (overlap with the arithmetic, a wider output) and not a result.

## 7. Decision for the team
None open from this block. The next block is 9b (hash and FO pieces); it starts when the team says so (ADR 0032).
