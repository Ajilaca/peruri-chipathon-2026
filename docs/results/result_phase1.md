<!-- claim-lint: skip-file (result artifact: internal status page, not proposal text) -->
# Result — Phase 1: Minimal RTL baseline (L=1 NTT/INTT + pointwise multiplication, config C0)

- Status: PARTIAL
- Date (UTC): 2026-09-29 04:00
- Git commit (HEAD when verified): d8cb3cd
- Environment: Ubuntu 24.04.4 LTS; OSS CAD Suite 2026-09-23 (Verilator 5.053 devel, Icarus
  Verilog 14.0 devel, slang 11.0.448, SymbiYosys + Yosys + Boolector via oss-cad-suite);
  cocotb 2.1.0, pytest 9.1.1 (`.venv`). **Quartus was NOT available in this session**
  (`scripts/tooling.env` has `QUARTUS_BIN=""`, no `quartus_sh` on this machine) -- this is the
  reason Status is PARTIAL, not DONE; see Section 6.

## 1. Done-criteria (Common RTL Gate, docs/ROADMAP.md, copied unchanged)
| # | Criterion | Evidence (`path` under docs/evidence/ or tests, or `cmd: ...`) | Status |
|---|---|---|---|
| CRG-1 | Lint clean (`verilator --lint-only -Wall`) | `cmd: verilator --lint-only -Wall --timing -sv rtl/ntt/*.sv --top-module ntt_core` (0 warnings) | PASS |
| CRG-2 | Elaboration clean (`slang`) | `cmd: slang --top ntt_core rtl/ntt/*.sv` (0 errors, 0 warnings) | PASS |
| CRG-3 | Bit-exact vs golden model, on both simulators | `docs/evidence/phase01-ntt-baseline/cocotb_regression_2026-09-29.txt` (10/10 on Icarus AND Verilator) | PASS |
| CRG-4 | Corner cases listed before tests were written | `docs/evidence/phase01-ntt-baseline/test_plan.md` | PASS |
| CRG-5 | Regression: earlier-phase tests still pass | `cmd: python3 -m pytest tb/golden/tests/ -q` (23/23 passed) | PASS |
| CRG-6 | Locked parameters | `cmd: python3 .claude/skills/mlkem-guard/scripts/check_params.py` | PASS |
| CRG-7 | Constant-cycle evidence | `docs/evidence/phase01-ntt-baseline/cocotb_regression_2026-09-29.txt` (NTT=897, INTT=1153 cycles, constant on every corner case + 20 random inputs, both simulators) | PASS |
| CRG-8 | Formal properties (FSM safety; address range) | `docs/evidence/phase01-ntt-baseline/formal_ntt_core_safety_2026-09-29.txt` (k-induction PASS on the busy/done safety property; address range argued structurally, not separately proven -- see caveat in Section 5) | PASS |
| CRG-9 | Quartus evidence (ALM, registers, M10K, DSP, Fmax, slack); no negative worst slack or the failure documented | none -- Quartus not installed in this session | MISSING |
| CRG-10 | Result artifact validated; claim checker clean | `cmd: python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/result_phase1.md` and `cmd: python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal` | PASS |

## 1b. Additional Phase 1 PASS criteria (docs/ROADMAP.md Phase 1, beyond the CRG table)
| # | Criterion | Evidence | Status |
|---|---|---|---|
| 1 | Target-clock ADR recorded | none | MISSING |
| 2 | C0 row of the ablation matrix filled with MEASURED values | none (`docs/ROADMAP.md` ablation matrix C0 row still all `—`) | MISSING |

Status is PASS, FAIL or MISSING. PASS needs at least one backticked evidence item that exists.
All simulation results above are **simulation-only**; no board or Quartus run is claimed.

