<!-- claim-lint: skip-file (result artifact: internal status page, not proposal text) -->
# Result — Phase 1: Minimal RTL baseline (L=1 NTT/INTT + pointwise multiplication, config C0)

- Status: PARTIAL
- Date (UTC): 2026-09-29 10:10
- Git commit (HEAD when verified): 10bb3f8 (RTL unchanged since d8cb3cd; Quartus compile of that RTL, evidence added in 42b9059/10bb3f8)
- Environment: Ubuntu 24.04.4 LTS; OSS CAD Suite 2026-09-23 (Verilator 5.053 devel, Icarus
  Verilog 14.0 devel, slang 11.0.448, SymbiYosys + Yosys + Boolector); cocotb 2.1.0, pytest 9.1.1
  (`.venv`); **Quartus Prime Lite 25.1std.0 Build 1129** (`~/altera_lite/25.1std`, compile run by
  the team on 2026-09-29, drill-down `quartus_sta` run read-only afterwards).
  *Note:* `scripts/tooling.env` still has `QUARTUS_BIN=""`; Quartus was called by full path.

## 1. Done-criteria (Common RTL Gate, docs/ROADMAP.md, copied unchanged)
| # | Criterion | Evidence (`path` under evidence/ or tests, or `cmd: ...`) | Status |
|---|---|---|---|
| CRG-1 | Lint clean (`verilator --lint-only -Wall`) | `cmd: verilator --lint-only -Wall --timing -sv rtl/ntt/*.sv --top-module ntt_core` (0 warnings) | PASS |
| CRG-2 | Elaboration clean (`slang`) | `cmd: slang --top ntt_core rtl/ntt/*.sv` (0 errors, 0 warnings) | PASS |
| CRG-3 | Bit-exact vs golden model, on both simulators | `evidence/phase01/cocotb_regression.txt` (10/10 on Icarus AND Verilator) | PASS |
| CRG-4 | Corner cases listed before tests were written | `evidence/phase01/test_plan.md` | PASS |
| CRG-5 | Regression: earlier-phase tests still pass | `cmd: python3 -m pytest tb/golden/tests/ -q` (23/23 passed) | PASS |
| CRG-6 | Locked parameters | `cmd: python3 .claude/skills/mlkem-guard/scripts/check_params.py` | PASS |
| CRG-7 | Constant-cycle evidence | `evidence/phase01/cocotb_regression.txt` (NTT=897, INTT=1153 cycles, constant on every corner case + 20 random inputs, both simulators) | PASS |
| CRG-8 | Formal properties (FSM safety; address range) | `evidence/phase01/formal_ntt_core_safety.txt` (k-induction PASS on the busy/done safety property; address range argued structurally -- see Section 5) | PASS |
| CRG-9 | Quartus evidence (ALM, registers, M10K, DSP, Fmax, slack); no negative worst slack or the failure documented | `evidence/quartus/C0.md` and `evidence/phase01/quartus_C0_timing_analysis.md` -- evidence exists and the failure is documented, but worst setup slack is **-48.323 ns** at the provisional 20.000 ns clock (timing NOT met, all 4 corners) | FAIL |
| CRG-10 | Result artifact validated; claim checker clean | `cmd: python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase01.md` and `cmd: python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal` | PASS |

CRG-9 is marked FAIL, not PASS, although the roadmap wording ("or the failure documented") could
be read as allowing PASS once the failure is written down. Choosing that reading is a team
decision; this document does not make it (Section 7).

## 1b. Additional Phase 1 PASS criteria (docs/ROADMAP.md Phase 1, beyond the CRG table)
| # | Criterion | Evidence | Status |
|---|---|---|---|
| 1 | Target-clock ADR recorded | none (20.000 ns in `quartus/phase01_ntt_c0/C0.sdc` is provisional) | MISSING |
| 2 | C0 row of the ablation matrix filled with MEASURED values | `evidence/phase01/quartus_C0_timing_analysis.md` (row filled in `docs/ROADMAP.md`; latency and AT deliberately not stated because timing is not met at the constrained clock) | PASS |

Status is PASS, FAIL or MISSING. PASS needs at least one backticked evidence item that exists.
Simulation results are **simulation-only**; Quartus results are post-fit static timing, **not**
hardware validation (no board).

