<!-- claim-lint: skip-file (result artifact: internal status page, not proposal text) -->
# Result - Phase 3: Multi-lane exploration (L = 1/2/4/8, config C2)

- Status: DONE
- Date (UTC): 2026-09-29 15:56; updated 2026-09-30 (formal re-run; supplementary K2/K1 experiments;
  ADR 0005)
- Git commit (HEAD when verified): 7b1d467 for the C2 sweep; dbefa86 for the 2026-09-30 update
- Selected operating point (ADR 0005, Accepted 2026-09-30): C2-K2-K1 at L = 8 (Section 3b)
- Environment: same as Phase 1/2 -- Ubuntu 24.04.4 LTS, OSS CAD Suite 2026-09-23, cocotb 2.1.0,
  pytest 9.1.1, Quartus Prime Lite 25.1std.0 Build 1129 (`~/altera_lite/25.1std`).

Process note, stated plainly: `scripts/tooling.env`'s `QUARTUS_BIN` was empty at the start of
this phase (Quartus was previously located manually, per Phase 1/2's own open item); it was found
at `~/altera_lite/25.1std/quartus/bin` and filled in this phase so `scripts/env.sh` puts Quartus on
PATH going forward. This is a local machine-config fix, not a design change.

## 1. Done-criteria (Common RTL Gate, docs/ROADMAP.md, copied unchanged)
| # | Criterion | Evidence | Status |
|---|---|---|---|
| CRG-1 | Lint clean | `cmd: verilator --lint-only -Wall --timing -sv rtl/ntt/*.sv rtl/mem/*.sv --top-module ntt_core_c2 -GNUM_LANES=<L>` for L in {1,2,4,8} (0 warnings each) | PASS |
| CRG-2 | Elaboration clean (slang) | `cmd: slang --top ntt_core_c2 rtl/ntt/*.sv rtl/mem/*.sv` (0 errors, 0 warnings; default NUM_LANES=1 elaboration) | PASS |
| CRG-3 | Bit-exact vs golden, both simulators | `evidence/phase03/cocotb_regression.txt` (16/16 on Icarus AND Verilator, all four L) | PASS |
| CRG-4 | Corner cases before tests | `evidence/phase03/test_plan.md`, written before `rtl/ntt/ntt_core_c2.sv` | PASS |
| CRG-5 | Regression: Phase 0-2 tests still pass | `cmd: python3 -m pytest tb/golden/tests/ -q` (23/23), `cmd: python3 tb/ntt/run_ntt_tests.py icarus` (10/10, C0 unaffected), `cmd: python3 tb/mem/run_mem_tests.py icarus` (12/12, C1 unaffected) | PASS |
| CRG-6 | Locked parameters | `cmd: python3 .claude/skills/mlkem-guard/scripts/check_params.py` | PASS |
| CRG-7 | Constant-cycle evidence | `evidence/phase03/cocotb_regression.txt` -- constant per L, and L=1 equals C0/C1 exactly (897/1153); L>1 is lower, not equal, which is the expected/measured effect of parallel lanes, not a stall | PASS |
| CRG-8 | Formal properties | `evidence/phase03/formal_rerun.md` (`cmd: python3 formal/run/run_formal_slang.py`, 19/19 results as expected): k-induction PASS for L=1, 2, 4 and 8 on C2 (and on the supplementary C2-K2 / C2-K2-K1) for bank_overflow_o == 0, the busy/done handshake and the t_q / layer_q range invariants; four negative controls fail as they must. The earlier L=2/4/8 UNKNOWN (`evidence/phase03/formal_verification.txt`) was a formal-harness artefact (ROMs modelled as free memory state in the induction step), corrected in the harness only -- RTL unchanged (Section 6). Scope: these properties only, not NTT/INTT bit-exactness | PASS |
| CRG-9 | Quartus evidence; no negative slack or the failure documented | `evidence/quartus/C2-L1.md`, `evidence/quartus/C2-L2.md`, `evidence/quartus/C2-L4.md`, `evidence/quartus/C2-L8.md` -- all four compiled and measured; all four have negative worst setup slack (timing NOT met); L=8 additionally exceeds ADR 0004's 10,478 ALM budget (11,446 ALM measured); the failure is documented, which is what the criterion asks | PASS |
| CRG-10 | Result artifact + claim checker | `cmd: python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase03.md` and `cmd: python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal` | PASS |

CRG-9 was first marked FAIL, as in Phase 1 and 2: timing not met at the provisional 20.000 ns
clock was expected (no target-clock ADR existed yet) and is documented, not hidden. On 2026-10-05 the
team chose the reading that a documented failure counts as PASS; the measured slack is unchanged. CRG-8 was FAIL in the first version of this file (2026-09-29: L=1 proven, L=2/4/8
UNKNOWN). It is PASS as of 2026-09-30, after the cause of the UNKNOWN was found in the formal
harness and every L was re-proven with negative controls (Section 6); the PASS covers the stated
control/bank-capacity properties, not arithmetic correctness.

## 1b. Phase 3 PASS criteria (docs/ROADMAP.md Phase 3, beyond the CRG table)
| # | Criterion | Evidence | Status |
|---|---|---|---|
| 1 | All four configurations correct | `evidence/phase03/cocotb_regression.txt` (bit-exact + roundtrip, all L, both simulators) | PASS |
| 2 | Four Quartus evidence files | `evidence/quartus/C2-L1.md` .. `C2-L8.md` | PASS |
| 3 | Comparison table complete | `docs/ROADMAP.md` ablation matrix, rows C2-L1/L2/L4/L8 | PASS |
| 4 | ADR choosing L (or keeping L configurable) signed by the team | `docs/decisions/adr/ADR-0004-phase-3-lane-count-l-selection-criterion.md` (Accepted, Faza Dzil, 2026-09-29) fixes the *criterion* before measuring; `docs/decisions/adr/ADR-0005-apply-adr-0004-l-selection-to-the-c2-k2-k1-supplementary-con.md` (Accepted, Faza Dzil, 2026-09-30) applies it and selects L = 8 on the optimised C2-K2-K1 configuration (Section 3b) | PASS |

## 2. What was produced
| Path | Purpose |
|---|---|
| `tb/mem/bank_model.py` (extended) | Added `zeta_index_of` (closed-form per-lane twiddle index) and `reference_zeta_trace` (C0's sequential rule, restated as ground truth) |
| `scripts/build/gen_lane_schedule.py` | Verifies the closed-form zeta formula against the sequential rule (0 mismatches, both directions) and the per-sub-cycle lane p-coverage (no duplicate, no gap), for all four L |
| `rtl/mem/poly_mem_multiport.sv` | Multi-port banked memory: 2*NUM_LANES packed-vector ports (not unpacked arrays -- see Section 6), `en_i` per-port enable, `bank_overflow_o` diagnostic |
| `rtl/ntt/ntt_core_c2.sv` | Configuration C2: NUM_LANES parallel butterflies/cycle, no shared sequential zeta counter (combinational per-lane closed form instead), FSM/scaling pass otherwise unchanged from C0/C1 |
| `rtl/ntt/ntt_core_c2_l1.sv` .. `_l8.sv` | Thin Quartus top-level wrappers, one NUM_LANES value fixed each (same pattern as C0 vs C1: one synthesizable top entity per config) |
| `tb/ntt/test_ntt_core_c2.py` | cocotb: bit-exact, roundtrip, constant-cycle-per-L, `bank_overflow_o` checked every cycle |
| `tb/ntt/run_ntt_c2_tests.py` | Runs all four L through one simulator |
| `formal/phase03-multilane/ntt_core_c2_formal_top.sv`, `ntt_core_c2_l{1,2,4,8}_safety.sby` | Formal re-proof of the FSM safety property + bank_overflow_o==0, per L |
| `quartus/phase03_multilane_c2/` | Quartus project, revisions C2-L1/L2/L4/L8, same virtual-pin methodology and provisional clock as C0/C1 |
| `docs/decisions/adr/ADR-0004-phase-3-lane-count-l-selection-criterion.md` | ADR: L-selection criterion, fixed before the sweep was measured |
| `evidence/phase03/test_plan.md` | CRG-4 test plan, written before any RTL |
| `evidence/phase03/lane_schedule_verification.txt` | Raw zeta-formula + p-coverage proof log |
| `evidence/phase03/cocotb_regression.txt` | Raw cocotb pass/fail + cycle-count log, both simulators, all four L |
| `evidence/phase03/formal_verification.txt` | First formal results per L (L>1 UNKNOWN) and the first investigation writeup; conclusion superseded by the next row |
| `formal/run/run_formal_slang.py`, `evidence/phase03/formal_rerun.md` | Corrected formal flow: runs every Phase 1-3 proof plus negative controls; root-cause analysis and the 19/19 result table |
| `evidence/quartus/C2-L1.md` .. `C2-L8.md` | Standard fitter/STA/Fmax extracts, one per L |
| `rtl/ntt/ntt_core_c2_k2.sv`, `rtl/ntt/ntt_core_c2_k2_l{1,2,4,8}.sv` | Supplementary experiment K2 (2026-09-30): C2 with `t_q` sized per L; separate files, C2 untouched |
| `rtl/ntt/butterfly_shared.sv`, `rtl/ntt/ntt_core_c2_k2_k1.sv`, `rtl/ntt/ntt_core_c2_k2_k1_l{1,2,4,8}.sv` | Supplementary experiment K1 on top of K2 (config C2-K2-K1): one shared multiplier per butterfly. Selected configuration at L=8 (ADR 0005) |
| `tb/ntt/run_k1_unit_tests.py`, `tb/ntt/k1_exhaustive/`, `formal/phase03-multilane/k1_*`, `formal/phase03-multilane/modmul_reduce_uf.sv` | K1 verification: butterfly unit test, exhaustive equivalence harness, formal equivalence with negative controls |
| `scripts/quartus/quartus_entity_breakdown.py` | Groups the fitter's per-entity table by function (used for the L=8 ALM audit) |
| `docs/decisions/adr/ADR-0005-apply-adr-0004-l-selection-to-the-c2-k2-k1-supplementary-con.md` | ADR: adopts C2-K2-K1 and selects L = 8 |
| `evidence/phase03/k2_experiment.md`, `k1_experiment.md` and the `k1_*` / `k2_*` / `l8_opt_*` files beside them; `evidence/quartus/C2-L{1,2,4,8}-K2.md`, `C2-K2-K1-L{1,2,4,8}.md` | Experiment records, regression/formal/equivalence logs, per-entity breakdowns, Quartus extracts |

## 3. Numbers (each labelled MEASURED, ESTIMATE, or cited [n])
| Quantity | L=1 | L=2 | L=4 | L=8 |
|---|---|---|---|---|
| ALM | 6,018 / 41,910 (14%) | 5,728 / 41,910 (14%) | 7,629 / 41,910 (18%) | 11,446 / 41,910 (27%) |
| Within ADR 0004 budget (10,478 ALM)? | yes | yes | yes | no |
| Registers | 3,100 | 3,098 | 3,102 | 3,100 |
| RAM Blocks (M10K) | 0 / 553 | 0 / 553 | 0 / 553 | 0 / 553 |
| DSP | 3 / 112 | 5 / 112 | 9 / 112 | 17 / 112 |
| Fmax (Slow 100C) | 14.76 MHz | 13.54 MHz | 11.60 MHz | 7.62 MHz |
| Worst setup slack @ 20.000 ns | -47.733 ns | -54.644 ns | -66.690 ns | -111.219 ns |
| NTT cycles (simulation) | 897 | 449 | 225 | 113 |
| INTT cycles (simulation) | 1,153 | 705 | 481 | 369 |
| Formal (bank_overflow_o + FSM safety), corrected flow 2026-09-30 | PASS (k-induction) | PASS (k-induction) | PASS (k-induction) | PASS (k-induction) |

All MEASURED, `evidence/quartus/C2-L{1,2,4,8}.md` and
`evidence/phase03/cocotb_regression.txt`.

Applying ADR 0004's criterion (primary: min cycle count within the 10,478 ALM budget; L=8 is
disqualified by the budget check above): among L∈{1,2,4}, cycle count strictly decreases with L
(897/1153 -> 449/705 -> 225/481), so L=4 has the lowest cycle count of the in-budget
candidates. Per ADR 0004 this is reported as the primary-criterion result, not unilaterally
adopted as the team's final choice -- Section 7 asks the team to confirm it. The secondary
(informational AT re-check) cannot run yet: no L meets timing at any clock, so there is no
timing-valid Fmax to compute AT from (ADR 0004 anticipated exactly this case).

## 3b. Supplementary optimisation experiments and the selected L (2026-09-30)
After the C2 sweep the team asked whether L=8 could be brought under the ALM budget without reducing
its 8 butterflies per cycle. Two experiments were run as separate configurations (the C2 RTL and
evidence above are unchanged and remain the baseline):
- K2 -- sub-cycle counter `t_q` sized to what each L needs. Valid but insufficient, and not a
  uniform improvement (`evidence/phase03/k2_experiment.md`).
- K1 -- one shared modular multiplier per butterfly instead of one per mode, on top of K2
  (config C2-K2-K1, `rtl/ntt/butterfly_shared.sv`, `rtl/ntt/ntt_core_c2_k2_k1.sv`). This changes
  the butterfly datapath, i.e. it is outside the written Phase 3 scope ("butterfly, arithmetic and
  memory as in Phase 2"); the team approved it as a supplementary experiment and then adopted it
  (ADR 0005). `modmul_reduce.sv` and the locked parameters are unchanged
  (`evidence/phase03/k1_experiment.md`).

| Quantity (MEASURED) | L=1 | L=2 | L=4 | L=8 |
|---|---|---|---|---|
| ALM, C2 (Section 3) | 6,018 | 5,728 | 7,629 | 11,446 |
| ALM, C2-K2 | 6,389 | 5,788 | 7,600 | 11,232 |
| ALM, C2-K2-K1 | 5,566 | 5,374 | 6,775 | 9,754 |
| C2-K2-K1 within the 10,478 ALM budget? | yes | yes | yes | yes (724 below) |
| Registers, C2-K2-K1 | 3,099 | 3,095 | 3,098 | 3,094 |
| M10K, C2-K2-K1 | 0 / 553 | 0 / 553 | 0 / 553 | 0 / 553 |
| DSP, C2-K2-K1 | 2 / 112 | 3 / 112 | 5 / 112 | 9 / 112 |
| Fmax (Slow 100C), C2-K2-K1 | 14.33 MHz | 12.63 MHz | 10.89 MHz | 7.68 MHz |
| Worst setup slack @ 20.000 ns, C2-K2-K1 | -49.804 ns | -59.148 ns | -71.868 ns | -110.494 ns |
| NTT / INTT cycles (simulation), identical to C2 | 897 / 1153 | 449 / 705 | 225 / 481 | 113 / 369 |
| Formal (bank_overflow_o + FSM safety), C2-K2-K1 | PASS | PASS | PASS | PASS |

Evidence: `evidence/quartus/C2-K2-K1-L1.md`, `evidence/quartus/C2-K2-K1-L2.md`,
`evidence/quartus/C2-K2-K1-L4.md`, `evidence/quartus/C2-K2-K1-L8.md`,
`evidence/quartus/C2-L1-K2.md`, `evidence/quartus/C2-L2-K2.md`,
`evidence/quartus/C2-L4-K2.md`, `evidence/quartus/C2-L8-K2.md`,
`evidence/phase03/k1_cocotb_regression.txt` (unit 2/2 and core 16/16 on both
simulators), `evidence/phase03/k1_entity_breakdown.txt`,
`evidence/phase03/formal_rerun.md`. Butterfly equivalence
(`butterfly.sv` vs `butterfly_shared.sv`): formal proof with the multiplier abstracted, PASS with
negative controls (`evidence/phase03/k1_equiv_abstraction.txt`), and
exhaustive simulation of all 73,785,560,578 inputs, 0 mismatches
(`evidence/phase03/k1_exhaustive_equivalence.txt`).

Selected L (ADR 0005, Accepted, Faza Dzil, Team J5, 2026-09-30): applying ADR 0004's rule
unchanged to C2-K2-K1, all four L are within budget and L=8 has the lowest cycle count, so the team
selects L = 8 on C2-K2-K1 (9,754 ALM; NTT 113 / INTT 369 cycles). Phase 4 starts from that
configuration. The C2 result above (L=4) is kept as the baseline comparison.

Limits carried with this selection (not resolved by it): timing is not met for any configuration;
the 724-ALM margin is larger than, but not far above, the largest fitter-packing swing observed
between compiles of identical logic (~370 ALM, K2 at L=1; no seed sweep was run); K1 lowers Fmax
slightly at L=1/2/4; 0 M10K blocks are used.

## 4. Standards and sources pinned
No new FIPS 203 reading this phase; no parameter or algorithm touched (`check_params.py` still
passes). Toolchain identical to Phase 1/2 (OSS CAD Suite `2026-09-23`, Quartus 25.1std.0 Build 1129).

## 5. Coverage and limits
- M10K still not used (0/553, all four L) -- inherited, unresolved Phase 2 gap; Phase 3's own
  PASS criteria do not require fixing it, and it was not silently patched.
- Timing gets worse as L grows, monotonically (Fmax 14.76 -> 7.62 MHz; worst slack -47.7 ->
  -111.2 ns). This is the expected cost of more combinational logic per cycle (NUM_LANES parallel
  butterflies, address generators, and twiddle-ROM reads, all still purely combinational, no
  pipelining -- Phase 4 scope) and is reported plainly, not attributed to noise.
- No target-clock ADR exists yet (inherited from Phase 1/2, still open) -- every Fmax/slack
  number above is relative-only, not a claim against a real target.
- Formal covers control and bank capacity only. As of 2026-09-30 `bank_overflow_o`==0 (the
  conflict-freedom guarantee the multi-lane memory rests on), the busy/done handshake and the
  `t_q`/`layer_q` ranges are proven by k-induction for all four L (Section 6). NTT/INTT
  bit-exactness, memory data integrity and liveness are NOT formally proven; they rest on the
  cocotb regressions on two simulators.
- Reduction method, address-range argument (still true here: `AW=8` cannot represent an address
  outside [0,255] by construction): same caveats as Phase 1/2, unchanged.

## 6. Deviations, failures and open issues
- `poly_mem_multiport.sv`'s ports were redesigned from unpacked arrays to packed vectors
  mid-phase. The first working version used `input wire we_i [0:2*NUM_LANES-1]`-style unpacked
  array ports (simulates and synthesizes fine under Verilator/Icarus). SymbiYosys's restricted
  `read -formal` SystemVerilog reader rejects unpacked-array module ports outright (`syntax
  error, unexpected '['`), so every array port and several internal arrays were rewritten as
  packed vectors with `[i*W +: W]` bit-slicing before formal verification could even elaborate
  the design. This is now the only style used in `rtl/mem/poly_mem_multiport.sv` and
  `rtl/ntt/ntt_core_c2.sv`'s per-port signals. cocotb (both simulators) was re-run after the
  rewrite and still shows 16/16 pass with identical cycle counts, so this was a port-shape
  change, not a behavior change.
- Icarus Verilog does not support the `automatic` storage-lifetime override inside a procedural
  block (`sorry: Overriding the default variable lifetime is not yet supported`), hit twice
  (once in the bank-slot counting loop, once in an abandoned helper). Fixed by declaring the
  helper variable outside the `always_comb` instead of using `automatic logic ... = ...;` inline
  -- functionally identical since the value is fully overwritten every evaluation.
- `bind` is not supported by SymbiYosys's restricted formal reader either (same class of
  error as the unpacked-array one). An attempt to add an auxiliary inductive invariant
  (`t_q <= TMax`, `layer_q <= 6`) via a `bind`-in per formal-only module was abandoned in favor of
  adding the `assert`s directly inside `rtl/ntt/ntt_core_c2.sv`, guarded by `` `ifdef FORMAL ``
  (never active in synthesis or normal simulation).
- CRG-8 formal gap for L=2/4/8: resolved 2026-09-30 -- it was a formal-harness artefact, and the
  explanation first written here was wrong about the mechanism. Status then was UNKNOWN (base
  case pass, induction fail), not FAIL and not a timeout. Root cause, from the induction trace
  (L=2, first NTT cycle, addresses 0/128/64/192 exactly as scheduled, yet the `bank_map_rom`
  instance for address 0 output bank 1 where the source says 0): Yosys's `proc_rom` turns
  `bank_map_rom`'s 256-entry `case` and `twiddle_rom` into `$mem` cells, whose contents are free
  state in the induction step, so the solver used a ROM whose contents are not the real table --
  an unreachable state. Fix in the harness only: `memory_map -rom-only` (ROM contents are
  constants: a design fact, not an assumption), plus the yosys-slang frontend (the native
  `read -formal` leaves `ntt_pkg`'s `add_mod`/`sub_mod` undriven) and an equivalent reset
  assumption. RTL unchanged. Result: all four L PASS; negative controls (a corrupted copy of
  `bank_map_rom`) fail in the base case or in induction as they must; Phase 1/2 proofs still PASS
  under the same flow. Full analysis: `evidence/phase03/formal_rerun.md`.
  *Correction of the earlier text (kept below for the record):* it attributed the mismatch to
  "how Yosys's `-formal` frontend evaluates the 256-entry `unique case` ROM" and called the
  counterexample state "reachable-looking"; the FSM state was reachable, the ROM contents were not,
  and the `t_q`/`layer_q` invariants added at the time did not address the cause.
- *Superseded 2026-09-29 text, kept for the record:* adding the
  `t_q`/`layer_q` range invariants fixed nothing for L=2/4/8; k-induction still reports a
  `bank_overflow_o` counterexample, this time at a *reachable-looking* state (L=2, `layer_q=3`,
  `t_q=32`, `state_q=S_RUN`). Manually decoded from the counterexample's own VCD trace and
  cross-checked three independent ways:
  1. `tb/mem/bank_model.py`: `bank_of(64,2)=1`, `bank_of(80,2)=0`, `bank_of(192,2)=0`,
     `bank_of(208,2)=1` -- exactly 2 accesses per bank, no overflow.
  2. `rtl/mem/bank_map_rom.sv`'s own source text for `NUM_BANKS==2`: the case-statement entries
     for addresses 64/80/192/208 match the Python model exactly (`bank_o=1'd1`/`1'd0`/`1'd0`/
     `1'd1` respectively).
  3. `evidence/phase03/cocotb_regression.txt`: any full L=2 NTT run
     necessarily sweeps every `(layer, t)` pair including this one, and `bank_overflow_o` was
     checked (asserted 0) every cycle in every test, on both simulators -- 16/16 passed.
  Yet the SMT trace's own per-instance `bank_o` outputs for the `bank_map_rom` instances handling
  addresses 80/192/208 do not match the source text or the Python model (the instance for
  address 64 is read correctly; the other three are not). This localizes the discrepancy to how
  Yosys's `-formal` frontend evaluates the 256-entry `unique case` ROM under k-induction, not to
  the design. This conclusion is stated as *investigated and believed*, not proven -- fully
  resolving it (a smaller reproduction case, a Yosys bug report, or a different ROM encoding that
  avoids the issue) is left as an open item rather than declared closed.
