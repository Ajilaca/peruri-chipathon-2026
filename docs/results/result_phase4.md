<!-- claim-lint: skip-file (result artifact: internal status page, not proposal text) -->
# Result — Phase 4: Butterfly pipeline sweep (P = 0 / 2 / 4 / 6, config C3)

- Status: PARTIAL
- Date (UTC): 2026-09-30; updated 2026-10-01 (fitter-seed sweep for P = 4 and P = 6)
- Git commit (HEAD when verified): c2cc16c plus the Phase 4 working tree, committed together with this file
- Proposed operating point: **P = 4** by the ADR 0007 rule, in `docs/decisions/0008-apply-adr-0007-to-the-phase-4-pipeline-sweep-proposed-pipeli.md` (**Proposed, not accepted**)
- Environment: as Phase 3 -- Ubuntu 24.04.4 LTS, OSS CAD Suite 2026-09-23, cocotb 2.1.0, Quartus Prime Lite 25.1std.0 Build 1129.
- Constraint: `create_clock -period 40.000` for all four revisions (ADR 0006: an experimental milestone target, not a hardware or system requirement).

## 1. Done-criteria (Common RTL Gate, docs/ROADMAP.md)
| # | Criterion | Evidence | Status |
|---|---|---|---|
| CRG-1 | Lint clean | `docs/evidence/phase04-pipeline/cocotb_regression_2026-09-30.txt` (Verilator -Wall, 0 warnings, three wrappers plus default core) | PASS |
| CRG-2 | Elaboration clean (slang) | `docs/evidence/phase04-pipeline/cocotb_regression_2026-09-30.txt` (0 errors, 0 warnings, three wrappers) | PASS |
| CRG-3 | Bit-exact vs golden, both simulators | `docs/evidence/phase04-pipeline/cocotb_regression_2026-09-30.txt` (core 16/16 and unit 32/32 on Icarus AND Verilator), `docs/evidence/phase04-pipeline/v2_modmul_staged_exhaustive_2026-09-30.txt` (staged reducer equals the frozen reducer for all 2^24 inputs, 0 mismatches) | PASS |
| CRG-4 | Corner cases before tests | `docs/evidence/phase04-pipeline/test_plan.md`, committed before any RTL | PASS |
| CRG-5 | Regression: Phase 0-3 still pass | `docs/evidence/phase04-pipeline/regression_2026-09-30.txt` (pytest 23/23; C0 10/10; C1 12/12; C2, K2, K1 16/16 each, both simulators) | PASS |
| CRG-6 | Locked parameters | `docs/evidence/phase04-pipeline/regression_2026-09-30.txt` (check_params: all locked parameters match) | PASS |
| CRG-7 | Constant-cycle evidence | `docs/evidence/phase04-pipeline/cocotb_regression_2026-09-30.txt` (constant per P and direction, identical on both simulators) | PASS |
| CRG-8 | Formal properties | `docs/evidence/phase04-pipeline/formal_2026-09-30.md` (P = 2/4/6 k-induction PASS, 9/9 as expected incl. negative controls); `docs/evidence/phase04-pipeline/regression_2026-09-30.txt` (Phase 1-3 proofs 19/19 unchanged). Control and bank-capacity properties only, not arithmetic | PASS |
| CRG-9 | Quartus evidence; no negative slack or the failure documented | `docs/evidence/phase04-pipeline/quartus_C3-P0_20260930.md`, `docs/evidence/phase04-pipeline/quartus_C3-P2_20260930.md`, `docs/evidence/phase04-pipeline/quartus_C3-P4_20260930.md`, `docs/evidence/phase04-pipeline/quartus_C3-P6_20260930.md` -- P = 0 and P = 2 have negative setup slack at 40.000 ns (documented in Section 3); P = 4 and P = 6 meet it. Whether "documented failure" counts as PASS for P = 0 / 2 is a team call, as in earlier phases | FAIL |
| CRG-10 | Result artifact + claim checker | `cmd: python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/result_phase4.md` and `cmd: python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal` | PASS |

## 1b. Phase 4 PASS criteria (docs/ROADMAP.md Phase 4)
| # | Criterion | Evidence | Status |
|---|---|---|---|
| 1 | Correct for every P | `docs/evidence/phase04-pipeline/cocotb_regression_2026-09-30.txt` (P = 2, 4, 6; P = 0 is the frozen Phase 3 core, `docs/evidence/phase04-pipeline/regression_2026-09-30.txt`) | PASS |
| 2 | Measured comparison complete | `docs/evidence/phase04-pipeline/selection_worksheet_2026-09-30.md` | PASS |
| 3 | ADR for the chosen P | `docs/decisions/0008-apply-adr-0007-to-the-phase-4-pipeline-sweep-proposed-pipeli.md` is **Proposed**; the team has not accepted it | MISSING |
| 4 | C3 row filled | `docs/ROADMAP.md`, rows C3-P0 / P2 / P4 / P6 | PASS |
| 5 | Hazard tests at layer boundaries; stall cycles per P | `docs/evidence/phase04-pipeline/cocotb_regression_2026-09-30.txt` (scoreboard 0 violations, boundary-directed data, negative control at depth 8 trips it; stall cycles 0 for every P) | PASS |

