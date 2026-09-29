<!-- claim-lint: skip-file (result artifact: internal status page, not proposal text) -->
# Result — Phase 3: Multi-lane exploration (L = 1/2/4/8, config C2)

- Status: PARTIAL
- Date (UTC): 2026-09-29 15:56
- Git commit (HEAD when verified): 7b1d467
- Environment: same as Phase 1/2 -- Ubuntu 24.04.4 LTS, OSS CAD Suite 2026-09-23, cocotb 2.1.0,
  pytest 9.1.1, Quartus Prime Lite 25.1std.0 Build 1129 (`~/altera_lite/25.1std`).

**Process note, stated plainly:** `scripts/tooling.env`'s `QUARTUS_BIN` was empty at the start of
this phase (Quartus was previously located manually, per Phase 1/2's own open item); it was found
at `~/altera_lite/25.1std/quartus/bin` and filled in this phase so `scripts/env.sh` puts Quartus on
PATH going forward. This is a local machine-config fix, not a design change.

## 1. Done-criteria (Common RTL Gate, docs/ROADMAP.md, copied unchanged)
| # | Criterion | Evidence | Status |
|---|---|---|---|
| CRG-1 | Lint clean | `cmd: verilator --lint-only -Wall --timing -sv rtl/ntt/*.sv rtl/mem/*.sv --top-module ntt_core_c2 -GNUM_LANES=<L>` for L in {1,2,4,8} (0 warnings each) | PASS |
| CRG-2 | Elaboration clean (slang) | `cmd: slang --top ntt_core_c2 rtl/ntt/*.sv rtl/mem/*.sv` (0 errors, 0 warnings; default NUM_LANES=1 elaboration) | PASS |
| CRG-3 | Bit-exact vs golden, both simulators | `docs/evidence/phase03-multilane/cocotb_regression_2026-09-29.txt` (16/16 on Icarus AND Verilator, all four L) | PASS |
| CRG-4 | Corner cases before tests | `docs/evidence/phase03-multilane/test_plan.md`, written before `rtl/ntt/ntt_core_c2.sv` | PASS |
| CRG-5 | Regression: Phase 0-2 tests still pass | `cmd: python3 -m pytest tb/golden/tests/ -q` (23/23), `cmd: python3 tb/ntt/run_ntt_tests.py icarus` (10/10, C0 unaffected), `cmd: python3 tb/mem/run_mem_tests.py icarus` (12/12, C1 unaffected) | PASS |
| CRG-6 | Locked parameters | `cmd: python3 .claude/skills/mlkem-guard/scripts/check_params.py` | PASS |
| CRG-7 | Constant-cycle evidence | `docs/evidence/phase03-multilane/cocotb_regression_2026-09-29.txt` -- constant per L, and L=1 equals C0/C1 exactly (897/1153); L>1 is **lower**, not equal, which is the expected/measured effect of parallel lanes, not a stall | PASS |
| CRG-8 | Formal properties | `docs/evidence/phase03-multilane/formal_verification_2026-09-29.txt` -- **L=1 PASS** (full k-induction, both the reused busy/done property and bank_overflow_o==0); **L=2/4/8 do not close**: a SymbiYosys induction counterexample investigated in detail and cross-checked against the Python model, the RTL source text, and both simulators' cocotb regressions -- none reproduce it, so it is reported as a probable Yosys `-formal` reader artifact on the 256-entry bank ROM (Section 6), but the criterion's own status is FAIL until that is actually resolved, not softened to a passing grade | FAIL |
| CRG-9 | Quartus evidence; no negative slack or the failure documented | `docs/evidence/quartus/C2-L1-20260929.md`, `C2-L2-20260929.md`, `C2-L4-20260929.md`, `C2-L8-20260929.md` -- all four compiled and measured; all four have negative worst setup slack (timing NOT met); **L=8 additionally exceeds ADR 0004's 10,478 ALM budget** (11,446 ALM measured) | FAIL |
| CRG-10 | Result artifact + claim checker | `cmd: python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/result_phase3.md` and `cmd: python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal` | PASS |

CRG-9 marked FAIL for the same reason as Phase 1/2's: timing not met at the provisional 20.000 ns
clock is expected (no target-clock ADR exists yet) and is documented, not hidden, but the roadmap
wording is read strictly here; whether "documented failure" should count as PASS is a team call,
not made here. CRG-8 marked FAIL for the same discipline: one of the four L values (L=1) is fully
proven by k-induction, but three are not, and an unresolved gap is FAIL even when it is
investigated and has a documented, plausible explanation (Section 6) -- that explanation is not
grounds for marking it PASS.

## 1b. Phase 3 PASS criteria (docs/ROADMAP.md Phase 3, beyond the CRG table)
| # | Criterion | Evidence | Status |
|---|---|---|---|
| 1 | All four configurations correct | `docs/evidence/phase03-multilane/cocotb_regression_2026-09-29.txt` (bit-exact + roundtrip, all L, both simulators) | PASS |
| 2 | Four Quartus evidence files | `docs/evidence/quartus/C2-L1-20260929.md` .. `C2-L8-20260929.md` | PASS |
| 3 | Comparison table complete | `docs/ROADMAP.md` ablation matrix, rows C2-L1/L2/L4/L8 | PASS |
| 4 | ADR choosing L (or keeping L configurable) signed by the team | `docs/decisions/0004-phase-3-lane-count-l-selection-criterion.md` (Accepted, Faza Dzil, 2026-09-29) fixes the *criterion* before measuring, satisfying the letter of this PASS criterion; **applying it to pick a value (Section 3 below) still needs a separate team sign-off**, not done unilaterally here | PASS |

## 2. What was produced
| Path | Purpose |
|---|---|
| `tb/mem/bank_model.py` (extended) | Added `zeta_index_of` (closed-form per-lane twiddle index) and `reference_zeta_trace` (C0's sequential rule, restated as ground truth) |
| `scripts/gen_lane_schedule.py` | Verifies the closed-form zeta formula against the sequential rule (0 mismatches, both directions) and the per-sub-cycle lane p-coverage (no duplicate, no gap), for all four L |
| `rtl/mem/poly_mem_multiport.sv` | Multi-port banked memory: 2*NUM_LANES packed-vector ports (not unpacked arrays -- see Section 6), `en_i` per-port enable, `bank_overflow_o` diagnostic |
| `rtl/ntt/ntt_core_c2.sv` | Configuration C2: NUM_LANES parallel butterflies/cycle, no shared sequential zeta counter (combinational per-lane closed form instead), FSM/scaling pass otherwise unchanged from C0/C1 |
| `rtl/ntt/ntt_core_c2_l1.sv` .. `_l8.sv` | Thin Quartus top-level wrappers, one NUM_LANES value fixed each (same pattern as C0 vs C1: one synthesizable top entity per config) |
| `tb/ntt/test_ntt_core_c2.py` | cocotb: bit-exact, roundtrip, constant-cycle-per-L, `bank_overflow_o` checked every cycle |
| `tb/ntt/run_ntt_c2_tests.py` | Runs all four L through one simulator |
| `formal/phase03-multilane/ntt_core_c2_formal_top.sv`, `ntt_core_c2_l{1,2,4,8}_safety.sby` | Formal re-proof of the FSM safety property + bank_overflow_o==0, per L |
| `quartus/phase03_multilane_c2/` | Quartus project, revisions C2-L1/L2/L4/L8, same virtual-pin methodology and provisional clock as C0/C1 |
| `docs/decisions/0004-phase-3-lane-count-l-selection-criterion.md` | ADR: L-selection criterion, fixed before the sweep was measured |
| `docs/evidence/phase03-multilane/test_plan.md` | CRG-4 test plan, written before any RTL |
| `docs/evidence/phase03-multilane/lane_schedule_verification_2026-09-29.txt` | Raw zeta-formula + p-coverage proof log |
| `docs/evidence/phase03-multilane/cocotb_regression_2026-09-29.txt` | Raw cocotb pass/fail + cycle-count log, both simulators, all four L |
| `docs/evidence/phase03-multilane/formal_verification_2026-09-29.txt` | Formal results per L, including the L>1 investigation writeup |
| `docs/evidence/quartus/C2-L1-20260929.md` .. `C2-L8-20260929.md` | Standard fitter/STA/Fmax extracts, one per L |

## 3. Numbers (each labelled MEASURED, ESTIMATE, or cited [n])
| Quantity | L=1 | L=2 | L=4 | L=8 |
|---|---|---|---|---|
| ALM | 6,018 / 41,910 (14%) | 5,728 / 41,910 (14%) | 7,629 / 41,910 (18%) | 11,446 / 41,910 (27%) |
| Within ADR 0004 budget (10,478 ALM)? | yes | yes | yes | **no** |
| Registers | 3,100 | 3,098 | 3,102 | 3,100 |
| RAM Blocks (M10K) | 0 / 553 | 0 / 553 | 0 / 553 | 0 / 553 |
| DSP | 3 / 112 | 5 / 112 | 9 / 112 | 17 / 112 |
| Fmax (Slow 100C) | 14.76 MHz | 13.54 MHz | 11.60 MHz | 7.62 MHz |
| Worst setup slack @ 20.000 ns | -47.733 ns | -54.644 ns | -66.690 ns | -111.219 ns |
| NTT cycles (simulation) | 897 | 449 | 225 | 113 |
| INTT cycles (simulation) | 1,153 | 705 | 481 | 369 |
| Formal (bank_overflow_o + FSM safety) | PASS (k-induction) | UNKNOWN (see Section 6) | UNKNOWN | UNKNOWN |

All MEASURED, `docs/evidence/quartus/C2-L{1,2,4,8}-20260929.md` and
`docs/evidence/phase03-multilane/cocotb_regression_2026-09-29.txt`.

**Applying ADR 0004's criterion** (primary: min cycle count within the 10,478 ALM budget; L=8 is
disqualified by the budget check above): among L∈{1,2,4}, cycle count strictly decreases with L
(897/1153 -> 449/705 -> 225/481), so **L=4 has the lowest cycle count of the in-budget
candidates**. Per ADR 0004 this is reported as the primary-criterion result, not unilaterally
adopted as the team's final choice -- Section 7 asks the team to confirm it. The secondary
(informational AT re-check) cannot run yet: no L meets timing at any clock, so there is no
timing-valid Fmax to compute AT from (ADR 0004 anticipated exactly this case).

## 4. Standards and sources pinned
No new FIPS 203 reading this phase; no parameter or algorithm touched (`check_params.py` still
passes). Toolchain identical to Phase 1/2 (OSS CAD Suite `2026-09-23`, Quartus 25.1std.0 Build 1129).

## 5. Coverage and limits
- **M10K still not used** (0/553, all four L) -- inherited, unresolved Phase 2 gap; Phase 3's own
  PASS criteria do not require fixing it, and it was not silently patched.
- **Timing gets worse as L grows**, monotonically (Fmax 14.76 -> 7.62 MHz; worst slack -47.7 ->
  -111.2 ns). This is the expected cost of more combinational logic per cycle (NUM_LANES parallel
  butterflies, address generators, and twiddle-ROM reads, all still purely combinational, no
  pipelining -- Phase 4 scope) and is reported plainly, not attributed to noise.
- **No target-clock ADR exists yet** (inherited from Phase 1/2, still open) -- every Fmax/slack
  number above is relative-only, not a claim against a real target.
- **Formal is incomplete for L>1** -- see Section 6. This is the most significant open item this
  phase, more consequential than the usual timing-not-met pattern, because it means the
  conflict-freedom guarantee that the whole multi-lane memory design rests on is *simulated and
  reasoned about* but not *proven* for three of the four L values.
- Reduction method, address-range argument (still true here: `AW=8` cannot represent an address
  outside [0,255] by construction): same caveats as Phase 1/2, unchanged.

## 6. Deviations, failures and open issues
- **`poly_mem_multiport.sv`'s ports were redesigned from unpacked arrays to packed vectors
  mid-phase.** The first working version used `input wire we_i [0:2*NUM_LANES-1]`-style unpacked
  array ports (simulates and synthesizes fine under Verilator/Icarus). SymbiYosys's restricted
  `read -formal` SystemVerilog reader rejects unpacked-array module ports outright (`syntax
  error, unexpected '['`), so every array port and several internal arrays were rewritten as
  packed vectors with `[i*W +: W]` bit-slicing before formal verification could even elaborate
  the design. This is now the only style used in `rtl/mem/poly_mem_multiport.sv` and
  `rtl/ntt/ntt_core_c2.sv`'s per-port signals. cocotb (both simulators) was re-run after the
  rewrite and still shows 16/16 pass with identical cycle counts, so this was a port-shape
  change, not a behavior change.
- **Icarus Verilog does not support the `automatic` storage-lifetime override inside a procedural
  block** (`sorry: Overriding the default variable lifetime is not yet supported`), hit twice
  (once in the bank-slot counting loop, once in an abandoned helper). Fixed by declaring the
  helper variable outside the `always_comb` instead of using `automatic logic ... = ...;` inline
  -- functionally identical since the value is fully overwritten every evaluation.
- **`bind` is not supported by SymbiYosys's restricted formal reader either** (same class of
  error as the unpacked-array one). An attempt to add an auxiliary inductive invariant
  (`t_q <= TMax`, `layer_q <= 6`) via a `bind`-in per formal-only module was abandoned in favor of
  adding the `assert`s directly inside `rtl/ntt/ntt_core_c2.sv`, guarded by `` `ifdef FORMAL ``
  (never active in synthesis or normal simulation).
- **CRG-8 formal gap, investigated in depth (not left as an unexplained FAIL):** adding the
  `t_q`/`layer_q` range invariants fixed nothing for L=2/4/8; k-induction still reports a
  `bank_overflow_o` counterexample, this time at a *reachable-looking* state (L=2, `layer_q=3`,
  `t_q=32`, `state_q=S_RUN`). Manually decoded from the counterexample's own VCD trace and
  cross-checked three independent ways:
  1. `tb/mem/bank_model.py`: `bank_of(64,2)=1`, `bank_of(80,2)=0`, `bank_of(192,2)=0`,
     `bank_of(208,2)=1` -- exactly 2 accesses per bank, no overflow.
  2. `rtl/mem/bank_map_rom.sv`'s own source text for `NUM_BANKS==2`: the case-statement entries
     for addresses 64/80/192/208 match the Python model exactly (`bank_o=1'd1`/`1'd0`/`1'd0`/
     `1'd1` respectively).
  3. `docs/evidence/phase03-multilane/cocotb_regression_2026-09-29.txt`: any full L=2 NTT run
     necessarily sweeps every `(layer, t)` pair including this one, and `bank_overflow_o` was
     checked (asserted 0) every cycle in every test, on both simulators -- 16/16 passed.
  Yet the SMT trace's own per-instance `bank_o` outputs for the `bank_map_rom` instances handling
  addresses 80/192/208 do **not** match the source text or the Python model (the instance for
  address 64 is read correctly; the other three are not). This localizes the discrepancy to how
  Yosys's `-formal` frontend evaluates the 256-entry `unique case` ROM under k-induction, not to
  the design. This conclusion is stated as *investigated and believed*, not proven -- fully
  resolving it (a smaller reproduction case, a Yosys bug report, or a different ROM encoding that
  avoids the issue) is left as an open item rather than declared closed.
