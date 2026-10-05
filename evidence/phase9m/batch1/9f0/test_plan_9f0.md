<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Phase 9F step S0: the 9M-1 core under tighter constraints — test plan and rule

Written 2026-10-04 before any S0 compile. Scope: ADR 0036 (Accepted, Faza Dzil: order S0 -> S1 -> S2, latency rule, Fmax reported at a tighter constraint beside 40 ns). No RTL change. Labels: MEASURED, ESTIMATE, INFERENCE, perhitungan tim.

## 1. Why
The critical-path report of the 9M-1 core (`../../critical_paths_MW.md`) shows that at 20 ns every one of the 300 worst paths is inside a C5 Keccak permutation (slack +4.355 ns) and, INFERENCE, that outside them the design allows about 69 MHz (14.5 ns). S0 finds how far the constraint can be tightened on the existing design (the limit of the C5 permutations), before S1 replaces them. It is the baseline for S1 and for the Fmax reporting at a tighter constraint decided in ADR 0036.

## 2. Revisions (one project `quartus/phase09f0_core`, one at a time; core = 9M-1, `CODEC_W2 = 1`, `HASH_C5 = 1`, sources as `quartus/phase09m1_core/MW.qsf`)
| Revision | Constraint | Seed | Effort |
|---|---|---|---|
| F16-s1, F16-s2 | 16.000 ns | 1, 2 | Quartus defaults |
| F15-s1, F15-s2 | 15.000 ns | 1, 2 | Quartus defaults |
| F14-s1, F14-s2 | 14.000 ns | 1, 2 | Quartus defaults |
| H14-s1, H14-s2 | 14.000 ns | 1, 2 | `OPTIMIZATION_MODE "HIGH PERFORMANCE EFFORT"`, `OPTIMIZATION_TECHNIQUE SPEED` |
The seeds 1 and 2 only (a sweep to find the limit, not the six-seed statement that ADR 0036 asks for at the final reporting constraint; that comes with S1). The ALM budget of the plan is 20,000.

## 3. Estimates written before measuring (ESTIMATE)
From the MW-20 path report: worst slack +4.355 ns at 20 ns, i.e. a period of about 15.6 ns for the worst path as the fitter left it under a 20 ns constraint; under a tighter constraint the fitter works harder. ESTIMATE: 16 ns met at both seeds; 15 ns met at one or both seeds; 14 ns not met at the default effort; the high-performance effort gains 0.3-1 ns on the worst path at 14 ns and may or may not meet it. ALM within +/- 3 % of 17,654 (effort and replication may add ALM); registers +/- 3 %; RAM blocks 54 and DSP 28 unchanged. If a constraint fails, the failing slack is reported as MEASURED; no setting is changed afterwards to turn it green.

## 4. Parameters measured (per revision, from the extract of `.claude/skills/quartus-report/scripts/extract_quartus_report.py`)
ALM (and % of the fitter's denominator), registers, RAM blocks, DSP, worst setup and hold slack (all corners), timing met yes / no, lowest slow-corner Fmax, critical warnings; per constraint: met at k of 2 seeds. Latency at the achieved Fmax: t = cycles / Fmax (perhitungan tim; the profile-input cycles of the 9M-1 core: 8,327 / 10,159 / 15,515) for the constraints met at both seeds, with the lower Fmax of the two seeds. The critical-path classification (script `scripts/quartus/phase5m_top_paths.tcl` on a copy) is made for the tightest constraint met at both seeds.

## 5. Rule (fixed before measuring)
Information; no adoption between candidates. The limit of the existing design is the tightest constraint met at both seeds; if no constraint is met at both seeds, the limit is the loosest of the sweep that is met at one seed, stated with the failing seed. The step is useful for S1 if it names the block that limits timing at that constraint.

## 6. Procedure
`quartus/phase09f0_core/run_f0.sh` compiles the eight revisions strictly one at a time (shared .qpf; restored after each compile), logs `compile_<rev>.log`; extracts into `evidence/phase9m/batch1/9f0/`; `scripts/quartus/select_9f0.py` writes `selection_worksheet_<date>.md` from the extracts; the path classification as in `../../critical_paths_MW.md`. No simulation or formal run is needed (no RTL change). Compiles run beside the item 3 compiles of `quartus/phase09m3_core` (different project directories; the machine is shared, which can lengthen the run time but does not change the results).

## 7. Amendment A2 (2026-10-04, after the first sweep; nothing above is edited)
The sweep of sections 2-6 (16, 15, 14 ns; `result_9f0.md`) found every constraint met, so it did not find the limit. Faza Dzil, chat 2026-10-04: extend the sweep and "check sampai fail; jika pada 10 ns masih pass kita stop di sana saja".
- **Added revisions:** F13, F12, F11, F10, each at seeds 1 and 2, Quartus defaults (the same settings as F14: no high performance effort, the SDC form of S0 without the reset false path, `C-13.sdc` .. `C-10.sdc`). Run by `quartus/phase09f0_core/run_f0x.sh`, strictly one compile at a time.
- **Rule (fixed before the runs):** constraints are tried in the order 13, 12, 11, 10 ns, both seeds of a constraint each time. The sweep stops after the first constraint at which either seed has a negative setup or hold slack in any corner of `sta.summary` (that constraint is then reported as not met at k of 2 seeds, and the limit lies between it and the previous one); it stops after 10 ns if every constraint down to 10 ns is met (then the limit lies below 10 ns and is not searched further).
- **Estimates written before the runs (ESTIMATE):** the three permutation classes and the NTT class are within 0.55 ns at 14 ns (slack +0.721 ns, i.e. the worst path about 13.3 ns); the fitter has been able to move paths so far, so the first failure is expected at 12 or 11 ns; 13 ns met at both seeds. Area rises as the constraint tightens (replication: ALM up to about +3 %, registers up to +10 %).
- **Reading rule:** as in section 5 (information, no adoption); the critical-path classification (`scripts/quartus/classify_paths_9f.py` on `phase5m_top_paths.tcl`) is made for the tightest constraint met at both seeds and for the first one not met.
