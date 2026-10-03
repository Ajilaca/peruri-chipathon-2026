<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Phase 8b: streaming samplers (SampleNTT from the XOF stream, CBD from the PRF stream), output width W1 then W2 — test plan, acceptance gate and selection rule

Written 2026-10-03, **before any 8b RTL and before any 8b measurement** (CRG-4). Scope: `docs/ROADMAP.md` Phase 8b; ADR 0026 (Accepted: 8a-8d go ahead; each sub-step has its own plan and a rule or a "no rule" statement written before measuring);
ADR 0019 point 3 (samplers). Base: the Keccak sponge of 8a (`keccak_sponge_r2.sv`, C5) and of Phase 7 (`keccak_sponge.sv`, K0), both unedited. Labels: MEASURED, INFERENCE, ESTIMATE, NOT MEASURED, perhitungan tim.
The mathematics is locked (C1): FIPS 203 Algorithm 7 (SampleNTT) and Algorithm 8 (SamplePolyCBD_eta) with q = 3329, n = 256, eta = 2 (ETA1 = ETA2 = 2 for ML-KEM-768); only the way the bytes are consumed is new.
PENDING #29 (accept C5 or keep K0) is open: the wrapper takes either sponge through a parameter, so 8b does not wait for it.

## 0. Team decision on the order of work and the two widths
Chat 2026-10-03 (the person who typed did not give a name; no decider is named here): "8b melakukan keduanya saja jadi pertama kita test 1 siklus dan setelah itu 2 siklus setelah itu selesai baru kita mulai 8c".
- **Stage W1:** one coefficient per cycle at the output (`OUTW` = 1). Built, verified and measured first (own Quartus revisions); its evidence is taken at a recorded git commit **before any W2 code exists**.
- **Stage W2:** two coefficients per cycle (`OUTW` = 2): the same files with the packing logic added; verified and measured second; the selection rule of section 5 decides which width is the 8b sampler.
- 8b is finished when both stages are measured and the rule is applied; then STOP (ADR 0026), then 8c. W1 and W2 are not separate sub-steps and there is no STOP between them unless a stage fails.

## 1. What "streaming" means here (no store between the sponge and the coefficient)
- The sponge output words (64 bit, valid/ready, as today) go **directly** into a byte window of at most 11 bytes and from there into the sampler. The XOF/PRF output is never written to a memory: the figure to check is **M10K = 0 and DSP = 0**.
  (ADR 0019 point 3 calls the first samplers "non-streaming-optimised"; no buffered sampler is built here, so the rule of section 4 is a gate, and section 5 chooses between W1 and W2 only.)
- New files (the arithmetic kernel and all Keccak files are **not modified**):
  - `rtl/sample/sample_ntt_core.sv`: word stream in; coefficient beats out (`coef_data_o` is `OUTW` x 12 bit, `coef_valid_o`, `coef_ready_i`, `coef_last_o` on the beat that holds the 256th coefficient); `bytes_o` = stream bytes consumed (3 per triple, counting the triple that completes the
    polynomial even when its second candidate is not used: the definition of `tb/golden/sampler_model.py`); `done_o`. Per triple (b0, b1, b2): d1 = b0 + 256 (b1 mod 16), d2 = b1 div 16 + 16 b2; a candidate is accepted when `d < 3329` (comparison with the
    constant, no modulo, no division). A triple gives 0, 1 or 2 coefficients; the second is dropped once the polynomial is full.
    A beat always holds `OUTW` consecutive coefficients (indices OUTW x m ... OUTW x m + OUTW - 1), so every beat is full (256 is a multiple of both widths).
    W1: the triple is held until its accepted coefficients have been output (a triple costs max(1, accepted) cycles).
    W2: one triple is taken per cycle; the accepted coefficients and one carried coefficient (0 or 1 held over) form a pool of 0 to 3; a beat is emitted whenever the pool reaches 2, the remainder (at most 1) is carried.
  - `rtl/sample/cbd2_core.sv`: word stream in, beats out; byte k of the 128 bytes gives coefficients 2k (low nibble) and 2k + 1 (high nibble); x = bit0 + bit1, y = bit2 + bit3, f = x - y mod 3329 (the five values 3327, 3328, 0, 1, 2; no
    division, no data-dependent path). W1 outputs one coefficient per cycle (256 cycles), W2 one byte, i.e. two coefficients, per cycle (128 cycles). Exactly 16 words are taken (the 17th word of the 136-byte SHAKE256 block is never taken).
  - `rtl/sample/keccak_sampler.sv` (top of the Quartus revisions): `parameter CORE_R2` selects `keccak_sponge_r2` (1) or `keccak_sponge` (0), `parameter OUTW` selects 1 or 2; `kind_i` 0 = SampleNTT on SHAKE128 (`mode_i` 2), 1 = CBD2 on SHAKE256 (`mode_i` 3); the message words
    (rho || j || i = 34 bytes, or sigma || N = 33 bytes; any `len_i` is allowed) pass through to the sponge; when the polynomial is complete the wrapper issues `stop_i` to the sponge (which wipes its state) and raises `done_o`; `abort_i` does the same at any time.
