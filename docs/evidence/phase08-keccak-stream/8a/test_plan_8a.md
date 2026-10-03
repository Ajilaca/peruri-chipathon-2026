<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Phase 8a: two Keccak rounds per cycle (configuration C5) — test plan and adoption rule

Written 2026-10-03, **before any 8a RTL and before any 8a measurement** (CRG-4). Scope: `docs/ROADMAP.md` Phase 8a; ADR 0026 (Accepted: 8a, 8b, 8c, 8d all go ahead; supersedes the skip in ADR 0019 point 2);
ADR 0012 (rules for timing work). Base: K0 (`rtl/keccak/keccak_f1600.sv`, `keccak_sponge.sv`, Phase 7, approved). Labels: MEASURED, INFERENCE, ESTIMATE, NOT MEASURED, perhitungan tim.
The mathematics is locked (C1): a permutation is still 24 rounds of theta, rho, pi, chi, iota; only the number of rounds computed in one clock cycle changes.

## 1. The change (one change: rounds per cycle 1 -> 2)
- new `rtl/keccak/keccak_f1600_r2.sv`: same ports as `keccak_f1600`; two `keccak_round` instances in series per cycle, round constants `RC[2k]` and `RC[2k+1]` for cycle counter k = 0..11
  (`{k, 1'b0}` and `{k, 1'b1}`); the state register takes the output of the second round; `busy_o` high for exactly **12** cycles; `done_o` one cycle after the last write, as in K0.
- new `rtl/keccak/keccak_sponge_r2.sv`: copy of `keccak_sponge.sv` with the permutation core replaced (same ports, same FSM, same names). A permutation is 1 run cycle + 12 busy + 1 done = **14** cycles in the sponge.
- `keccak_round.sv` and `keccak_pkg.sv` are reused unedited. K0 RTL files are **not modified**. The K0 test files `tb/keccak/test_keccak_f1600.py`, `test_keccak_sponge.py` and `run_keccak_tests.py` get environment parameters
  (rounds per cycle) whose defaults reproduce K0 exactly; because existing test files change, the K0 verification (`scripts/phase7_verify.sh`) is rerun as the regression and its result recorded.
- Cycle formula for the sponge with p = 14 instead of 26: `1 + (len div 8 + 1) + pad2 + p * (len div rate + 1) + out_words + p * ((out_words - 1) div rate_words)`.
- ESTIMATE written before measuring: ALM about 1.6-2.0 times the round logic of K0 (K0 total 3,572 ALM MEASURED; round logic is the bulk), so about 5,500-7,500 ALM; registers unchanged (1,653 expected, the state register is the same);
  M10K 0, DSP 0; Fmax lower than K0 (the path doubles: about two rounds of logic); permutation 14 cycles instead of 26 (a ratio of 0.538); Keccak cycles per ML-KEM operation about 2,000 - 12 x 44 = about 1,500
  (the 2,026 / 2,078 / 2,070 of `docs/evidence/phase07-keccak/keccak_cycles_2026-10-03.md` less 12 cycles per permutation). The figure of about 1,200 quoted in chat on 2026-10-03 omitted the 2 control cycles and the word
  transfers and is superseded by this one.

## 2. Corner cases (same as the Phase 7 plan, section 3, plus)
- All of Phase 7's permutation and sponge corner cases at the new latency (zero, all-ones, 1,600 single-bit states, 200 random states, chain of 10; every boundary length of the four modes; ML-KEM lengths; back-pressure; stop; reset).
- Every round constant exercised: an error in an odd-indexed constant would show only in the second half of a cycle, so the trace of the state after every **cycle** (rounds 2k+1) is compared and, in addition, the state after every
  even round is checked through a test-only probe of the intermediate value (`mid`, the output of the first round, exposed to the testbench).
- `stop_i` in the middle of a 12-cycle permutation; `run_i` and xor ignored while busy.

## 3. Tests
| ID | Check | Tool | Required |
|---|---|---|---|
| V1 | Lint of `keccak_f1600_r2`, `keccak_sponge_r2` (CRG-1, CRG-2) | Verilator `-Wall`, slang | 0 warnings, 0 errors |
| V2 | Golden (`tb/golden/keccak.py`, unchanged) equals hashlib | pytest (Phase 7 test file) | all equal (already PASS; rerun) |
| V4 | Permutation core: state after every cycle equals the golden trace at rounds 1, 3, ..., 23; first-round output equals the golden trace at rounds 0, 2, ..., 22; `busy_o` exactly 12 cycles for every state | cocotb, both simulators (CRG-3) | all equal, 12 in every run |
| V5 | Sponge: Phase 7 V5 at the new latency, against hashlib and the golden sponge; permutation counter equal to the golden count | cocotb, both simulators | all equal |
| V6 | Constant cycles (CRG-7): three messages per (mode, length, output words), identical counts; every point equal to the formula with p = 14 | cocotb | identical per point; formula matches every logged point |
| V7 | Negative controls (test-only copies): NC-RC2 one bit of an odd-indexed round constant wrong; NC-R2 11 cycles (22 rounds); NC-PAD2 SHA3 domain byte 0x1F | cocotb | bit-exact checks FAIL (NC-R2 also fails the 12-cycle check) |
| V8 | Formal: K1-K5 of Phase 7 with the counter 0..11 and busy exactly 12 cycles (new formal top, new files); controls NC-K1 (11 cycles) and NC-K4 | SymbiYosys | PASS; controls FAIL |
| V9 | Locked parameters (CRG-6); regression of K0: `scripts/phase7_verify.sh` and `python3 formal/run_formal_phase7.py` again after the test-file change | scripts | PASS |
| V10 | Quartus: baseline **K0 seeds 2-6** (K0 seed 1 exists) and **C5 seeds 1-6** at 40.000 ns, one at a time; plus `C5-20` seed 1 at 20.000 ns (information) | `quartus_sh`, `/quartus-report` | evidence extracted |

## 4. Adoption rule (ADR 0012 style, fixed before measuring; no tolerance)
C5 replaces K0 as the Keccak permutation core only if **all** hold:
1. V1-V9 PASS and the controls fail as required, on both simulators.
2. `busy_o` exactly 12 cycles for every state and the sponge cycle counts equal the formula with p = 14 at every logged point.
3. ALM <= 12,573 at every seed (working cap = the only ALM ceiling in the project, ADR 0009; it was written for the NTT core and is used here as an assumption the team may overrule) and timing met at 40.000 ns at every seed 1-6.
4. With F the median over seeds 1-6 of the lowest slow-corner Fmax at 40 ns: **t = 14 / F_C5 < 26 / F_K0** (F_K0 the median of K0 seeds 1-6, recomputed from the files), i.e. F_C5 > 0.5385 x F_K0.
Whether a result at 20 ns is met is reported, not part of the rule. If the rule fails, 8a is recorded as measured and not adopted (as S8 was); K0 stays the Keccak core for 8b-8d and Phase 9 unless the team decides otherwise.

## 5. Not covered
Hardware (no board); seeds beyond 6; the effect of 8a on a whole ML-KEM operation (the blocks are connected only in Phase 9; the per-operation figure is perhitungan tim from the formula, not a measurement);
8b, 8c and 8d (own plans, written before each).
