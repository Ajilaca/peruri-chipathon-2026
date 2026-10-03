<!-- claim-lint: skip-file (result artifact: internal status page, not proposal text) -->
# Result — Phase 8: Keccak optimisation and streaming (sub-steps 8a, 8b, 8c, 8d)

- Status: PARTIAL
- Status note: ADR 0026 (Accepted, Jose, 2026-10-03) sends all four sub-steps ahead. **8a is done and measured; 8b, 8c and 8d are not started.** This file grows one sub-step section at a time; each sub-step is reviewed separately (ROADMAP). The Approval box (Section 10) is for the whole phase and stays empty.
- Date (UTC): 2026-10-03 (8a)
- Git commit (HEAD when verified): 4926b1a (8a RTL, tests, formal, Quartus revisions and verification evidence), plus the documentation commit of this file
- **Result so far (8a):** two Keccak rounds per cycle (configuration C5): a permutation is 14 cycles in the sponge instead of 26, ALM 6,167 (median, seeds 1-6; K0 3,567), median Fmax 50.655 MHz at 40 ns (K0 67.675), timing met at every seed; **C5 is adopted by the pre-fixed rule** (ADR 0027 Proposed: the team accepts or rejects). Kernel-only, virtual pins, simulation and formal; nothing on a board.
- Environment: Ubuntu 24.04.4 LTS, OSS CAD Suite 2026-09-23 (Verilator 5.053, Icarus 14.0 devel), cocotb 2.1.0, Quartus Prime Lite 25.1std.0 Build 1129.
- Constraint: 40.000 ns (`quartus/phase08_keccak/C.sdc`, identical to the Phase 7 constraint); information compile at 20.000 ns (`C-20.sdc`).

## 1. Done-criteria (Common RTL Gate, docs/ROADMAP.md), for sub-step 8a
| # | Criterion | Evidence | Status |
|---|---|---|---|
| CRG-1 | Lint clean | `docs/evidence/phase08-keccak-stream/8a/verify_2026-10-03.md` (Verilator -Wall: 0 warnings on keccak_f1600_r2 and keccak_sponge_r2) | PASS |
| CRG-2 | Elaboration clean (slang) | `docs/evidence/phase08-keccak-stream/8a/verify_2026-10-03.md` (slang: 0 errors, 0 warnings) | PASS |
| CRG-3 | Bit-exact vs golden, both simulators | `docs/evidence/phase08-keccak-stream/8a/verify_2026-10-03.md` (every one of the 24 rounds compared; sponge against hashlib; Verilator and Icarus) | PASS |
| CRG-4 | Corner cases before tests | `docs/evidence/phase08-keccak-stream/8a/test_plan_8a.md` (written and committed before the RTL and any measurement) | PASS |
| CRG-5 | Regression: earlier phases still pass | The K0 test files were parameterised (defaults unchanged); the K0 verification was rerun and passes: `docs/evidence/phase08-keccak-stream/8a/verify_2026-10-03.md` (first block, OVERALL PASS). No RTL file of an earlier phase was modified: `cmd: git diff --name-status b1b5789 HEAD -- rtl` lists additions only | PASS |
| CRG-6 | Locked parameters | `docs/evidence/phase08-keccak-stream/8a/verify_2026-10-03.md` (`cmd: python3 .claude/skills/mlkem-guard/scripts/check_params.py` inside the K0 regression: all locked parameters match); nothing of FIPS 202 or FIPS 203 changed | PASS |
| CRG-7 | Constant-cycle evidence | `docs/evidence/phase08-keccak-stream/8a/keccak_cycles_2026-10-03.md`, `docs/evidence/phase08-keccak-stream/8a/cycles_c5_2026-10-03.json` (306 points, three messages each, one count per point, equal to the formula with p = 14) | PASS |
| CRG-8 | Formal properties | `docs/evidence/phase08-keccak-stream/8a/formal_2026-10-03.md` (K1-K5 PASS, busy exactly 12 cycles; NC-K1 and NC-K4 fail as required) | PASS |
| CRG-9 | Quartus evidence; no negative slack or the failure documented | `docs/evidence/phase08-keccak-stream/8a/selection_worksheet_2026-10-03.md` (seeds 1-6 at 40 ns, timing met at every seed), `docs/evidence/phase08-keccak-stream/8a/quartus_C5-20_20261003.md` (20 ns, met, information) | PASS |
| CRG-10 | Result artifact + claim checker | `cmd: python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/result_phase8.md` and `cmd: python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal` | PASS |

## 1b. Phase 8 sub-steps (docs/ROADMAP.md Phase 8)
| # | Sub-step | Evidence | Status |
|---|---|---|---|
| 8a | Two rounds per cycle (C5), measured, rule applied | `docs/evidence/phase08-keccak-stream/8a/selection_worksheet_2026-10-03.md`, `docs/decisions/0027-phase-8a-two-keccak-rounds-per-cycle-c5-rule-result.md` | PASS |
| 8b | Streaming samplers (CBD from the PRF stream, SampleNTT from the XOF stream; XOF bytes consumed exact) | not started | MISSING |
| 8c | Matrix A generated on the fly | not started | MISSING |
| 8d | Overlap of Keccak with arithmetic | not started | MISSING |

