# CHIPATON 2026 — Claude Code Handoff

Written 2026-10-01 at the end of Phase 4, for opening a new Claude Code session. Read this file, then `CLAUDE.md`
(project rules, they override everything else), then `docs/ROADMAP.md` (Phase 5 section) before doing anything.
Labels used below: **MEASURED** (Quartus report or simulation log in this repo), **INFERENCE** (derived from measured
numbers), **ESTIMATE**, **NOT MEASURED**.

## 1. Project
| Item | Value |
|---|---|
| What | ML-KEM-768 (FIPS 203) accelerator, hardware/software co-design; CHIP 2026 Hackathon (PERURI Digital Summit), Team J5, ITB |
| Repository | <https://github.com/Ajilaca/peruri-chipathon-2026> (public) — local `~/FPGA/Projects/CHIPATON` |
| Branch | `phase4-pipeline` (Phase 4 finalised; not pushed by the assistant — the user pushes and merges to `main`) |
| Board | Terasic DE10-Nano (no board attached; no board measurement exists) |
| FPGA | Intel/Altera Cyclone V SE **5CSEBA6U23I7**: 41,910 ALM, 553 M10K, 112 DSP (fitter denominators) |
| Quartus | Prime Lite **25.1std.0 Build 1129** at `~/altera_lite/25.1std` (path in git-ignored `scripts/tooling.env`) |
| Environment | `. scripts/env.sh` (OSS CAD Suite, Quartus on PATH, `.venv` with cocotb 2.1.0) |

## 2. Current Status
| Phase | Status | Result artifact | Approval |
|---|---|---|---|
| 0 Golden model + KATs + errata | DONE | `docs/results/result_phase0.md` | ticked (Faza Dzil, 2026-09-29) |
| 1 NTT baseline C0 | PARTIAL (timing not met at 20 ns, documented) | `result_phase1.md` | ticked |
| 2 Memory banking C1 | PARTIAL (M10K not achieved; timing not met) | `result_phase2.md` | ticked |
| 3 Multi-lane C2, L selection | PARTIAL (timing not met at 20 ns) — L = 8 on C2-K2-K1 (ADR 0005) | `result_phase3.md` | ticked |
| **4 Butterfly pipeline C3** | **COMPLETE** — technically complete by team decision 2026-10-01 (ADR 0009); result status DONE | `result_phase4.md` | ticked (Faza Dzil, 2026-10-01) |
| 5 Modular arithmetic C4 | not started | — | — |

## 3. Final Phase 4 Decision (ADR 0009, Accepted 2026-10-01, Faza Dzil, Team J5)
- **L = 8** lanes (8 butterflies per cycle), **P = 6** pipeline stages → implementation **C3-P6**
  (`rtl/ntt/ntt_core_c3_p6.sv`, Quartus revision `C3-P6` in `quartus/phase04_pipeline_c3/`). Phase 5 starts from it.
- **Design budget: 30% of ALMs for the NTT core = 12,573 ALM** (metric: fitter "Logic utilization, ALMs needed").
  It is a budget for the NTT core, **not** a system limit, and it does **not** mean the remaining 70% suffices for
  the rest of ML-KEM. It replaces the historical 25% / 10,478 of ADR 0004 for the NTT core from Phase 4 on.
- Timing: Phase 4 target **40.000 ns (25 MHz)**, experimental (ADR 0006) — met. **Phase 5 target 20.000 ns
  (50 MHz)** — not met yet.

