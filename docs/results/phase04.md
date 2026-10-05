<!-- claim-lint: skip-file (result artifact: internal status page, not proposal text) -->
# Result — Phase 4: Butterfly pipeline sweep (P = 0 / 2 / 4 / 6, config C3)

- Status: DONE
- Status note: technically complete by team decision 2026-10-01 (ADR 0009); Approval ticked 2026-10-01 (Section 10).
- Date (UTC): 2026-09-30; updated 2026-10-01 (fitter-seed sweep for P = 4 and P = 6; GHRD shell and GHRD + C3-P4 integration evidence; final decision)
- Git commit (HEAD when verified): c2cc16c plus the Phase 4 working tree, committed together with this file
- **Current decision (ADR 0009, Accepted 2026-10-01, Faza Dzil, Team J5): L = 8, P = 6, implementation C3-P6; NTT-core design budget 30% = 12,573 ALM.**
- Historical: ADR 0008 (Proposed 2026-09-30, never accepted, now superseded) applied the then 25% / 10,478 ALM budget and proposed P = 4. Sections 3 and 5 keep those figures as measured.
- Environment: as Phase 3 -- Ubuntu 24.04.4 LTS, OSS CAD Suite 2026-09-23, cocotb 2.1.0, Quartus Prime Lite 25.1std.0 Build 1129.
- Constraint: `create_clock -period 40.000` for all four revisions (ADR 0006: an experimental milestone target, not a hardware or system requirement).

## 1. Done-criteria (Common RTL Gate, docs/ROADMAP.md)
| # | Criterion | Evidence | Status |
|---|---|---|---|
| CRG-1 | Lint clean | `evidence/phase04/cocotb_regression.txt` (Verilator -Wall, 0 warnings, three wrappers plus default core) | PASS |
| CRG-2 | Elaboration clean (slang) | `evidence/phase04/cocotb_regression.txt` (0 errors, 0 warnings, three wrappers) | PASS |
| CRG-3 | Bit-exact vs golden, both simulators | `evidence/phase04/cocotb_regression.txt` (core 16/16 and unit 32/32 on Icarus AND Verilator), `evidence/phase04/v2_modmul_staged_exhaustive.txt` (staged reducer equals the frozen reducer for all 2^24 inputs, 0 mismatches) | PASS |
| CRG-4 | Corner cases before tests | `evidence/phase04/test_plan.md`, committed before any RTL | PASS |
| CRG-5 | Regression: Phase 0-3 still pass | `evidence/phase04/regression.txt` (pytest 23/23; C0 10/10; C1 12/12; C2, K2, K1 16/16 each, both simulators) | PASS |
| CRG-6 | Locked parameters | `evidence/phase04/regression.txt` (check_params: all locked parameters match) | PASS |
| CRG-7 | Constant-cycle evidence | `evidence/phase04/cocotb_regression.txt` (constant per P and direction, identical on both simulators) | PASS |
| CRG-8 | Formal properties | `evidence/phase04/formal.md` (P = 2/4/6 k-induction PASS, 9/9 as expected incl. negative controls); `evidence/phase04/regression.txt` (Phase 1-3 proofs 19/19 unchanged). Control and bank-capacity properties only, not arithmetic | PASS |
| CRG-9 | Quartus evidence; no negative slack or the failure documented | `evidence/phase04/quartus_C3-P6.md` (selected C3-P6: timing met at 40.000 ns, also at seeds 2–6, `evidence/phase04/seed_sweep.md`); `evidence/phase04/quartus_C3-P0.md` and `evidence/phase04/quartus_C3-P2.md` record negative setup slack for the non-selected P = 0 / P = 2 (documented, not hidden) | PASS |
| CRG-10 | Result artifact + claim checker | `cmd: python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase04.md` and `cmd: python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal` | PASS |

