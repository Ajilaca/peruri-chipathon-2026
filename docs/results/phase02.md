<!-- claim-lint: skip-file (result artifact: internal status page, not proposal text) -->
# Result — Phase 2: Memory architecture (M10K storage, banking, address generation, config C1)

- Status: PARTIAL
- Date (UTC): 2026-09-29 11:07
- Git commit (HEAD when verified): 4e26498
- Environment: same as Phase 1 (`docs/results/phase01.md`) -- Ubuntu 24.04.4 LTS, OSS CAD
  Suite 2026-09-23, cocotb 2.1.0, pytest 9.1.1, Quartus Prime Lite 25.1std.0 Build 1129
  (`~/altera_lite/25.1std`).

**Process note, stated plainly:** `docs/ROADMAP.md`'s own gate rule is "a phase starts only after
the previous phase's result artifact passes `check_result.py` **and** a team member has ticked
its Approval box." Phase 1's Approval box is still unticked (`docs/results/phase01.md`
Section 10) and its CRG-9 is FAIL. This phase was started anyway, on an explicit team instruction
("lanjut fase 2") to continue in the same session, not because the gate was met. Recorded here
so nobody reading only this file assumes Phase 1 was approved.

## 1. Done-criteria (Common RTL Gate, docs/ROADMAP.md, copied unchanged)
| # | Criterion | Evidence | Status |
|---|---|---|---|
| CRG-1 | Lint clean | `cmd: verilator --lint-only -Wall --timing -sv rtl/ntt/*.sv rtl/mem/*.sv --top-module ntt_core_c1` (0 warnings); also checked standalone for the bank-map ROM and banked-memory modules at NUM_BANKS∈{1,2,4,8} | PASS |
| CRG-2 | Elaboration clean (slang) | `cmd: slang --top ntt_core_c1 rtl/ntt/*.sv rtl/mem/*.sv` (0 errors, 0 warnings) | PASS |
| CRG-3 | Bit-exact vs golden, both simulators | `evidence/phase02/cocotb_regression.txt` (12/12 on Icarus AND Verilator: bank_map_rom x4 L values + ntt_core_c1) | PASS |
| CRG-4 | Corner cases before tests | `evidence/phase02/test_plan.md` | PASS |
| CRG-5 | Regression: Phase 0 + Phase 1 tests still pass | `cmd: python3 -m pytest tb/golden/tests/ -q` (23/23) and `cmd: python3 tb/ntt/run_ntt_tests.py icarus` (10/10, C0 unaffected) | PASS |
| CRG-6 | Locked parameters | `cmd: python3 .claude/skills/mlkem-guard/scripts/check_params.py` | PASS |
| CRG-7 | Constant-cycle evidence | `evidence/phase02/cocotb_regression.txt` (NTT=897, INTT=1153, **equal to C0**, i.e. 0 stall cycles) | PASS |
| CRG-8 | Formal properties | `evidence/phase02/formal_bank_map.txt` (own-pair property, L=8, BMC depth 1, PASS) and `evidence/phase02/formal_ntt_core_c1_safety.txt` (FSM safety, k-induction depth 6, PASS) | PASS |
| CRG-9 | Quartus evidence; no negative slack or the failure documented | `evidence/quartus/C1.md`, `evidence/phase02/quartus_C1_vs_C0.md` -- evidence exists, failure documented, but worst setup slack is **-46.720 ns** at 20.000 ns (timing NOT met, same as C0) | FAIL |
| CRG-10 | Result artifact + claim checker | `cmd: python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase02.md` and `cmd: python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal` | PASS |

CRG-9 marked FAIL for the same reason as Phase 1's (`docs/results/phase01.md`): the roadmap
wording could be read as PASS-with-documented-failure; that reading is a team decision, not made
here.

## 1b. Phase 2 PASS criteria (docs/ROADMAP.md Phase 2, beyond the CRG table)
| # | Criterion | Evidence | Status |
|---|---|---|---|
| 1 | Conflict-freedom proven for all four L values (1,2,4,8) | `evidence/phase02/bank_scheme_exploration.txt` (exhaustive Python: own-pair, balance, bijectivity, multi-lane <=2/bank/cycle) + `evidence/phase02/formal_bank_map.txt` (formal, on the actual ROM) | PASS |
| 2 | Measured stall cycles = 0 at L = 1 | `evidence/phase02/cocotb_regression.txt` (C1 cycles == C0 cycles exactly, both directions) | PASS |
| 3 | Bit-exact | same cocotb log | PASS |
| 4 | Constant cycle count | same cocotb log | PASS |
| 5 | C1 row of the ablation matrix filled | `docs/ROADMAP.md` ablation matrix, row C1 | PASS |

All five of this phase's own stated PASS criteria are met. Status is still PARTIAL overall
because of CRG-9 (timing) and because Phase 1's own gate was not satisfied when this phase
started (see the process note above).

