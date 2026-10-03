<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Phase 8c: matrix A generated on the fly (no storage of Â) — test plan and adoption rule

Written 2026-10-03, **before any 8c RTL and before any 8c measurement** (CRG-4). Scope: `docs/ROADMAP.md` Phase 8c; ADR 0026 (Accepted: 8a-8d go ahead, each with its own plan and rule). Chat 2026-10-03 (no name given): do 8b, 8c and 8d without stopping between them, then the report and the result.
Base (all unedited, frozen): the Phase 6 sequencer and store (`rtl/sched/kpke_sched.sv`, `poly_store.sv`, `pwm_unit.sv`, `gamma_rom.sv`), the S10 NTT/INTT core (`rtl/ntt/ntt_core_s10_p5.sv`, ADR 0025 Proposed), the 8b sampler (`rtl/sample/`, stage W2 if it is the one chosen by `docs/evidence/phase08-keccak-stream/8b/` section 5 rule, otherwise W1) on the C5 sponge (ADR 0027 Proposed; PENDING #29 open).
Labels: MEASURED, INFERENCE, ESTIMATE, NOT MEASURED, perhitungan tim. The mathematics is locked (C1): the only change is where the coefficients of Â come from.

## 1. What is built (one change: Â is not stored, its samples go straight into the pointwise unit)
Today (Phase 6) the 9 matrix polynomials Â[i][j] (slots 3i + j) are written by the testbench and read from the store by the PWM passes. In 8c the sampler produces them while the PWM pass runs.
New files (the Phase 6 files are **not modified**; the new sequencer is a separate module so the Phase 6 evidence stays valid):
- `tb/golden/kpke_smp_model.py`: golden programs with sampling, written first. Operations added to the Phase 6 list: `SMPN d ctr` (slot d <- SamplePolyCBD_2(PRF(seed, ctr)), FIPS 203 Algorithm 8 with eta = 2), `SMPA d m` (slot d <- SampleNTT(rho || j || i) with m = 3i + j, i.e. Â[i][j]; the baseline),
  `PWMS d m b F L` (as PWM, but operand a is the sampler stream of Â[i][j] instead of slot a). Â[i][j] = SampleNTT(rho || j || i) is the entry stored in slot 3i + j by the Phase 6 model (`_matrix`), so every program keeps the Phase 6 arithmetic exactly.
  Two program sets: **STORE** (the baseline: `SMPA` for the nine entries into slots 0-8, then the unchanged `PWM` ops; Phase 6 slot numbers, 24 slots) and **STREAM** (`PWMS`; the matrix slots do not exist, so the slots 9-20 are renumbered 0-11 and the store has 12 slots).
  Decrypt has no sampling and is the same in both sets (renumbered in STREAM).
- `scripts/gen_kpke_smp_roms.py` generates `rtl/sched/kpke_smp_prog_rom.sv` from the model (as the Phase 6 ROM is generated). Operation word: {opc[3:0], first, last, dst[4:0], a[4:0], b[4:0]}; opc 6 SMPN, 7 SMPA, 8 PWMS (opc 0-5 as in Phase 6).
- `rtl/sched/kpke_sched_smp.sv`: the sequencer of the Phase 6 `kpke_sched` plus the sampler: `parameter STREAM_A` (1 implements `PWMS`; 0 is the STORE build), `NPOLY`, `CORE_RDLAT`; the sampler `keccak_sampler` (C5) inside; a message feeder (the 34 bytes rho || j || i or the 33 bytes seed || N come from two 256-bit seed registers
  written through a seed port while idle, plus the index bytes from the operation); `SMPN`/`SMPA` are **blocking** (the sequencer waits for the sampler's `done_o`); the beats (two coefficients, one store pair) are written into slot d, pair by pair.
  `PWMS`: the sampler's beat feeds the PWM unit's a operand; the b operand (ŝ or ŷ), the accumulator word and gamma are addressed one cycle ahead by the beat counter (the address of the next beat, so data are aligned when a beat arrives);
  a valid/index/last shift register of the PWM latency (7 cycles) tags the results, which are accumulated or stored by index; a bubble (no beat) feeds nothing; `coef_ready_i` is always 1 in `PWMS`.
- `rtl/sched/kpke_smp_top_s10.sv`: Quartus top (sequencer + store + PWM + S10 core + sampler), parameters `VAR` (0 STORE, 1 STREAM; selects the ROM contents at compile time) and `NPOLY` (24 or 12).
Seeds (rho, sigma or r) are inputs written by the testbench (no hardware G/H/J here; ROADMAP "not allowed yet": full KEM control, hashing of keys).

## 2. Golden model first
`tb/golden/tests/test_kpke_smp_model.py`: the STORE and STREAM programs run on Python slots with the unmodified golden primitives (`sample_ntt`, `sample_poly_cbd`, `PRF`, `ntt`, `intt`, `multiply_ntts`), and the end results are compared with the **unmodified golden K-PKE**: KeyGen t̂ equals `byte_decode(12, ek_PKE)`;
Encrypt u and v (compressed, encoded) equal the ciphertext of `k_pke_encrypt`; for random seeds; the STREAM result equals the STORE result in the logical slots 9-20.

## 3. Corner cases (enumerated before the tests)
- Entries of Â: all nine (j, i) byte orders (the message is rho || j || i, j first), including i = j and the transposed use in Encrypt (slot 3j + i); a rho whose entry needs a 4th XOF block (the 4-block rho values of 8b).
- `PWMS` pipeline: a sampler stall (a rejected-triple bubble) in the middle of a pass, at the first beat, at the last beat, at a block boundary (the 14-cycle sponge stall); first/middle/last passes (accumulator not used on first, stored only on last); the b operand and gamma aligned to the beat after every bubble length.
- `SMPN`: counter values 0-6 (KeyGen 0-5, Encrypt 0-6); sigma and r all-zero and all-ones.
- Both seeds registers rewritten between programs; a program started while the seed port writes (writes while busy ignored).
- Constant cycles: fixed rho and varied sigma/r give identical cycle counts (the secrets only enter the CBD, which has a fixed count); the same inputs give the same count; with varied rho the count differs only through the public rejection pattern (reported, section 4 V6).
- Reset in the middle of a program; start while busy ignored; Phase 6 behaviour of the other operations unchanged.

## 4. Tests
| ID | Check | Tool | Required |
|---|---|---|---|
| V1 | Lint of the new sequencer, ROM and top, both `VAR` (CRG-1, CRG-2) | Verilator `-Wall`, slang | 0 warnings, 0 errors |
| V2 | Golden model equals the unmodified golden K-PKE; STREAM equals STORE in logical slots 9-20; ROM regenerated byte for byte (`scripts/gen_kpke_smp_roms.py --check`) | pytest | all equal, 0 differences |
| V3 | Top: KeyGen, Encrypt, Decrypt on random seeds and corner seeds, STORE and STREAM: every logical slot (that exists) read back equals the model, end results equal the golden K-PKE; counters (ntt, intt, pwm incl. pwms, smp) equal the model's counts | cocotb, both simulators (CRG-3) | all equal |
| V4 | `PWMS` stall coverage: per pass the number of bubbles and their positions are logged from the sampler's handshake; the cases of section 3 are all seen (test-only probe) | cocotb | every case seen, results equal |
| V5 | Constant cycles (CRG-7): fixed rho, 8 different seeds: identical cycle count per program; same input twice: same count; cycles per program per rho logged (STORE and STREAM) | cocotb | identical per fixed rho |
| V6 | Negative controls (test-only copies): NC-IJ message bytes i, j swapped; NC-CTR the CBD counter off by one; NC-ALIGN the PWMS b/acc/gamma address one beat late; NC-VALID the PWM result written for a bubble; NC-ACC the accumulator not used on a middle pass | cocotb | the bit-exact checks FAIL |
| V7 | Formal (new files, SymbiYosys; the sampler and the NTT core replaced by protocol stubs): F1 sequencer state legal and the program counter in range; F2 the sampler is started only when idle and a seed write never happens while busy; F3 `PWMS` accepts at most 128 beats per pass and the pipeline tag never exceeds them; F4 no store write of the sequencer and of the beat writer in the same cycle | SymbiYosys | PASS; control NC-F3 FAILS |
| V8 | Regression: Phase 6 files unmodified (`git diff --name-status` of `rtl/sched/kpke_sched.sv` etc. empty); `scripts/phase8b_verify.sh` and the Phase 6 verify rerun | scripts | PASS |
| V9 | Quartus (kernel-only, virtual pins): `kpke_smp_top_s10` STORE (NPOLY 24) and STREAM (NPOLY 12), 40.000 ns, **seeds 1-6 each, one at a time**; information: seed 1 at 20.000 ns | `quartus_sh`, `/quartus-report` | evidence extracted |

## 5. Adoption rule (ADR 0012 style, fixed before measuring; no tolerance)
STREAM is adopted over STORE only if **all** hold:
1. V1-V8 PASS on both simulators and every control fails as required (both variants correct).
2. The fit succeeds for both and timing is met at 40.000 ns at every seed for STREAM.
3. With F the median over seeds 1-6 of the lowest slow-corner Fmax at 40 ns and c the mean cycles over the same rho set (V5 set, C5 sponge): **t = c / F is lower for STREAM than for STORE for KeyGen and for Encrypt**.
4. M10K(STREAM) <= M10K(STORE) at every seed (the point of not storing Â is memory; the ALM figure is reported against the fitter's denominator; no ALM cap is set here because the team has set none for a whole system, C5).
If the rule fails, 8c is recorded as measured and not adopted; STORE stays the 8c reference and 8d is built on the variant the rule leaves.

## 6. ESTIMATE written before measuring (method and assumptions; not measurements)
- Cycles (perhitungan tim from Phase 6 with S10: KeyGen 5,475, Encrypt 6,789, Decrypt 3,109 MEASURED, and the 8b W2 sampler: about 210 cycles per matrix entry and about 152 per noise polynomial, plus about 10 cycles of sequencer overhead per sampling operation):
  STORE KeyGen about 5,475 + 9 x 220 + 6 x 162 = about 8,400, Encrypt about 6,789 + 1,980 + 7 x 162 = about 9,900; STREAM replaces each 136-cycle PWM pass by a sampler-bound pass of about 228 cycles: KeyGen about 7,300, Encrypt about 8,750 (about 15 % fewer cycles than STORE).
  Decrypt unchanged (3,109). These use the W2 figures; with W1 each sampling step is about 100 cycles longer.
- Memory: STORE 24 slots (73,728 bits of coefficients, 51 M10K in the Phase 6 top with S10 as MEASURED, of which 24 in the core) against STREAM 12 slots; the slot store is about half of the non-core M10K, so about 10-14 fewer M10K blocks (INFERENCE from the block structure, not measured).
- ALM/registers: sequencer + sampler on top of the Phase 6 top (5,553 ALM MEASURED) and the 8b sampler (5,279 ALM W1 median MEASURED): about 11,000-12,500 ALM for either variant; STREAM adds the valid/index shift register (about 9 bits x 7 stages) and the beat counter: a few dozen registers. Fmax: the 8b sampler (51.2 MHz W1) and the S10 core (44.3 MHz) are separate paths; the new connection paths (beat to PWM operand) are short; expect the system near the S10 core, about 40-44 MHz (low confidence).

## 7. Not covered
Hardware (no board); hashing of the keys (G, H, J) and the whole KEM; overlap of sampling with arithmetic (8d); compression and encoding; seeds beyond 6; a hardware seed expander for rho and sigma.
Formal covers control, not values (simulation against the golden covers values).

## 8. Amendment A1 (2026-10-03, written after the first runs of the RTL, the tests and the formal proof; the adoption rule of section 5 is unchanged)
1. **Formal control realised differently:** the plan's V7 named a control NC-F3 (PWMS beat limit). A violation of F3 needs 128 beats, i.e. more than 128 cycles, beyond the BMC base depth (12), and a violation that only the induction step can reach is reported by SymbiYosys as UNKNOWN, not FAIL. The control is therefore **NC-F2** (the seed registers are written while the sequencer is busy), which fails in the base case;
   F3 itself is proved (induction passes) with supporting invariants: in a PWMS pass the beat counter equals the beats the sampler stub has handed over; the drain counter is 0 until the last beat; the result tags younger than the drain counter minus one are empty; without OVERLAP the beat writer is armed only in the blocking sampling state.
2. **Finding of the first formal run (RTL changed):** the valid tags `tag_v` of the PWMS result pipeline had no reset, so after power-up they could hold junk for 7 cycles; a stray accumulator write was possible in principle (no program reaches PWMS within 7 cycles of reset, so no simulation could show it). `tag_v` now has an asynchronous reset; the index tags stay data registers.
3. **Lint-driven new file:** Verilator `-Wall` flags the Phase 6 `poly_store.sv` for NPOLY < 17 (the 12-bit word index is wider than the memory index). The Phase 6 file is frozen, so `rtl/sched/poly_store_smp.sv` is a copy with the index width taken from the depth (same behaviour). The 8b sampler cores named a local constant `Q`, which hid `ntt_pkg::Q` when compiled together with the Phase 6 files (VARHIDDEN); it is now `QC` (a rename only).
   The 8b W1 Quartus evidence was taken at commit 794db0d before the rename; the W1 test set was rerun after it (8b verification, V10).
4. **Inputs identical across variants:** the testbench draws its random inputs with the same seeds for every variant so that the mean cycles of two variants are over the same rho set, as section 5 requires.
5. The cycle figures of the first smoke runs (STORE KeyGen 8,268-8,276, Encrypt 9,716-9,738; STREAM KeyGen 7,076-7,092, Encrypt 8,546-8,559) are close to the ESTIMATE of section 6 (about 8,400 / 9,900 and 7,300 / 8,750); the final numbers are in the selection worksheet.
