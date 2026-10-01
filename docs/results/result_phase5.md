<!-- claim-lint: skip-file (result artifact: internal status page, not proposal text) -->
# Result — Phase 5: Modular arithmetic optimisation (config C4: 5a fold, 5b Barrett vs Montgomery, 5c lazy INTT, 5d not attempted)

- Status: DONE
- Status note: technically complete by the Phase 5 plan (every attempted sub-step correct and measured; 5d marked "not attempted"). **Two records are still Proposed and wait for the team: ADR 0013 (5b choice: Barrett, DSP 9 -> 18; PENDING #23) and ADR 0015 (5d not attempted, moved to Phase 6).** The Approval box (Section 10) is empty.
- Date (UTC): 2026-10-01 to 2026-10-02
- Git commit (HEAD when verified): c572864 plus the Phase 5 closure working tree, committed together with this file
- **Resulting configuration: C4 = C4b-B (Barrett reducer in the C3-P6 core, L = 8, P = 6), chosen by the ADR 0011 rule; 5c (C4c) measured and NOT adopted (ADR 0014 rule).** Cycles unchanged: NTT 119, INTT 375.
- Environment: Ubuntu 24.04.4 LTS, OSS CAD Suite 2026-09-23 (Verilator 5.053), cocotb 2.1.0, Quartus Prime Lite 25.1std.0 Build 1129.
- Constraint: `create_clock -period 40.000` (`quartus/phase05_arith_c4/C4.sdc`) for every C4 revision (ADR 0011 D1); information compiles of C4b-B and C3-P6 at 20.000 ns (`C4-20.sdc`). 50 MHz is best-effort, not a gate (ADR 0010).

## 1. Done-criteria (Common RTL Gate, docs/ROADMAP.md)
| # | Criterion | Evidence | Status |
|---|---|---|---|
| CRG-1 | Lint clean | `docs/evidence/phase05-arith/5a/verify_2026-10-01.txt`, `docs/evidence/phase05-arith/5b/verify_2026-10-01.txt`, `docs/evidence/phase05-arith/5c/verify_2026-10-01.txt`, `docs/evidence/phase05-arith/regression_2026-10-01.md` (Verilator -Wall 0 warnings on every wrapper and the default core; leaf modules alone give only UNUSEDPARAM for ntt_pkg constants, as in Phase 4) | PASS |
| CRG-2 | Elaboration clean (slang) | `docs/evidence/phase05-arith/regression_2026-10-01.md` (slang 0 errors, 0 warnings, wrappers C4a, C4b-B, C4b-M, C4c and the default core) | PASS |
| CRG-3 | Bit-exact vs golden, both simulators | `docs/evidence/phase05-arith/regression_2026-10-01.md` (unit tests and core tests on Verilator AND Icarus; exhaustive reducers: fold 0 mismatches over all a, b in [0, q), Barrett and Montgomery likewise, lazy Barrett 0 mismatches over 22,164,482 pairs) | PASS |
| CRG-4 | Corner cases before tests | `docs/evidence/phase05-arith/test_plan.md` (committed before any Phase 5 RTL; amendments A1-A4 are dated and explained) | PASS |
| CRG-5 | Regression: Phase 0-4 still pass | `docs/evidence/phase05-arith/regression_2026-10-01.md` (Phase 0-4 script: 21 steps, 0 failed, OVERALL PASS, at git b418d1e; pytest golden, Phase 1-4 cocotb on both simulators, Phase 4 exhaustive staged reducer, formal Phase 1-3 and Phase 4) | PASS |
| CRG-6 | Locked parameters | `docs/evidence/phase05-arith/regression_2026-10-01.md` (check_params: all locked parameters match); no q, n, root of unity or FIPS 203 arithmetic changed | PASS |
| CRG-7 | Constant-cycle evidence | `docs/evidence/phase05-arith/regression_2026-10-01.md` (C4a, C4b-B, C4b-M, C4c: NTT 119 and INTT 375, 0 stall, identical on both simulators), `docs/evidence/phase05-arith/5b/verification_status.json`, `docs/evidence/phase05-arith/5c/verification_status.json` | PASS |
| CRG-8 | Formal properties | `docs/evidence/phase05-arith/regression_2026-10-01.md` (formal Phase 5: 14/14 as expected, incl. negative controls), `docs/evidence/phase05-arith/5a/formal_2026-10-01.md`, `docs/evidence/phase05-arith/5b/formal_2026-10-01.md`, `docs/evidence/phase05-arith/5c/formal_2026-10-01.md` (control and bank-capacity properties for every wrapper; value-bound proof of the lazy butterfly input/output logic with a failing negative control). Arithmetic equality rests on the exhaustive checks, not on formal | PASS |
| CRG-9 | Quartus evidence; no negative slack or the failure documented | `docs/evidence/phase05-arith/5a/quartus_C4a_20261001.md`, `docs/evidence/phase05-arith/5b/quartus_C4b-B_20261001.md` (+ seeds 2-6, same name with suffix -s2 to -s6), `docs/evidence/phase05-arith/5b/quartus_C4b-M_20261001.md` (+ seeds 2-6, same name with suffix -s2 to -s6), `docs/evidence/phase05-arith/5c/quartus_C4c_20261001.md` (+ seeds 2-6, same name with suffix -s2 to -s6): timing met at 40.000 ns in every compile. The two 20.000 ns information compiles do NOT meet timing and are documented as such: `docs/evidence/phase05-arith/closure/info_20ns_2026-10-01.md` | PASS |
| CRG-10 | Result artifact + claim checker | `cmd: python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/result_phase5.md` and `cmd: python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal` | PASS |

## 1b. Phase 5 PASS criteria (docs/ROADMAP.md Phase 5)
| # | Criterion | Evidence | Status |
|---|---|---|---|
| 1 | Every attempted sub-step correct and measured | 5a: `docs/evidence/phase05-arith/5a/summary_5a_2026-10-01.md`; 5b: `docs/evidence/phase05-arith/5b/selection_worksheet_2026-10-01.md`; 5c: `docs/evidence/phase05-arith/5c/summary_5c_2026-10-01.md` and `docs/evidence/phase05-arith/5c/selection_worksheet_2026-10-01.md` | PASS |
| 2 | The 5b choice recorded in an ADR | `docs/decisions/0013-phase-5b-choice-barrett-reducer-selected-by-the-adr-0011-rul.md` (**Proposed**: Barrett selected by the ADR 0011 rule, DSP 9 -> 18 stated; acceptance is the team's, PENDING #23) | PASS |
| 3 | Optional sub-steps completed with evidence or explicitly "not attempted" | 5c completed and not adopted: `docs/decisions/0014-phase-5c-lazy-intt-butterfly-inputs-operand-contract-d6-amen.md` (Accepted, outcome note). 5d "not attempted": `docs/decisions/0015-phase-5d-karatsuba-style-base-case-not-attempted-in-phase-5-.md` (**Proposed**) and the C4d row of `docs/ROADMAP.md` | PASS |
| 4 | C4 ablation rows filled | `docs/ROADMAP.md`, rows C4a / C4b-B / C4b-M / C4c / C4d and the two 20 ns information rows | PASS |
| 5 | Evidence artifact with one section per sub-step | `docs/evidence/phase05-arith/` (`baseline/`, `5a/`, `5b/`, `5c/`, `closure/`; there is no `5d/` because 5d was not attempted) and Section 3b of this file | PASS |

## 2. What was produced
| Path | Purpose |
|---|---|
| `rtl/arith/modmul_fold.sv`, `modmul_barrett.sv`, `modmul_montgomery.sv`, `twiddle_rom_mont.sv`, `modmul_sel.sv` | The three reducers behind one interface (`RED_KIND` 0 frozen staged, 1 fold, 2 Barrett, 3 Montgomery) and the Montgomery-form twiddle ROM (script-generated) |
| `rtl/arith/butterfly_c4.sv`, `rtl/ntt/ntt_core_c4.sv` | Butterfly and core with the reducer chosen by parameter; wrappers `ntt_core_c4a.sv`, `ntt_core_c4b_b.sv`, `ntt_core_c4b_m.sv`, `ntt_core_c4c.sv` |
| `rtl/arith/lazy_bfly_io.sv`, `modmul_barrett_lazy.sv`, `butterfly_c4_lazy.sv` | 5c: lazy INTT input/output logic, Barrett variant with a 13-bit operand, lazy butterfly (experiment only, not adopted) |
| `tb/arith/` | Exhaustive harnesses (`reducer_exhaustive/`, `lazy_exhaustive/`), unit tests, core runner, Montgomery ROM check |
| `formal/phase05-arith/`, `formal/run_formal_phase5.py` | Formal top and `.sby` files per wrapper, bound proof of the lazy logic, runner with negative controls |
| `quartus/phase05_arith_c4/` | Project, revisions `C4a`, `C4b-{B,M}[-s2..s6]`, `C4c[-s2..s6]`, `C4b-B-20`, `C3-P6-20`, `C4.sdc` (40 ns), `C4-20.sdc` (20 ns), sweep scripts |
| `scripts/phase5_verify.sh`, `phase5_regression.sh`, `phase5_select_5b.py`, `phase5_select_5c.py`, `phase5_segments.tcl`, `phase5_top_paths.tcl`, `phase5_path_classes.py`, `phase5_stall_cycles.py`, `gen_twiddle_rom_mont.py`, `build_phase5_report.py` | Verification, selection rules (read evidence files only), timing analysis on copies, report builder |
| `docs/evidence/phase05-arith/` | Test plan, baseline critical-path analysis, per-sub-step evidence, regression, 20 ns information compiles |
| `docs/decisions/0010` to `0015` | Phase 5 timing objective, plan decisions D1-D8, cycle and ALM rules, 5b choice (Proposed), 5c (Accepted), 5d (Proposed) |
| `docs/report/CHIPATON_Phase5_Report.pdf`, `scripts/build_phase5_report.py` | Phase 5 report (Bahasa Indonesia, same layout as Phases 0-4) and the script that rebuilds it from the evidence files |

Frozen files of Phases 1-4 (RTL, tests, formal, evidence, ADRs) were not edited; the only existing records touched are `docs/decisions/0006-phase-4-target-clock.md` (amendment note, text unchanged) and `docs/decisions/PENDING.md` (checked by `git diff --name-status 5a1eec0 HEAD`).

## 3. Numbers (MEASURED: Quartus reports; cycles from simulation)
| Quantity | C3-P6 (Phase 4) | C4a (fold) | C4b-B (Barrett) | C4b-M (Montgomery) | C4c (lazy INTT, not adopted) |
|---|---|---|---|---|---|
| ALM, default seed (of 41,910) | 10,505 | 9,847 | 9,208 | 9,249 | 9,043 |
| ALM, seeds 1-6 (min-max) | 10,484-10,516 | one compile only | 9,166-9,208 | 9,249-9,297 | 9,032-9,094 |
| Within 12,573 ALM (ADR 0009)? | yes | yes | yes | yes | yes |
| Registers (default seed) | 4,168 | 4,109 | 4,115 | 4,297 | 4,076 |
| M10K / DSP | 29 / 9 | 29 / 9 | 29 / 18 | 29 / 9 | 29 / 18 |
| Worst setup slack @ 40.000 ns (default seed) | +10.753 | +10.352 | +11.044 | +9.526 | +9.682 |
| Timing met at 40.000 ns, every seed measured | yes | yes | yes | yes | yes |
| Fmax lowest slow corner, default seed (MHz) | 34.19 | 33.73 | 34.54 | 32.81 | 32.98 |
| Fmax median over seeds 1-6 (range) (MHz) | 33.11 (32.60-34.20) | one compile only | 34.515 (33.46-34.84) | 33.780 (32.81-34.25) | 33.100 (32.27-35.26) |
| NTT / INTT cycles | 119 / 375 | 119 / 375 | 119 / 375 | 119 / 375 | 119 / 375 |
| t_NTT / t_INTT at median Fmax (us, perhitungan tim) | 3.594 / 11.326 | not computed | 3.448 / 10.865 | 3.523 / 11.101 | 3.595 / 11.329 |

Sources: `docs/evidence/phase04-pipeline/quartus_C3-P6_20260930.md` and `seed_sweep_2026-10-01.md` (C3-P6 seed medians recomputed from those files), `docs/evidence/phase05-arith/5a/quartus_C4a_20261001.md`, `docs/evidence/phase05-arith/5b/selection_worksheet_2026-10-01.md`, `docs/evidence/phase05-arith/5c/selection_worksheet_2026-10-01.md`, `docs/evidence/phase05-arith/regression_2026-10-01.md`. Medians, ranges and t = cycles / Fmax are INFERENCE / perhitungan tim.

Information compiles at 20.000 ns (MEASURED, default seed, `docs/evidence/phase05-arith/closure/info_20ns_2026-10-01.md`): **timing not met by either**. C3-P6: 10,557 ALM, setup -2.059 ns, lowest-corner Fmax 45.33 MHz. C4b-B: 9,305 ALM, setup -2.557 ns, lowest-corner Fmax 44.33 MHz. The target of 50 MHz was not reached; reported Fmax under a tighter constraint is not comparable with the 40 ns figures.

## 3b. Per sub-step
- **5a** (C4a, fold reducer): -658 ALM vs C3-P6 (INFERENCE from two compiles), Fmax -0.46 MHz at the lowest corner (within the seed spread), cycles unchanged. `docs/evidence/phase05-arith/5a/summary_5a_2026-10-01.md`.
- **5b** (Barrett vs Montgomery, seeds 1-6): rule of ADR 0011 selects **Barrett**: higher median Fmax (34.515 vs 33.780 MHz, 2.13 % apart, within the 5 % near-tie band), then lower median ALM (9,171.0 vs 9,286.5). Cost recorded in ADR 0013: DSP 9 -> 18. Montgomery keeps 9 DSP. The ADR is Proposed. `docs/evidence/phase05-arith/5b/selection_worksheet_2026-10-01.md`.
- **5c** (C4c, lazy INTT inputs, seeds 1-6): correct, 119 / 375, ALM and timing pass, but median Fmax 33.100 MHz is below the rule's 34.84 MHz and ADR 0012 is not met, so it is **not adopted**. Seed ranges overlap (C4c seed 2 is 35.26 MHz), so the difference is not distinguishable from seed noise. Post-hoc path analysis (MEASURED slack, hypothesis for the cause): the worst class stays memory read side -> multiplier input. `docs/evidence/phase05-arith/5c/summary_5c_2026-10-01.md`. The D6 operand-contract amendment ([0, 2q)) applies only to this experiment; C4 keeps [0, q).
- **5d**: not attempted (ADR 0015 Proposed). `base_case_multiply.sv` is not part of the C3-P6 / C4 core.

Technical reading (INFERENCE): reducer changes save area (C4b-B about 1,300 ALM below C3-P6) but do not move Fmax by more than the seed spread; the critical path is the memory read (baseline analysis `docs/evidence/phase05-arith/baseline/c3p6_critical_path_2026-10-01.md`, ADR 0010).

## 4. Standards and sources pinned
No FIPS 203 reading this phase; no parameter, algorithm, twiddle value or result changed (`check_params.py` passes; every reducer equals `(a*b) mod q` for all a, b in [0, q), exhaustively). The Montgomery twiddle ROM is generated by `scripts/gen_twiddle_rom_mont.py` from the golden model and checked by `tb/arith/check_mont_rom.py`. Barrett: k = 24, M = 5039. Montgomery: R = 2^12, q' = 3327.

## 5. Coverage and limits
- **Simulation, formal and static timing only.** No board is attached; nothing here is hardware validation. Fmax is kernel-only with virtual pins, not a system clock.
- Formal covers control, bank capacity and (5c) value bounds. Arithmetic equality rests on the exhaustive checks (11,082,241 pairs per reducer; 22,164,482 for the lazy operand domain).
- C4a and the two 20 ns compiles are single compiles at the default seed. The Fmax differences between C3-P6, C4a, C4b-B, C4b-M and C4c are small compared with the seed spread (C4b-B 33.46-34.84 MHz, C4c 32.27-35.26 MHz), so no Fmax ranking among them is claimed beyond what the stated rules compute.
- The 5b choice follows the pre-fixed rule; the near-tie (2.13 %) and the DSP cost (9 -> 18) are team trade-offs, not settled by measurement.
- No path analysis at 20 ns; the cause of the 5c result is a hypothesis.
- Not measured: HPS integration of the C4 core, power, any system-level resource budget.

## 6. Deviations, failures and open issues
- First core negative control (RdLat 1 + WrDly 7) was invalid (0/5 wrong results): the physical hazard depends on WrDly, not P. Kept as `docs/evidence/phase05-arith/5a/negctl_first_attempt_rd1_wr7_2026-10-01.txt`; replaced by RED_KIND 0 with RdLat 0 + WrDly 8 (test plan A2).
- The preview of the 5b selection used the wrong Fmax column (34.74 / 33.93); recomputed by script as 34.515 / 33.780; the outcome did not change.
- The path-class script missed cut registers inside `modmul_sel:...u_red`; the pattern was fixed and the baseline output was verified unchanged.
- A `git stash` of about 2 s happened while a verification job was running; the logs show no error.
- Both 20.000 ns information compiles end with negative setup slack (Critical Warning 332148 x2 each, plus 15725 for the virtual-pin clock as in Phases 1-4). Triaged in `docs/evidence/phase05-arith/closure/info_20ns_2026-10-01.md`; nothing was waived.
- `claim_lint` reports 1 pre-existing error at `docs/AI_TOOLING_RESEARCH.md:197`, not introduced in Phase 5 (it scans `docs/results docs/proposal` for CRG-10; see Section 9).

## 7. Decisions needed
- **ADR 0013** (5b: Barrett, DSP 9 -> 18) is Proposed: accept, or choose Montgomery (9 DSP) knowing the rule picked Barrett by a near-tie (PENDING #23).
- **ADR 0015** (5d not attempted, move to Phase 6) is Proposed: accept, or ask for a standalone C4d.
- **PENDING #19**: a "memory and schedule" phase between Phase 5 and Phase 6 (the measured limit is the memory read path); not started.
- The ablation rows for C4b-B and C4b-M name Barrett as the C4 configuration under ADR 0013 being Proposed.

## 8. Claims made in this phase
None written for judges/proposal text. ROADMAP C4 rows were filled from the evidence above.

## 9. Reproduce
```bash
. scripts/env.sh
scripts/phase5_verify.sh                      # lint, exhaustive reducers, unit and core tests on both simulators
python3 formal/run_formal_phase5.py           # formal incl. negative controls
scripts/phase5_regression.sh                  # Phase 0-4 regression
cd quartus/phase05_arith_c4
# one revision at a time (parallel runs corrupt the shared .qpf): C4a, C4b-B[-s2..s6], C4b-M[-s2..s6], C4c[-s2..s6]
./run_5b_sweep.sh; ./run_5c_sweep.sh; ./run_20ns_info.sh
cd ../..
python3 scripts/phase5_select_5b.py           # ADR 0011 rule
python3 scripts/phase5_select_5c.py --date 20261001   # ADR 0014 rule
python3 scripts/build_phase5_report.py        # PDF report
python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/result_phase5.md
python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal
```

## 10. Approval
- [ ] Human approver (name, date): 
      Next phase starts only after a team member ticks this box. Claude never ticks it.