- The byte window, the triple register, the carried coefficient and the sponge state are cleared on `done_o`, on `abort_i` and on reset (the window holds secret bytes in the CBD case). Reset: asynchronous, active low (as the sponge). One clock domain, `clk_i`.
- Floors, stated as known limits and not as results: W1 needs at least 256 cycles per polynomial; W2 at least 128 (CBD) and about one cycle per triple (SampleNTT, 157.8 triples on average).

## 2. Corner cases (written before the tests; every case is run for `OUTW` = 1 and for `OUTW` = 2)
SampleNTT (core level, with crafted streams, and top level with real XOF streams):
- candidate exactly q - 1 = 3328 accepted, exactly q = 3329 rejected (d1 and d2 separately), 4095 rejected; d = 0 accepted.
- a triple with both candidates rejected (0 coefficients), exactly one accepted (d1 only, d2 only), both accepted.
- the 256th coefficient is d1 of a triple (second candidate unused: `bytes_o` still counts the triple), and the 256th is d2 of a triple.
- W2 packing: carry present and a triple that adds 0, 1, 2; carry absent and a triple that adds 0, 1, 2 (all six pool sizes 0-3); a carry pending when the 256th coefficient arrives (pool of 3 at count 255 with the second candidate dropped); a long run with no accepted candidate while a carry is held.
- a stream where every triple is accepted twice (128 triples, `bytes_o` = 384) and a long run of rejected triples (more than 100 in a row) followed by accepted ones: no hang, no early `done_o`.
- the three alignments of a triple against the 8-byte words (8 mod 3 = 2): a triple wholly inside a word, straddling two words with 1 byte then 2 bytes, and with 2 then 1; every one of the 56 triples of a block (168 bytes = 21 words).
- polynomials that need exactly 3 and exactly 4 XOF blocks. One or two blocks can never be enough (2 blocks = 112 triples = 224 candidates < 256), so every polynomial crosses at least two block boundaries (T = 56 and 112 triples). In 3,000 golden XOF streams (fixed PRNG seed, checked 2026-10-03) 2,970 needed 3 blocks
  and 30 needed 4 (1 %), with 157.8 triples and 261.6 output cycles (W1 model) on average; rho values for the 4-block case are found by search with a fixed PRNG seed and listed in the evidence. A 5th block is reachable only with a crafted stream at core level.