## 1b. Phase 4 PASS criteria (docs/ROADMAP.md Phase 4)
| # | Criterion | Evidence | Status |
|---|---|---|---|
| 1 | Correct for every P | `evidence/phase04/cocotb_regression.txt` (P = 2, 4, 6; P = 0 is the frozen Phase 3 core, `evidence/phase04/regression.txt`) | PASS |
| 2 | Measured comparison complete | `evidence/phase04/selection_worksheet.md` | PASS |
| 3 | ADR for the chosen P | `docs/decisions/adr/ADR-0009-phase-4-final-decision-l-8-p-6-c3-p6-and-a-30-alm-design-bud.md` (Accepted: P = 6, 30% budget); ADR 0008 superseded | PASS |
| 4 | C3 row filled | `docs/ROADMAP.md`, rows C3-P0 / P2 / P4 / P6 | PASS |
| 5 | Hazard tests at layer boundaries; stall cycles per P | `evidence/phase04/cocotb_regression.txt` (scoreboard 0 violations, boundary-directed data, negative control at depth 8 trips it; stall cycles 0 for every P) | PASS |

## 2. What was produced
| Path | Purpose |
|---|---|
| `rtl/ntt/modmul_reduce_staged.sv` | `(a*b) mod q` with the reduction written as 13 conditional-subtract stages and optional registers between them; same function as `modmul_reduce.sv` |
| `rtl/ntt/butterfly_shared_pipe.sv`, `rtl/ntt/pipe_delay.sv` | The shared-multiplier butterfly with the staged reducer; delay line for the operand that bypasses it |
| `rtl/mem/poly_mem_multiport_pipe.sv` | Memory with request/read/write in time, slot arbitration with optional register stages; the read's (bank, offset, slot) is reused for the write |
| `rtl/ntt/ntt_core_c3.sv`, `rtl/ntt/ntt_core_c3_p2.sv`, `_p4.sv`, `_p6.sv` | Config C3 core (C2-K2-K1 schedule + drain) and the three Quartus wrappers; register positions are those of test plan section 2 |
| `tb/ntt/test_modmul_staged.py`, `test_butterfly_pipe.py`, `test_poly_mem_pipe.py`, `run_p4_unit_tests.py`, `tb/ntt/p4_reducer/` | Unit tests (V2-V4) and the exhaustive reducer harness |
| `tb/ntt/test_ntt_core_c3.py`, `tb/ntt/run_ntt_c3_tests.py` | Core tests (V5-V8) with the hazard scoreboard and the depth-8 negative control |
| `formal/phase04-pipeline/`, `formal/run/run_formal_phase4.py` | Formal top, three `.sby`, runner with negative controls |
| `quartus/phase04_pipeline_c3/` | Four revisions, one SDC at 40.000 ns |
| `scripts/quartus/phase4_select_p.py`, `evidence/phase04/verification_status.json` | The ADR 0007 rule, reading only evidence files |
| `quartus/phase04_pipeline_c3/C3-P{4,6}-s{2..6}.qsf`, `run_seed_sweep.sh`, `scripts/quartus/phase4_seed_sweep_summary.py`, `evidence/phase04/seed_sweep/` | Fitter-seed sweep (2026-10-01), input to ADR 0008 |
| `docs/decisions/adr/ADR-0008-apply-adr-0007-to-the-phase-4-pipeline-sweep-proposed-pipeli.md` | Proposed ADR with the measured table (superseded by ADR 0009) |
| `docs/decisions/adr/ADR-0009-phase-4-final-decision-l-8-p-6-c3-p6-and-a-30-alm-design-bud.md` | Final decision: L = 8, P = 6, 30% NTT-core budget |
| `evidence/phase04/ghrd_shell_measured.md`, `quartus_GHRD-de10-nano-base.md` | DE10-Nano GHRD shell, MEASURED (no NTT core) |
| `evidence/phase04/ghrd_plus_c3p4_integration.md` | GHRD + C3-P4 in one compile (integration baseline) |
| `evidence/phase04/ghrd_plus_c3p6_integration.md` | GHRD + C3-P6 in one compile (the selected configuration), plus C3-P6 standalone with the GHRD's settings and a fresh GHRD build; added 2026-10-01 after the approval to close the evidence gap |
| `evidence/phase04/fabric_estimate_DRAFT.md` | DRAFT, ESTIMATE: fabric content of Phases 5–10 |
| `docs/reports/CHIPATON_Phase4_Report.pdf`, `scripts/build/build_phase4_report.py` | Phase 4 report (Bahasa Indonesia, same layout as Phases 0–3) and the script that rebuilds it from the evidence files |

Frozen files (`modmul_reduce.sv`, `butterfly*.sv`, `twiddle_rom.sv`, `bank_map_rom.sv`, `poly_mem_multiport.sv`, `ntt_core_c2*.sv`, Phase 1-3 evidence, ADR 0004) were not edited.