- No RTL correctness bug was found in `ntt_core_c2`/`poly_mem_multiport` themselves at any point;
  every issue above was a tooling/syntax compatibility issue, caught by lint/build/formal
  immediately, not discovered after a test was declared passing.

## 7. Decisions needed
- Everything already open from Phase 1/2 (`docs/results/phase02.md` Section 7): target-clock
  ADR, whether to pursue synchronous-read M10K mapping, how to read CRG-9.
- ~~Confirm or override the ADR 0004 primary-criterion result (L=4 on C2)~~ -- decided 2026-09-30
  by ADR 0005: the team adopts the optimised C2-K2-K1 configuration and selects L = 8 (Section 3b).
- New (optional): a fitter seed sweep on C2-K2-K1 L=8 to quantify the ALM-packing margin
  against the 10,478 ALM budget (Section 3b limits).
- ~~How to treat the CRG-8 formal gap for L=2/4/8~~ -- closed 2026-09-30: the gap was a harness
  artefact and all four L are proven (Section 6). Remaining, optional: formal properties beyond
  control/bank capacity (memory data integrity, liveness) if the team wants them.
- New: `QUARTUS_BIN` was filled in `scripts/tooling.env` this phase (Section "Process note"
  above) -- confirm the path is correct for every team member's machine or that each teammate
  sets their own local value (the file is git-ignored, so this is not shared automatically).