- No RTL correctness bug was found in `ntt_core_c2`/`poly_mem_multiport` themselves at any point;
  every issue above was a tooling/syntax compatibility issue, caught by lint/build/formal
  immediately, not discovered after a test was declared passing.

## 7. Decisions needed
- Everything already open from Phase 1/2 (`docs/results/result_phase2.md` Section 7): target-clock
  ADR, whether to pursue synchronous-read M10K mapping, how to read CRG-9.
- **New:** confirm or override the ADR 0004 primary-criterion result (Section 3): L=4 has the
  lowest cycle count among the in-budget (≤10,478 ALM) candidates. This result is reported, not
  adopted -- ADR 0004 requires a team confirmation (or a follow-up ADR) before it is treated as
  the selected L for Phase 4.
- **New:** how to treat the CRG-8 formal gap for L=2/4/8 (Section 6) -- accept the simulation +
  Python + source-text cross-check as sufficient evidence of correctness for now and revisit the
  Yosys issue later, or block on resolving it (smaller repro case / bug report / alternate ROM
  encoding) before Phase 4.
- **New:** `QUARTUS_BIN` was filled in `scripts/tooling.env` this phase (Section "Process note"
  above) -- confirm the path is correct for every team member's machine or that each teammate
  sets their own local value (the file is git-ignored, so this is not shared automatically).

