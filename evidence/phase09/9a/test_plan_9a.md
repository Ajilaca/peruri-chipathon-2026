<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Phase 9a: coefficient <-> byte codec (Compress / ByteEncode, ByteDecode / Decompress) - test plan and pass rule

Written 2026-10-03, **before any 9a RTL and before any 9a measurement**. Scope: `evidence/phase09/phase9_plan.md` block 9a; `docs/ROADMAP.md` Phase 9; FIPS 203 Algorithms 5 and 6, Section 4.2.1 (Compress, Decompress). Golden: `tb/golden/primitives.py` (`compress`, `decompress`, `byte_encode`, `byte_decode`, unmodified, checked against the official vectors in Phase 0). Labels: MEASURED, INFERENCE, ESTIMATE, NOT MEASURED, perhitungan tim. The mathematics is locked (C1): the RTL implements the same functions; only the arithmetic is written without division.

## 1. What is built
- `rtl/mlkem/mlkem_pack.sv`: input a stream of 256 coefficients (12 bit, value in [0, q-1]), output `32 * d` bytes: for d in {1, 4, 10} each coefficient is compressed with Compress_d, for d = 12 it is passed unchanged (ByteEncode_12); the bits are packed LSB first (ByteEncode_d). d is chosen per run by `dsel_i` (0: 1, 1: 4, 2: 10, 3: 12) and latched at `start_i`.
- `rtl/mlkem/mlkem_unpack.sv`: input `32 * d` bytes, output 256 coefficients: ByteDecode_d, then Decompress_d for d in {1, 4, 10}; for d = 12 the 12-bit value is reduced mod q (ByteDecode_12 of the standard: `m = q`; one subtraction of q when the value is >= q, never more because 4,095 < 2q).
- Used values: d = 1 (message), 4 (v), 10 (u), 12 (t_hat, s_hat). Other d are not built.
- Division-free arithmetic (the reason for the constants: no division on secret data, KyberSlash): `Compress_d(x) = (((x << d) + 1664) * M_d >> S_d) mod 2^d` with (M, S) = (315, 20) for d = 1 and 4, (161,271, 29) for d = 10; `Decompress_d(y) = (3329 * y + 2^(d-1)) >> d`. The constants were found by search and **checked on all 3,329 inputs against the golden `compress`** and on all `2^d` inputs for `decompress` (`tb/golden/tests/test_codec_model.py`); they are valid for x in [0, q-1], the only values a coefficient takes.
- Interfaces (valid / ready streams; `done_o` one pulse after the last output is accepted; `busy_o` high from `start_i` to `done_o`; `start_i` is accepted only when idle):
  - pack: `coef_valid_i`, `coef_ready_o`, `coef_data_i[11:0]` in; `byte_valid_o`, `byte_ready_i`, `byte_data_o[7:0]`, `byte_last_o` out. It accepts exactly 256 coefficients per run and puts out exactly `32 * d` bytes; `byte_last_o` is on the last.
  - unpack: `byte_valid_i`, `byte_ready_o`, `byte_data_i[7:0]` in; `coef_valid_o`, `coef_ready_i`, `coef_data_o[11:0]`, `coef_last_o` out. It accepts exactly `32 * d` bytes and puts out exactly 256 coefficients; `coef_last_o` is on the last.
- Control never looks at data: the counters, the bit buffer fill and the stalls depend on `d` and on the handshakes only (constant-time argument).
- Reset: asynchronous active low on the control state; datapath registers are not reset; the bit buffers are cleared at `start_i`.

## 2. Golden model first
`tb/golden/codec_model.py` (new, independent of the RTL): the division-free `compress_hw` and `decompress_hw`, `pack_poly(d, coeffs)` and `unpack_poly(d, data)` written with the hardware formulas and the bit-buffer order. `tb/golden/tests/test_codec_model.py`: `compress_hw` equals `primitives.compress` for every x in [0, q-1] and d in {1, 4, 10}; `decompress_hw` equals `primitives.decompress` for every y and d; `pack_poly` equals `byte_encode(d, compress(d, .))` and `unpack_poly` equals `decompress(d, byte_decode(d, .))` on random and special polynomials; for d = 12 `unpack_poly` equals `byte_decode(12, .)`, including every 12-bit value 0..4095.

## 3. Corner cases
- Every x in [0, q-1] through the RTL for d = 1, 4, 10 (the whole input domain, including x = 0, x = q-1 where Compress_10 gives 0 by wrap-around, and the rounding ties); every 12-bit input of unpack d = 12 (0..4095, values >= q reduced); every y in [0, 2^d - 1] of unpack for d = 1, 4, 10.
- Random polynomials; all-zero, all q-1, alternating 0 / q-1, ramp.
- Back pressure: `byte_ready_i` / `coef_ready_i` always high, random (p = 0.5), long low runs; input valid gaps (random, long); the output is held (valid and data stable) while not accepted.
- `start_i` while busy ignored; `dsel_i` changed while busy ignored (latched); reset in the middle of a run, then a clean run; two runs back to back with different d.
- Exact counts: 256 coefficients in / out and 32 d bytes out / in per run; `byte_last_o` / `coef_last_o` on the last only.
- Constant cycles: with always-ready sinks and no input gaps the cycle count of a run is identical for every data value of the same d (fixed random and special polynomials, 100 each).