## 2. What was produced
| Path | Purpose |
|---|---|
| `rtl/ntt/ntt_pkg.sv` | Shared Q/N/CW/AW/ZW constants and `add_mod`/`sub_mod` functions |
| `rtl/ntt/twiddle_rom.sv` | **Generated** ROM (`scripts/build/gen_twiddle_rom.py` from `tb/golden/primitives.py`) |
| `rtl/ntt/modmul_reduce.sv` | `(a*b) mod q`, combinational, generic `%` |
| `rtl/ntt/base_case_multiply.sv` | FIPS 203 Algorithm 12, direct 5-multiplication form |
| `rtl/ntt/butterfly.sv` | NTT (Cooley-Tukey) / INTT (Gentleman-Sande) butterfly, mode-selected |
| `rtl/ntt/poly_mem.sv` | 256x12-bit polynomial memory, 2 async-read/sync-write ports, unbanked |
| `rtl/ntt/ntt_core.sv` | Top-level FSM: L=1, one butterfly/cycle, 7 layers + INTT x3303 pass |
| `scripts/build/gen_twiddle_rom.py` | Regenerates `twiddle_rom.sv` from the golden model |
| `tb/ntt/*.py` | cocotb tests + runner, bit-exact against `tb/golden/primitives.py` |
| `formal/phase01-ntt/*` | SymbiYosys safety proof (CRG-8) |
| `quartus/phase01_ntt_c0/phase01_ntt_c0.qpf`, `C0.qsf`, `C0.sdc` | Quartus project for revision C0 (virtual pins, provisional 20.000 ns clock) |
| `quartus/phase01_ntt_c0/report_critical_paths.tcl` | Read-only `quartus_sta` drill-down on the existing post-fit netlist |
| `quartus/phase01_ntt_c0/segment_path.py`, `extract_c0_timing_evidence.py` | Turn the Quartus path reports into the evidence file (no hand-typed numbers) |
| `evidence/quartus/C0.md` | Fitter/STA summary extract (`extract_quartus_report.py`) |
| `evidence/phase01/quartus_C0_timing_analysis.md` (+ `.json`) | Stage status, resources, all corners, worst path, per-structure delay attribution, endpoint classification, clock-method evidence |
| `evidence/phase01/test_plan.md`, `cocotb_regression.txt`, `formal_ntt_core_safety.txt` | Earlier Phase 1 evidence |

## 3. Numbers (each labelled MEASURED, ESTIMATE, or cited [n])
| Quantity | Value | Label | Evidence |
|---|---|---|---|
| cocotb tests | 10/10 passed, both simulators | MEASURED (simulation) | `evidence/phase01/cocotb_regression.txt` |
| NTT / INTT cycle count (C0) | 897 / 1153, constant across all tested inputs | MEASURED (simulation) | `evidence/phase01/cocotb_regression.txt` |
| Logic utilization | 7,010 / 41,910 ALMs (17 %) | MEASURED | `evidence/quartus/C0.md` |
| Registers | 3104 | MEASURED | `evidence/quartus/C0.md` |
| RAM blocks (M10K) / block memory bits | 0 / 553; 0 / 5,662,720 | MEASURED | `evidence/quartus/C0.md` |
| DSP blocks | 3 / 112 (three "Two Independent 18x18", unsigned, unregistered) | MEASURED | `evidence/phase01/quartus_C0_timing_analysis.md` |
| Fmax (clk_i) | 14.64 MHz (Slow 1100mV 100C); 14.69 MHz (Slow 1100mV -40C) | MEASURED | `evidence/quartus/C0.md` |
| Worst setup slack / TNS @ 20.000 ns | -48.323 ns / -143688.194 ns (Slow 1100mV 100C) | MEASURED | `evidence/quartus/C0.md` |
| Worst hold slack | 0.211 ns (Fast 1100mV -40C) -- met | MEASURED | `evidence/quartus/C0.md` |
| Worst path | `layer_q[2]` -> `poly_mem:u_mem|mem[64][5]`, data delay 67.684 ns, 146 `lpm_divide` cells on it | MEASURED | `evidence/phase01/quartus_C0_timing_analysis.md` |
| Modulo divider share of worst data path | 38.926 ns (57.5 %) | derived from MEASURED path report (`segment_path.py`) | `evidence/phase01/quartus_C0_timing_analysis.md` |
| Latency / AT | not stated -- timing not met at the constrained clock (`docs/ROADMAP.md`: latency only at a clock that met timing) | -- | -- |

## 4. Standards and sources pinned
- FIPS 203 Algorithms 9-12, as verified in Phase 0 (`evidence/phase00/fips203_errata.md`);
  no parameter or algorithm changed (`check_params.py` passes).
- OSS CAD Suite tag `2026-09-23`; Quartus Prime Lite 25.1std.0 Build 1129 (from the report headers).
- Timing constraint: `create_clock -period 20.000 [get_ports {clk_i}]`, `derive_clock_uncertainty`,
  `set_false_path -from [get_ports {rst_ni}]` -- **provisional**, not a team decision.

## 5. Coverage and limits
- **Timing is not met.** Every one of the 3072 `poly_mem` storage registers has a failing path
  (slack between -50 and -40 ns), plus 2 `layer_q` paths; all 3074 failing endpoints are reached
  from `layer_q`. Details and the structural attribution are in the timing-analysis evidence file.
- **The ~14.6 MHz Fmax is a measurement of the unoptimised baseline, not a target.** The SDC was
  not loosened and no RTL was changed after the compile.