## 2. What was produced
| Path | Purpose |
|---|---|
| `tb/mem/bank_model.py` | Golden model: XOR-group bank scheme, offset assignment, lane grouping, and the exact address-generation arithmetic factored out of `rtl/ntt/ntt_core.sv` |
| `scripts/build/gen_bank_map.py` | Runs the exhaustive conflict-freedom proof; **generates** `rtl/mem/bank_map_rom.sv` from the golden model (never hand-typed) |
| `rtl/mem/bank_map_rom.sv` | Generated ROM: `addr -> (bank, offset)` for NUM_BANKS ∈ {1,2,4,8} |
| `rtl/mem/poly_mem_banked.sv` | Banked polynomial memory (generic NUM_BANKS; only NUM_BANKS=1 exercised/tested this phase) |
| `rtl/mem/ntt_core_c1.sv` | Configuration C1: C0's FSM/butterfly/twiddle-ROM unchanged, memory swapped for the banked version at NUM_BANKS=1 |
| `tb/mem/test_bank_map.py` | cocotb, exhaustive (256/256 addresses) vs `tb/mem/bank_model.py`, all 4 L values |
| `tb/mem/test_ntt_core_c1.py` | cocotb regression: bit-exact + cycle-exact (== C0) vs `tb/golden/primitives.py` |
| `tb/mem/run_mem_tests.py` | Runs all Phase 2 cocotb tests against one simulator |
| `formal/phase02-mem/bank_map_props.sv`, `bank_map_safety.sby` | Formal own-pair proof on the actual ROM (L=8) |
| `formal/phase02-mem/ntt_core_c1_formal_top.sv`, `ntt_core_c1_safety.sby` | Formal FSM-safety re-proof on `ntt_core_c1` |
| `quartus/phase02_mem_c1/` | Quartus project for C1 (same virtual-pin methodology and provisional clock as C0) |
| `evidence/phase02/test_plan.md` | CRG-4 test plan, written before any test code |
| `evidence/phase02/bank_map_spec.md` | Bank-mapping scheme specification and rationale |
| `evidence/phase02/bank_scheme_exploration.txt` | Raw exhaustive-proof log |
| `evidence/phase02/formal_bank_map.txt`, `formal_ntt_core_c1_safety.txt` | Raw SymbiYosys logs |
| `evidence/phase02/cocotb_regression.txt` | Raw cocotb pass/fail + cycle-count log, both simulators |
| `evidence/quartus/C1.md` | Standard fitter/STA summary extract |
| `evidence/phase02/quartus_C1_vs_C0.md` | C1 vs C0 comparison, worst-path re-check, honest M10K finding |

## 3. Numbers (each labelled MEASURED, ESTIMATE, or cited [n])
| Quantity | C0 | C1 | Evidence |
|---|---|---|---|
| ALM | 7,010 / 41,910 | 6,749 / 41,910 | MEASURED, `evidence/phase02/quartus_C1_vs_C0.md` |
| Registers | 3,104 | 3,105 | MEASURED, same |
| RAM Blocks (M10K) | 0 / 553 | 0 / 553 | MEASURED, same (M10K goal not achieved -- Section 5) |
| DSP | 3 / 112 | 3 / 112 | MEASURED, same |
| Fmax (Slow 100C) | 14.64 MHz | 14.99 MHz | MEASURED, same |
| Worst setup slack @ 20.000 ns | -48.323 ns | -46.720 ns | MEASURED, same |
| NTT / INTT cycles (simulation) | 897 / 1153 | 897 / 1153 (identical) | MEASURED (simulation), `evidence/phase02/cocotb_regression.txt` |
| Bank-map conflict-freedom, all L∈{1,2,4,8} | n/a | 0 collisions (exhaustive + formal) | MEASURED, `evidence/phase02/bank_scheme_exploration.txt` |

## 4. Standards and sources pinned
No new FIPS 203 reading this phase; no parameter or algorithm touched (`check_params.py` still
passes). Toolchain identical to Phase 1 (OSS CAD Suite `2026-09-23`, Quartus 25.1std.0 Build 1129).

## 5. Coverage and limits
- **M10K was NOT used, despite the phase's own title ("M10K polynomial storage").** Measured 0/553
  RAM blocks, identical to C0. Root cause (from the Quartus log, not a guess): both `poly_mem.sv`
  and `poly_mem_banked.sv` use asynchronous (combinational) reads, and Quartus's RAM inference
  requires a synchronous read to map to M10K. This is a genuine, honestly-reported gap relative
  to the phase's stated goal, not something the roadmap's own PASS criteria happen to require
  fixing this phase -- see `evidence/phase02/quartus_C1_vs_C0.md` Section 4
  for the full explanation and why it was not silently patched.