## 3. Numbers (MEASURED: Quartus reports; cycles from simulation)
| Quantity | P = 0 | P = 2 | P = 4 | P = 6 |
|---|---|---|---|---|
| ALM (of 41,910) | 9,723 | 9,696 | 10,439 | 10,505 |
| Within the historical 25% budget (10,478; ADR 0004, used by ADR 0008)? | yes | yes | yes (39 below) | **no (27 over)** |
| Within the current 30% budget (12,573; ADR 0009)? | yes | yes | yes (2,134 below) | **yes (2,068 below)** |
| Candidate under the current budget (ADR 0007 rule, default seed)? | no (timing) | no (timing) | yes (d = 0.051) | **yes, selected (t_NTT minimum)** |
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

Sources: `evidence/phase04/quartus_C3-P<n>.md`, `selection_worksheet.md`,
`cocotb_regression.txt`. The P = 0 figures are a fresh compile at 40.000 ns, not the Phase 3 20.000 ns result. The
historical result under 25% was: P = 4 the only candidate, proposed by ADR 0008 and never accepted. Under the 30% budget of ADR 0009 the candidates are {4, 6} and the rule selects P = 6 at the default seed; across seeds 1–6 it selects P = 6 at seeds 1, 4, 5 and P = 4 at seeds 2, 3, 6 (near the 5% tie line). Latency of C3-P6 at the met 40.000 ns constraint (perhitungan tim): NTT 119 × 40 ns = 4.76 µs, INTT 375 × 40 ns = 15.00 µs.

## 4. Standards and sources pinned
No FIPS 203 reading this phase; no parameter, algorithm, twiddle value or reduction result changed
(`check_params.py` passes; the staged reducer is equal to `modmul_reduce` for all 2^24 input pairs).

## 5. Coverage and limits
- **Simulation and static timing only.** No board is attached; nothing here is hardware validation. Fmax is kernel-only, virtual pins, and is not a system clock.
- **ALM margins and the seed sweep (2026-10-01).** P = 4 is 39 ALM under the budget and P = 6 27 ALM over it at the default seed. A sweep over fitter seeds 1–6 (`evidence/phase04/seed_sweep.md`) found P = 6 over budget at every seed (10,484–10,516 ALM) and P = 4 within budget at 4 of 6 seeds (10,439–10,503 ALM); all 12 compiles meet 40.000 ns. The rule therefore never selects P = 6; for P = 4 the budget margin is a few tens of ALM and seed-dependent.
- **Tool inference changed the resource picture.** With registers in the memory path Quartus inferred `bank_map_rom` and some register chains into M10K (16 / 26 / 29 blocks). This was not designed; it is why P = 2 has fewer ALM than P = 0 despite more registers.
- **Near-tie (default seed).** P = 6 has the lowest t_NTT (3.481 us); P = 4 is 5.1% above it. The ALM condition keeps P = 6 out, at every seed measured.
- **P = 2 misses timing by 0.368 ns** at one slow corner (slow 100C is +0.061 ns); no exception was added.
- **Formal covers control and bank capacity only.** Arithmetic and data integrity rest on the simulations and the exhaustive reducer check. Two negative controls (NC-B, NC-C) are UNKNOWN in the proof flow, not demonstrated failures; NC-B was demonstrated by a depth-125 BMC, NC-C only by the failed induction.
- The expected outcomes stated in the test plan before measuring (P = 0 and probably P = 2 not candidates) held.