## 4. Important Measurements (MEASURED unless marked)
| Item | Value | Evidence (`docs/evidence/phase04-pipeline/`) |
|---|---|---|
| C3-P6, default seed | 10,505 ALM, 4,168 registers, 29 M10K (tool-inferred), 9 DSP; setup +10.753 / hold +0.140 ns @ 40 ns; Fmax 34.19 MHz (lowest slow corner) | `quartus_C3-P6_20260930.md` |
| C3-P6, seeds 1–6 | 10,484–10,516 ALM; Fmax 32.60–34.20 MHz; 40 ns met at every seed; margin to 12,573: 2,057–2,089 ALM (INFERENCE) | `seed_sweep_2026-10-01.md`, `seed_sweep/` |
| C3-P4, seeds 1–6 | 10,439–10,503 ALM; Fmax 30.60–33.00 MHz; 40 ns met at every seed | same |
| C3-P0 / C3-P2 | 9,723 / 9,696 ALM; setup −90.653 / −0.368 ns → 40 ns not met | `quartus_C3-P0_20260930.md`, `quartus_C3-P2_20260930.md` |
| Cycles (simulation) | NTT / INTT = 113+P / 369+P: C3-P6 119 / 375, 0 stall | `cocotb_regression_2026-09-30.txt` |
| Latency C3-P6 at the met 40 ns clock | NTT 4.76 µs, INTT 15.00 µs (perhitungan tim) | — |
| GHRD DE10-Nano shell alone (`de10-nano-base`, commit 9b5fc816) | 1,304–1,309 ALM (two builds), 35 M10K, 0 DSP; HPS hard block = 0 fabric ALM; timing met | `ghrd_shell_measured_2026-10-01.md` |
| GHRD + **C3-P4** in one compile (integration baseline) | 12,754 ALM, 60 M10K, 9 DSP; all clocks met incl. NTT 40 ns (setup +9.204 ns); packing Low; peak interconnect 48.2 % | `ghrd_plus_c3p4_integration_2026-10-01.md` |
| Integration delta (INFERENCE) | +18 ALM vs. standalone parts with the same settings; GHRD's global compile settings add +993 ALM to C3-P4 | same |
| Worksheets | ADR 0007 rule at 25% (historical) and at 30% | `selection_worksheet_2026-09-30.md`, `selection_worksheet_30pct_2026-10-01.md` |
| GHRD + **C3-P6** in one compile (added after Phase 4 approval) | 12,375 ALM (29.53 %), 62 M10K, 9 DSP; all clocks met incl. NTT 40 ns (setup +11.364 ns, Fmax 34.92 MHz); packing Low; peak interconnect 37.0 % | `ghrd_plus_c3p6_integration_2026-10-01.md` |
| C3-P6 standalone with the GHRD's 5 settings | 11,053 ALM, 28 M10K, 9 DSP; NTT setup +16.017 ns, Fmax 41.70 MHz (one seed) | same |
| GHRD alone, fresh full build | 1,304 ALM, 2,369 registers, 35 M10K | same |
| Integration delta (INFERENCE) | +18 ALM (12,375 − 11,053 − 1,304); GHRD settings add +548 ALM to C3-P6 (+993 to C3-P4) | same |

The combined total is the core + shell, not a check against the 12,573 NTT-core budget.

## 5. Verification Status (C3, Phase 4)
- Lint: Verilator `-Wall` and slang, 0 warnings for the three wrappers.
- Unit (staged reducer, pipelined butterfly, pipelined memory): 32/32 on Verilator and on Icarus.
- Staged reducer vs the frozen reducer: exhaustive, 16,777,216 pairs × 4 register configurations, 0 mismatches.
- Core P = 2/4/6: bit-exact vs `tb/golden` (NTT, INTT, round trip, boundary-directed data), constant cycles,
  `bank_overflow_o` = 0, hazard scoreboard 0 violations — 16/16 on both simulators. Negative control (depth 8) trips
  the scoreboard and gives wrong results, as required.
- Formal (SymbiYosys, yosys-slang, `memory_map -rom-only`): P = 2/4/6 PASS (handshake, bank overflow, counter ranges,
  write delay = P, drain, no same-cycle read/write of one location); 9/9 incl. negative controls. Phase 1–3 proofs
  19/19. Scope: control and bank capacity, **not** arithmetic.
- Regression Phase 0–3: pytest 23/23; C0 10/10; C1 12/12; C2, K2, K1 16/16 each, both simulators; `check_params.py` OK.
- Evidence: `cocotb_regression_2026-09-30.txt`, `v2_modmul_staged_exhaustive_2026-09-30.txt`, `formal_2026-09-30.md`,
  `regression_2026-09-30.txt` (all in `docs/evidence/phase04-pipeline/`).