- **Only NUM_BANKS=1 is built into a tested, measured datapath.** `rtl/mem/poly_mem_banked.sv`
  compiles (lint-clean) for NUM_BANKS∈{2,4,8}, and `rtl/mem/bank_map_rom.sv`'s address function is
  exhaustively proven conflict-free for all four L values -- but the multi-bank read/write
  crossbar for L>1 has no cocotb test and was not measured by Quartus this phase. Building and
  measuring the actual L-lane datapath is Phase 3 scope.
- **Timing is still not met** (same root cause as C0, `modmul_reduce.sv`'s inferred divider,
  untouched this phase) -- the ~1.6 ns slack improvement is attributed to routing/placement
  differences around the swapped memory, not to any timing fix.
- **Phase 1's own gate (Approval ticked) was not met when this phase started** -- see the process
  note at the top of this file.
- **Target-clock ADR still does not exist** (inherited from Phase 1, still open).
- Reduction method, formal liveness scope, and address-range argument: same caveats as Phase 1
  (`docs/results/phase01.md` Section 5), unchanged this phase.

## 6. Deviations, failures and open issues
- No RTL bug was found or fixed this phase. The two "generate a ROM function with output
  arguments" attempts that failed under Icarus Verilog (SV `function` with `output` ports is not
  accepted by Icarus) and the "`module X import pkg::*; #(...)`" header syntax that Yosys's
  `read -formal` rejected (same issue Phase 1 hit and fixed the same way) were both caught by
  lint/formal runs immediately and fixed in the generator/RTL before any test was declared
  passing -- not discovered later.
- **Tooling mistake, disclosed:** during the Quartus C1 compile, the working directory
  (`db/`, `incremental_db/`) was accidentally deleted while `quartus_fit` was still running,
  corrupting that compile (`Fitter Status: Failed`). The directory was cleaned and the compile
  re-run from scratch; the MEASURED numbers in this document are from the clean re-run. No
  corrupted output was used as evidence anywhere.
- **CRG-9 (Quartus) is FAIL** for the same substantive reason as Phase 1 (timing not met at the
  provisional clock); this is expected, not a surprise, since Phase 2 did not touch arithmetic.

## 7. Decisions needed
- Everything already open from Phase 1 (`docs/results/phase01.md` Section 7): target-clock
  ADR, how to read CRG-9, `QUARTUS_BIN` in `scripts/tooling.env`.
- **New**: whether to pursue synchronous-read M10K mapping (a scheduling change) in a later
  phase, given it was not required by Phase 2's own PASS criteria but was the phase's stated
  goal.
- **New**: whether starting Phase 2 before Phase 1's Approval box was ticked is acceptable
  process for this team, or whether Phase 1 needs to be formally approved (or explicitly
  superseded) before Phase 3 starts.

## 8. Claims made in this phase
None written for judges/proposal text. `docs/ROADMAP.md`'s C1 ablation row was filled from the
evidence above; no proposal number was invented.

## 9. Reproduce
```bash
# from repo root, branch phase2-memory-banking
. scripts/env.sh

python3 scripts/build/gen_bank_map.py   # exhaustive proof + regenerates rtl/mem/bank_map_rom.sv

verilator --lint-only -Wall --timing -sv rtl/ntt/*.sv rtl/mem/*.sv --top-module ntt_core_c1
slang --top ntt_core_c1 rtl/ntt/*.sv rtl/mem/*.sv

python3 tb/mem/run_mem_tests.py icarus
python3 tb/mem/run_mem_tests.py verilator
python3 tb/ntt/run_ntt_tests.py icarus   # Phase 1 regression, unaffected
python3 -m pytest tb/golden/tests/ -q
python3 .claude/skills/mlkem-guard/scripts/check_params.py

(cd formal/phase02-mem && sby -f bank_map_safety.sby)
(cd formal/phase02-mem && sby -f ntt_core_c1_safety.sby)

# Quartus (paths for this machine)
export PATH=$HOME/altera_lite/25.1std/quartus/bin:$PATH
(cd quartus/phase02_mem_c1 && quartus_sh --flow compile phase02_mem_c1 -c C1)
python3 .claude/skills/quartus-report/scripts/extract_quartus_report.py \
    quartus/phase02_mem_c1/output_files C1 --log quartus/phase02_mem_c1/output_files/C1.flow.rpt

python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase02.md
python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal
```

## 10. Approval
- [x] Human approver (name, date): Faza Dzil, 2026-09-29
      Next phase starts only after a team member ticks this box. Given CRG-9 is FAIL, approving
      this PARTIAL status means the team explicitly accepts the process deviation noted at the
      top of this file (Phase 2 started before Phase 1's own box was ticked), not just this
      phase's own numbers. Phase 1's box was ticked the same day, after the fact.