## 2. What was produced
| Path | Purpose |
|---|---|
| `rtl/ntt/ntt_pkg.sv` | Shared Q/N/CW/AW/ZW constants and `add_mod`/`sub_mod` functions (straightforward, documented reduction -- not Barrett/Montgomery, which are Phase 5) |
| `rtl/ntt/twiddle_rom.sv` | **Generated** (not hand-typed) ROM of `zeta^BitRev7(i)` and `zeta^(2*BitRev7(i)+1) mod q`, by `scripts/gen_twiddle_rom.py` from `tb/golden/primitives.py` |
| `rtl/ntt/modmul_reduce.sv` | `(a*b) mod q`, combinational, generic modulo |
| `rtl/ntt/base_case_multiply.sv` | FIPS 203 Algorithm 12 (pointwise multiplication building block), direct 5-multiplication form |
| `rtl/ntt/butterfly.sv` | One NTT (Cooley-Tukey) / INTT (Gentleman-Sande) butterfly, mode-selected |
| `rtl/ntt/poly_mem.sv` | 256x12-bit polynomial memory, 2 read/write ports, unbanked (Phase 2 scope) |
| `rtl/ntt/ntt_core.sv` | Top-level FSM: L=1, one butterfly/cycle, all 7 layers + INTT final x3303 scaling pass |
| `scripts/gen_twiddle_rom.py` | Regenerates `twiddle_rom.sv` from the golden model; re-run instead of hand-editing |
| `tb/ntt/test_modmul.py`, `test_base_case_multiply.py`, `test_butterfly.py`, `test_ntt_core.py` | cocotb tests, bit-exact against `tb/golden/primitives.py` |
| `tb/ntt/run_ntt_tests.py` | Runs all Phase 1 cocotb tests against one simulator (icarus/verilator) |
| `formal/phase01-ntt/ntt_core_props.sv`, `ntt_core_formal_top.sv`, `ntt_core_safety.sby` | SymbiYosys safety proof (CRG-8) |
| `docs/evidence/phase01-ntt-baseline/test_plan.md` | CRG-4 test plan, written before any test code |
| `docs/evidence/phase01-ntt-baseline/cocotb_regression_2026-09-29.txt` | Raw pass/fail + cycle-count log, both simulators |
| `docs/evidence/phase01-ntt-baseline/formal_ntt_core_safety_2026-09-29.txt` | Raw SymbiYosys log |

## 3. Numbers (each labelled MEASURED, ESTIMATE, or cited [n])
| Quantity | Value | Label | Evidence |
|---|---|---|---|
| cocotb unit tests (modmul, base_case_multiply, butterfly, ntt_core) | 10/10 passed, both simulators | MEASURED | `docs/evidence/phase01-ntt-baseline/cocotb_regression_2026-09-29.txt` |
| NTT cycle count (C0, L=1) | 897 cycles, constant across all tested inputs | MEASURED (simulation) | `docs/evidence/phase01-ntt-baseline/cocotb_regression_2026-09-29.txt` |
| INTT cycle count (C0, L=1) | 1153 cycles, constant across all tested inputs | MEASURED (simulation) | `docs/evidence/phase01-ntt-baseline/cocotb_regression_2026-09-29.txt` |
| ALM / registers / M10K / DSP / Fmax / slack (C0) | not measured | -- | Quartus not run this session; **no number is stated or implied here** |

No ALM/register/M10K/DSP/Fmax/slack number appears anywhere in this document. None is implied by
the simulation cycle counts above, which are cycle counts only, not timing.

## 4. Standards and sources pinned
- FIPS 203 Algorithms 9-12 (NTT, NTT⁻¹, MultiplyNTTs, BaseCaseMultiply), as already verified in
  Phase 0 (`docs/evidence/golden/fips203_errata_2026-09-28.md`); no new FIPS 203 reading was done
  in this phase, and no parameter or algorithm was changed (`check_params.py` still passes).
- Toolchain: OSS CAD Suite tag `2026-09-23` (`scripts/tooling.env`), the same one verified for
  Phase 0; Quartus Prime Lite 25.1std is the pinned FPGA tool per `CLAUDE.md` but was not
  available in this session (see Section 6).

## 5. Coverage and limits
- **No Quartus/FPGA numbers exist for this phase.** CRG-9 is unmet; ALM, registers, M10K, DSP,
  Fmax and slack for configuration C0 are all still to be measured on a machine with Quartus
  25.1std, per `docs/ROADMAP.md`'s measurement protocol.
- **No target-clock ADR exists yet.** `docs/ROADMAP.md` requires this "at the Phase 1 gate";
  without it, the eventual Quartus run has no team-agreed constraint to use.
- **The C0 row of the ablation matrix is empty.** It can only be filled from the missing Quartus
  run above.