## 2. What was produced (8a)
| Path | Purpose |
|---|---|
| `rtl/keccak/keccak_f1600_r2.sv`, `keccak_sponge_r2.sv` | Two rounds per cycle (12 busy cycles); sponge copy on that core (14 cycles per permutation) |
| `tb/keccak/` (parameterised by `KK_RPC`, `KK_PERM`), `scripts/phase8a_verify.sh` | Tests and verification script (also reruns K0 as the regression) |
| `formal/phase08-keccak-stream/`, `formal/run_formal_phase8a.py` | Formal top (K1-K5, 12 cycles), sby file, runner with NC-K1 and NC-K4 |
| `quartus/phase08_keccak/`, `quartus/phase07_keccak/K0-s2..s6` | Revisions C5 seeds 1-6, C5-20; baseline K0 seeds 2-6 |
| `scripts/select_8a.py`, `scripts/phase7_op_cycles.py` (now with a cycles-per-permutation argument) | Adoption rule from files; Keccak cycles per ML-KEM operation |
| `docs/evidence/phase08-keccak-stream/8a/` | Test plan, verify, formal, cycles, selection worksheet, Quartus extracts |
| `docs/decisions/0026`, `0027` | Phase 8 scope (Accepted), 8a result (Proposed) |

## 3. Numbers, 8a (MEASURED: Quartus reports and simulation; medians and t are INFERENCE / perhitungan tim)
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
Sources: `docs/evidence/phase08-keccak-stream/8a/selection_worksheet_2026-10-03.md`, `keccak_cycles_2026-10-03.md`, `quartus_C5*_20261003.md`, `docs/evidence/phase07-keccak/quartus_K0*_20261003.md`.

## 4. Standards and sources pinned
FIPS 202 as in Phase 7; the permutation is still 24 rounds of theta, rho, pi, chi, iota, so every digest is unchanged and equals hashlib. No parameter or arithmetic of FIPS 203 changed (C1).

## 5. Coverage and limits
- **Simulation, formal and static timing only.** No board; Fmax is kernel-only with virtual pins. "Timing met at 20 ns" is this flow's static timing, not a system at 50 MHz.
- C5 and S10 have not been compiled together; whether the Keccak core limits a system is INFERENCE (the S10 median of 44.320 MHz is below C5's 50.655 MHz).
- 8b, 8c and 8d are not started. 8c needs the matrix entries to reach the pointwise unit from the sampler stream and 8d a scheduler interface between the Phase 6 sequencer and the sampler (ADR 0026): neither is designed yet.
- Formal covers control, not digests; digests are covered by simulation against hashlib.

## 6. Deviations, failures and open issues
- The K0 baseline needed seeds 2-6: the K0 figure of Phase 7 (56.99 MHz) was seed 1 and the lowest of six; recorded as amendment note 1 in `result_phase7.md` and in ADR 0027.
- The cycle estimate quoted in chat on 2026-10-03 for 8a (about 1,200 per operation) omitted the control cycles and the word transfers; the test plan fixed it at about 1,500 before measuring, and the measured formula gives 1,510-1,550.
- The NC-K4 runner text says "about 30 cycles to the squeeze phase" (copied from Phase 7); for C5 it is about 18; BMC depth 40 covers it; noted in `formal_2026-10-03.md`.
- Critical Warning 15725 (virtual pin clock) in every compile, as in earlier phases; Warning 10036 (`unused_ok` sink); nothing waived.

## 7. Decisions needed
- **ADR 0027** (C5 adopted by the rule): accept C5 as the Keccak core for 8b-8d and Phase 9 (PENDING #29), or keep K0.
- STOP after 8a (ADR 0026): confirm to go on with 8b (streaming samplers). PENDING #25 and #26 still open.
- Schedule (ADR 0026 states it): the remaining sub-steps and Phase 9 do not all fit before 2026-10-08 at 6-8 h per day (ESTIMATE); the team may stop or reorder at any STOP.

## 8. Claims made in this phase
None written for judges/proposal text. ROADMAP rows were filled from the evidence above.

## 9. Reproduce (8a)
```bash
. scripts/env.sh
scripts/phase8a_verify.sh; python3 formal/run_formal_phase8a.py
cd quartus/phase07_keccak && ./run_k0_seeds.sh; cd ../phase08_keccak && ./run_c5.sh; cd ../..
python3 scripts/select_8a.py
python3 scripts/phase7_op_cycles.py 200 14
python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/result_phase8.md
python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal
```

## 10. Approval
- [ ] Human approver (name, date): 
      Next phase starts only after a team member ticks this box. Claude never ticks it.
