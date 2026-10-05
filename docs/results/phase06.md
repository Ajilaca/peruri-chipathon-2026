<!-- claim-lint: skip-file (result artifact: internal status page, not proposal text) -->
# Result — Phase 6: NTT scheduling at operation level (K-PKE arithmetic sequencer) and S10 (16-bank 1R1W memory)

- Status: DONE
- Status note: Phase 6 PASS criteria met (bit-exact, counts, constant cycles, Quartus evidence). S10 adopted by its pre-fixed rule (ADR 0025 Proposed: the team accepts or rejects). The 50 MHz options 1 and 2 of 2026-10-03 are recorded. The Approval box (Section 10) is empty; the Phase 5 and 5M boxes are also still empty.
- Date (UTC): 2026-10-02 to 2026-10-03
- Git commit (HEAD when verified): 016bff0 (Phase 6 RTL), 8d8cb6f (S10 RTL), plus documentation commits
- Result: the K-PKE arithmetic of KeyGen, Encrypt and Decrypt runs as fixed programs in hardware, bit-exact against the unmodified golden K-PKE, with the reference transform counts and constant cycles (KeyGen 5,493, Encrypt 6,810, Decrypt 3,121 with the S7 core). S10 removes the slot arbitration: median Fmax 44.320 MHz at 40 ns (S7 38.720), ALM 5,077 (S7 9,391), 118 cycles, and timing met at 20.000 ns at 6 of 6 seeds (kernel-only).
- Environment: Ubuntu 24.04.4 LTS, OSS CAD Suite 2026-09-23 (Verilator 5.053), cocotb 2.1.0, Quartus Prime Lite 25.1std.0 Build 1129.
- Constraint: 40.000 ns (`quartus/phase06_sched/P.sdc`); information compiles at 20.000 ns (`P-20.sdc`, `quartus/phase05m_memsched/M-20.sdc`).

## 1. Done-criteria (Common RTL Gate, docs/ROADMAP.md)
| # | Criterion | Evidence | Status |
|---|---|---|---|
| CRG-1 | Lint clean | `evidence/phase06/verify.md`, `evidence/phase06/s10/verify.md` (Verilator -Wall: 0 warnings on kpke_sched_top, ntt_core_s10_p5, kpke_sched_top_s10) | PASS |
| CRG-2 | Elaboration clean (slang) | `evidence/phase06/verify.md`, `evidence/phase06/s10/verify.md` (slang rc 0) | PASS |
| CRG-3 | Bit-exact vs golden, both simulators | `evidence/phase06/verify.md` (golden schedule model 26 pytest; pwm_unit 20,035 pairs; top 3 random + 2 corner cases per program, end to end against the golden K-PKE; Verilator and Icarus), `evidence/phase06/s10/verify.md` (S10 memory, core, Phase 6 top with S10) | PASS |
| CRG-4 | Corner cases before tests | `evidence/phase06/test_plan.md`, `evidence/phase06/test_plan_s10.md` (written before RTL; S10 Amendment A1 dated and explained) | PASS |
| CRG-5 | Regression: earlier phases still pass | No existing RTL, test or proof file was modified (all new files; git diff --name-status f5e4e21 HEAD lists additions plus one document, ADR 0019); the full Phase 0-5M regression ran at 300aaf3: `evidence/phase05m/s8/regression.md` | PASS |
| CRG-6 | Locked parameters | `evidence/phase06/verify.md` (ROMs regenerated from the golden model byte for byte); no q, n, root or FIPS 203 arithmetic changed | PASS |
| CRG-7 | Constant-cycle evidence | `evidence/phase06/verify.md` (one cycle count per program over random and corner inputs, both simulators), `evidence/phase06/s10/verification_status.json` (118 / 118) | PASS |
| CRG-8 | Formal properties | `evidence/phase06/formal.md` (sequencer H, T, C, R; NC-T fails), `evidence/phase06/s10/formal.md` (S10 H, O, R, A, B, C; NC-O, NC-A fail) | PASS |
| CRG-9 | Quartus evidence; no negative slack or the failure documented | `evidence/phase06/quartus_P6.md` (timing met at 40 ns), `evidence/phase06/s10/quartus_S10.md` (+ seeds 2-6, suffix -s2 to -s6, all met), `evidence/phase06/s10/quartus_S10-20.md` (+ seeds 2-6, met at 20 ns). S7 at 20 ns does NOT meet timing and is documented: `evidence/phase05m/fmax50/quartus_S7-20.md` (+ seeds 2-6) | PASS |
| CRG-10 | Result artifact + claim checker | `cmd: python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase06.md` and `cmd: python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal` | PASS |

