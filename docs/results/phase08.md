<!-- claim-lint: skip-file (result artifact: internal status page, not proposal text) -->
# Result — Phase 8: Keccak optimisation and streaming (sub-steps 8a, 8b, 8c, 8d)

- Status: DONE (all four sub-steps built, verified and measured; the acceptance of ADR 0027-0030 and the Approval box are the team's)
- Status note: ADR 0026 (Accepted) sent 8a, 8b, 8c and 8d ahead. Chat 2026-10-03 (no name given) asked for 8b at two output widths and for 8b, 8c, 8d to be done one after the other, then this result and the report. **Every sub-step has its own test plan written before its measurement and an adoption rule; every rule was applied to files and none was changed after measuring** (the Amendments A1 of the plans record findings and one changed expected value, section 6).
- Date (UTC): 2026-10-03
- Git commit (HEAD when verified): see `git log main..phase8-keccak-stream` (8a 02d41bd, af62526, 12e1663; 8b plan dcae678, W1 794db0d, W2 fbca60f; 8c/8d plans f614b79, RTL 7a21af0, Quartus configuration d965b4d, evidence and ADRs after), plus the documentation commit of this file
- **Result:** 8a C5 two rounds per cycle (adopted by its rule, ADR 0027); 8b streaming samplers with no store between sponge and sampler: **W2** (two coefficients per cycle) chosen by the rule over W1 (ADR 0028): SampleNTT 206.48 cycles and CBD 152 (W1: 305.23 and 280), 5,290 ALM, 0 M10K, median Fmax 50.220 MHz; 8c matrix A streamed into the PWM unit and not stored: **STREAM** adopted over STORE (ADR 0029): KeyGen 7,089 against 8,268 cycles, 44 against 55 M10K;
  8d noise sampling overlapped with the transforms: **OVERLAP** adopted over STREAM (ADR 0030): KeyGen 6,344 and Encrypt 7,655 cycles (STREAM 7,089 and 8,549; the Phase 6 arithmetic alone 5,475 and 6,789), same ALM and M10K. All outputs are bit-exact against the golden model and the unmodified golden K-PKE on both simulators; formal proofs and negative controls as required; timing met at 40 ns at every seed of every configuration (kernel-only).
- Environment: Ubuntu 24.04.4 LTS, OSS CAD Suite 2026-09-23 (Verilator 5.053, Icarus 14.0 devel, slang, SymbiYosys with boolector), cocotb 2.1.0, Quartus Prime Lite 25.1std.0 Build 1129.
- Constraint: 40.000 ns (`C.sdc` of `quartus/phase08_keccak` and `phase08b_sampler`, `P.sdc` of `phase08c_smp`: identical to the Phase 5-7 constraint); information compiles at 20.000 ns.

## 1. Done-criteria (Common RTL Gate, docs/ROADMAP.md), Phase 8
| # | Criterion | Evidence | Status |
|---|---|---|---|
| CRG-1 | Lint clean | `evidence/phase08/8a/verify.md`, `evidence/phase08/8b/verify_W1.md`, `evidence/phase08/8b/verify_W2.md`, `evidence/phase08/8c/verify.md` (Verilator -Wall: 0 warnings for every module and variant) | PASS |
| CRG-2 | Elaboration clean (slang) | `evidence/phase08/8a/verify.md`, `evidence/phase08/8b/verify_W2.md`, `evidence/phase08/8c/verify.md` (slang: 0 errors, 0 warnings) | PASS |
| CRG-3 | Bit-exact vs golden, both simulators | 8a: every Keccak round and the sponge against hashlib; 8b: SampleNTT and CBD against `tb/golden/sampler_model.py` (equal to the unmodified golden primitives) including the XOF bytes consumed; 8c/8d: every slot and the end results against `tb/golden/kpke_smp_model.py` and the unmodified golden K-PKE (KeyGen, Encrypt, Decrypt) | PASS |
| CRG-4 | Corner cases before tests | `evidence/phase08/8a/test_plan_8a.md`, `evidence/phase08/8b/test_plan_8b.md`, `evidence/phase08/8c/test_plan_8c.md`, `evidence/phase08/8d/test_plan_8d.md` (written before the RTL and any measurement; the 8c and 8d plans were committed together with their amendments after the first runs, see section 6) | PASS |
| CRG-5 | Regression: earlier phases still pass | `evidence/phase08/8b/verify_W2.md` (reruns 8a, Phase 7 and the whole W1 set), `evidence/phase08/8c/verify.md` (the Phase 6 and core files are unmodified: 0 files differ from the Phase 7 base 6874609) | PASS |
| CRG-6 | Locked parameters | `.claude/skills/mlkem-guard/scripts/check_params.py` inside the K0 regression (all locked parameters match); nothing of FIPS 202 or FIPS 203 changed; the constants of the samplers are q = 3329 and the CBD eta = 2 of ML-KEM-768 | PASS |
| CRG-7 | Constant-cycle evidence | `evidence/phase08/8a/keccak_cycles.md` (306 points); `evidence/phase08/8b/sampler_cycles_W2.md`, `evidence/phase08/8c/cycles_v1.json`: 8b CBD cycles identical for every sigma and N (102 points), SampleNTT repeatable and, at W2, equal to the triples consumed + 49 (3 XOF blocks) or + 61 (4 blocks) at 500 polynomials; 8c/8d: fixed rho with 8 different secrets gives identical cycles per program in every variant | PASS |
| CRG-8 | Formal properties | `evidence/phase08/8a/formal.md`, `evidence/phase08/8b/formal_W2.md` (S1-S6 at both widths), `evidence/phase08/8c/formal.md`, `evidence/phase08/8d/formal.md` (F1-F5); every negative control fails as required | PASS |
| CRG-9 | Quartus evidence; no negative slack or the failure documented | `evidence/phase08/8a/selection_worksheet.md`, `evidence/phase08/8b/selection_worksheet.md`, `evidence/phase08/8c/selection_worksheet.md`, `evidence/phase08/8d/selection_worksheet.md`: seeds 1-6 at 40 ns for each configuration, timing met at every seed; the 20 ns compiles (information) are met for the 8a to 8d configurations measured at 20 ns | PASS |
| CRG-10 | Result artifact + claim checker | `cmd: python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase08.md` and `cmd: python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal` | PASS |

## 1b. Phase 8 sub-steps (docs/ROADMAP.md Phase 8)
| # | Sub-step | Evidence | Status |
|---|---|---|---|
| 8a | Two rounds per cycle (C5), measured, rule applied | `evidence/phase08/8a/selection_worksheet.md`, `docs/decisions/adr/ADR-0027-phase-8a-two-keccak-rounds-per-cycle-c5-rule-result.md` | PASS |
| 8b | Streaming samplers (CBD from the PRF stream, SampleNTT from the XOF stream; XOF bytes consumed exact), W1 then W2, rule applied | `evidence/phase08/8b/selection_worksheet.md`, `docs/decisions/adr/ADR-0028-phase-8b-streaming-samplers-output-width-w2-two-coefficients.md` | PASS |
| 8c | Matrix A generated on the fly (STREAM against STORE), rule applied | `evidence/phase08/8c/selection_worksheet.md`, `docs/decisions/adr/ADR-0029-phase-8c-matrix-a-streamed-from-the-sampler-into-the-pwm-uni.md` | PASS |
| 8d | Overlap of the sampler with the arithmetic (OVERLAP against STREAM), rule applied | `evidence/phase08/8d/selection_worksheet.md`, `docs/decisions/adr/ADR-0030-phase-8d-noise-sampling-overlapped-with-the-transforms-overl.md` | PASS |

## 2. What was produced
| Path | Purpose |
|---|---|
| `rtl/keccak/keccak_f1600_r2.sv`, `keccak_sponge_r2.sv` | 8a: two rounds per cycle (12 busy cycles); sponge copy on that core (14 cycles per permutation) |
| `rtl/sample/sample_ntt_core.sv`, `cbd2_core.sv`, `keccak_sampler.sv` | 8b: streaming SampleNTT and CBD (`OUTW` 1 or 2), wrapper with the C5 or K0 sponge (`CORE_R2`) |
| `rtl/sched/kpke_sched_smp.sv`, `kpke_smp_top_s10.sv`, `poly_store_smp.sv`, `kpke_smp_prog_rom.sv` (generated) | 8c/8d: the Phase 6 sequencer plus the sampler (`SMPN`, `SMPA`, `PWMS`, `WAIT`, non-blocking sampling, store-port arbitration); top with the S10 core |
| `tb/golden/sampler_model.py`, `tb/golden/kpke_smp_model.py` and their tests | golden models first (sampler with the consumed-byte count; programs with sampling and a hazard checker) |
| `tb/keccak/`, `tb/sample/`, `tb/smp/` | cocotb tests on both simulators with negative controls |
| `formal/phase08-keccak-stream/`, `formal/run/run_formal_phase8a.py` to `8d.py` | SymbiYosys proofs and controls (8c/8d with a sampler protocol stub) |
| `quartus/phase08_keccak/`, `phase08b_sampler/`, `phase08c_smp/` | Quartus revisions (kernel-only, virtual pins) |
| `scripts/test/phase8a_verify.sh`, `phase8b_verify.sh`, `phase8cd_verify.sh`, `select_8a.py`, `select_8b.py`, `select_8cd.py`, `gen_kpke_smp_roms.py`, `phase8b_cycles.py`, `build_phase8_report.py` | verification, rules from files, ROM generation, cycle summaries, the PDF report |
| `evidence/phase08/8a`, `8b`, `8c`, `8d` | test plans, verification and formal logs, cycle tables, Quartus extracts, worksheets |
| `docs/decisions/0026` to `0030` | Phase 8 scope (Accepted), results of 8a to 8d (Proposed) |
| `docs/reports/CHIPATON_Phase8_Report.pdf` | the report (Bahasa Indonesia) |

## 3. Numbers (MEASURED: Quartus reports and simulation; medians, t and sums per operation are INFERENCE / perhitungan tim)
### 3a. 8a, Keccak core (C5 against K0)
| Quantity | K0 (seeds 1-6) | C5 (seeds 1-6) | Estimate written before measuring (ESTIMATE) |
|---|---|---|---|
| ALM, median (min-max) | 3,566.5 (3,558-3,572) | 6,167.0 (6,152-6,169) | 5,500-7,500: inside |
| Registers | 1,653 | 1,652 | 1,653 expected: **1 fewer** (the cycle counter is 4 bits, not 5) |
| M10K / DSP | 0 / 0 | 0 / 0 | 0 / 0 |
| Timing at 40.000 ns | met at every seed | met at every seed | - |
| Fmax lowest slow corner at 40 ns, median (min-max) MHz | 67.675 (56.99-70.39) | 50.655 (47.38-51.67) | "lower than K0": yes (-25 %) |
| Cycles per permutation (sponge) | 26 | 14 | 14 |
| H(ek) 1184 B (cycles) | 389 | 281 | - |
| t per permutation at median Fmax (us) | 0.3842 | 0.2764 | ratio 0.538 of the cycles, rule: C5 must exceed 36.440 MHz: it does (50.655) |
| Keccak cycles per ML-KEM operation, median (KeyGen / Encaps / Decaps) | 2,026 / 2,078 / 2,070 | 1,510 / 1,550 / 1,542 | about 1,500: inside |
Information at 20.000 ns (seed 1): C5-20 6,178 ALM, setup +4.591 ns (met), 64.90 MHz; K0-20 3,573 ALM, +6.893 ns, 76.30 MHz. Fmax under a 20 ns constraint is not comparable with the 40 ns figures.
Sources: `evidence/phase08/8a/selection_worksheet.md`, `keccak_cycles.md`, `quartus_C5*.md`, `evidence/phase07/quartus_K0*.md`.


### 3b. 8b, streaming samplers (sampler + C5 sponge; sources: `8b/selection_worksheet.md`, `8b/sampler_cycles_W1.md`, `8b/sampler_cycles_W2.md`)
| Quantity | W1 (one coefficient per cycle) | W2 (two per cycle) | ESTIMATE written before measuring |
|---|---|---|---|
| ALM, median (min-max) | 5,279.0 (5,271-5,311) | 5,290.0 (5,282-5,308) | W1 6,400-6,700 (the top is **smaller** than the 8a sponge alone, 6,167: not investigated); W2 +100-300 over W1: measured +11 |
| Registers / M10K / DSP | 1,913 / 0 / 0 | 1,947 / 0 / 0 | 150-350 more than the sponge; 0 / 0 |
| Timing at 40.000 ns | met at every seed | met at every seed | - |
| Fmax lowest slow corner, median (min-max) MHz | 51.220 (50.10-55.79) | 50.220 (48.46-53.42) | about 47-51: W2 inside, W1 slightly above |
| SampleNTT cycles per polynomial (mean of 500, min-max) | 305.23 (298-323) | 206.48 (194-231) | about 310 / about 210: inside |
| CBD cycles per polynomial | 280 | 152 | about 280 / about 150: inside |
| Sampling cycles per operation, KeyGen / Encaps (perhitungan tim: 9 SampleNTT + 6 or 7 CBD) | 4,427 / 4,707 | 2,770 / 2,922 | about 4,500 / 4,800 and 2,800 / 2,900: inside |
| Gate (M10K 0, DSP 0, ALM at most 12,573, timing met, median Fmax at least the S10 median 44.320 MHz) | PASSED | PASSED | |
| Rule W1 against W2 (t = cycles / Fmax, SampleNTT and CBD) | t 5.959 / 5.467 us | t 4.111 / 3.027 us: **W2 chosen** | |
With the K0 sponge (information, seed 1): W1 3,470 ALM, W2 3,551 ALM, setup +23.9 and +23.5 ns at 40 ns; at 20 ns with the C5 sponge both met (+3.892 and +4.214 ns). The W2 SampleNTT cycles equal the triples consumed + 49 (3 XOF blocks) or + 61 (4 blocks) at every one of 500 polynomials; at W1 the same quantity varies (41-48 for 3 blocks).

### 3c. 8c and 8d, whole K-PKE programs with sampling (S10 core, W2 sampler, C5 sponge; sources: `8c/selection_worksheet.md`, `8d/selection_worksheet.md`, the cycle tables)
| Quantity | STORE (8c reference) | STREAM (8c) | OVERLAP (8d) | ESTIMATE written before measuring |
|---|---|---|---|---|
| ALM, median (min-max) | 10,958.0 (10,941-10,969) | 10,995.5 (10,958-11,032) | 10,992.5 (10,954-11,012) | about 11,000-12,500: inside |
| Registers | 3,342-3,378 | 3,377-3,395 | 3,368-3,414 | a few dozen more for STREAM: about +35 |
| M10K / DSP | 55 / 26 | 44 / 26 | 44 / 26 | STREAM about 10-14 fewer M10K: 11 fewer |
| Timing at 40.000 ns | met at every seed | met at every seed | met at every seed | - |
| Fmax lowest slow corner, median (min-max) MHz | 42.270 (41.21-44.28) | 43.355 (40.37-45.66) | 43.755 (42.14-46.38) | about 40-44: inside |
| KeyGen cycles (mean over the same inputs) | 8,268.1 | 7,089.1 | 6,344.1 | STORE about 8,400, STREAM about 7,300, OVERLAP about 6,300: inside |
| Encrypt cycles | 9,727.6 | 8,548.6 | 7,654.6 | about 9,900 / 8,750 / 7,600: inside |
| Decrypt cycles (no sampling) | 3,109 | 3,109 | 3,109 | Phase 6: 3,109 |
| t = cycles / median Fmax, KeyGen / Encrypt (us) | 195.6 / 230.1 | 163.5 / 197.2 | 145.0 / 174.9 | |
| Rule | reference | STREAM over STORE: **adopted** | OVERLAP over STREAM: **adopted** | |
Information at 20.000 ns (seed 1): STORE met (+0.992 ns, 52.61 MHz, 11,058 ALM), STREAM met (+1.783 ns, 54.89 MHz, 11,031 ALM), OVERLAP met (+1.535 ns, 54.16 MHz, 11,049 ALM); kernel-only static timing, not a system at 50 MHz.
For comparison, the Phase 6 top with the S10 core (arithmetic only, inputs given by the testbench): 5,553 ALM, 51 M10K, 5,475 / 6,789 / 3,109 cycles (MEASURED, Phase 6). The system of this phase adds the sampler (about 5,300 ALM) and the sampling cycles; hashing of the keys and the KEM control are not in it.
In STRESS (test only) 763 sampler-beat cycles were held back by sequencer writes: the arbitration of the store write port was exercised, the results stay bit-exact.

## 4. Standards and sources pinned
FIPS 202 as in Phase 7; FIPS 203 Algorithm 7 (SampleNTT) and Algorithm 8 (SamplePolyCBD) with eta = 2 (ML-KEM-768), with PRF = SHAKE256 and XOF = SHAKE128 as in the unmodified golden `tb/golden/primitives.py`. The permutation is still 24 rounds; no parameter or arithmetic of FIPS 203 changed (C1).

## 5. Coverage and limits
- **Simulation, formal and static timing only.** No board; Fmax is kernel-only with virtual pins. "Timing met at 20 ns" is this flow's static timing, not a system at 50 MHz. No claim on speed against software, power or side channels (C3).
- The cycles per operation are the arithmetic of Phase 6 plus the sampling inside one sequencer, MEASURED in simulation per program; hashing of the keys (G, H, J), compression, encoding, the FO transform and the KEM control are not in hardware yet (Phase 9); the seeds are written by the testbench.
- One sampler only: the matrix and the noise are sampled one after the other. The 8d overlap hides noise sampling behind the transforms; the matrix streaming (sampler-bound, about 206 cycles per entry) is not hidden.
- Formal covers control and range properties (the NTT core abstracted, the sampler replaced by a protocol stub in 8c/8d), not values; values are covered by simulation against the golden model and hashlib. `bytes_o` of the SampleNTT core is 16 bit and the proof assumes at most 8,000 stream words per polynomial.
- The seed registers are not wiped after a program (no side-channel claim; constant time here means the cycle count does not depend on a secret value).
- Quartus numbers: seeds 1-6 per configuration (kernel-only), a few compiles were run in parallel in copies of the project directory with identical sources and settings (named in the extracts).

## 6. Deviations, failures and open issues
- **Two RTL defects found by the verification and fixed:** (1) the valid tags of the PWMS result pipeline had no reset (found by the first formal run; invisible in simulation); (2) a sampler start in the same cycle as the previous sample's `done_o` pulse cleared the PWMS marker and hung the program (found only by the test-only STRESS program). Both proofs and all simulations were rerun on the final RTL; the 8c Quartus revisions were recompiled twice for RTL changes.
- **An expected value changed after seeing a result** (8b Amendment A1): the sponge permutation counter may be one above the golden count when the byte window has already taken the last word of the final block while the output was held back (1 of 500 K0 cases at W1, both simulators); the output is unaffected. The first test version also miscounted absorb permutations for messages of 168 bytes or more (a test error, corrected before any recorded run).
- **Formal controls:** NC-F3 and NC-F4 could not fail inside the BMC depth (their violations are reachable only by the induction step, which SymbiYosys reports as UNKNOWN); NC-F2 is the control used for 8c and 8d (Amendments A1). NC-HAZ of 8d is a ROM mutation, because ignoring `WAIT` does not break the schedule (the overlapped transform is longer than a noise sample).
- **ESTIMATE misses:** the ALM added by W2 (estimated 100-300, measured +11); the sampler + C5 top is smaller than the sponge alone (not investigated); the other estimates of the plans are inside their ranges (sections 3b, 3c).
- **Process:** the 8c and 8d plans were written before the RTL but committed together with their amendments (the plan commit f614b79 follows the golden-model work, not the RTL); one 8b W2 verification run was discarded because a command of the operator session killed its simulator processes, and the script was rerun from the start (`8b/verify_W2.md`); the 8b W1 Quartus evidence was taken at commit 794db0d, before the rename of a local constant (`Q` to `QC`) in the sampler cores, and the W1 test set was rerun afterwards.
- The K0 baseline of 8a, the notes of 8a and its Quartus numbers are in section 3a and in `evidence/phase08/8a/`.
- Critical Warning 15725 (virtual pin clock) in every compile, as in earlier phases; Warning 10036 (`unused_ok` sinks); nothing waived.

## 7. Decisions needed
- **ADR 0027** (C5 as the Keccak core, PENDING #29), **ADR 0028** (W2 as the 8b sampler, PENDING #30), **ADR 0029** (STREAM, PENDING #31), **ADR 0030** (OVERLAP, PENDING #32): all Proposed; the team accepts or rejects each. PENDING #25 (FIPS 203 input checks in hardware or on the HPS) and #26 (checkpoint protocol) are still open.
- Phase 9 (full ML-KEM-768 integration in simulation) is not started; the schedule risk to the tiers T2 and T3 before 2026-10-08 is stated in ADR 0026 and is the team's.

## 8. Claims made in this phase
None written for judges or proposal text. The ROADMAP rows C5, C6b-W1, C6b-W2, C6c-STORE, C6c and C6d were filled from the evidence above.

## 9. Reproduce
```bash
. scripts/env.sh
scripts/test/phase8a_verify.sh; KS_OUTW=2 scripts/test/phase8b_verify.sh; scripts/test/phase8cd_verify.sh
python3 formal/run/run_formal_phase8a.py; python3 formal/run/run_formal_phase8b.py all; python3 formal/run/run_formal_phase8c.py; python3 formal/run/run_formal_phase8d.py
cd quartus/phase07_keccak && ./run_k0_seeds.sh; cd ../phase08_keccak && ./run_c5.sh; cd ../phase08b_sampler && ./run_sm1.sh && ./run_sm2.sh; cd ../phase08c_smp && ./run_smp.sh; cd ../..
python3 scripts/quartus/select_8a.py; python3 scripts/quartus/select_8b.py; python3 scripts/quartus/select_8cd.py
python3 scripts/build/gen_kpke_smp_roms.py --check
python3 scripts/build/build_phase8_report.py
python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase08.md
python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal
```

## 10. Approval
- [x] Human approver (name, date): Jose (Team J5), 2026-10-03
      Next phase starts only after a team member ticks this box. Claude never ticks it.