- `coef_ready_i` low for runs of 1, 2, 7 and 40 cycles at random points, including exactly when a permutation is running and at the block boundary; the output is held (valid and data stable) while not ready; with W2 also while a carry is held.
- `abort_i` in the middle of a polynomial, during absorb, during a permutation; reset in the middle; `start_i` while busy is ignored; two polynomials back to back with the same and with different rho (the carry of one polynomial must not leak into the next).
CBD:
- every nibble value 0-15 in both nibble positions and in all 16 words (the table of 16 results is fixed by x - y); all-zero and all-ones streams; one hot bytes; 128 random bytes with a fixed PRNG seed.
- the 17th word is not taken (checked from the sponge's word counter); output held under back-pressure; abort; reset.
Both: stream words arriving with gaps (`in_valid`/`out_valid` low for 1-5 cycles at random points, core level), and the zeroisation of the window after `done_o`/`abort_i`/reset.

## 3. Tests (run for `OUTW` = 1 in stage W1 and again, with `OUTW` = 2 added, in stage W2)
| ID | Check | Tool | Required |
|---|---|---|---|
| V1 | Lint of the three new modules (CRG-1, CRG-2), both `OUTW` | Verilator `-Wall`, slang | 0 warnings, 0 errors |
| V2 | Golden model `tb/golden/sampler_model.py` equals the unmodified `primitives.sample_ntt` and `sample_poly_cbd`, including the consumed byte count (already written; rerun) | pytest | all equal |
| V3 | `sample_ntt_core` against the golden on crafted streams (every case of section 2) and on 500 XOF streams (fixed PRNG seed): 256 coefficients in order (beat m holds coefficients OUTW x m ...), `bytes_o` equal to the golden's consumed bytes, `coef_last_o` only on the last beat, `done_o` once | cocotb, both simulators (CRG-3) | all equal |
| V4 | `cbd2_core` against the golden on every nibble case and 500 PRF streams: 256 coefficients in order, 16 words taken | cocotb, both simulators | all equal |
| V5 | Top `keccak_sampler`, `CORE_R2` = 1 and 0: SampleNTT for rho || j || i with 3 x 3 index pairs and random rho (500 cases), CBD2 for sigma || N (500 cases); the output equals the golden fed with `hashlib.shake_128` / `shake_256` of the same message; back-pressure patterns of section 2; `bytes_o` equal; the sponge permutation counter equal to the number of blocks the golden says were needed | cocotb, both simulators | all equal |
| V6 | Constant cycles (CRG-7). **CBD:** cycles from `start_i` to `done_o` identical for all sigma and N at one `len_i` (at least 3 different sigma per N, 100 points); **SampleNTT:** the same input twice gives the same count; with r = cycles - (W1: sum over triples of max(1, accepted candidates); W2: number of triples consumed), both taken from the golden, r is reported per number of XOF blocks B (3 or 4; public data only). Expected, not required: one value of r per B and `CORE_R2` (a fixed block-boundary stall); if r varies with the stream, the variation is a function of the public rho and is reported as it is. Cycle counts are measured with `coef_ready_i` always high | cocotb | CBD identical at every point; SampleNTT repeatable; r table written to the evidence |
| V7 | Zeroisation: after `done_o`, `abort_i` and reset the byte window, the triple register and the carry read zero (test-only probe) | cocotb | zero in every case |
| V8 | Negative controls (test-only copies, so that the unit tests fail as they should): NC-LT `d <= q` (accepts 3329); NC-2ND the second candidate is accepted when the polynomial is full (or `bytes_o` not counting that triple); NC-ORD byte order of a word reversed; NC-CBD f = y - x; NC-17 CBD takes a 17th word; NC-STOP the wrapper never issues `stop_i`; W2 only: NC-CARRY the carried coefficient is dropped when a pool of 3 occurs, and NC-LEAK the carry is not cleared between polynomials | cocotb | the checks FAIL (each control has its own named check) |
| V9 | Formal (new files; SymbiYosys, yosys-slang): S1 `coef_data_o` < 3329 in every lane whenever valid; S2 at most 256 coefficients accepted per run and `coef_last_o` only on the last beat; S3 output stable while valid and not ready; S4 `bytes_o` never decreases and never exceeds the words taken x 8; S5 FSM legality and, after `done_o`, no valid output; S6 (W2) the carry holds at most one coefficient; free input stream (any bytes, any gaps); induction depth 30 as in Phase 7; controls NC-S1 (`<=`) and NC-S2 (257th coefficient) must FAIL | SymbiYosys | PASS; controls FAIL |
| V10 | Regression (CRG-5, CRG-6): `scripts/phase7_verify.sh`, `scripts/phase8a_verify.sh`, `formal/run_formal_phase7.py` and `formal/run_formal_phase8a.py` unchanged results; `check_params.py`; in stage W2 also the whole W1 test set rerun with `OUTW` = 1 (the W1 behaviour must be unchanged) | scripts | PASS |
| V11 | Quartus (kernel-only, virtual pins): `keccak_sampler`, `CORE_R2` = 1, at 40.000 ns, **seeds 1-6 per width, one at a time** (the revisions share one .qpf): W1 in stage W1, W2 in stage W2; information: `CORE_R2` = 0 seed 1 per width and the C5 top at 20.000 ns seed 1 per width | `quartus_sh`, `/quartus-report` | evidence extracted |

## 4. Acceptance gate (fixed before measuring; no tolerance; applied to each width separately)
A width of the streaming samplers on the C5 sponge passes the gate only if **all** hold:
1. V1-V10 PASS and every control fails as required, on both simulators.
2. SampleNTT and CBD outputs and `bytes_o` equal the golden at every test point; CBD cycles identical at every point; every logged SampleNTT run repeatable.
3. M10K = 0 and DSP = 0 at every seed (no buffer between sponge and sampler).
4. ALM <= 12,573 at every seed (the working cap of ADR 0009, assumed for the whole top and open to the team) and timing met at 40.000 ns at every seed 1-6.
5. The median over seeds 1-6 of the lowest slow-corner Fmax at 40 ns is **>= 44.320 MHz**, the median of S10, the NTT/INTT core (`docs/decisions/0025-*.md`, MEASURED in Phase 6): the sampler must not make the Keccak side slower than the NTT core. (The C5 sponge alone is 50.655 MHz, MEASURED in 8a.)
A width that fails the gate is recorded as measured and not accepted, with the failing items; there is no other sampler to fall back on, so whether to keep it anyway is the team's decision (C5).

## 5. Selection rule W1 versus W2 (fixed before any measurement; ADR 0012 style, no tolerance)
Let F be the median over seeds 1-6 of the lowest slow-corner Fmax at 40 ns of the C5 top, and c the mean cycles from `start_i` to `done_o` with `coef_ready_i` always high: for SampleNTT over the same 500 streams for both widths (the V5 set), for CBD over the V5 set (identical at every point).
- t = c / F for SampleNTT and for CBD, per width. **W2 is chosen over W1 only if:** W2 passes the gate of section 4, and t_W2 < t_W1 for SampleNTT **and** for CBD.
- Otherwise W1 stays the 8b sampler (if W1 passes the gate); if W1 fails the gate and W2 passes it, W2 is chosen; if both fail, 8b is recorded as not accepted and the team decides.
- The result is a **Proposed** ADR (as for 8a); the team accepts it (PENDING). ALM and registers are reported, not part of the choice beyond the cap of the gate.

## 6. ESTIMATE written before measuring (method and assumptions; not measurements)
- Sampler logic (without the sponge), W1: about 200-500 ALM and 150-350 registers (an 11-byte window, a triple register, two small cores, comparators against 3329); M10K 0; DSP 0. Top with C5: about 6,400-6,700 ALM (C5 median 6,167 ALM MEASURED, 8a).
  W2 adds the pool and the second accept path: about 100-300 ALM more than W1 and about 20-50 registers more. Low confidence: earlier Phase 7 estimates missed their ranges by a few percent.
- Fmax: the new paths are short (a 12-bit compare, a byte multiplexer; W2 adds a small adder for the pool count); the top should stay near the sponge, about 47-51 MHz (C5: 47.38-51.67 over seeds 1-6, MEASURED, 8a); W2 may be a little lower than W1.
- Cycles per polynomial with C5 and `coef_ready_i` high (perhitungan tim from the golden model's 157.8 triples and 261.6 W1 output cycles over 3,000 streams, plus the sponge: absorb of 34 bytes about 21 cycles, a 14-cycle stall at each of the 2 block boundaries every polynomial crosses, 3 in 1 % of cases):
  W1 SampleNTT about 310 (K0: about 350), W1 CBD about 280; W2 SampleNTT about 210 (about 22 + 158 + 28), W2 CBD about 150 (about 22 + 128). Per operation, sampling alone (perhitungan tim, not measured): KeyGen 9 SampleNTT + 6 CBD, Encaps 9 + 7, Decaps repeats the Encaps sampling:
  W1 about 4,500 / 4,800 cycles, W2 about 2,800 / 2,900 cycles. These exceed the 1,510-1,550 Keccak cycles of the 8a table, which counted word transfers only; the Phase 6 arithmetic is 5,493 (KeyGen) and 6,810 (Encrypt) cycles. Overlap (8d) is **not** claimed here.

## 7. Not covered
Hardware (no board); connection to the Phase 6 memory or sequencer (8c, 8d); the matrix A organisation (8c); widths above 2; `ETA` other than 2; seeds beyond 6; the full-operation cycle count (a sum of per-block figures, perhitungan tim until Phase 9 connects the blocks).
Formal covers control and range properties, not the digests (those are covered by simulation against hashlib).
