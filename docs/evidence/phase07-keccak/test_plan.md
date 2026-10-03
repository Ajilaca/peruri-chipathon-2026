<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Phase 7: Keccak-f[1600] + SHA3/SHAKE baseline (K0) — test plan

Written 2026-10-03, **before the Phase 7 golden model, before any Phase 7 RTL and before any Phase 7 measurement** (CRG-4). Scope: `docs/ROADMAP.md` Phase 7; ADR 0019 (minimal path, single compile
for a new block without an adoption rule); ADR 0025 (S10 is the NTT/INTT core; not touched in this phase). Labels: MEASURED, INFERENCE, ESTIMATE, NOT MEASURED, perhitungan tim.
Standards: FIPS 202 (Keccak-p, sponge, SHA3-256, SHA3-512, SHAKE128, SHAKE256) as used by FIPS 203 (H, J, G, PRF, XOF). The mathematics is locked (C1): nothing here changes a hash function.

## 1. What is built
| Block (new files) | Function |
|---|---|
| `tb/golden/keccak.py` | Golden Keccak independent of the RTL: state as 25 lanes of 64 bit (index x + 5y), the five step maps θ, ρ, π, χ, ι per FIPS 202, round constants computed by the rc(t) LFSR (FIPS 202 Alg. 5) and ρ offsets by Alg. 2 (not typed in), `keccak_round`, `keccak_f1600`, a per-round trace, `sponge(rate, ds, msg, outlen)` with pad10*1, and the four functions |
| `scripts/gen_keccak_consts.py` | Generates `rtl/keccak/keccak_consts_pkg.sv` (24 round constants, 25 ρ offsets) from the golden model; `--check` regenerates byte for byte |
| `rtl/keccak/keccak_round.sv` | One combinational round θ → ρ → π → χ → ι on 1600 bits, round constant as input |
| `rtl/keccak/keccak_f1600.sv` | State register (1600 FF), round counter 0..23, **one round per cycle, exactly 24 cycles per permutation** (no early exit, no data-dependent condition); a lane-XOR port (absorb), a lane-read port (squeeze), a clear |
| `rtl/keccak/keccak_sponge.sv` | Sponge controller and Quartus top of K0: modes, absorb in 64-bit words, padding in hardware, squeeze in 64-bit words |

Interface of `keccak_sponge` (fixed here so tests and RTL are written against one contract):
- `start_i` with `mode_i[1:0]` (0 SHA3-256, 1 SHA3-512, 2 SHAKE128, 3 SHAKE256) and `len_i[15:0]` (message length in bytes, public). Accepted in IDLE; clears the state.
- Input: `in_valid_i`, `in_ready_o`, `in_data_i[63:0]`. Exactly ceil(len / 8) words are taken; byte k of a word (bits 8k+7..8k) is message byte 8w + k (FIPS 202 lane byte order). Bytes past `len` in the last word are ignored.
- Output: `out_valid_o`, `out_ready_i`, `out_data_o[63:0]` (same byte order), `out_last_o` on the last digest word of SHA3-256 (4 words) and SHA3-512 (8 words), then IDLE. SHAKE squeezes without end
  (a new block every rate words) until `stop_i`.
- `stop_i`: back to IDLE from any state on the next cycle (ends a SHAKE stream). `busy_o`, and a permutation counter `perm_cnt_o` (test and evidence only).
- Rates (bytes / 64-bit words): SHA3-256 136 / 17, SHA3-512 72 / 9, SHAKE128 168 / 21, SHAKE256 136 / 17. Domain bytes: 0x06 (SHA3), 0x1F (SHAKE); final bit 0x80 at byte rate − 1.
- Padding: after the last message word the domain byte is XORed at byte `len mod rate` of the final block and 0x80 at byte rate − 1 (one byte 0x86 when `len mod rate = rate − 1`). When `len` is a multiple of the
  rate (including 0) the final block holds only padding. Absorb permutations = floor(len / rate) + 1 for every length.

## 2. Golden model first (V2)
`tb/golden/tests/test_keccak.py` (pytest) compares `tb/golden/keccak.py` with Python `hashlib` (sha3_256, sha3_512, shake_128, shake_256):
every length 0 .. 3·rate + 1 per mode, the ML-KEM-768 input lengths 32, 33, 34, 64, 1120, 1184, 50 random lengths up to 2,000 bytes; SHAKE output lengths 0 .. 3·rate + 1, 128 (PRF, η = 2), 504 and 840
(SampleNTT streams); all-0x00 and all-0xFF messages. The per-round trace composed over 24 rounds must equal `keccak_f1600`. Only then is RTL written.

