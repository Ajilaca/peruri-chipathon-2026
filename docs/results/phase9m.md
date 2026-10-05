<!-- claim-lint: skip-file (result artifact: internal status page, not proposal text) -->
# Result — Phase 9M: optimisation of the ML-KEM-768 core (cycles, area, Fmax), simulation and static timing

- Status: PARTIAL (every step was built, verified, measured and reported; the formal evidence is incomplete for three bounded checks that timed out, see section 6; the acceptance of the ADRs and the Approval box are the team's)
- Status note: scope ADR 0034 (Accepted, Faza Dzil 2026-10-04: items 1-4; item 5, the second sampler, kept as an idea and not built), Fmax plan ADR 0036 and reporting limit ADR 0039 (both Accepted). Batch 1 (9M-1, 9M-2, 9M-3, S0, S1, S1b) was done under Faza Dzil and committed (16 commits on the branch); Batch 2 (S2, S2b, item 4) was done under Jevan in the same session and is not committed at the time of writing. Every step has a test plan with its adoption rule; only the item 4 plan was written after its RTL (stated in that plan). The ADRs 0035, 0037, 0038, 0040, 0041, 0042, 0043 are Proposed; nothing was adopted for the team.
- Date (UTC): 2026-10-04 / 2026-10-05 (this result: 2026-10-04 23:09 UTC, 2026-10-05 06:09 WIB)
- Git commit (HEAD when verified): cf81581 on branch `phase9m-optimisation` (Batch 2 files uncommitted on top)
- Result: the Phase 9 core (`mlkem_core`, 17,620.5 ALM, 9,095 / 10,735 / 16,667 cycles for KeyGen / Encaps / Decaps) became `mlkem_core4` (K4) with 14,222.0 ALM at 40 ns (-19 %), 8,416 / 9,611 / 12,989 cycles (-7.5 % / -10.5 % / -22.1 %) and timing met at 15.000 ns at 6 of 6 seeds (median Fmax 76.665 MHz, lowest slow corner). Latency at 15 ns (cycles / median Fmax, perhitungan tim, kernel-only static timing, not a board measurement): 109.8 / 125.4 / 169.4 us. ACVP is 100 % on both simulators (keyGen 25, encapsulation 25, decapsulation 10), Encaps and Decaps cycles are identical across the tested inputs. K4 stands on K3 (ADR 0042), which its own rule did not adopt as written. P1 of K4 and two negative controls have no formal result (timeout).
- Environment: Ubuntu 24.04 (Linux 7.0.0-34), OSS CAD Suite (Verilator 5.053 devel, Icarus 14.0 devel, Yosys 0.69, slang 11.0, SymbiYosys with boolector), cocotb 2.1.0, Python 3.12.3, Quartus Prime Lite 25.1std.0 Build 1129.
- Constraint: 40.000 ns is the gate (the `C.sdc` of Phases 5-9); 15.000 ns is the Fmax reporting limit (ADR 0039; no compile below 15 ns except the S0 sweep to 13 ns that located the limit); no virtual-pin result is a board result.

## 1. Done-criteria (derived from ADR 0034, 0036 and 0039; Phase 9M has no entry in docs/ROADMAP.md)
| # | Criterion | Evidence | Status |
|---|---|---|---|
| M-1 | Item 1: two bytes per cycle on the codec path, rule met, ACVP 100 % on both simulators | `evidence/phase9m/batch1/9m1/result_9m1.md`, `evidence/phase9m/batch1/9m1/sim_verilator.md`, `evidence/phase9m/batch1/9m1/sim_icarus.md` | PASS |
| M-2 | Item 2: core at 20 ns at six seeds | `evidence/phase9m/batch1/9m2/result_9m2.md` (timing met at 20 ns at 6 of 6 seeds for both cores) | PASS |
| M-3 | Item 3: K0 hash sponge, rule met | `evidence/phase9m/batch1/9m3/result_9m3.md` (ALM -1,736.5, +120 cycles) | PASS |
| M-4 | S0, S1, S1b: limit located; K0 sampler; background hash; each with plan, rule, six-seed Quartus at 40 ns and 15 ns | `evidence/phase9m/batch1/9f0/result_9f0.md`, `evidence/phase9m/batch1/9f1/result_9f1.md`, `evidence/phase9m/batch1/9f1b/result_9f1b.md` | PASS |
| M-5 | S2 (P = 6), S2b (registered address): plan before measuring, rule applied, result reported honestly (S2 neutral; S2b not adopted by the rule as written) | `evidence/phase9m/batch2/9s2/result_9s2.md`, `evidence/phase9m/batch2/9s2b/result_9s2b.md` | PASS |
| M-6 | Item 4: loads behind the engine (K4), rule met | `evidence/phase9m/batch2/9i4/result_9i4.md`, `evidence/phase9m/batch2/9i4/selection_worksheet.md` | PASS |
| M-7 | Bit-exact against the golden model and ACVP, both simulators, for the final K4 (simulation only) | `evidence/phase9m/batch2/9i4/sim.md` (Verilator 6/6, Icarus 6/6), `evidence/phase9m/batch2/9s2b/sim.md` | PASS |
| M-8 | Constant-cycle evidence (Encaps and Decaps identical across tested inputs) | `evidence/phase9m/batch2/9i4/cycles_verilator_core_k4.json`, `evidence/phase9m/batch2/9i4/cycles_icarus_core_k4.json` | PASS |
| M-9 | Negative controls fail as required (and a throttled host port passes with the interlock) | `evidence/phase9m/batch2/9i4/sim.md`, `evidence/phase9m/batch2/9s2b/sim.md` | PASS |
| M-10 | Quartus evidence for every reported configuration; negative slack or failure documented | worksheets in `evidence/phase9m/batch1/9m1` ... `evidence/phase9m/batch2/9i4`; K4: timing met at 40 ns and 15 ns at 6 of 6 seeds each | PASS |
| M-11 | Formal evidence complete (every property and every control has a result) | `evidence/phase9m/batch2/9i4/formal.md`, `evidence/phase9m/batch1/9f1b/formal.md`: P1 of core4, NC-E1-4 and NC-B7 of core3 timed out; all other properties PASS and the other controls FAIL as required | MISSING |
| M-12 | Regression: the defaults reproduce the earlier cycle counts; frozen Phase 6-8 files unchanged | `evidence/phase9m/batch2/9s2b/sim.md` (defaults 118 / 118, 13/13, core 6/6), `evidence/phase9m/batch1/9m1/regression_default.md` | PASS |
| M-13 | Locked parameters | `cmd: python3 .claude/skills/mlkem-guard/scripts/check_params.py` (run 2026-10-05: all locked parameters match); no FIPS 203 arithmetic changed | PASS |
| M-14 | Result artifact and claim checker | `cmd: python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase9m.md` and `cmd: python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results` | PASS |

## 2. What was produced
| Path | Purpose |
|---|---|
| `rtl/mlkem/mlkem_pack2.sv`, `mlkem_unpack2.sv`, `mlkem_wordbytes2.sv`, `mlkem_bytedst2.sv`, `mlkem_ldpoly2.sv`, `mlkem_stpoly2.sv` | two-byte codec path (`CODEC_W2`) |
| `rtl/mlkem/mlkem_core2.sv`, `mlkem_core3.sv`, `rtl/sample/*` (K0 sampler parameter) | K0 sampler and hash (`SMP_C5`, `HASH_C5`), background hash sidecar (K1b) |
| `rtl/ntt/ntt_core_s10.sv`, `ntt_core_s10_p5.sv`, `rtl/sched/kpke_smp_top_s10.sv` (parameters `NTT_P6`, `NTT_AR`, default 0) | P = 6 and the registered issue address (S2, S2b) |
| `rtl/mlkem/mlkem_core4.sv`, `mlkem_ldpoly2o.sv`, `mlkem_ctl_rom3.sv`, `rtl/sched/kpke_sched_smp4.sv`, `kpke_smp_top_s10o.sv` | loads behind the engine (item 4, K4) |
| `evidence/phase9m/` | plans, results, worksheets, simulation, formal and Quartus extracts per step (9m1, 9m2, 9m3, 9f0, 9f1, 9f1b, 9s2, 9s2b, 9i4) |
| `quartus/phase09*_core/` | Quartus projects of every step (outputs are not committed; archived outside the repository) |
| `formal/run/run_formal_phase9*.py`, `formal/phase09m-optimisation/` | formal runners and tops |
| `docs/decisions/0034 .. 0043`, `docs/decisions/PENDING.md` #34 - #40 | decisions (0034, 0036, 0039 Accepted; the others Proposed) |
| `docs/reports/CHIPATON_Phase9M_Report.pdf` (built by `scripts/build/build_phase9m_report.py`), `docs/reports/CHIPATON_COMPLETE_REPORT.pdf` (built by `scripts/build/build_complete_report.py`) | the narrative reports |

## 3. Numbers (each MEASURED, kernel-only static timing with virtual pins unless noted; latency = cycles / median Fmax, perhitungan tim)
Median of six seeds. Fitter denominators: 41,910 ALM, 553 RAM blocks, 112 DSP. RAM blocks 53-54 and DSP 28 in every configuration.
| Configuration | Change | ALM 40 ns | Fmax 15 ns (MHz) | Cycles KeyGen / Encaps / Decaps | Latency at 15 ns (us) | Evidence |
|---|---|---|---|---|---|---|
| Phase 9 core (C7-core) | baseline | 17,620.5 | not measured (20 ns: 63.645) | 9,095 / 10,735 / 16,667 | (20 ns: 142.9 / 168.7 / 261.9) | `evidence/phase9m/batch1/9m2/result_9m2.md` |
| MW (9M-1) | + two-byte codec | 17,654.0 | 73.635 (2 seeds) | 8,327 / 10,159 / 15,515 | 113.6 / 138.5 / 211.6 (lower of 2 seeds) | `evidence/phase9m/batch1/9m1/result_9m1.md`, `evidence/phase9m/batch1/9f0/result_9f0.md` |
| MK (9M-3) | + K0 hash | 15,917.5 | not measured | 8,447 / 10,279 / 15,635 | (40 ns only) | `evidence/phase9m/batch1/9m3/result_9m3.md` |
| K1 (S1) | + K0 sampler | 14,061.0 | 73.070 | 8,795 / 10,627 / 15,983 | 120.4 / 145.4 / 218.7 | `evidence/phase9m/batch1/9f1/result_9f1.md` |
| K1b (S1b) | + background hash | 14,335.0 | 73.855 | 8,404 / 10,236 / 15,597 | 113.8 / 138.6 / 211.2 | `evidence/phase9m/batch1/9f1b/result_9f1b.md` |
| K2 (S2) | + P = 6 | 14,213.0 | 74.125 | 8,416 / 10,250 / 15,619 | 113.5 / 138.3 / 210.7 | `evidence/phase9m/batch2/9s2/result_9s2.md` |
| K3 (S2b) | + registered address | 14,115.5 | 77.555 | 8,416 / 10,250 / 15,619 | 108.5 / 132.2 / 201.4 | `evidence/phase9m/batch2/9s2b/result_9s2b.md` |
| K4 (item 4) | + loads behind the engine | 14,222.0 | 76.665 | 8,416 / 9,611 / 12,989 | 109.8 / 125.4 / 169.4 | `evidence/phase9m/batch2/9i4/result_9i4.md` |
Timing at 15.000 ns is met at 6 of 6 seeds for K1, K1b, K2, K3 and K4 (nine of nine for K3) and at 40.000 ns at 6 of 6 seeds for every configuration. K4 against MW at 15 ns (indicative, MW has two seeds): KeyGen -3.3 %, Encaps -9.5 %, Decaps -19.9 % latency. K4 against the Phase 9 core: ALM -3,398.5 (-19.3 %), cycles -7.5 % / -10.5 % / -22.1 % (the Phase 9 core was not measured at 15 ns, so its latency at 15 ns is not stated).
Fmax of the K4 seeds at 15 ns: 80.99, 74.97, 78.27, 75.67, 77.66, 69.43 MHz (spread 11.56 MHz); the seed noise is 3 MHz for the early configurations and larger for K3 and K4. S0 located the limit of the 9M-1 core between 13 and 14 ns (14 ns met at both seeds, 75.3-77.3 MHz; 13 ns met at 1 of 2 seeds), which is why 15 ns is the reporting limit.

## 4. Standards and sources pinned
FIPS 203 ML-KEM-768, ACVP sample vectors as pinned in `reference/kat_sources.md` (NIST sample sets; keyGen 25, encapsulation 25, decapsulation 10; the key-check groups run on the HPS by ADR 0031). Golden model: `tb/golden/` (independent of the RTL); hashlib for SHA-3 and SHAKE. No constant of FIPS 203 changed (check_params).

## 5. Coverage and limits
- Simulation, formal with protocol stubs, and static timing with virtual pins only: no board result, no HPS result, no speed claim against software. Latencies are cycles divided by the lowest slow-corner Fmax of a static timing run (perhitungan tim).
- Seed noise is 3 MHz (early) to 11 MHz (K4 spread); a gain below that is not called a gain. S2 (+0.27 MHz) and the K4 drop (-0.89 MHz against K3) are inside it. S2b (+3.43 MHz) is a median gain that its own rule did not accept as written.
- ACVP covers keyGen, encapsulation and decapsulation vectors (25, 25, 10); the interlock of item 4 is tested by ACVP and by one stall pattern (the throttled host port), not by all of them.
- Constant time means cycle-count invariance only (Encaps and Decaps identical across the tested inputs; KeyGen varies with the public rejection sampling of A, 8,344-8,397 cycles over the ACVP seeds). It is not side-channel resistance.
- The formal model uses protocol stubs for the engine, sampler and sponge; it proves control and range properties, not values.
- Stores are still in series with the engine and KeyGen is unchanged by item 4; the second sampler (item 5) was not built (estimated 1 to 4 % of the latency for about +3,500 ALM, ESTIMATE).

## 6. Deviations, failures and open issues
1. Formal timeouts (M-11). P1 of `mlkem_core4` (no STP or SDL while the engine is busy; bounded depth 160) and the negative control NC-E1-4 timed out at 1,800 s; a 4 h retry was stopped after about 2 h 40 min by decision of the team; NC-B7 of `mlkem_core3` (Batch 1) timed out too (3 h retries killed by restarts). P1 rests on simulation and on NC-JOIN4, which fails as required. P2 (`pend_q` equals 0 when idle) was dropped because it fails induction without a program-position invariant; it is not proven. `evidence/phase9m/batch2/9i4/formal.md`, `evidence/phase9m/batch1/9f1b/formal.md`.
2. S2b is not adopted by its rule as written (the gain of the median, +3.430 MHz, is smaller than the seed spread of K3, 6.35 MHz; seed 4 at 73.02 MHz is below the highest seed of K2). Three extra seeds were run on request after the result and are reported beside it (nine-seed median 77.320 MHz). K4 was measured on this base: if K3 is rejected, K4 must be remeasured on K2.
3. S2 neutral: +0.27 MHz, inside the spread; the rule adopts it, the evidence says neutral. Several estimates of the plans were missed and are recorded in the results (S2 cycles +12 / +14 / +22 against +6 / +7 / +11; S2 Fmax 74.1 against 76-80 MHz).
4. Item 4 process: its plan was written after the RTL and the first core simulation (the plan says so); the rule was written before any compile and before the controls. Two controls were first wrongly built (`ncthrld`, `ncgrant`), fixed and re-run (`evidence/phase9m/batch2/9i4/sim.md`).
5. The weakest K4 seed (69.43 MHz) is limited by a path of S2b (`cnt_q` through the host write enable and `start_go` to the registered address), not by item 4 (`evidence/phase9m/batch2/9i4/critical_paths_K4-15.md`).
6. Tooling incidents: an editor crash killed two parallel Quartus compiles and a formal run (none of their output is used; compiles run one at a time with at least 2 GB of RAM free); a status question was misread once and the compile queue was stopped and restored (`evidence/phase9m/batch2/9s2b/test_plan_9s2b.md` A1).
7. The Quartus outputs are archived outside the repository and are never committed.

## 7. Decisions needed
PENDING #34 (ADR 0035, two-byte codec), #35 (ADR 0037, K0 hash), #36 (ADR 0038, K1), #37 (ADR 0040, K1b), #38 (ADR 0041, K2), #39 (ADR 0042, K3: the rule says no, the median says +3.4 MHz), #40 (ADR 0043, K4: the rule says yes, on the base of K3). The chain is nested: K4 requires K3, K3 requires K2, K2 requires K1b; the team can stop at any link, but the later measurements then have to be repeated on the new base. See `docs/decisions/PENDING.md`.

## 8. Claims made in this phase
Every number above is labelled MEASURED (kernel-only static timing or simulation) or perhitungan tim (latency). No claim of hardware validation, of speed against software, of power, or of side-channel resistance. The only security statement is cycle-count invariance of Encaps and Decaps across the tested inputs. Nothing here is proposal text; claims for judges go through `/proposal-claims`.

## 9. Reproduce
```bash
. scripts/env.sh
python3 .claude/skills/mlkem-guard/scripts/check_params.py
# K4 core target on both simulators (about 2 minutes on Verilator, about 1 hour on Icarus):
CORE_TOP=mlkem_core4 CORE_SMP0=1 CORE_K0=1 CORE_W2=1 CORE_P6=1 CORE_AR=1 python3 tb/mlkem/run_core_tests.py verilator core
CORE_TOP=mlkem_core4 CORE_SMP0=1 CORE_K0=1 CORE_W2=1 CORE_P6=1 CORE_AR=1 python3 tb/mlkem/run_core_tests.py icarus core nclen
# controls of item 4 (Verilator):
CORE_TOP=mlkem_core4 CORE_SMP0=1 CORE_K0=1 CORE_W2=1 CORE_P6=1 CORE_AR=1 python3 tb/mlkem/run_core_tests.py verilator nclen ncoff ncrom ncprio ncwr ncjob ncthr ncilk ncthrld ncgrant ncjoin
python3 tb/s10/run_s10_tests.py verilator s10p6a ncar s10p6 s10      # NTT core at P = 6 with the registered address, and the defaults
python3 formal/run/run_formal_phase9i4.py proofs                         # item 4 formal (P1 and NC-E1-4 time out)
cd quartus/phase09i4_core && quartus_sh --flow compile phase09i4_core -c K4-15-s1   # one Quartus compile (about 12 min)
python3 scripts/quartus/select_9i4.py                                       # worksheet of K4 against K3
python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase9m.md
```

## 10. Approval
- [ ] Human approver (name, date): 
      Next phase starts only after a team member ticks this box. Claude never ticks it.