- **Clock methodology caveat:** `clk_i` is a virtual pin, so Quartus raises Critical Warning
  15725 ("ripple clock"); the clock enters the global network (`CLKCTRL_G3`, fan-out 3104) from a
  logic cell. On the worst path the clock terms are skew -0.579 ns and uncertainty 0.060 ns versus
  a 67.684 ns data delay, so they do not change the conclusion; absolute clock insertion delays
  are not representative of a real board clock pin.
- **I/O paths are not analysed:** 23 input and 14 output ports have no `set_input_delay` /
  `set_output_delay` (kernel-only compile). All failing paths are register-to-register.
- **Formal coverage is partial by design** (safety property only; liveness from simulation;
  address range argued structurally).
- **Reduction method is a plain `%`**, tested with 2000 random pairs plus corners; the exhaustive
  3329² sweep is Phase 5 scope.
- **Only C0 exists** (L=1, unbanked memory, no pipelining); everything "Not allowed yet" in the
  roadmap for Phase 1 is genuinely absent.

## 6. Deviations, failures and open issues
- **CRG-9 FAIL: setup timing not met at 20.000 ns (-48.323 ns worst slack).** Root-cause evidence
  from the reports (not a guess): on the worst path the combinational 24-bit/12-bit `lpm_divide`
  inferred from `%` in `rtl/ntt/modmul_reduce.sv` accounts for 38.926 ns (57.5 %) of the
  67.684 ns data delay; the rest of the same single-cycle read-compute-write path (FSM/address
  arithmetic 9.952 ns, register-based memory read mux 5.504 ns, DSP multiply 3.780 ns, add/sub
  mod 3.060 ns, write mux into the storage register 6.462 ns) totals 28.758 ns, which by itself
  also exceeds the 20.000 ns period. The INTT (`u_inv_mul`) and scaling (`u_scale_mul`) paths show
  the same pattern (-47.787 ns and -46.444 ns). A control-only path (`layer_q[1]` -> `layer_q[2]`,
  -3.829 ns) is 92.7 % interconnect, including one 11.986 ns hop from row Y37 to row Y4.
- **Not done here, on purpose:** no RTL change, no SDC change, no lower clock. The critical path is
  now identified and documented; any fix is a separate, reviewed step (roadmap Phases 4/5 cover
  pipelining and arithmetic; Phase 2 covers memory).
- Earlier (resolved) episodes: testbench start-pulse race fixed in the testbench; an incorrect
  formal property caught by k-induction and corrected. Neither changed the RTL.

## 7. Decisions needed
- **Target clock for C0** (ADR required at the Phase 1 gate). The measured baseline cannot run at
  the provisional 50 MHz; the team decides what clock to commit to and whether any Phase 1 RTL
  change is in scope before C0 is frozen, or whether C0 stays the documented (failing) baseline
  and fixes happen in the phases the roadmap assigns them to.
- **How to read CRG-9** ("or the failure documented"): PASS-with-documented-failure or FAIL.
- Whether to set `QUARTUS_BIN` in `scripts/tooling.env` so `scripts/env.sh` finds Quartus.

## 8. Claims made in this phase
None written for judges/proposal text. Only `docs/ROADMAP.md` (status line and ablation matrix C0
row) was updated, from the evidence files above.

## 9. Reproduce
```bash
# from repo root, branch phase1-ntt-baseline
. scripts/env.sh
verilator --lint-only -Wall --timing -sv rtl/ntt/*.sv --top-module ntt_core
slang --top ntt_core rtl/ntt/*.sv
python3 tb/ntt/run_ntt_tests.py icarus
python3 tb/ntt/run_ntt_tests.py verilator
python3 -m pytest tb/golden/tests/ -q
python3 .claude/skills/mlkem-guard/scripts/check_params.py
(cd formal/phase01-ntt && sby -f ntt_core_safety.sby)

# Quartus (paths for this machine)
export PATH=$HOME/altera_lite/25.1std/quartus/bin:$PATH
(cd quartus/phase01_ntt_c0 && quartus_sh --flow compile phase01_ntt_c0 -c C0)
python3 .claude/skills/quartus-report/scripts/extract_quartus_report.py \
    quartus/phase01_ntt_c0/output_files C0 --log quartus/phase01_ntt_c0/output_files/C0.flow.rpt
(cd quartus/phase01_ntt_c0 && quartus_sta -t report_critical_paths.tcl \
    && python3 extract_c0_timing_evidence.py)

python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase01.md
python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal
```

## 10. Approval
- [x] Human approver (name, date): Faza Dzil, 2026-09-29
      Next phase starts only after a team member ticks this box. With CRG-9 FAIL and the
      target-clock ADR missing, this phase is PARTIAL; approving it means the team accepts C0 as a
      documented failing baseline and decides how to proceed (Section 7).
