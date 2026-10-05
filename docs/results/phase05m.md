<!-- claim-lint: skip-file (result artifact: internal status page, not proposal text) -->
# Result — Phase 5M: Memory and schedule (S6 INTT without scaling pass, S7 split memory read, S8 write-path register, S9 M10K study)

- Status: DONE
- Status note: technically complete by ADR 0017 / 0019 (S6, S7, S8 correct and measured; S9 is the documentation-only study). **Records waiting for the team: ADR 0021 (S7, Proposed), ADR 0022 (S9, Proposed), ADR 0023 (S8, Proposed).** The Approval box (Section 10) is empty; the Phase 5 Approval box is also still empty.
- Date (UTC): 2026-10-02 to 2026-10-03
- Git commit (HEAD when verified): 300aaf3 (RTL, tests and proofs of S6-S8; the full regression ran at this commit), plus the documentation commits that follow it
- **Result:** S6 (M6) is the base by team decision although the pre-fixed rule did not adopt it (ADR 0020); **S7 is adopted by the rule** (median Fmax 38.720 MHz, NTT = INTT = 120 cycles); **S8 is not adopted by the rule** (median Fmax 37.990 MHz, 122 cycles); S9 shows a conflict-free 1R1W 16-bank map exists, no hardware number.
- Environment: Ubuntu 24.04.4 LTS, OSS CAD Suite 2026-09-23 (Verilator 5.053), cocotb 2.1.0, Quartus Prime Lite 25.1std.0 Build 1129.
- Constraint: `create_clock -period 40.000` (`quartus/phase05m_memsched/M.sdc`) for every revision; one information compile of S8 at 20.000 ns (`M-20.sdc`).

## 1. Done-criteria (Common RTL Gate, docs/ROADMAP.md)
| # | Criterion | Evidence | Status |
|---|---|---|---|
| CRG-1 | Lint clean | `evidence/phase05m/s6/verify.md`, `evidence/phase05m/s7/verify.md`, `evidence/phase05m/s8/verify.md` (Verilator -Wall and slang: 0 warnings, 0 errors on every wrapper) | PASS |
| CRG-2 | Elaboration clean (slang) | `evidence/phase05m/s6/verify.md`, `evidence/phase05m/s7/verify.md`, `evidence/phase05m/s8/verify.md` (slang: 0 errors, 0 warnings) | PASS |
| CRG-3 | Bit-exact vs golden, both simulators | `evidence/phase05m/s6/verify.md`, `evidence/phase05m/s7/verify.md`, `evidence/phase05m/s8/verify.md` (core tests incl. 512 INTT unit vectors; half_mod exhaustive; memory unit and differential tests) | PASS |
| CRG-4 | Corner cases before tests | `evidence/phase05m/test_plan.md`, `evidence/phase05m/test_plan_s7.md`, `evidence/phase05m/test_plan_s8.md`, `evidence/phase05m/test_plan_s9.md` (each committed before its measurement; amendments dated) | PASS |
| CRG-5 | Regression: Phase 0-5 still pass | `evidence/phase05m/s8/regression.md` (one run on the final tree, Amendment A1: Phase 0-5 regression, Phase 5 verification, S6 and S7 verification: OVERALL PASS; 95 files added, 2 documents modified, no RTL, test or proof file of Phases 1-5 modified) | PASS |
| CRG-6 | Locked parameters | `evidence/phase05m/s8/regression.md` (check_params passes); the INTT halving is proved equal to FIPS 203 Algorithm 10 (ADR 0020, `tb/golden/tests/test_intt_halving.py`) | PASS |
| CRG-7 | Constant-cycle evidence | `evidence/phase05m/s6/verification_status.json` (119 / 119), `evidence/phase05m/s7/verification_status.json` (120 / 120), `evidence/phase05m/s8/verification_status.json` (122 / 122), identical on both simulators | PASS |
| CRG-8 | Formal properties | `evidence/phase05m/s6/formal.md`, `evidence/phase05m/s7/formal.md`, `evidence/phase05m/s8/formal.md` (control and bank-capacity properties H, O, R, A, B, C; negative controls fail). Data correctness rests on simulation, not formal | PASS |
| CRG-9 | Quartus evidence; no negative slack or the failure documented | `evidence/phase05m/s6/quartus_M6.md`, `evidence/phase05m/s7/quartus_S7.md`, `evidence/phase05m/s8/quartus_S8.md` (each with seeds 2-6 as suffix -s2 to -s6): timing met at 40.000 ns at every seed. The 20.000 ns information compile does NOT meet timing and is documented as such: `evidence/phase05m/s8/quartus_S8-20.md` | PASS |
| CRG-10 | Result artifact + claim checker | `cmd: python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase05m.md` and `cmd: python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal` | PASS |