## 5b. System-shell and integration evidence (2026-10-01)
- MEASURED, `evidence/phase04/ghrd_shell_measured.md`: Intel DE10-Nano GHRD (`de10-nano-base`, no NTT core) uses 1,304–1,309 ALM (two builds), 35 M10K, 0 DSP; the HPS hard block uses 0 fabric ALM.
- MEASURED, `evidence/phase04/ghrd_plus_c3p4_integration.md`: GHRD + C3-P4 in one compile = 12,754 ALM; C3-P4 alone with the GHRD's compile settings = 11,432; GHRD alone = 1,304; timing met on every clock incl. the NTT clock at 40.000 ns; packing difficulty Low; peak interconnect 48.2 %.
- INFERENCE: integration delta +18 ALM with consistent settings; the GHRD's global optimisation settings account for +993 ALM on the core.
- MEASURED, `evidence/phase04/ghrd_plus_c3p6_integration.md` (added 2026-10-01, after the Approval, for the selected C3-P6): GHRD + C3-P6 in one compile = 12,375 ALM (29.53 % of the device), 62 M10K, 9 DSP; C3-P6 alone with the GHRD's compile settings = 11,053; GHRD alone (fresh full build) = 1,304; timing met on every clock incl. the NTT clock at 40.000 ns (setup +11.364 ns, Fmax 34.92 MHz at the lowest slow corner); packing difficulty Low; peak interconnect 37.0 %.
- INFERENCE: integration delta +18 ALM with consistent settings (same as for C3-P4); the GHRD's global settings account for +548 ALM on the C3-P6 core (+993 on C3-P4). 12,375 is the combined design, not a check against the 12,573 NTT-core budget of ADR 0009.
- NOT MEASURED: a real HPS–NTT bridge connection; other seeds of the combined compile.

## 6. Deviations, failures and open issues
- The plan expected the register-stage counts to come out as P = RdLat + WrDly with WrDly = P/2; that is how the cuts were placed (A/M cuts before the read data, X/D cuts after), and the measured cycle counts equal 113 + P and 369 + P for every P.
- New warning types relative to Phase 3: Warning 10036 (x8 per revision, the intentionally unused `unused_clk` / `unused_ck_rst` dummy nets in `modmul_reduce_staged.sv` and `pipe_delay.sv`; benign, they exist to keep the port lint-clean). Critical warnings: 15725 (virtual-pin clock, all revisions, as in Phase 1-3) and 332148 (timing not met; P = 0 x4, P = 2 x1, P = 4 and P = 6 none). No waiver, false path other than the reset input, or multicycle constraint was added.
- The Icarus/Verilator memory test initially failed on Icarus because storage is unreset (X); the test was corrected to convert only the ports of already-written addresses. RTL unchanged by that.
- Icarus rejected a design style that mixed continuous and procedural drivers of one array; the RTL (`pipe_delay`, the arbitration registers) was changed to a per-stage register plus an assign. Function unchanged, re-verified.

## 7. Decisions needed
- ~~Accept, change or reject ADR 0008 (P = 4 proposed)~~ — decided 2026-10-01 by ADR 0009: P = 6 with a 30% NTT-core budget; ADR 0008 superseded.
- ~~How to read CRG-9 for P = 0 / 2~~ — the selected C3-P6 meets 40.000 ns; P = 0 / 2 failures stay documented as measured non-candidates.
- Open for later phases: the compile settings of the system build (the GHRD settings raised C3-P4 from 10,439 to 11,432 ALM, MEASURED); the P = 6 + GHRD compile is done (Section 5b, MEASURED); a system-level resource budget (not defined).

## 8. Claims made in this phase
None written for judges/proposal text. ROADMAP C3 rows were filled from the evidence above.

## 9. Reproduce
```bash
. scripts/env.sh
python3 tb/ntt/run_p4_unit_tests.py verilator && python3 tb/ntt/run_p4_unit_tests.py icarus
python3 tb/ntt/run_ntt_c3_tests.py verilator && python3 tb/ntt/run_ntt_c3_tests.py icarus
tb/ntt/p4_reducer/run_modmul_staged_exhaustive.sh
python3 formal/run/run_formal_phase4.py          # ~40 min (one BMC depth 125)
python3 formal/run/run_formal_slang.py           # Phase 1-3 proofs, unchanged
cd quartus/phase04_pipeline_c3
for r in C3-P0 C3-P2 C3-P4 C3-P6; do quartus_sh --flow compile phase04_pipeline_c3 -c $r; done
python3 scripts/quartus/phase4_select_p.py
# seed sweep: run the C3-P4-s<n> / C3-P6-s<n> revisions ONE AT A TIME (parallel runs corrupt the shared .qpf)
python3 scripts/quartus/phase4_seed_sweep_summary.py
python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase04.md
python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal
```

## 10. Approval
- [x] Human approver (Faza Dzil, 2026-10-01; ticked by the assistant on the approver's explicit instruction):
      Next phase starts only after a team member ticks this box. The team declared Phase 4 technically
      complete on 2026-10-01 and recorded the decision as ADR 0009 (L = 8, P = 6, 30% NTT-core budget).
