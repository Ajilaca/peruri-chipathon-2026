# CHIPATON 2026 — Claude Code Handoff

Written 2026-10-02 at the end of Phase 5 and updated 2026-10-03 at the end of Phase 5M (S6-S9) and of Phase 6 (with S10), for opening a new Claude Code session. Read this file, then `CLAUDE.md`
(project rules, they override everything else), then `docs/ROADMAP.md` and `docs/decisions/PENDING.md` before doing anything.
Labels used below: **MEASURED** (Quartus report or simulation log in this repo), **INFERENCE** (derived from measured
numbers), **ESTIMATE**, **NOT MEASURED**.

## 1. Project
| Item | Value |
|---|---|
| What | ML-KEM-768 (FIPS 203) accelerator, hardware/software co-design; CHIP 2026 Hackathon (PERURI Digital Summit), Team J5, ITB |
| Repository | <https://github.com/Ajilaca/peruri-chipathon-2026> (public, MIT licence, ADR 0016) — local `~/FPGA/Projects/CHIPATON` |
| Branch | `phase6-scheduling` (Phase 6 + S10, not pushed; `main` has Phase 5M, PR #3, tag `phase5m-done-2026-10-03`) |
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
| 3 Multi-lane C2, L selection | PARTIAL — L = 8 on C2-K2-K1 (ADR 0005) | `result_phase3.md` | ticked |
| 4 Butterfly pipeline C3 | DONE — L = 8, P = 6 (ADR 0009) | `result_phase4.md` | ticked (Faza Dzil, 2026-10-01) |
| 5 Modular arithmetic C4 | DONE — C4b-B (ADR 0013, 0015 Accepted) | `result_phase5.md` | ticked (Jevan, 2026-10-03) |
| Phase 5M memory / schedule (ADR 0017, S6-S9) | DONE (2026-10-03) — S6 M6 base by team decision (ADR 0020), S7 adopted by the rule, S8 not adopted, S9 study (ADR 0021/0023/0022 superseded by 0025) | `result_phase5m.md`, PDF `docs/report/CHIPATON_Phase5M_Report.pdf` | ticked (Jevan, 2026-10-03) |
| 6 NTT scheduling at operation level (+ S10) | DONE (2026-10-03) — sequencer bit-exact, S10 adopted by its rule and accepted as the core (ADR 0025 Accepted), 20 ns met at 6/6 seeds | `result_phase6.md`, PDF `docs/report/CHIPATON_Phase6_Report.pdf` | ticked (Jevan, 2026-10-03) |

## 3. Phase 5 outcome (MEASURED unless marked; `docs/results/result_phase5.md`, PDF `docs/report/CHIPATON_Phase5_Report.pdf`)
- **C4 = C4b-B**: C3-P6 core (L = 8, P = 6) with a Barrett reducer (k = 24, M = 5039), `rtl/ntt/ntt_core_c4b_b.sv`, revision
  `C4b-B` in `quartus/phase05_arith_c4/`. Chosen by the ADR 0011 rule (higher median Fmax, 2.13 % apart = near tie, then lower
  median ALM). ADR 0013 (accepted 2026-10-02, Jevan, Team J5) records the price, DSP 9 -> 18.
- Cycles unchanged: NTT 119, INTT 375, 0 stall. Bit-exact vs `tb/golden` on Verilator and Icarus; every reducer exhaustively equal
  to `(a*b) mod q` over a, b in [0, q).
- The mathematics was not changed (C1). The Phase 1–4 files are frozen and unedited.

| Revision | ALM (seeds 1–6) | DSP | Fmax lowest slow corner (MHz), median (range) | Evidence (`docs/evidence/phase05-arith/`) |
|---|---|---|---|---|
| C3-P6 (baseline) | 10,505 (10,484–10,516) | 9 | 33.11 (32.60–34.20) | `../phase04-pipeline/seed_sweep_2026-10-01.md` |
| C4a fold reducer (5a) | 9,847 (one compile) | 9 | 33.73 (one compile) | `5a/summary_5a_2026-10-01.md` |
| **C4b-B Barrett (5b), the C4 configuration** | 9,208 (9,166–9,208) | 18 | 34.515 (33.46–34.84) | `5b/selection_worksheet_2026-10-01.md` |
| C4b-M Montgomery (5b) | 9,249 (9,249–9,297) | 9 | 33.780 (32.81–34.25) | same |
| C4c lazy INTT inputs (5c), **NOT adopted** | 9,043 (9,032–9,094) | 18 | 33.100 (32.27–35.26) | `5c/summary_5c_2026-10-01.md`, `5c/selection_worksheet_2026-10-01.md` |
| 5d Karatsuba base case | **not attempted** (ADR 0015 accepted) | — | — | `docs/decisions/0015-*.md` |

Timing is met at 40.000 ns in every compile above. t_NTT / t_INTT at the median Fmax (perhitungan tim): C4b-B 3.448 / 10.865 µs,
C3-P6 3.594 / 11.326 µs, C4c 3.595 / 11.329 µs. The seed ranges overlap, so small Fmax differences are not distinguishable from seed noise.

**Information compiles at 20.000 ns (default seed, not a gate; `closure/info_20ns_2026-10-01.md`): neither meets timing.**
C3-P6: 10,557 ALM, setup −2.059 ns, Fmax 45.33 MHz. C4b-B: 9,305 ALM, setup −2.557 ns, Fmax 44.33 MHz. The target of 50 MHz was
not reached (ADR 0010: best-effort, not a gate).

**Key finding (INFERENCE from `baseline/c3p6_critical_path_2026-10-01.md`):** the worst C3-P6 path is the memory read (21.292 ns of
29.345 ns), then `sub_mod` (4.348 ns) and the DSP (3.705 ns). No path inside the reducer is among the 300 worst. Arithmetic changes save
area (C4b-B about 1,300 ALM below C3-P6) but do not move Fmax beyond the seed spread. Reaching 50 MHz needs memory / schedule work
(PENDING #19), which is outside Phase 5's fixed scope. The cause of the 5c result is a hypothesis, not tested.

Regression (CRG-5, `regression_2026-10-01.md`, git b418d1e): Phase 0–4 script 21 steps 0 failed; Phase 5 verify 17 steps 0 failed;
formal Phase 5 14/14 as expected (control and bank properties, 5c value bounds, negative controls).

## 3b. Phase 5M outcome (MEASURED unless marked; `docs/results/result_phase5m.md`, PDF `docs/report/CHIPATON_Phase5M_Report.pdf`)
| Revision | ALM median (range) | DSP | Fmax median (range) MHz | NTT / INTT cycles | t at median Fmax (us, perhitungan tim) | Rule |
|---|---|---|---|---|---|---|
| C4b-B (Phase 5) | 9,171.0 (9,166-9,208) | 18 | 34.515 (33.46-34.84) | 119 / 375 | 3.448 / 10.865 | base |
| M6 (S6, INTT halving) | 9,421.5 (9,394-9,441) | 16 | 34.430 (32.35-35.04) | 119 / 119 | 3.456 | not adopted by the rule; base by team decision (ADR 0020) |
| **S7 (split memory read, P = 7)** | 9,391.0 (9,361-9,405) | 16 | **38.720 (37.89-40.29)** | 120 / 120 | **3.099** | adopted (ADR 0021 Proposed) |
| S8 (write register, P = 8, bubble) | 9,443.5 (9,402-9,471) | 16 | 37.990 (36.76-40.22) | 122 / 122 | 3.211 | not adopted (ADR 0023 Proposed) |
- S8 at 20 ns (information): 9,443 ALM, setup -2.242 ns, Fmax 44.96 MHz, timing not met. S7 is the best measured configuration; the team has not yet accepted it as the base for Phase 6 and 7.
- S9 (study, no RTL): the 8-bank map needs 2R + 2W per bank per cycle; a 16-bank map `bank = (a1^a2^a3^a4, a7, a6, a5)`, `offset = a[3:0]` needs 1R + 1W over the whole schedule (`docs/evidence/phase05m-memsched/s9/`). No Quartus number for it; option list in ADR 0022.
- The one full Phase 0-5 regression ran at 300aaf3 (Amendment A1): OVERALL PASS. Statements "S7-S9 not done" in ADR 0019 and 0020 were edited in place with a trace (2026-10-03, at the team's request).

## 3c. Phase 6 outcome (MEASURED unless marked; `docs/results/result_phase6.md`)
- K-PKE arithmetic sequencer (`rtl/sched/`): KeyGen / Encrypt / Decrypt programs generated from `tb/golden/kpke_sched_model.py`, bit-exact end to end against the golden K-PKE on Verilator and Icarus; counts 6/0/9,
  3/4/12, 3/1/3; constant cycles 5,493 / 6,810 / 3,121 (S7 core). P6 (seed 1): 9,840 ALM, 26 DSP, 58 M10K, 37.59 MHz, timing met at 40 ns.
- S7 path analysis (option 1): the limit is the slot-arbitration ripple; S7 at 20 ns (option 2): 0/6 seeds met.
- **S10** (`rtl/mem/poly_mem_m10k.sv`, `rtl/ntt/ntt_core_s10_p5.sv`): 16 x 1R1W banks, no arbitration, P = 5, 118 cycles; 5,045-5,091 ALM; median Fmax 44.320 MHz at 40 ns; **20 ns met at 6/6 seeds** (kernel-only, virtual
  pins; not a board result). ADR 0025 Accepted 2026-10-03 (Jevan): S10 is the NTT/INTT core for the next phases.

## 4. Phase 4 summary (still the base; details in `docs/results/result_phase4.md`)
- ADR 0009 (Accepted): L = 8, P = 6 (C3-P6); NTT-core budget 30 % = **12,573 ALM** (a budget for the NTT core, not a system limit;
  exceeding it needs a new team decision, ADR 0012).
- C3-P6: 10,505 ALM, 29 M10K (tool-inferred), 9 DSP; 119 / 375 cycles; 40 ns met at every seed (`docs/evidence/phase04-pipeline/`).
- GHRD shell alone 1,304 ALM; GHRD + C3-P6 in one compile 12,375 ALM (29.53 %), NTT 40 ns met, NTT not connected to the HPS.

## 5. ADRs (`docs/decisions/`)
| ADR | Status | Content |
|---|---|---|
| 0004, 0007 | Accepted; amended by 0009 | Phase 3 L-selection (25 %) and the Phase 4 P rule (condition 3 now 12,573 ALM) |
| 0005 | Accepted | C2-K2-K1, L = 8 |
| 0006 | Accepted; amendment note added | Clock: Phase 4 40 ns; expectation of 50 MHz after Phase 5 corrected by ADR 0010 |
| 0008 | Superseded by 0009 | never accepted |
| 0009 | Accepted | L = 8, P = 6, 30 % NTT-core budget |
| 0010 | Accepted | 50 MHz kept as best-effort project target, not a Phase 5 gate; critical path is the memory read |
| 0011 | Accepted | Phase 5 plan decisions D1–D8 and the 5b selection rule |
| 0012 | Accepted | Cycle increase accepted only if t_NTT and t_INTT at measured Fmax beat the baseline and cycles stay constant; 12,573 ALM stays the limit |
| 0013 | Accepted 2026-10-02 (Jevan) | 5b: Barrett selected by the rule; DSP 9 -> 18 |
| 0014 | Accepted | 5c lazy INTT inputs, scope (b), adoption rule; outcome note: not adopted; D6 amendment [0, 2q) only for C4c |
| 0015 | Accepted 2026-10-02 (Jevan) | 5d not attempted in Phase 5, moves to Phase 6 |
| 0017 | Accepted 2026-10-02 (Jevan) | Separate phase "Phase 5M: memory and schedule" (S6-S9) between Phase 5 and 6; branch `phase5m-memory-schedule` |
| 0018 | Superseded by 0019 | Earlier scope until the deadline |
| 0019 | Accepted 2026-10-02 (Jevan), notes 1-3 | Minimal path to full ML-KEM before 2026-10-08 (tiers T1-T3, skips Phase 6 and 8a/8c/8d); note 2: S7, S8 planned; note 3 (2026-10-03): S7-S9 all done |
| 0020 | Accepted 2026-10-02 (Jevan) | S6 (M6) result; M6 base for S7/S8 by team decision, rule result "not adopted" stays on record |
| 0021 | Superseded by 0025 (2026-10-03) | S7 split memory read: adopted by the rule (median Fmax 38.720 MHz) |
| 0022 | Superseded by 0025 (2026-10-03; option A built as S10) | S9 M10K study: options for the team |
| 0023 | Superseded by 0025 (2026-10-03) | S8 write-path register: not adopted by the rule (37.990 MHz, 122 cycles) |
| 0024 | Accepted 2026-10-03 (Jevan) | Phase 6 now (supersedes ADR 0019 point 2), S10 inside Phase 6 |
| 0025 | Accepted 2026-10-03 (Jevan) | S10 16-bank memory: adopted by the rule, accepted as the core; 20 ns met at 6/6 seeds |
| 0016 | Accepted | Repository licence MIT (copyright line wording chosen by the assistant; the team may change it) |
Open team decisions: `docs/decisions/PENDING.md` (older #1, #3, #8 ...). The team user on 2026-10-02 identified as Jevan (laptop of Faza Dzil; local git identity set per repo).

## 6. Known Limitations (not hidden)
- No board measurement of anything; all timing is Quartus static analysis (kernel-only, virtual pins).
- 50 MHz not reached (C4b-B and C3-P6 both fail at 20 ns); best Fmax at 40 ns is about 35 MHz.
- C4a and the two 20 ns compiles are single compiles; Fmax rankings between nearby revisions are not claimed.
- No path analysis at 20 ns. No HPS–NTT connection (bridge, CSR, CDC undecided, PENDING #3).
- Keccak, samplers, KEM controller, encode/compress, storage, SignalTap: NOT MEASURED (only a DRAFT ESTIMATE,
  `docs/evidence/phase04-pipeline/fabric_estimate_DRAFT_2026-10-01.md`). No system-level ALM budget defined.
- Polynomial memory is flip-flop storage (about 73 % of the core ALM); the designed M10K mapping is not achieved.
- Tool variation: up to 64 ALM between seeds (Phase 4); C4 seed spreads are in Section 3.
- `claim_lint` has 1 pre-existing error at `docs/AI_TOOLING_RESEARCH.md:197` when run over all of `docs/` (not in `docs/results docs/proposal`).

## 7. Repository Structure
```
rtl/ntt/, rtl/mem/   SystemVerilog; C3: ntt_core_c3*.sv ...; C4: ntt_core_c4.sv + wrappers ntt_core_c4{a,b_b,b_m,c}.sv
rtl/arith/           Phase 5 reducers (fold, Barrett, Montgomery, lazy Barrett), modmul_sel.sv, butterfly_c4*.sv, lazy_bfly_io.sv
tb/                  cocotb tests + Python golden model (tb/golden/, params.py = locked constants); tb/arith/ for Phase 5
formal/              SymbiYosys: phase0N-*/ .sby + tops; run_formal_slang.py (Phase 1–3), run_formal_phase4.py, run_formal_phase5.py
quartus/             one project per phase; phase05_arith_c4/ (C4a, C4b-{B,M}, C4c + seed and 20 ns revisions, C4.sdc, C4-20.sdc)
docs/                ROADMAP, decisions/ (ADRs, PENDING), results/, evidence/phaseNN-*/, report/ (Phase 0–5 PDFs), proposal/
scripts/             env.sh, phase5_verify.sh, phase5_regression.sh, phase5_select_5b.py, phase5_select_5c.py,
                     phase5_*.tcl/py (timing analysis on copies), build_phase5_report.py, ...
sw/hps/              HPS software (not started)
.claude/             settings.json, skills/ (quartus-report, phase-gate, proposal-claims, mlkem-guard, decision-record)
```
Outside the repo: `~/FPGA/Projects/CHIPATON_experiments/` (GHRD clone, combined GHRD projects, `metrics.py`).
Rebuild reports: `python3 scripts/build_phase5_report.py` (also `build_phase4_report.py`).

## 8. Git State
- On `main` after PR #2 (Phase 5), tag `phase5-done-2026-10-02`. Earlier tags: `v0.1-phase0-golden-model`, `phase2-partial-2026-09-29`,
  `phase3-partial-2026-09-30`, `phase4-p6-ghrd-2026-10-01`, `phase4-done-2026-10-01`. The user pushes, merges and tags.
- Never commit `db/`, `output_files*/`, `compile_*.log`, `.venv/`, secrets or personal data. `.obsidian/` is git-ignored.
- Pitfalls: parallel `quartus_sh` runs on one project corrupt the shared `.qpf` (the sweep scripts restore it); `quartus_sta`
  `project_open` rewrites `.qpf` (run it on copies); Quartus wrote the extract path relative to the working directory (run the
  extract script from the repository root); comments starting with "synthesis" are parsed as pragmas.

## 9. Rules for the Next Session
- Talk to the user in Bahasa Indonesia; code, identifiers and comments in English; reports per phase in Indonesian.
- **Never push automatically.** Commit only when asked. **No Claude attribution** (no Co-Authored-By / "Generated with Claude") in commits or PRs.
- Never invent measurements; label everything MEASURED / INFERENCE / ESTIMATE / NOT MEASURED. Resource/timing numbers only from Quartus in this repo.
- Never change historical evidence or rewrite accepted ADRs; record changes in a new ADR (amendment notes are allowed, as for ADR 0006 and 0014).
- Never tick an Approval box; never decide for the team (C5) — ask, then record with `/decision-record`.
- The mathematics is locked (C1). Verify before optimising; never weaken a check to make it pass.
- Run Quartus revisions one at a time in the background; add a status time estimate in replies (the user asks for it).
- For every RTL-changing step: write the test plan and adoption rule BEFORE measuring; adoption includes ADR 0012 (t_NTT and t_INTT
  better at the median Fmax of seeds 1–6, constant cycles, core ALM ≤ 12,573).

## 10. Immediate Next Steps (after Phase 6)
1. Done 2026-10-03 (Jevan): Approval boxes of Phases 5, 5M, 6 ticked (PR #5); ADR 0025 accepted (S10 is the core), ADR 0021/0022/0023 superseded. Still open: PENDING #25, #26.
2. Phase 7 (Keccak-f[1600] K0, SHA3/SHAKE) per ROADMAP and ADR 0019: golden `tb/golden/keccak.py` against hashlib first, then RTL; test plan before RTL.
3. Then samplers, encode/compress, K-PKE with the Phase 6 sequencer, full Encaps/Decaps with FO and ACVP vectors (ADR 0019 tiers). A wider host interface of the core is the next data-movement lever (56 % of KeyGen cycles).
4. Proposal Section 3 (pages 4-6) in parallel, evidence-only, under `/proposal-claims`.
