<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Phase 8d: overlap of the sampler with the arithmetic - test plan and adoption rule

Written 2026-10-03, **before any 8d RTL change and before any 8d measurement** (CRG-4). Scope: `docs/ROADMAP.md` Phase 8d; ADR 0026 (Accepted); chat 2026-10-03 (no name given): do 8b, 8c and 8d without stopping, then the report and the result.
Base: the 8c sequencer `rtl/sched/kpke_sched_smp.sv` (STREAM build, `evidence/phase08/8c/`), the Phase 6 files and the 8b sampler, all as they are. Labels: MEASURED, INFERENCE, ESTIMATE, NOT MEASURED, perhitungan tim. The mathematics is locked (C1): only the order and the time at which noise polynomials are sampled change.

## 1. What is built (one change: sampling of the noise polynomials runs while the transforms compute)
In 8c the sampler is idle while the NTT core transforms and while the INTT runs (about 635 cycles per transform in the Phase 6 operation) and the sequencer waits for every `SMPN`. In 8d a noise polynomial is sampled **non-blocking**: the sampler starts and the sequencer goes on with the next operation; the sampler's beats
are written into the store whenever the store write port is free; the sequencer always has priority on that port. The matrix entries stay streamed (`PWMS`, which needs the sampler and therefore waits until it is idle: the sampler is one shared unit, so the matrix and the noise are sampled one after the other, never at the same time).
- `rtl/sched/kpke_sched_smp.sv` (the file of 8c, extended; parameter `OVERLAP`, default 0, so the 8c build is unchanged): with `OVERLAP = 1` the operation `SMPN` with `first = 1` is non-blocking, `WAIT` waits until the sampler is idle, the store write of a sampler beat is allowed only when the sequencer does not write
  (`wr_free = !seq_wr && !idle`), and an `END` waits for a busy sampler. These are already in the 8c source as inactive paths (selected by the parameter); the 8c evidence was taken with `OVERLAP = 0`, and the paths are exercised and measured only here.
- Program set **OVERLAP** (`VAR` = 2), generated from `tb/golden/kpke_smp_model.py` (extended) by `scripts/build/gen_kpke_smp_roms.py`: the STREAM programs with the noise sampling moved. KeyGen: s0 blocking; then each next noise polynomial is started non-blocking right before the transform of the previous one, and a `WAIT` follows each transform
  (s1 during NTT s0, s2 during NTT s1, e0 during NTT s2, e1 during NTT e0, e2 during NTT e1; NTT e2 needs e2). Encrypt: y0 blocking; y1 and y2 during NTT y0 and y1; e1_0 during NTT y2; e1_1, e1_2 and e2 each started right before the INTT of the previous pass (the polynomial is first needed at the ADD after the next
  PWMS passes, which wait for the sampler anyway); a `WAIT` before every operation that reads a polynomial sampled non-blocking and not separated from its start by a `PWMS`. Decrypt has no sampling and is unchanged. Slot numbers as STREAM (12 slots).
- Program set **STRESS** (`VAR` = 3, **test only**, never compiled in Quartus): Encrypt of STREAM with e1_2 (slot 14) started non-blocking right before the first `ADD` (a pass that writes the store in 128 of its 130 cycles), so that sampler beats and sequencer writes are ready in the same cycles and the arbitration is exercised; KeyGen as OVERLAP. Same results by construction.
Not changed: the sampler, the NTT core, the store, the PWM unit, the Phase 6 files.

## 2. Golden model first
`tb/golden/tests/test_kpke_smp_model.py` is extended: the OVERLAP and STRESS programs run with the golden primitives give the same logical slots as STREAM and the same end results as the unmodified golden K-PKE; the operation counts are unchanged; every `WAIT` is checked statically against the data flow: no operation reads a slot that a non-blocking `SMPN` writes
unless a `WAIT` or a `PWMS` (which waits for the sampler) lies between them (a checker in the model, a hazard exists exactly when this fails).

## 3. Corner cases
- A sampler beat while the sequencer writes the store: during an `ADD` pass (STRESS), during the unload of a transform, during the final slot write of a `PWMS` pass; the beat is held (valid and data stable) and written afterwards; the pair index of the beat writer is the right one afterwards.
- A non-blocking sample that is still running when the sequencer reaches the next sampling operation or `PWMS` (waits), `WAIT` with an idle sampler (no delay beyond the fetch), `END` with a busy sampler.
- The same slot is never read before its sample is complete (hazard checker); the noise polynomial used by the transform that follows is correct for every ctr.
- Constant cycles: fixed rho, varied secrets give identical cycles (the sampling of the noise has a fixed length; the overlap does not make a secret-dependent difference); same input twice, same count.
- Reset in the middle of a program with a non-blocking sample running; start while busy ignored.