## 1b. Phase 6 PASS criteria (docs/ROADMAP.md Phase 6)
| # | Criterion | Evidence | Status |
|---|---|---|---|
| 1 | Operation-level arithmetic bit-exact, matrices and noise injected from the golden model | `evidence/phase06/verify.md` | PASS |
| 2 | Transform counters equal the reproduced counts (KeyGen 6/0/9, Encaps 3/4/12, Decaps 6/5/15) | `tb/golden/op_counts.py`, `evidence/phase06/verify.md` (hardware counters 6/0/9, 3/4/12, 3/1/3; Decaps = Decrypt + Encrypt) | PASS |
| 3 | Constant cycle count; cycles and Quartus evidence recorded | `evidence/phase06/verify.md`, `evidence/phase06/quartus_P6.md` | PASS |
| 4 | Sub-step 6b (radix-4) measured or "not attempted" | not attempted (not requested; ADR 0024 scope) | PASS |

## 2. What was produced
| Path | Purpose |
|---|---|
| `tb/golden/op_counts.py`, `tb/golden/kpke_sched_model.py`, `tb/golden/tests/test_kpke_sched_model.py` | Reproduced transform counts; golden schedule model proved equal to the golden K-PKE |
| `scripts/build/gen_kpke_sched_roms.py`, `rtl/sched/gamma_rom.sv`, `rtl/sched/kpke_prog_rom.sv` | Generated γ table and operation programs |
| `rtl/sched/poly_store.sv`, `pwm_unit.sv`, `kpke_sched.sv`, `kpke_sched_top.sv`, `kpke_sched_top_s10.sv` | Phase 6 block: slots, pointwise multiply-accumulate, sequencer, tops with the S7 and S10 cores |
| `rtl/mem/poly_mem_m10k.sv`, `rtl/ntt/ntt_core_s10.sv`, `ntt_core_s10_p5.sv` | S10: 16-bank 1R1W memory, core and wrapper |
| `tb/sched/`, `tb/s10/`, `formal/phase06-scheduling/`, `formal/s10/`, `formal/run/run_formal_phase6.py`, `formal/run/run_formal_s10.py` | Tests, formal tops and runners with negative controls |
| `quartus/phase06_sched/`, `quartus/phase05m_memsched/S7-20*.qsf` | Revisions P6, S10[-s2..s6], S10-20[-s2..s6], P6S10, P6S10-20, S7-20[-s2..s6] |
| `scripts/test/phase6_verify.sh`, `s10_verify.sh`, `select_s10.py`, `phase5m_top_paths.tcl`, `build_phase6_report.py` | Verification, rule, path analysis, report |
| `evidence/phase06/`, `evidence/phase05m/fmax50/` | Evidence |
| `docs/decisions/0024`, `0025` | Phase 6 / S10 order (Accepted), S10 result (Proposed) |
| `docs/reports/CHIPATON_Phase6_Report.pdf` | Report (Bahasa Indonesia) |

## 3. Numbers (MEASURED: Quartus reports; cycles from simulation; medians and t INFERENCE / perhitungan tim)
| Quantity | S7 core | S10 core | P6 (sequencer + S7) |
|---|---|---|---|
| ALM (seeds 1-6 median, min-max; P6 seed 1) | 9,391.0 (9,361-9,405) | 5,077.0 (5,045-5,091) | 9,840 |
| Registers | 4,296-4,324 | 543-555 | 4,589 |
| M10K / DSP | 31 / 16 | 24 / 16 | 58 / 26 |
| Timing at 40.000 ns | met, every seed | met, every seed | met |
| Fmax lowest slow corner at 40 ns (MHz) | median 38.720 (37.89-40.29) | median 44.320 (42.34-46.65) | 37.59 (seed 1) |
| Timing at 20.000 ns, seeds met | 0 / 6 (worst setup -1.388 to -2.431 ns) | 6 / 6 (worst setup +0.792 to +1.718 ns) | not compiled with S7; with S10 (P6S10-20, seed 1): met, +0.619 ns, 51.60 MHz, 5,643 ALM |
| NTT / INTT cycles | 120 / 120 | 118 / 118 | - |
| t_NTT at median Fmax (us) | 3.099 | 2.662 | - |
| K-PKE cycles KeyGen / Encrypt / Decrypt | 5,493 / 6,810 / 3,121 (P6 with S7) | 5,475 / 6,789 / 3,109 (P6 with S10) | |