## 2. What was produced
| Path | Purpose |
|---|---|
| `rtl/ntt/modmul_reduce_staged.sv` | `(a*b) mod q` with the reduction written as 13 conditional-subtract stages and optional registers between them; same function as `modmul_reduce.sv` |
| `rtl/ntt/butterfly_shared_pipe.sv`, `rtl/ntt/pipe_delay.sv` | The shared-multiplier butterfly with the staged reducer; delay line for the operand that bypasses it |
| `rtl/mem/poly_mem_multiport_pipe.sv` | Memory with request/read/write in time, slot arbitration with optional register stages; the read's (bank, offset, slot) is reused for the write |
| `rtl/ntt/ntt_core_c3.sv`, `rtl/ntt/ntt_core_c3_p2.sv`, `_p4.sv`, `_p6.sv` | Config C3 core (C2-K2-K1 schedule + drain) and the three Quartus wrappers; register positions are those of test plan section 2 |
| `tb/ntt/test_modmul_staged.py`, `test_butterfly_pipe.py`, `test_poly_mem_pipe.py`, `run_p4_unit_tests.py`, `tb/ntt/p4_reducer/` | Unit tests (V2-V4) and the exhaustive reducer harness |
| `tb/ntt/test_ntt_core_c3.py`, `tb/ntt/run_ntt_c3_tests.py` | Core tests (V5-V8) with the hazard scoreboard and the depth-8 negative control |
| `formal/phase04-pipeline/`, `formal/run_formal_phase4.py` | Formal top, three `.sby`, runner with negative controls |
| `quartus/phase04_pipeline_c3/` | Four revisions, one SDC at 40.000 ns |
| `scripts/phase4_select_p.py`, `docs/evidence/phase04-pipeline/verification_status.json` | The ADR 0007 rule, reading only evidence files |
| `quartus/phase04_pipeline_c3/C3-P{4,6}-s{2..6}.qsf`, `run_seed_sweep.sh`, `scripts/phase4_seed_sweep_summary.py`, `docs/evidence/phase04-pipeline/seed_sweep/` | Fitter-seed sweep (2026-10-01), input to ADR 0008 |
| `docs/decisions/0008-apply-adr-0007-to-the-phase-4-pipeline-sweep-proposed-pipeli.md` | Proposed ADR with the measured table |

Frozen files (`modmul_reduce.sv`, `butterfly*.sv`, `twiddle_rom.sv`, `bank_map_rom.sv`, `poly_mem_multiport.sv`, `ntt_core_c2*.sv`, Phase 1-3 evidence, ADR 0004) were not edited.

## 3. Numbers (MEASURED: Quartus reports; cycles from simulation)
| Quantity | P = 0 | P = 2 | P = 4 | P = 6 |
|---|---|---|---|---|
| ALM (of 41,910) | 9,723 | 9,696 | 10,439 | 10,505 |
| Within ADR 0004 budget (10,478)? | yes | yes | yes (39 below) | **no (27 over)** |
| Registers | 3,097 | 3,817 | 4,145 | 4,168 |
| RAM blocks (M10K) | 0 / 553 | 16 / 553 | 26 / 553 | 29 / 553 |
| DSP | 9 / 112 | 9 / 112 | 9 / 112 | 9 / 112 |
| Worst setup slack @ 40.000 ns | -90.653 ns | -0.368 ns | +8.734 ns | +10.753 ns |
| Worst hold slack | +0.207 ns | +0.174 ns | +0.157 ns | +0.140 ns |
| Timing met at 40.000 ns? | no | no | yes | yes |
| Fmax, lowest slow corner (MHz) | 7.65 | 24.77 | 31.98 | 34.19 |
| NTT / INTT cycles | 113 / 369 | 115 / 371 | 117 / 373 | 119 / 375 |
| Stall cycles vs 113+P / 369+P | 0 | 0 | 0 | 0 |
| t_NTT / t_INTT (us) = cycles / Fmax | 14.771 / 48.235 | 4.643 / 14.978 | 3.659 / 11.664 | 3.481 / 10.968 |
| Candidate (ADR 0007)? | no | no | yes | no |

Sources: `docs/evidence/phase04-pipeline/quartus_C3-P<n>_20260930.md`, `selection_worksheet_2026-09-30.md`,
`cocotb_regression_2026-09-30.txt`. The P = 0 figures are a fresh compile at 40.000 ns, not the Phase 3 20.000 ns result. The
sweep result is **PARTIAL**: P = 4 is the only candidate and is proposed, not accepted.