## 8. Claims made in this phase
None written for judges/proposal text. `docs/ROADMAP.md`'s C2-L1/L2/L4/L8 ablation rows were
filled from the evidence above; no proposal number was invented.

## 9. Reproduce
```bash
# from repo root, branch phase3-multilane
. scripts/env.sh

python3 scripts/gen_lane_schedule.py   # zeta-formula + p-coverage proof

for L in 1 2 4 8; do
  verilator --lint-only -Wall --timing -sv rtl/ntt/*.sv rtl/mem/*.sv --top-module ntt_core_c2 -GNUM_LANES=$L
done
slang --top ntt_core_c2 rtl/ntt/*.sv rtl/mem/*.sv

python3 tb/ntt/run_ntt_c2_tests.py icarus
python3 tb/ntt/run_ntt_c2_tests.py verilator
python3 tb/ntt/run_ntt_tests.py icarus   # Phase 1 regression, unaffected
python3 tb/mem/run_mem_tests.py icarus   # Phase 2 regression, unaffected
python3 -m pytest tb/golden/tests/ -q
python3 .claude/skills/mlkem-guard/scripts/check_params.py

for L in 1 2 4 8; do
  (cd formal/phase03-multilane && sby -f ntt_core_c2_l${L}_safety.sby)
done

# Quartus (paths for this machine; QUARTUS_BIN in scripts/tooling.env, git-ignored)
cd quartus/phase03_multilane_c2
for L in 1 2 4 8; do
  quartus_sh --flow compile C2-L$L
  python3 ../../.claude/skills/quartus-report/scripts/extract_quartus_report.py \
      output_files_L$L C2-L$L --log compile_L$L.log
done

python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/result_phase3.md
python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal
```

## 10. Approval
- [ ] Human approver (name, date):
      Next phase starts only after a team member ticks this box. Beyond the usual CRG-9
      (timing not met) pattern already accepted for C0/C1, this phase has two items that need an
      explicit team decision before approval means what it usually means: (1) whether L=4's
      primary-criterion result (Section 3) is accepted as the selected L per ADR 0004, and (2)
      how to treat the CRG-8 formal gap for L=2/4/8 (Section 6) going into Phase 4.