## 3. Corner cases (enumerated before the tests)
- Permutation: all-zero state; all-ones state; each single-bit state (1,600 states); 200 random states; a chain (output fed back as input, 10 times). Every round compared, not only the final state.
- Round constants: all 24 rounds reached in every permutation (ι is the only round-dependent step: an error in one constant shows only in that round's trace).
- Message lengths per mode: 0, 1, 7, 8, 9 (word boundary), rate − 1, rate, rate + 1, 2·rate − 1, 2·rate, 2·rate + 1, 3·rate; ML-KEM lengths 32, 33, 34, 64, 1120, 1184; random lengths up to 1,200.
- Last word: 0 (no words), 1..7 valid bytes, 8 valid bytes; garbage in the ignored bytes of the last word (must not change the digest).
- Squeeze: SHA3 digests (4 and 8 words); SHAKE128 one block exactly (21 words), 22 words, 63 and 105 words (3 and 5 blocks); SHAKE256 16 words (PRF η = 2 output, 128 bytes), 4 words (J).
- Back-to-back messages of different modes without reset; `stop_i` in the middle of absorb, during a permutation and during a SHAKE squeeze, then a new message (must be exact: the state is cleared at start).
- Back-pressure: random gaps in `in_valid_i` and `out_ready_i` (digest bit-exact; cycle counts are not compared in these runs).
- Reset in the middle of a message; `start_i` while busy is ignored.

## 4. Tests
| ID | Check | Tool | Required |
|---|---|---|---|
| V1 | Lint of every new module (CRG-1, CRG-2) | Verilator `-Wall`, slang | 0 warnings, 0 errors |
| V2 | Golden Keccak equals `hashlib` (section 2) | pytest `tb/golden/tests/test_keccak.py` | all equal |
| V3 | Constants package generated from the golden model, regenerated byte for byte | `scripts/gen_keccak_consts.py --check` | 0 differences |
| V4 | `keccak_f1600`: permutation corner cases of section 3, state after **every round** equal to the golden trace; done exactly 24 cycles after start for every state | cocotb `tb/keccak/test_keccak_f1600.py`, both simulators (CRG-3) | all equal; latency 24 in every run |
| V5 | `keccak_sponge`: all four modes, every length and squeeze case of section 3, against `hashlib` and the golden sponge; `perm_cnt_o` equal to the golden number of permutations | cocotb `tb/keccak/test_keccak_sponge.py`, both simulators | all equal |
| V6 | Constant cycles (CRG-7): for each mode, length and output length, three messages (random, all-0x00, all-0xFF) with no back-pressure give identical cycle counts; cycles recorded as a table and as a formula in `len` and output words | cocotb (same test, cycle log `cycles_k0.json`) | identical per (mode, len, out); formula matches every logged point |
| V7 | Negative controls (test-only copies): NC-RC one bit of one round constant wrong; NC-PAD SHA3 domain byte 0x1F instead of 0x06; NC-R 23 rounds | cocotb | bit-exact checks FAIL (NC-R also fails the latency check) |
| V8 | Formal (CRG-8) on the sponge with the permutation: K1 round counter in 0..23 and a permutation lasts exactly 24 cycles; K2 no input word accepted and no state XOR during a permutation; K3 absorb and squeeze lane index < rate words of the mode; K4 `out_valid_o` stays high with stable data until `out_ready_i`; K5 legal FSM state, `stop_i` reaches IDLE in one cycle. Controls: NC-K1 (23 rounds) and NC-K4 (valid dropped without ready) must FAIL | SymbiYosys | PASS; controls FAIL |
| V9 | Locked parameters (CRG-6) and regression (CRG-5) | `check_params.py`; Phase 0-6 scripts only if an existing RTL or test file is modified (Phase 5M Amendment A1); `git diff --name-status` as evidence | PASS / not required |
| V10 | Quartus (CRG-9): revision `K0` (top `keccak_sponge`, kernel-only, virtual pins), 40.000 ns, seed 1 (ADR 0019); information revision `K0-20` at 20.000 ns, seed 1. One revision at a time | `quartus_sh`, `/quartus-report` | evidence extracted; timing met or the failure documented |

## 5. Parameters recorded
| Parameter | Source | Label |
|---|---|---|
| ALM, registers, M10K, DSP (fitter denominators quoted) | `K0` fit summary | MEASURED |
| Fmax lowest slow corner, worst setup and hold slack (all corners), critical warnings triaged | `K0`, `K0-20` timing reports | MEASURED |
| Cycles per permutation (must be 24) | V4 | MEASURED (simulation) |
| Cycles per message per mode as a function of `len` and output words | V6 | MEASURED (simulation) |
| Throughput (absorbed bytes per cycle per mode, at long lengths) and time per permutation at Fmax | computed from the two lines above | perhitungan tim |
| Permutations per ML-KEM-768 KeyGen / Encaps / Decaps | golden model instrumentation (43-44 / 44-45 / 44-45 on three random seeds; SHAKE128 count depends on ρ, public) | perhitungan tim |

## 6. PASS criteria (ROADMAP Phase 7) and expectation
- PASS: V1-V9 as required; all modes bit-exact; fixed permutation latency of 24 cycles shown; Quartus evidence recorded; K0 row of ROADMAP filled. **No adoption rule**: K0 is a new block (a baseline), it
  replaces nothing.
- ESTIMATE (written before measuring; FSM assumed: one clear cycle, one word per cycle, one padding cycle, 24 cycles per permutation, one word per cycle out, no overlap of I/O with the permutation):
  cycles(len, out_words) ≈ 1 + ceil(len / 8) + 1 + 24·(floor(len / rate) + 1) + out_words + 24·(ceil(out_words / rate_words) − 1). Example SHA3-256 of 1,184 bytes (H(ek)): 1 + 148 + 1 + 24·9 + 4 = 370 cycles.
  The RTL may differ by a few transition cycles; the measured formula replaces this one (recorded, not tuned to match). Per ML-KEM-768 operation about 44 permutations × 24 ≈ 1,060 cycles of permutation
  plus word I/O (perhitungan tim), against KeyGen arithmetic 5,475 cycles with S10 (MEASURED, simulation).
- ESTIMATE resources: registers about 1,700-2,000 (1,600 state + control); ALM about 1,500-3,500 (method: θ column parities 320 bits, θ output 1,600 bits, χ 1,600 bits as 3-input functions, plus a 25-way 64-bit
  read select and the sponge control; ALM packing by the fitter unknown); DSP 0; M10K 0 expected (the round-constant table could be inferred as a ROM block: reported, not assumed).
- Fmax: INFERENCE, a round is a few LUT levels plus the input XOR and read select; expected not to be the system limit. Not a rule; 20 ns is information only.

## 7. Not allowed in this phase / not covered
- Not allowed (ROADMAP): two rounds per cycle or unrolling; streaming samplers; connection to the Phase 6 arithmetic unit; overlap of I/O with the permutation.
- Not covered: hardware (no board); seeds beyond 1; samplers, compression, encoding and FO (later phases). Constant-time here means cycle counts depend only on public lengths; it is not a side-channel claim.

## Amendment A1 (2026-10-03, after the RTL and the first verification run; no threshold, rule or required result changed)
Differences between this plan and what was built, recorded as found:
- File name: the generated constants package is `rtl/keccak/keccak_pkg.sv` (functions `keccak_rc`, `keccak_rho`), not `keccak_consts_pkg.sv`; `scripts/gen_keccak_consts.py --check` is V3 as planned.
- Section 5 / 6 ESTIMATE of cycles: the plan assumed 24 cycles per permutation. The controller needs 1 run cycle and 1 done cycle around the 24 busy cycles, so a permutation is 26 cycles there; the
  measured formula and the H(ek) value (389 instead of about 370) are in `keccak_cycles_2026-10-03.md`. The planned figure stays above as written; it is superseded, not edited. V4 still requires, and measures, exactly 24 busy cycles.
- The state is also wiped on `stop_i`, on the last SHA3 digest word and on reset (hygiene: the state holds secret-dependent intermediate values); the plan only required clearing at start.
- V8: NC-K4 runs as BMC to depth 40, not induction, because the squeeze phase is reached after about 30 cycles (the induction run on the mutant did not terminate in reasonable time). Properties and the required FAIL are unchanged.
- First-run test fixes, all in the testbenches (the RTL was right): the digest-end check lowered `out_ready_i` before the clock edge (the last word was never accepted); the stop test asked for 1 output word from SHA3 (digests are 4 or 8 words);
  the cycle log was deleted by the next build (file name now per test). The RTL had one change after the first verification: an enum ternary rewritten as if/else because Icarus rejected it. The whole verification and formal runs
  in `verify_2026-10-03.md` and `formal_2026-10-03.md` are of the final RTL.
- A wrong assertion of the golden test (24 distinct round constants) was corrected to the true value (22 distinct: rounds 5 and 22, and 6 and 20, share a value); all hashes equal hashlib.