## 4. Tests
| ID | Check | Tool | Required |
|---|---|---|---|
| V1 | Lint of the sequencer for `OVERLAP` = 1 and the ROM (CRG-1, CRG-2) | Verilator `-Wall`, slang | 0 warnings, 0 errors |
| V2 | Golden model, hazard checker, ROM regenerated byte for byte | pytest, `scripts/build/gen_kpke_smp_roms.py --check` | all equal |
| V3 | Top with OVERLAP and STRESS: every slot read back equals the model, end results equal the golden K-PKE, counters as before (smp counts 6 / 7 / 0) | cocotb, both simulators | all equal |
| V4 | Overlap seen: in OVERLAP the cycles of KeyGen and Encrypt are lower than STREAM's by about the hidden sampling; in STRESS at least one sampler beat is held back by a sequencer write (probe `smp_cvalid && !smp_cready`) | cocotb | seen |
| V5 | Constant cycles as in section 3 (OVERLAP and STRESS) | cocotb | identical per fixed rho |
| V6 | Negative controls (test-only copies): NC-HAZ `WAIT` ignored (a transform reads a slot too early); NC-ARB no arbitration (`wr_free` always 1), run on STRESS where the beats and the sequencer writes collide | cocotb | the bit-exact checks FAIL |
| V7 | Formal: the 8c properties F1-F5 for `OVERLAP` = 1 (F4 now relies on the arbitration: no sequencer write and beat write in the same cycle) | SymbiYosys | PASS |
| V8 | Regression: the 8c tests for STORE and STREAM (the same file now has the OVERLAP paths) and the 8b and 8a scripts | scripts | PASS |
| V9 | Quartus: `kpke_smp_top_s10` OVERLAP (NPOLY 12, `OVERLAP` = 1), 40.000 ns, **seeds 1-6, one at a time**; information: seed 1 at 20.000 ns. The STREAM revisions of 8c are the baseline | `quartus_sh`, `/quartus-report` | evidence extracted |

## 5. Adoption rule (ADR 0012 style, fixed before measuring; no tolerance)
OVERLAP is adopted over STREAM only if **all** hold: 1. V1-V8 PASS on both simulators and the controls fail as required; 2. timing met at 40.000 ns at every seed for OVERLAP and the fit succeeds; 3. with F the median over seeds 1-6 of the lowest slow-corner Fmax at 40 ns and c the mean cycles over the same rho set:
**t = c / F is lower for OVERLAP than for STREAM for KeyGen and for Encrypt**; 4. M10K(OVERLAP) <= M10K(STREAM). If the rule fails, 8d is recorded as measured and not adopted and STREAM stays.

## 6. ESTIMATE written before measuring (not measurements)
- Cycles (perhitungan tim from the 8c STREAM figures of the same simulation, KeyGen about 7,090 and Encrypt about 8,550, and the sampling time of one noise polynomial, about 160 cycles with the sequencer overhead): KeyGen hides 5 of 6 noise polynomials, about 5 x 160 = about 800 cycles: about 6,300; Encrypt hides 6 of 7: about 960 cycles: about 7,600 (about 11 % fewer than STREAM).
  The first polynomial of each program cannot be hidden (nothing to overlap with).
- Resources: the OVERLAP paths are a few comparators and one more state; ALM, registers and M10K within a few dozen of STREAM; Fmax: the arbitration puts `seq_wr` (a function of the sequencer state) into the beat's ready path, a short path; expect Fmax within the seed spread of STREAM (INFERENCE, not measured).

## 7. Not covered
Hardware (no board); more than one sampler (the matrix cannot be sampled while the noise is); overlap of the matrix streaming with the transforms (needs a second sampler or a buffer); hashing of the keys and the whole KEM; seeds beyond 6.

## 8. Amendment A1 (2026-10-03, written after the first runs of the OVERLAP and STRESS programs; the adoption rule of section 5 is unchanged)
1. **Finding of the STRESS run (RTL changed):** when the sequencer starts the sampler in the same cycle in which the previous non-blocking sample reports its `done_o` pulse, the `done` branch cleared `smp_pwm_q` after the start branch had set it, so a following `PWMS` pass never received a beat and the program never finished (`done_o` never rose within 120,000 cycles).
   The OVERLAP programs never produce that coincidence (their transforms take hundreds of cycles); the STRESS Encrypt does (a `PWMS` right behind the non-blocking sample). The `done` branch now comes before the start branch, so a start wins. The 8c evidence is not affected functionally (the case needs a non-blocking sample), but the file changed, so the 8c Quartus revisions were recompiled from the final file.
2. **NC-HAZ realised differently:** ignoring `WAIT` does not break the OVERLAP programs (every sample is started long before its use: the overlapped transform takes 635 cycles and a noise sample about 160), so that control would pass. The control is a test-only copy of the ROM in which the first transform of the OVERLAP KeyGen reads the slot that the non-blocking sample has just started: the bit-exact check must fail.
   This also shows that the `WAIT` operations are a safety property of the schedule, not a measured need; the static hazard checker (V2) is what guards them.
3. **Formal control:** for OVERLAP = 1 the control is NC-F2 as in 8c (F4 holds by construction through `wr_free`; a violation of it is reachable only by the induction step, which SymbiYosys reports as UNKNOWN).
4. **ESTIMATE check:** the smoke runs gave OVERLAP KeyGen 6,326-6,351 and Encrypt 7,655-7,665 cycles (ESTIMATE about 6,300 and 7,600); in STRESS 545 sampler-beat cycles were held back by sequencer writes (the arbitration was exercised).