## 8. Claims made in this phase
None written for judges/proposal text. `docs/ROADMAP.md`'s C2-L1/L2/L4/L8 ablation rows were
filled from the evidence above; no proposal number was invented.

## 9. Reproduce
```bash
# from repo root, branch phase3-multilane
. scripts/env.sh

python3 scripts/build/gen_lane_schedule.py   # zeta-formula + p-coverage proof

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

python3 formal/run/run_formal_slang.py   # every Phase 1-3 proof + negative controls (19 results)

# Supplementary experiments (Section 3b): K2 and K2+K1 regressions, butterfly equivalence
python3 tb/ntt/run_ntt_c2_tests.py verilator k2 && python3 tb/ntt/run_ntt_c2_tests.py icarus k2
python3 tb/ntt/run_ntt_c2_tests.py verilator k1 && python3 tb/ntt/run_ntt_c2_tests.py icarus k1
python3 tb/ntt/run_k1_unit_tests.py verilator && python3 tb/ntt/run_k1_unit_tests.py icarus
(cd formal/phase03-multilane && sby -f k1_butterfly_equiv_abs.sby)   # PASS; k1_negctl_*.sby must FAIL
tb/ntt/k1_exhaustive/run_k1_exhaustive.sh                            # ~20 min on 8 cores
# Quartus revisions: C2-L<n>-K2 and C2-K2-K1-L<n> in quartus/phase03_multilane_c2/ (same flow as below)

# Quartus (paths for this machine; QUARTUS_BIN in scripts/tooling.env, git-ignored)
cd quartus/phase03_multilane_c2
for L in 1 2 4 8; do
  quartus_sh --flow compile C2-L$L
  python3 ../../.claude/skills/quartus-report/scripts/extract_quartus_report.py \
      output_files_L$L C2-L$L --log compile_L$L.log
done

python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase03.md
python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal
```

## 10. Approval
- [x] Human approver (faza dzil, 30-09-2026):
      Next phase starts only after a team member ticks this box. Beyond the usual CRG-9
      (timing not met) pattern already accepted for C0/C1, this phase has two items that need an
      explicit team decision before approval means what it usually means; both were settled on
      2026-09-30: (1) the selected L is L = 8 on the optimised C2-K2-K1 configuration (ADR 0005,
      Section 3b), and (2) the CRG-8 formal gap for L=2/4/8 was a harness artefact and is closed
      (Section 6). Approving this PARTIAL status therefore means accepting CRG-9 (timing not
      met) and the Section 3b limits as the documented starting point for Phase 4.

## Status update (2026-10-05)
The team set this phase to DONE because its goals are met by the final phases: the later configurations meet timing (40 ns at 6 of 6 seeds, and 15 ns for the Phase 9M core, `docs/results/phase9m.md`). The measurements of this phase are unchanged (slack and ALM figures above stay as measured). CRG-9 reads "no negative slack or the failure documented"; the failure is documented in the evidence named in its row. The Approval box above was ticked earlier and is not edited.