## 4. Standards and sources pinned
No FIPS 203 reading this phase; no parameter, algorithm, twiddle value or reduction result changed
(`check_params.py` passes; the staged reducer is equal to `modmul_reduce` for all 2^24 input pairs).

## 5. Coverage and limits
- **Simulation and static timing only.** No board is attached; nothing here is hardware validation. Fmax is kernel-only, virtual pins, and is not a system clock.
- **ALM margins and the seed sweep (2026-10-01).** P = 4 is 39 ALM under the budget and P = 6 27 ALM over it at the default seed. A sweep over fitter seeds 1–6 (`docs/evidence/phase04-pipeline/seed_sweep_2026-10-01.md`) found P = 6 over budget at every seed (10,484–10,516 ALM) and P = 4 within budget at 4 of 6 seeds (10,439–10,503 ALM); all 12 compiles meet 40.000 ns. The rule therefore never selects P = 6; for P = 4 the budget margin is a few tens of ALM and seed-dependent.
- **Tool inference changed the resource picture.** With registers in the memory path Quartus inferred `bank_map_rom` and some register chains into M10K (16 / 26 / 29 blocks). This was not designed; it is why P = 2 has fewer ALM than P = 0 despite more registers.
- **Near-tie (default seed).** P = 6 has the lowest t_NTT (3.481 us); P = 4 is 5.1% above it. The ALM condition keeps P = 6 out, at every seed measured.
- **P = 2 misses timing by 0.368 ns** at one slow corner (slow 100C is +0.061 ns); no exception was added.
- **Formal covers control and bank capacity only.** Arithmetic and data integrity rest on the simulations and the exhaustive reducer check. Two negative controls (NC-B, NC-C) are UNKNOWN in the proof flow, not demonstrated failures; NC-B was demonstrated by a depth-125 BMC, NC-C only by the failed induction.
- The expected outcomes stated in the test plan before measuring (P = 0 and probably P = 2 not candidates) held.

## 6. Deviations, failures and open issues
- The plan expected the register-stage counts to come out as P = RdLat + WrDly with WrDly = P/2; that is how the cuts were placed (A/M cuts before the read data, X/D cuts after), and the measured cycle counts equal 113 + P and 369 + P for every P.
- New warning types relative to Phase 3: Warning 10036 (x8 per revision, the intentionally unused `unused_clk` / `unused_ck_rst` dummy nets in `modmul_reduce_staged.sv` and `pipe_delay.sv`; benign, they exist to keep the port lint-clean). Critical warnings: 15725 (virtual-pin clock, all revisions, as in Phase 1-3) and 332148 (timing not met; P = 0 x4, P = 2 x1, P = 4 and P = 6 none). No waiver, false path other than the reset input, or multicycle constraint was added.
- The Icarus/Verilator memory test initially failed on Icarus because storage is unreset (X); the test was corrected to convert only the ports of already-written addresses. RTL unchanged by that.
- Icarus rejected a design style that mixed continuous and procedural drivers of one array; the RTL (`pipe_delay`, the arbitration registers) was changed to a per-stage register plus an assign. Function unchanged, re-verified.

## 7. Decisions needed
- **Accept, change or reject ADR 0008 (P = 4 proposed).** The seed sweep requested as input to it is done (Section 5).
- How to read CRG-9 for P = 0 / 2 (negative slack at 40.000 ns), as in earlier phases.
- The 20.000 ns end goal (ADR 0006) is not reached by any measured revision (best Fmax 34.19 MHz vs 50 MHz); this is input to Phase 5, not a Phase 4 failure.

## 8. Claims made in this phase
None written for judges/proposal text. ROADMAP C3 rows were filled from the evidence above.

## 9. Reproduce
```bash
. scripts/env.sh
python3 tb/ntt/run_p4_unit_tests.py verilator && python3 tb/ntt/run_p4_unit_tests.py icarus
python3 tb/ntt/run_ntt_c3_tests.py verilator && python3 tb/ntt/run_ntt_c3_tests.py icarus
tb/ntt/p4_reducer/run_modmul_staged_exhaustive.sh
python3 formal/run_formal_phase4.py          # ~40 min (one BMC depth 125)
python3 formal/run_formal_slang.py           # Phase 1-3 proofs, unchanged
cd quartus/phase04_pipeline_c3
for r in C3-P0 C3-P2 C3-P4 C3-P6; do quartus_sh --flow compile phase04_pipeline_c3 -c $r; done
python3 scripts/phase4_select_p.py
# seed sweep: run the C3-P4-s<n> / C3-P6-s<n> revisions ONE AT A TIME (parallel runs corrupt the shared .qpf)
python3 scripts/phase4_seed_sweep_summary.py
python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/result_phase4.md
python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal
```

## 10. Approval
- [ ] Human approver (name, date):
      Next phase starts only after a team member ticks this box. Approving means accepting CRG-9
      (negative slack for P = 0 / 2) and deciding ADR 0008 (Section 7).