Sources: `evidence/phase06/s10/selection_worksheet.md`, `evidence/phase06/quartus_P6.md`, `evidence/phase05m/fmax50/path_analysis.md`, the verify files above.
Phase 6 top with the S10 core (information, seed 1; `evidence/phase06/quartus_P6S10.md`, `evidence/phase06/quartus_P6S10-20.md`): 40 ns 5,553 ALM, 840 registers, 26 DSP, 51 M10K, 43.26 MHz; 20 ns timing met, setup +0.619 ns, 51.60 MHz, 5,643 ALM.
Data movement through the core's host port (one coefficient per cycle): transforms x (257 load + 260 read-back) cycles = 3,102 of 5,493 KeyGen cycles (56 %, perhitungan tim from the RTL operation lengths).

## 4. Standards and sources pinned
FIPS 203 Algorithms 11 (MultiplyNTTs), 12 (BaseCaseMultiply), 13-15 (K-PKE) as transcribed in `tb/golden/`; γ table and programs generated from the golden model; no parameter or arithmetic changed (`check_params.py` unchanged and passing in the last regression).

## 5. Coverage and limits
- Simulation, formal and static timing only. No board; Fmax is kernel-only with virtual pins. "Timing met at 20 ns" is this flow's static timing, not a system at 50 MHz.
- Keccak, samplers, compression, encoding and the FO transform are not in hardware (inputs injected by the testbench, as the ROADMAP requires for Phase 6).
- Formal covers control, not data. P6 is one compile (seed 1). No path analysis after S10.
- The host port of the core (one coefficient per cycle) dominates the operation cycles; a wider interface is future work (not measured).

## 6. Deviations, failures and open issues
- S10 core test: the first run failed only on the start-latency bound of the reused S7 test; recorded as Amendment A1 of the S10 plan with the derivation (no threshold changed).
- The first information compile P6S10 was started with a wrong top entity name (`kpke_sched_top_s10_s10`, a text-replacement slip), stopped, fixed and restarted; the tool rewrote the project's `.qpf` meanwhile; the revision list was restored.
- A status message quoted "-0.836 ns" for S7 at 20 ns seed 1; that was one corner; the worst over all corners is -1.388 ns (corrected in `fmax50/path_analysis.md`).
- `%Warning-UNOPTFLAT` in the cocotb Verilator builds of the frozen Barrett reducer (as in Phase 5): a simulation-scheduling notice, recorded in the verify files.
- Critical Warning 15725 (virtual pin clock) in every compile, as in earlier phases; no 332148 in any S10 compile; triaged, nothing waived.

## 7. Decisions needed
- ADR 0025 (S10 adopted by the rule): accept S10 as the core memory (and the Phase 6 top with S10) for the next phases?
- ADR 0021 (S7), ADR 0022 (S9), ADR 0023 (S8) are still Proposed (S10 supersedes the S9 question if ADR 0025 is accepted). PENDING #25, #26, #27. Approval boxes of Phases 5, 5M and 6.

## 8. Claims made in this phase
None written for judges/proposal text. ROADMAP rows were filled from the evidence above.

## 9. Reproduce
```bash
. scripts/env.sh
scripts/test/phase6_verify.sh; python3 formal/run/run_formal_phase6.py
scripts/test/s10_verify.sh;    python3 formal/run/run_formal_s10.py
cd quartus/phase06_sched && ./run_p6.sh && ./run_s10_sweep.sh && ./run_p6s10.sh; cd ../..
cd quartus/phase05m_memsched && ./run_s7_20_sweep.sh; cd ../..
python3 scripts/quartus/select_s10.py
python3 scripts/build/build_phase6_report.py
python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase06.md
python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal
```

## 10. Approval
- [x] Human approver (name, date): Jevan (Team J5), 2026-10-03
      Next phase starts only after a team member ticks this box. Claude never ticks it.