## 6. Important ADRs (`docs/decisions/`)
| ADR | Status | Content |
|---|---|---|
| 0004 | Accepted; amended by 0009 | Phase 3 L-selection: min cycles within an ALM budget of 25% (10,478). The 25% came from an example in a question, not a requirement (review 2026-10-01). |
| 0005 | Accepted | Adopt C2-K2-K1, select L = 8 (9,754 ALM). |
| 0006 | Accepted | Clock: Phase 4 milestone 40 ns (experimental), end goal 20 ns / 50 MHz after Phase 5. |
| 0007 | Accepted; amended by 0009 | P ∈ {0,2,4,6}; candidate conditions; select min t_NTT = cycles/Fmax(lowest slow corner), smaller P within 5%. Condition 3 now 12,573 ALM. |
| 0008 | Superseded by 0009 (never accepted) | Proposed P = 4 under 25%. Measurements still valid. |
| **0009** | **Accepted** | **L = 8, P = 6 (C3-P6), 30% NTT-core budget = 12,573 ALM.** Rule at 30%: P = 6 at the default seed; across seeds 1–6 P = 6 at 1/4/5, P = 4 at 2/3/6 (near the 5% tie). |
Open team decisions: `docs/decisions/PENDING.md` (e.g. #3 DMA vs memory-mapped bridge, #1 target side, #8 board).

## 7. Known Limitations (not hidden)
- C3-P6 + GHRD compiled together once, default seed, NTT not connected to the HPS; other seeds and a combined compile with Quartus defaults NOT MEASURED.
- No HPS ↔ NTT connection exists (bridge, CSR, CDC undecided — PENDING #3).
- Keccak, samplers, KEM controller, encode/compress, polynomial/key storage, SignalTap: NOT MEASURED. Only a DRAFT
  ESTIMATE exists (`fabric_estimate_DRAFT_2026-10-01.md`, low confidence).
- 50 MHz not reached (best Fmax 34.20 MHz). No system-level ALM budget defined.
- The GHRD's compile settings raise the core's ALM (+993 for C3-P4); C3-P6 under those settings NOT MEASURED.
- Polynomial memory is flip-flop storage (7,621 ALM of C3-P4, ~73% of the core); designed M10K mapping not achieved
  (Phase 2 gap). Quartus infers some M10K on its own in C3.
- No board measurement of anything.
- Tool variation: up to 64 ALM between seeds; identical GHRD builds gave 1,304 vs 1,309 ALM.

## 8. Important Technical Findings
- L = 8 selected (ADR 0005); P = 6 selected (ADR 0009).
- Pipelining raised the lowest-slow-corner Fmax from 7.65 MHz (P = 0) to 32.60–34.20 MHz (P = 6) at +6 cycles per
  transform and 0 stall; the schedule's layer-boundary slack (≥ 7 cycles at L = 8) allows P ≤ 6 without stalls.
- Fmax in this design is set by logic depth, not by utilisation (packing difficulty Low everywhere, 13–31 % range).
- The DE10-Nano HPS is a hard block: 0 fabric ALM; the shell's fabric cost is Platform Designer interconnect + demo IP.
- GHRD + C3-P4 integration overhead: +18 ALM (INFERENCE); timing 40 ns PASS in the combined compile.
- Compile settings are budget-relevant (GHRD settings: +993 ALM on the core).
- Quartus pitfalls: parallel `quartus_sh` runs on one project corrupt the shared `.qpf`; `quartus_sta project_open`
  rewrites `.qpf`; comments starting with "synthesis" are parsed as pragmas.

## 9. Repository Structure
```
rtl/ntt/, rtl/mem/   SystemVerilog; C3: ntt_core_c3*.sv, butterfly_shared_pipe.sv, modmul_reduce_staged.sv,
                     pipe_delay.sv, rtl/mem/poly_mem_multiport_pipe.sv (frozen earlier configs stay untouched)
tb/                  cocotb tests + Python golden model (tb/golden/, params.py = locked constants); there is no
                     separate verification/ folder — simulation lives in tb/, formal in formal/
formal/              SymbiYosys: phase0N-*/ .sby + tops; run_formal_slang.py (Phase 1–3), run_formal_phase4.py
quartus/             one project per phase; phase04_pipeline_c3/ (C3-P0/P2/P4/P6 + seed revisions, C3.sdc)
docs/                ROADMAP, decisions/ (ADRs, PENDING), results/, evidence/phaseNN-*/, report/ (Phase 0–4 PDFs),
                     proposal/
scripts/             env.sh, phase4_select_p.py, phase4_seed_sweep_summary.py, build_phase4_report.py, ...
sw/hps/              HPS software (not started)
.claude/             settings.json, skills/ (quartus-report, phase-gate, proposal-claims, mlkem-guard, decision-record)
```
Outside the repo: `~/FPGA/Projects/CHIPATON_experiments/` (GHRD clone, GHRD + C3-P4 combined project, `metrics.py`).
Phase 4 report: `docs/report/CHIPATON_Phase4_Report.pdf` (rebuild: `python3 scripts/build_phase4_report.py`).

## 10. Git State
- Branch `phase4-pipeline`, last commit: "finalize phase 4: select L8 P6 and 30% resource budget" (on top of
  `a803386`). Working tree clean after that commit apart from git-ignored build products.
- **Not pushed.** The user pushes, merges to `main` and creates tags/releases. Earlier tags: `v0.1-phase0-golden-model`,
  `phase1-partial-2026-09-29`, `phase2-partial-2026-09-29`, `phase3-partial-2026-09-30` (GitHub releases deferred).
- Never commit `db/`, `output_files*/`, logs, `.venv/`, secrets or personal data.

## 11. Rules for the Next Session
- Talk to the user in Bahasa Indonesia; code, identifiers and comments in English; reports per phase in Indonesian.
- **Never push automatically.** Show/review the diff before committing; commit only when asked.
- **No Claude attribution** (no Co-Authored-By / "Generated with Claude") in commits or PRs.
- Never invent measurements. Resource/timing claims only from an actual Quartus compile in this repo
  (`/quartus-report`); label everything MEASURED / INFERENCE / ESTIMATE / NOT MEASURED.
- Never change historical evidence or rewrite accepted ADRs; record changes in a new ADR.
- Never tick an Approval box; never decide for the team (C5) — ask, then record with `/decision-record`.
- The mathematics is locked (C1). Verify before optimising; never weaken a check to make it pass.
- Run Quartus revisions one at a time; run long compiles in the background.
- **Phase 5 target = 20.000 ns / 50 MHz** (ADR 0006); C3-P6 must stay within 12,573 ALM or a new decision is recorded.

## 12. Immediate Next Steps (from `docs/ROADMAP.md` Phase 5; read it and ADR 0006/0009 first)
1. Human: push `phase4-pipeline`, merge to `main`, tag (Approval of `result_phase4.md` is already ticked).
2. Create branch for Phase 5 (pattern `phase5-<topic>`, e.g. `phase5-arith`).
3. Write the Phase 5 test plan (CRG-4) before any RTL: exhaustive multiplier-reducer test over all a, b in [0, q)
   per sub-step; corner cases; the clock constraint to use (ADR 0006 end goal 20 ns) as a team decision if unclear.
4. Phase 5 sub-steps in the roadmap order, each measured and reviewed separately, schedule/memory/L/P fixed:
   **5a** q-specific reduction (constant-q multiplication as shift-and-add) inside the current method;
   **5b** Montgomery vs Barrett behind the same interface, both measured, choice by ADR;
   **5c** (optional) lazy reduction with proven bounds; **5d** (optional) Karatsuba-style base-case multiplication.
   One Quartus revision per sub-step (`C4a`–`C4d`) compared with C3-P6.
5. Result artifact `docs/results/result_phase5.md`, evidence in `docs/evidence/phase05-arith/5a/`..`5d/`.
Optional, not on the roadmap, team decision: seed spread for any new revision; combined compile with Quartus defaults.