## 4. Tests
| ID | Check | Tool | Required |
|---|---|---|---|
| V1 | Lint of the two modules (CRG-1, CRG-2) | Verilator `-Wall`, slang | 0 warnings, 0 errors |
| V2 | Golden model tests (section 2) | pytest | all pass |
| V3 | pack: random and special polynomials, all four d, all back-pressure modes, bytes equal `byte_encode(d, compress(d, .))` of the unmodified golden | cocotb, both simulators | all equal |
| V4 | unpack: the same, coefficients equal `decompress(d, byte_decode(d, .))`; d = 12 with every 12-bit value | cocotb, both simulators | all equal |
| V5 | Exhaustive: every x for compress (d = 1, 4, 10) and every input of decompress, through the RTL; round trip pack then unpack of whole polynomials equals the golden round trip | cocotb, both simulators | all equal |
| V6 | Handshake and counts: the output is held until accepted; exact counts; start-while-busy and dsel-while-busy ignored; reset mid-run | cocotb | all pass |
| V7 | Constant cycles (section 3) | cocotb | identical per d |
| V8 | Negative controls (test-only copies): NC-RND compress without the rounding term (1664 -> 0); NC-ORD bit order of the packer reversed; NC-MOD unpack d = 12 without the reduction; NC-CNT pack accepts a 257th coefficient | cocotb | the check named for each FAILS |
| V9 | Formal: counts and ranges of both modules with free handshakes and free data: at most 256 coefficients and `32 d` bytes per run, `*_last` exactly on the last, an unaccepted output is held, no output while idle, the bit-buffer fill stays in range | SymbiYosys (yosys-slang) | PASS |
| V10 | Quartus kernel-only (both modules in one wrapper `mlkem_codec_top`, virtual pins), 40.000 ns, **seeds 1-6, one at a time**; information: seed 1 at 20.000 ns | `quartus_sh`, `/quartus-report` | evidence extracted |
| V11 | Cycles per polynomial and d with always-ready sinks (a table for the controller's budget) | cocotb | table written |

## 5. Pass rule (fixed before measuring; no tolerance)
9a is PASS only if: 1. V1-V9 pass on both simulators and every control of V8 fails as required; 2. V10: the fit succeeds and timing is met at 40.000 ns at every seed; 3. the resource counts and Fmax (median of the lowest slow-corner Fmax over seeds 1-6) are reported as MEASURED. There is no adoption rule (nothing is chosen between alternatives); the numbers feed the budget of 9c. DSP usage is reported and not limited here (112 DSP blocks available per the datasheet; the 8d engine uses 26).

## 6. ESTIMATE written before measuring (not measurements)
- Throughput (perhitungan tim): the packer outputs one byte per cycle, so a polynomial takes about `32 d` cycles plus the latency of the compress pipeline (about 4): about 388 (d = 12), 324 (d = 10), 132 (d = 4), 36 (d = 1). The unpacker takes input one byte per cycle: about `32 d` cycles for d = 12, 10, 4 and about 256 for d = 1 (one coefficient per cycle is the limit).
- Resources: two small FSMs with a 24-bit bit buffer each, one multiplier of about 22 x 18 bits in the packer (it may map to DSP blocks or to ALMs: not predicted), a constant multiplication by 3329 (four shifted terms) in the unpacker: ALM in the low hundreds each (INFERENCE; no figure is claimed). Fmax: not predicted; the compress multiplier is pipelined into two stages for that reason.

## 7. Not covered
The memory interface and the controller (9c); hashing (9b); the input checks (ADR 0031); the board; side channels. The codec is checked for cycle invariance in simulation only.

## 8. Amendment A1 (2026-10-03, written after the first runs; the pass rule of section 5 is unchanged)
1. **Void control found and fixed (test driver, RTL unchanged):** the first version of the drivers offered exactly 256 coefficients (or `32 d` bytes) and nothing more, so NC-CNT (the packer accepts a 257th coefficient) passed all tests: the control was void. The drivers now keep offering data after the exact count; the exact-count checks (`accepted == 256`, `accepted == 32 d`) then fail for NC-CNT. The first runs of V8 are not used as evidence.
2. **Unreset data registers:** the first driver converted an unresolved (X) output value to an integer while the output was not valid; the drivers now read values that are not 0/1 as -1 and require resolved values whenever `*_valid_o` is 1. No RTL change.
3. **Lint:** the first lint of `mlkem_pack.sv` reported unused bits of the 40-bit product register; the register was narrowed to the 14 bits that are used (`q10_q`, `q4_q`). Same function; every test was run on the final file.
4. **Formal (V9):** (a) the induction step needs the supporting invariants "the DUT's own counters equal the black-box counters" (`cin_q == nin`, `bout_q == nout`, `bin_q == nbin`, `cout_q == ntake`); the first induction run of the packer failed on P1 without them; (b) a placeholder (`|| 1'b1`, a tautology) had been typed in P4 of the first draft of the formal top and was replaced by the exact bit-balance equation before the first proof run; no result was taken from the draft; (c) the controls NC-P1 and NC-U1 (a count violation that needs 257 coefficients or 33 bytes) cannot be reached inside the induction depth 40: the proof returns UNKNOWN (base case passes, the induction step fails), not PASS, which shows the property is not vacuous; as NC-B of `formal/run/run_formal_slang.py` they are completed by a BMC run at depth 300 that must FAIL. The runner's expected values were written accordingly (UNKNOWN for the proof, FAIL for the BMC run); the properties were not weakened.
5. **ESTIMATE check (section 6):** pack cycles MEASURED 261 (d = 1), 261 (d = 4), 325 (d = 10), 389 (d = 12) against the ESTIMATE of about 36, 132, 324, 388: the estimate was right for d = 10 and 12 (output bound, one byte per cycle) and **wrong for d = 1 and 4**, which are bounded by the input (one coefficient per cycle: 256 + 5). Unpack MEASURED 259, 259, 323, 387 against about 256 (d = 1), 128 (d = 4), 320, 384: wrong for d = 4 for the same reason (one coefficient per cycle). The resources were not estimated in numbers (section 6); MEASURED values are in the worksheet.