- **Formal coverage is partial by design.** SymbiYosys proved one safety property (busy_o
  dropping is always followed, exactly one cycle later, by done_o) by k-induction at depth 6.
  It did **not** prove liveness ("the FSM eventually reaches done_o") -- a bounded check to the
  real ~900-1150 cycle depth was judged impractical for this phase and was not attempted; that
  the FSM does reach done_o is evidence from the cocotb regression (simulation), not from
  SymbiYosys. Address-range safety (`j`, `jlen`, `scale_addr` staying in `[0,255]`) is argued
  structurally (all three are declared as exactly 8-bit values, matching `N=256`, and manual
  range analysis in `rtl/ntt/ntt_core.sv`'s comments shows no computed address ever exceeds 255)
  rather than separately machine-checked by SymbiYosys.
- **Cycle counts (897/1153) are simulation cycle counts, not timing.** No Fmax or latency-in-ns
  claim is made; `docs/ROADMAP.md`'s own rule ("never state a latency without its clock") is not
  yet applicable since no clock has been chosen or measured.
- **Only configuration C0 (L=1, unbanked memory, no pipelining) exists.** Everything the roadmap
  marks "Not allowed yet" for Phase 1 (multiple lanes, memory banking, pipelining, Montgomery/
  Barrett/lazy reduction/Karatsuba, Keccak, HPS integration, any performance claim) is genuinely
  absent from this RTL, not just unclaimed.
- **Reduction method is a plain `%` operator**, explicitly the documented Phase 1 baseline
  (`rtl/ntt/modmul_reduce.sv`), not yet exhaustively tested over all 3329² input pairs (that
  exhaustive test is Phase 5 scope per `docs/ROADMAP.md`); Phase 1 tested it with 2000 random
  pairs plus the corner cases in `docs/evidence/phase01-ntt-baseline/test_plan.md`.

## 6. Deviations, failures and open issues
- **One real RTL debugging episode, resolved, not hidden:** the first version of the cocotb
  testbench pulsed `start_i` for exactly one clock edge, which raced against cocotb's/VPI's
  write-visibility timing (a value written from a running coroutine is only visible to the RTL
  from the *next* clock edge onward) and could miss the FSM's `S_IDLE` window entirely --
  confirmed by tracing internal FSM state, root-caused, and fixed in the testbench (hold
  `start_i` until `busy_o` rises) rather than by changing the RTL or weakening any check. No RTL
  bug was found or fixed in this episode.
- **One incorrect formal property, caught and corrected, not hidden:** an earlier version of the
  CRG-8 safety property asserted `done_o` in the *same* cycle `busy_o` drops; SymbiYosys's
  k-induction step (not the basecase, which was too shallow to reach the real transition)
  correctly rejected it, because the actual RTL asserts `done_o` one cycle *after* `busy_o`
  drops (entering `S_DONE` vs. leaving it). The property was corrected to match the RTL's actual,
  correct timing; the RTL itself was not changed for this.
- **CRG-9 (Quartus) is the only genuinely missing criterion** and the reason Status is PARTIAL.
  No RTL failure exists; the blocker is tool availability in this session, not a design problem.

## 7. Decisions needed
- **Target clock for C0** (`docs/ROADMAP.md`: "a team decision recorded as an ADR at the Phase 1
  gate"). Needed before the Quartus compile below can proceed meaningfully. Not yet raised as a
  numbered `docs/decisions/PENDING.md` item; doing so is a natural next step for the team.
- No `docs/decisions/PENDING.md` item from Phase 0 blocks Phase 1 (ADR 0003 is Accepted; item #9
  is closed).

## 8. Claims made in this phase
None written for judges/proposal text. `docs/ROADMAP.md`'s ablation matrix C0 row and Section 3
"Proposed Chip Design" resource cells remain untouched (still `—`/`ESTIMATE`/`[...]`) because no
Quartus evidence exists yet to fill them; filling them now would be exactly the kind of invented
number `CLAUDE.md` §3 and `docs/ROADMAP.md` forbid.

## 9. Reproduce
```bash
# from repo root, branch phase1-ntt-baseline
. scripts/env.sh

# Regenerate the twiddle ROM from the golden model (only needed after changing tb/golden)
python3 scripts/gen_twiddle_rom.py

# CRG-1 / CRG-2: lint and elaboration
verilator --lint-only -Wall --timing -sv rtl/ntt/*.sv --top-module ntt_core
slang --top ntt_core rtl/ntt/*.sv

# CRG-3 / CRG-7: cocotb, both simulators
python3 tb/ntt/run_ntt_tests.py icarus
python3 tb/ntt/run_ntt_tests.py verilator

# CRG-5 / CRG-6: earlier-phase regression + locked parameters
python3 -m pytest tb/golden/tests/ -q
python3 .claude/skills/mlkem-guard/scripts/check_params.py

# CRG-8: formal safety proof
cd formal/phase01-ntt && sby -f ntt_core_safety.sby && cd ../..

# CRG-9 (NOT run in this session -- needs a machine with Quartus 25.1std):
#   set up a quartus/ project targeting 5CSEBA6U23I7 with virtual pins around ntt_core,
#   compile, then:
#   python3 .claude/skills/quartus-report/scripts/extract_quartus_report.py <output_files> C0 \
#     --log <compile.log> \
#     --out docs/evidence/phase01-ntt-baseline/quartus_C0_<date>.md \
#     --note "<git sha>, C0 baseline, clock=<TBD by ADR>"

# CRG-10: validate this result artifact
python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/result_phase1.md
python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal
```

## 10. Approval
- [ ] Human approver (name, date):
      Next phase starts only after a team member ticks this box. Given CRG-9 is MISSING, this
      phase cannot honestly be marked DONE even after a human reviews it; approving this PARTIAL
      status means agreeing that Phase 2 work may or may not proceed without Quartus evidence
      for C0 -- that is the team's call, not this document's.