## 1b. Phase 5M PASS criteria (ADR 0017, ADR 0019)
| # | Criterion | Evidence | Status |
|---|---|---|---|
| 1 | Each step has a test plan and rule written before measuring | the four test plans above (plans of S7 and S8 committed before their RTL ran / compiled; S8's RTL had been written and linted, disclosed in its header) | PASS |
| 2 | Each step measured with seeds 1-6 and the rule applied without change | `evidence/phase05m/s6/selection_worksheet.md`, `evidence/phase05m/s7/selection_worksheet.md`, `evidence/phase05m/s8/selection_worksheet.md` | PASS |
| 3 | Each result recorded in an ADR | `docs/decisions/adr/ADR-0020-phase-5m-s6-intt-without-the-scaling-pass-halving-in-every-l.md` (Accepted), `docs/decisions/adr/ADR-0021-phase-5m-s7-split-memory-read-path-rd-split-p-7-rule-result-.md`, `docs/decisions/adr/ADR-0023-phase-5m-s8-write-path-register-and-one-bubble-per-direction.md`, `docs/decisions/adr/ADR-0022-phase-5m-s9-m10k-study-result-options-for-the-memory-team-ch.md` (Proposed) | PASS |
| 4 | S9 study with port demand, options and evidence conditions, no RTL | `evidence/phase05m/s9/study_m10k.md`, `evidence/phase05m/s9/port_analysis.txt` | PASS |
| 5 | ROADMAP ablation rows M6, S7, S8, S8-20 | `docs/ROADMAP.md` | PASS |

## 2. What was produced
| Path | Purpose |
|---|---|
| `rtl/arith/half_mod.sv`, `butterfly_m6.sv`, `twiddle_rom_half.sv`, `rtl/ntt/ntt_core_m6.sv`, `ntt_core_m6_p6.sv` | S6: INTT halving in every layer, no scaling pass; NTT = INTT = 119 cycles |
| `rtl/mem/poly_mem_multiport_split.sv`, `rtl/ntt/ntt_core_s7.sv`, `ntt_core_s7_p7.sv` | S7: one register stage inside the memory read (RD_SPLIT), P = 7, 120 cycles |
| `rtl/ntt/ntt_core_s8.sv`, `ntt_core_s8_p8.sv` | S8: write-path register (WR_REG), P = 8, one bubble per direction, 122 cycles |
| `tb/golden/intt_halving.py`, `tb/phase5m/`, `formal/phase05m-memsched/`, `formal/run/run_formal_phase5m*.py` | Golden model of the halved INTT, tests per step, formal tops and runners with negative controls |
| `quartus/phase05m_memsched/` | Project, revisions `M6[-s2..s6]`, `S7[-s2..s6]`, `S8[-s2..s6]`, `S8-20`, `M.sdc`, `M-20.sdc`, sweep scripts |
| `scripts/phase5m_verify*.sh`, `phase5m_select_s6.py`, `phase5m_select_s7.py`, `phase5m_select_s8.py`, `phase5m_final_regression.sh`, `phase5m_s9_port_analysis.py`, `build_phase5m_report.py` | Verification, rules (read evidence files only), the one regression, the S9 analysis, the report builder |
| `evidence/phase05m/` | Test plans, per-step evidence (`s6/`, `s7/`, `s8/`, `s9/`), regression |
| `docs/decisions/0017` to `0023` | Phase 5M scope, minimal path, M6 base, S7, S9, S8 records |
| `docs/reports/CHIPATON_Phase5M_Report.pdf` | Phase 5M report (Bahasa Indonesia, same layout as Phases 0-5) |

No frozen file of Phases 1-5 (RTL, tests, formal, evidence) was edited. Existing records edited: `docs/decisions/0017-...` (amendment note), `docs/decisions/0019-...` and `docs/decisions/0020-...` (statements that S7-S9 are not done were edited in place with a bracketed trace, 2026-10-03, at the team's request), `docs/decisions/PENDING.md`, `docs/ROADMAP.md`, `CLAUDE.md`, `HANDOFF.md`, `README.md` (status lines).

## 3. Numbers (MEASURED: Quartus reports; cycles from simulation; medians and t INFERENCE)
| Quantity | C4b-B (Phase 5) | M6 (S6) | S7 | S8 |
|---|---|---|---|---|
| ALM median (seeds 1-6, min-max) | 9,171.0 (9,166-9,208) | 9,421.5 (9,394-9,441) | 9,391.0 (9,361-9,405) | 9,443.5 (9,402-9,471) |
| Within 12,573 ALM (ADR 0009)? | yes | yes | yes | yes |
| Registers (min-max) | 4,083-4,115 | 4,030-4,080 | 4,296-4,324 | 4,130-4,144 |
| M10K / DSP | 29 / 18 | 29 / 16 | 31 / 16 | 33 / 16 |
| Timing met at 40.000 ns, every seed | yes | yes | yes | yes |
| Fmax lowest slow corner, median (min-max) MHz | 34.515 (33.46-34.84) | 34.430 (32.35-35.04) | **38.720 (37.89-40.29)** | 37.990 (36.76-40.22) |
| NTT / INTT cycles | 119 / 375 | 119 / 119 | 120 / 120 | 122 / 122 |
| t_NTT / t_INTT at median Fmax (us, perhitungan tim) | 3.448 / 10.865 | 3.456 / 3.456 | **3.099 / 3.099** | 3.211 / 3.211 |
| Rule result | (Phase 5 base) | not adopted by the rule; base by team decision (ADR 0020) | adopted | not adopted |

Sources: `evidence/phase05m/s8/selection_worksheet.md` (all four rows, recomputed from the evidence files), `s7/selection_worksheet.md`, `s6/selection_worksheet.md`.
Information compile at 20.000 ns (MEASURED, S8, seed 1, `s8/quartus_S8-20.md`): 9,443 ALM, setup -2.242 ns, Fmax 44.96 MHz, timing **not met**. Earlier 20 ns compiles: C3-P6 10,557 ALM, -2.059 ns; C4b-B 9,305 ALM, -2.557 ns (`evidence/phase05/closure/info_20ns.md`).
S9 (model of the real schedule, perhitungan tim): the 8-bank map needs 2 reads + 2 writes per bank per cycle; the 16-bank map `bank = (a1^a2^a3^a4, a7, a6, a5)`, `offset = a[3:0]` needs 1 + 1 over the whole timeline (`s9/port_analysis.txt`).

## 3b. Per step
- **S6 (M6):** INTT 375 -> 119 cycles, DSP 18 -> 16, median Fmax -0.25 % versus C4b-B (inside seed noise); the rule failed only on the NTT part by 0.008 us; the team adopted M6 anyway (ADR 0020).
- **S7:** median Fmax +12.5 % (38.720 versus 34.430 MHz), the lowest S7 seed above the highest M6 seed, ALM not higher; adopted by the rule (ADR 0021, Proposed).
- **S8:** cycles as predicted, median Fmax 0.73 MHz below S7 (inside the seed spreads), +2 cycles: not adopted by the rule (ADR 0023, Proposed). Cause not analysed (hypothesis in the ADR).
- **S9:** a conflict-free 1R1W 16-bank map exists; option list and evidence conditions for an M10K memory (ADR 0022, Proposed). The first hand-derived map was wrong and was refuted by the script (plan Amendment A1).

## 4. Standards and sources pinned
No FIPS 203 reading this phase; no parameter, algorithm, twiddle value or result changed (`check_params.py` passes). The halved INTT equals FIPS 203 Algorithm 10 by the argument and checks recorded in ADR 0020 (3303 = 2^-7 mod q, 128 x 3303 = 127 x 3329 + 1). Intel M10K device facts used in S9 are NOT VERIFIED against the handbook (stated in the study).

## 5. Coverage and limits
- **Simulation, formal and static timing only.** No board is attached; nothing here is hardware validation. Fmax is kernel-only with virtual pins, not a system clock.
- Formal covers control and bank capacity, not data. One 20 ns compile (S8 only). Seed spreads: M6 2.69, S7 2.40, S8 3.46 MHz; S8 versus S7 is inside them, but the rule uses no tolerance.
- No path analysis after S7 or S8: why S7 gained and S8 did not is a hypothesis. Register and M10K counts changed between steps without a per-entity explanation.
- S9 produced no Quartus number. Not measured: HPS integration, power, system-level budget.

## 6. Deviations, failures and open issues
- Quartus rejected `$error` in `ntt_core_m6.sv` (syntax error): replaced by a localparam check with a sink; the sweep was restarted from a clean db.
- `phase5m_verify.sh` first printed "0 warnings" with a top module that had not been found (a fake pass, newline in the source list); fixed with the `lint_v` function used in Phase 5 and all S6 verification was re-run.
- Two `pkill`/`pgrep -f` calls matched the assistant's own shell and killed it; no data lost. The laptop was switched off during the first regression: outputs rediscovered by re-running; the regression was then run once at S8 (Amendment A1).
- The S9 hand-derived 16-bank map was wrong (placed lane bits on the wrong address bits); caught by the script, recorded in plan Amendment A1, corrected map verified.
- S8's RTL was written and linted before its test plan was committed (disclosed in the plan header); no simulation or compile had been run, and the rule only compares with S7's already-fixed measurement.
- The S7 plan's threshold 34.720 MHz is a rounded value of 34.7193; no effect. `%Warning-WIDTHEXPAND` lines in the cocotb Verilator builds come from the runner's ARB_REG parameter value, not from RTL lint.
- 20 ns compile: Critical Warnings 15725 and 332148 x2 as in earlier phases, triaged, nothing waived.

## 7. Decisions needed
- **ADR 0021** (S7, rule passed): accept S7 as the NTT/INTT configuration for Phase 6 and 7? **ADR 0023** (S8, not adopted): keep S7, or another base? **ADR 0022** (S9): which option, and when (suggestion: S7 now, M10K experiment after the deadline-critical blocks)?
- PENDING #25 (FIPS 203 input checks: hardware or HPS) and #26 (one STOP per block or per step). The Phase 5 and Phase 5M Approval boxes.

## 8. Claims made in this phase
None written for judges/proposal text. ROADMAP rows were filled from the evidence above.

## 9. Reproduce
```bash
. scripts/env.sh
scripts/test/phase5m_verify.sh; scripts/test/phase5m_verify_s7.sh; scripts/test/phase5m_verify_s8.sh
python3 formal/run/run_formal_phase5m.py; python3 formal/run/run_formal_phase5m_s7.py; python3 formal/run/run_formal_phase5m_s8.py
cd quartus/phase05m_memsched
# one revision at a time (parallel runs corrupt the shared .qpf)
./run_m6_sweep.sh; ./run_s7_sweep.sh; ./run_s8_sweep.sh
cd ../..
scripts/test/phase5m_final_regression.sh
python3 scripts/quartus/phase5m_select_s6.py; python3 scripts/quartus/phase5m_select_s7.py; python3 scripts/quartus/phase5m_select_s8.py
python3 scripts/test/phase5m_s9_port_analysis.py
python3 scripts/build/build_phase5m_report.py
python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase05m.md
python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal
```

## 10. Approval
- [x] Human approver (name, date): Jevan (Team J5), 2026-10-03
      Next phase starts only after a team member ticks this box. Claude never ticks it.
