<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Phase 5 test plan - modular arithmetic for q = 3329 (C4), written before any RTL is coded (CRG-4)

- Date (UTC): 2026-10-01. Branch `phase5-arith` (from `main` at 5a1eec0). No Phase 5 RTL, testbench or Quartus
  project exists at the time of writing.
- **Status: FINAL (2026-10-01).** Decisions D0–D8 of Section 13 were answered by the team: D0 = ADR 0010, D1–D8 and
  the 5b selection rule = ADR 0011 (all suggestions accepted); limits for later timing work = ADR 0012. Items marked
  *[D<n>]* below follow those ADRs. Register positions inside each new reducer are added as amendments (Section 14)
  before the Quartus revision concerned is compiled.
- Governing decisions: ADR 0009 (start from C3-P6: L = 8, P = 6; NTT-core design budget 12,573 ALM), ADR 0006
  (end goal 20.000 ns / 50 MHz "after Phase 5"; Phase 4 milestone 40.000 ns), ADR 0007 (bit-exact function; register
  positions of P = 6), ADR 0002 / C1 (mathematics locked).
- Scope from `docs/ROADMAP.md` Phase 5: 5a q-specific reduction; 5b Montgomery vs Barrett behind the same interface,
  both measured, choice by ADR; 5c (optional) lazy reduction with proven bounds; 5d (optional) Karatsuba-style
  base-case multiplication. Schedule, memory, L and P stay fixed. Not allowed: changes to q or FIPS 203 arithmetic,
  approximate reduction without proof, scheduling changes, Keccak.
- Reference models: `tb/golden/primitives.py` (`ntt`, `intt`, `base_case_multiply`), integer formula (a·b) mod 3329.

## 1. Starting point (MEASURED unless marked)
| Item | Value | Evidence |
|---|---|---|
| C3-P6, default seed | 10,505 ALM, 4,168 registers, 29 M10K, 9 DSP; setup +10.753 ns @ 40 ns; Fmax 34.19 MHz (lowest slow corner) | `evidence/phase04/quartus_C3-P6.md` |
| C3-P6, seeds 1–6 | 10,484–10,516 ALM; Fmax 32.60–34.20 MHz | `evidence/phase04/seed_sweep.md` |
| Cycles | NTT 119, INTT 375, 0 stall (simulation) | `evidence/phase04/cocotb_regression.txt` |
| Reducers in C3-P6 | 8 × `modmul_reduce_staged` (153.2–157.2 ALM, 1 DSP each) + 1 scaling reducer (148.9 ALM, 1 DSP); sum 1,395.8 ALM (INFERENCE) | `baseline/c3p6_critical_path.md` |
| GHRD + C3-P6 (GHRD settings) | 12,375 ALM combined; core alone with GHRD settings 11,053 | `evidence/phase04/ghrd_plus_c3p6_integration.md` |

**Frozen, not edited in Phase 5:** every file of Phases 1–4 under `rtl/`, `tb/`, `formal/`, `quartus/` and all Phase
1–4 evidence - in particular `modmul_reduce.sv`, `modmul_reduce_staged.sv`, `butterfly*.sv`, `twiddle_rom.sv`,
`base_case_multiply.sv`, `poly_mem_multiport_pipe.sv`, `ntt_core_c3*.sv`.

## 2. Baseline finding that shapes this plan (`baseline/c3p6_critical_path.md`)
- MEASURED: the 300 worst setup paths of C3-P6 (Slow 100C) all start at the memory's slot-arbitration registers
  (cut M). The worst path (slack 10.753 ns) is: memory read decode + read mux ≈ 21.3 ns → butterfly `sub_mod(b, a)`
  ≈ 4.3 ns → DSP multiplier ≈ 3.7 ns → cut X. No reducer-internal path is among the 300.
- MEASURED slack per reducer segment: X → D_5 +24.457 ns, D_5 → D_11 +23.592 ns, D_11 → memory +16.382 ns.
- INFERENCE: **with memory, schedule, L and P fixed, Phase 5 arithmetic changes cannot reach 20.000 ns**: the memory
  read part alone is longer than 20 ns. Arithmetic can affect the ~8 ns of `sub_mod` + multiplier on the critical
  segment, the D_11 → memory segment and ALM (at most about the 1,395.8 ALM of today's reducers if a new reducer were
  free). This is reported to the team as decision D0 before any work.

## 3. Sub-steps, candidate designs and the 5a / 5b boundary *[D4]*
The current reducer is **not** a multiplication by q: it is 13 conditional subtractions of the constants q·2^k
(k = 12..0) from the 24-bit product. The roadmap wording of 5a ("multiplication by the constant q as shift-and-add
inside the current reduction method") therefore applies only partly. Three readings (D4):

| Reading | What 5a builds | Boundary to 5b |
|---|---|---|
| (i) | the same restoring method with fewer stages, using the operand bound a, b < q (product ≤ (q−1)² = 11,075,584 < 2^24) | 5b replaces the method |
| **(ii)** *(suggestion)* | a q-specific **fold** reducer: q = 2^11 + 2^10 + 2^8 + 1, so 2^12 ≡ 767 (mod q) with 767 = 2^10 − 2^8 − 1; x = x_h·2^12 + x_l is folded to 767·x_h + x_l with shifts and adds only, repeated until the value is below a small multiple of q, then a fixed number of conditional subtractions | 5b = Barrett and Montgomery, each using a multiplication by an approximate inverse; in both, the multiplication **by q** is written as shift-and-add (the 5a technique) |
| (iii) | only the INTT ×3303 scaling multiplier as a shift-and-add constant multiplier (3303 = 0b1100_1110_0111) | 5b replaces the lane reducers |

Candidate parameters (perhitungan tim, confirmed only by the exhaustive test V2):
- **Barrett**, k = 24, m = ⌊2^24 / q⌋ = 5039 (13 bits): t = ⌊x·m / 2^24⌋, r = x − t·q; for every x ≤ (q−1)² the
  remainder satisfies r < 2q (checked over all x by script), so one conditional subtraction follows. Smaller k
  (22 / 23) needs 2–3 subtractions.
- **Montgomery**, R = 2^12, q' = −q⁻¹ mod 2^12 = 3327: m = (x mod R)·q' mod R, t = (x + m·q) / R < 2q because
  x ≤ (q−1)² < q·R = 13,635,584; one conditional subtraction. Output = x·R⁻¹ mod q. To keep the butterfly's
  function (a·b mod q) unchanged, the operand that is always a constant is stored in Montgomery form: twiddles
  ζ·R mod q in a **new** generated ROM (`scripts/build/gen_twiddle_rom_mont.py` from `tb/golden/primitives.py`;
  `twiddle_rom.sv` stays frozen) and the INTT scaling constant 3303·R mod q. Every multiplier in C3 has one operand
  from a table or a constant (`zeta_i` in the butterflies, 3303 in the scaling pass - checked in
  `rtl/ntt/butterfly_shared_pipe.sv` and `rtl/ntt/ntt_core_c3.sv`), so no conversion of polynomial data is needed.
- Whether the extra multiplication (x·m in Barrett, (x mod R)·q' in Montgomery) uses a DSP or ALM shift-and-add is a
  design parameter; both variants may be built if D2 allows extra DSPs.

5c *(optional, [D3])* - lazy reduction. The only lazy spot compatible with fixed memory (12-bit words, values < q
written back) is **inside the butterfly**. Concrete candidate targeting the measured critical segment: feed
`b + q − a` (13 bits, in [1, 2q)) to the multiplier instead of `sub_mod(b, a)`, removing the conditional subtraction
(part of the ~4.3 ns) from the M → X segment. The multiplier input range becomes [0, 2q) and the product exceeds
2^24 (max 2q·(q−1) ≈ 22.2 M), so the reducer must be proven for that wider domain (Barrett with larger k, or
Montgomery with R = 2^13). Allowed only with the formal bound proof of Section 8.

5d *(optional, [D3])* - Karatsuba-style base case: c1 = (a0 + a1)(b0 + b1) − a0·b0 − a1·b1, c0 = a0·b0 + γ·(a1·b1),
4 modular multiplications instead of 5. **Finding:** `base_case_multiply.sv` is **not part of C3-P6**: no core instantiates it
(it is only listed as a source file in some Phase 1–4 QSFs; the C3 core does NTT/INTT only). C4d therefore cannot be a change of the C3-P6 kernel;
it is a standalone unit compared against a standalone compile of the frozen `base_case_multiply.sv` *[D3]*.

## 4. Interface contract and operand domain (checked in RTL)
- Lane multiplier: `a_i = zeta_i` from `twiddle_rom` (all 128 entries < q), `b_i = mul_in` = `b` (forward) or
  `sub_mod(b, a)` (inverse). Scaling multiplier: memory word × 3303. With polynomial coefficients < q, **every
  multiplier operand is in [0, q)**.
- Coefficients ≥ q written by the host are outside the contract: `add_mod` / `sub_mod` already assume inputs < q, so
  the C3 core gives no result specified to match FIPS 203 for them today. Proposed contract *[D6]*: new reducers must equal (a·b) mod q
  for **all a, b in [0, q)**; behaviour for 12-bit operands ≥ q is measured and reported (V2-info) but not
  required. The frozen staged reducer happens to be exact for all 2^24 12-bit pairs; a new reducer may not be.
- Every reducer has the same port list as `modmul_reduce_staged` (`clk_i`, `a_i`, `b_i`, `p_o`, parameter for register
  positions) so that a C4 butterfly can select the reducer by parameter.

## 5. Latency and register positions (P = 6 fixed)
- In C3-P6 the multiplier path carries 3 of the 6 pipeline registers (`MUL_REG` = X, D_5, D_11; the memory carries
  A_4, A_11, M). **Every C4 reducer used in the core has latency exactly 3** so that P = 6, the schedule and the
  cycle counts (NTT 119, INTT 375) are unchanged.
- Default rule: one register directly after the product (cut X, unchanged) and two inside the new reducer, placed to
  split its logic roughly evenly. The exact positions per reducer are written into an amendment of this plan
  **before** the Quartus revision concerned is compiled (Phase 4 rule against tuning after the fact). Changing a
  position after a Quartus result has been seen creates a separately named revision (e.g. `C4b-M2`); both are kept.
- Moving a register **out of** the multiplier path (e.g. into the memory read path or before the multiplier) changes
  the P = 6 positions fixed by the Phase 4 plan and needs a team decision *[D5]*.

## 6. Corner cases (CRG-4), listed before any test is written
Unit level (every reducer):
- a = 0 or b = 0; a = b = 1; a = 1, b = q−1; a = b = q−1 (largest product 11,075,584).
- Products exactly k·q and k·q ± 1 for k = 1, 2, q−2, q−1 (each reachable product near a multiple of q).
- Products at the Barrett / Montgomery boundary cases found by script: the x with the largest r before the final
  subtraction, and x just below and above each 2^12·j fold boundary used by the fold reducer.
- All 128 twiddle constants (and their Montgomery forms) × {0, 1, q−1} and the scaling constant × {0, 1, q−1}.
- Back-to-back inputs every cycle (no bubbles) and a single isolated input, to check the latency of exactly 3.
Core level: all-zero polynomial; all q−1; impulse at 0; impulse at 255; alternating 0 / q−1; 100 random per direction;
50 round trips `intt(ntt(f)) == f`; the boundary-directed hazard data of Phase 4.
5c: the extreme inputs of the lazy range (b + q − a with a = 0, b = q−1 → 2q−1; a = q−1, b = 0 → 1) with every
twiddle; 5d: (a0, a1, b0, b1) ∈ {0, 1, q−1}^4 with every γ.

## 7. Verification per sub-step (every item on Icarus **and** Verilator unless stated)
**V1 Lint / elaboration (CRG-1, CRG-2).** `verilator --lint-only -Wall` and `slang`, 0 warnings, every new file and
wrapper; `default_nettype none` at the top and `wire` restored at the end; no comment line starting with the word
"synthesis"; no `automatic` variables in procedural blocks (Icarus).

**V2 Exhaustive reducer test (roadmap requirement).** Verilator C++ harness modelled on `tb/ntt/p4_reducer/`:
every (a, b) in [0, q)², 11,082,241 pairs, at the register configuration actually used, comparing the output (after
its latency) with (a·b) mod 3329 **and** with the frozen `modmul_reduce_staged`. For Montgomery the harness drives
b in Montgomery form (b·R mod q, a bijection on [0, q)) so the comparison is still against (a·b) mod q for every
pair. 0 mismatches required. *V2-info [D6]:* the same over all 2^24 12-bit pairs, result reported only.

**V3 cocotb unit tests.** Section 6 corners plus 10,000 random pairs streamed back-to-back; latency checked.

**V4 Butterfly (C4 variant).** Phase 4 V3 corners and 1,000 random (a, b, ζ) per mode against the golden butterfly
step, back-to-back, at the expected latency.

**V5 Core bit-exact (CRG-3).** Section 6 core list against `tb/golden/primitives.py`; the Phase 4 hazard scoreboard
and `bank_overflow_o` check run during every core test (must stay 0 / 0).

**V6 Constant cycles (CRG-7).** Start-to-done cycles identical for every input and on both simulators, and **equal to
C3-P6's 119 / 375**; any other value means P or the schedule changed and is a failure of this phase's scope.

**V7 Generated tables.** If a Montgomery ROM or constant is used: the generator script recomputes every entry from
`tb/golden/primitives.py`; a test checks each entry ζ_M[i] · R⁻¹ ≡ ζ[i] (mod q) against the frozen ROM's values.

**V8 Formal (CRG-8).** No new control logic is planned; the Phase 4 formal flow is re-run on the C4 core to show the
control properties still hold (`formal/run/run_formal_phase4.py` pattern, new top). 5c adds Section 8.

**V9 Regression (CRG-5, CRG-6).** Phase 0 pytest, Phase 1–4 cocotb and formal regressions, `check_params.py`.

**V10 Negative controls.** One deliberately wrong reducer constant (e.g. m − 1 for Barrett, wrong q' for
Montgomery) in a test-only build must make V2 fail; a wrong ROM entry must make V7 and V5 fail. If not, the test is
void.

A sub-step is **correct** only if V1–V7, V9, V10 pass (and Section 8 for 5c) on both simulators.

## 8. Formal plan for 5c (lazy reduction) - required before any lazy design is used
- SymbiYosys with the yosys-slang frontend (no `bind`, packed-vector ports), on a combinational wrapper of the lane
  datapath: assume a, b < q and ζ < q; prove (mode `prove`) that (1) the multiplier input is < 2q, (2) the product
  fits the reducer's input width, (3) the reducer output and every value written to memory is < q, (4) no
  intermediate signal overflows its declared width.
- Equality with the exact result: the lazy multiplier input u = b + q − a ≡ b − a (mod q) lies in [1, 2q), so the
  extended reducer is tested exhaustively for every ζ in [0, q) and u in [0, 2q) (3,329 × 6,658 = 22,164,482 pairs,
  the V2 harness with a wider input) against (ζ·u) mod q, and the butterfly against the golden step (V4). No
  approximate reduction.
- Negative control: the same proof with the bound weakened in the RTL (e.g. one bit narrower) must fail.

## 9. Quartus (CRG-9)
- New project `quartus/phase05_arith_c4/`; revisions `C4a`, `C4b-B` (Barrett), `C4b-M` (Montgomery), `C4c`, and for
  5d `C4d` + `BCM-ref` (frozen `base_case_multiply.sv`, standalone) *[D3]*. Same device, virtual pins and QSF
  assignments as `C3-P6.qsf`; only top entity, output folder and RTL list differ.
- Constraint *[D1]*: suggestion - `create_clock -period 40.000` for every C4 revision (comparable with C3-P6), plus
  one extra compile of the final C4 configuration **and** of C3-P6 at 20.000 ns, reported as information.
- Settings *[D2]*: suggestion - Quartus defaults as in Phase 4; optionally one GHRD-settings compile of the final C4
  (compare with C3-P6-ghrdset 11,053 ALM).
- Seeds *[D7]*: suggestion - default seed for every revision; seeds 1–6 for the two 5b candidates (12 compiles) so
  the 5b choice does not rest on one seed; C3-P6's seeds 1–6 already exist.
- One compile at a time, in the background; reports extracted with the `/quartus-report` skill; per-entity ALM of
  every reducer and the top-path class report (`scripts/quartus/phase5_top_paths.tcl` on a copy of the project,
  `scripts/quartus/phase5_path_classes.py`) for every revision, so that a change of the critical path is visible.

## 10. Success criteria per sub-step (roadmap PASS: "every attempted sub-step correct and measured")
| Sub-step | Required (PASS) | Reported (not a pass condition) |
|---|---|---|
| 5a | correct (Section 7); revision `C4a` compiled; NTT/INTT cycles 119/375; timing at the D1 constraint met **or** the failure documented | Δ ALM, Δ registers, Δ DSP, Δ Fmax and Δ slack vs C3-P6 (same constraint, settings, seed); reducer per-entity ALM; path classes |
| 5b | both candidates correct and compiled; selection rule (ADR, written before compiling) applied; ADR recorded | same deltas for both candidates (and per seed if D7) |
| 5c | formal bound proof PASS with negative control; correct; `C4c` compiled - or "not attempted" | change of the M → X segment slack |
| 5d | correct (exhaustive or bounded per D3); `C4d` and `BCM-ref` compiled - or "not attempted" | DSP and ALM vs `BCM-ref` |
Any revision above 12,573 ALM or not meeting the D1 constraint is reported as such; it is not hidden and not
"fixed" by a waiver, false path or weakened check.

## 11. 5b selection rule - proposal, to be accepted as an ADR before any 5b compile *[D8]*
*Step 1.* Build, verify and compile both candidates (and seeds per D7) before applying the rule.
*Step 2 - candidate conditions (all must hold):* correct (Section 7); cycles exactly 119 / 375; ALM ≤ 12,573
(fitter "ALMs needed"); timing met at the D1 constraint (non-negative setup and hold at every reported corner).
*Step 3 - metric.* Fmax(c) = lowest slow-corner Fmax (median over seeds if D7 gives several). Cycles are equal by
condition, so time per NTT is proportional to 1/Fmax.
*Step 4 - selection.* Highest Fmax wins, unless the other candidate is within 5% of it (near tie); in a near tie
the candidate with fewer ALMs wins; if their ALM also differ by less than the measured seed spread of C3-P6
(32 ALM), the team decides (suggested tie-break: Barrett, because it needs no Montgomery-form tables).
*Step 5.* If no candidate qualifies, nothing is selected automatically; results are reported and the team decides.
Expectation stated beforehand (INFERENCE from Section 2): Fmax is likely to tie because the critical path lies in
the memory read path; the rule then reduces to ALM.

## 12. Evidence layout
`evidence/phase05/`: `test_plan.md` (this file), `baseline/` (critical-path analysis), `5a/` … `5d/`
(exhaustive-test logs, cocotb logs, formal logs, Quartus evidence files, path-class reports, worksheets),
`docs/results/phase05.md` (one section per sub-step; Approval box left empty), ADR for 5b, row C4 (one sub-row
per sub-step) in the ablation matrix of `docs/ROADMAP.md`, `docs/reports/CHIPATON_Phase5_Report.pdf` (Bahasa
Indonesia, generated by a script modelled on `scripts/build/build_phase4_report.py`), new `HANDOFF.md`.

## 13. Team decisions (answered 2026-10-01, Faza Dzil, Team J5)
| # | Question | Decision |
|---|---|---|
| D0 | Phase 5 objective given Section 2 | ADR 0010: 50 MHz kept as best-effort project target, not a Phase 5 gate; ADR 0006 expectation corrected; memory / P / schedule work in a separate phase or sub-phase after 5a/5b (name and position open, PENDING #19) |
| D1 | Constraint for C4 revisions | ADR 0011: 40.000 ns for every C4 revision; final C4 and C3-P6 additionally compiled at 20.000 ns (information) |
| D2 | Budget, settings, DSP | ADR 0011: 12,573 ALM unchanged; Quartus defaults; DSP reported, no DSP limit |
| D3 | 5c and 5d | ADR 0011: decided after the 5a / 5b results; plans kept |
| D4 | Reading of 5a | ADR 0011: reading (ii), boundary to 5b as in Section 3 |
| D5 | Register positions inside P = 6 | ADR 0011: no moves between memory and multiplier path in Phase 5; multiplier path keeps exactly 3 registers |
| D6 | Operand contract | ADR 0011: exact for a, b in [0, q); operands ≥ q reported, not required |
| D7 | Seeds | ADR 0011: default seed for all; seeds 1–6 for the two 5b candidates |
| D8 | 5b selection rule | ADR 0011 (the rule of Section 11, made precise there: per-seed qualification, median Fmax and median ALM) |

Later timing work (outside Phase 5): ADR 0012 - more cycles only if t_NTT and t_INTT at the measured Fmax beat C3-P6
and constant-cycle holds; NTT core ≤ 12,573 ALM remains the limit.

## 14. Amendments (register positions and design details fixed before each compile)

**A1 - 5a, revision C4a (2026-10-01, before any C4a compile).**
- Reducer `rtl/arith/modmul_fold.sv`: stages F_1..F_5 (folds v → 767·(v >> 12) + (v mod 2^12), widths 22, 20, 17,
  15, 14 bits) and S (one select among v, v − q, v − 2q, both subtractions in parallel). Upper bounds for every
  24-bit input (perhitungan tim, then confirmed by V2 over all 2^24 12-bit pairs): 3,144,960 → 592,384 → 114,543
  → 24,804 → 8,697 < 3q.
- Register positions (multiplier path, 3 registers, ADR 0011 D5): **X, F_3, F_5** (`REG_AFTER` bits 0, 3, 5 = 41).
  Segments: product → X; F_1–F_3 → reg; F_4–F_5 → reg; S + butterfly `add_mod`/`sub_mod` + memory write.
  Reason: the C3-P6 segment D_11 → memory (2 reduction stages + butterfly + write) is its second-longest (≈ 23.6 ns,
  `baseline/c3p6_critical_path.md`); placing only the one select stage there shortens it; the first two
  segments hold three and two fold stages. Memory cuts unchanged (A_4, A_11, M).
- Wrapper `rtl/ntt/ntt_core_c4a.sv` (top of revision C4a); core `rtl/ntt/ntt_core_c4.sv` = `ntt_core_c3.sv` with the
  reducer / butterfly instances replaced through `rtl/arith/modmul_sel.sv` and `rtl/arith/butterfly_c4.sv` (diff
  limited to those lines).
- Quartus: project `quartus/phase05_arith_c4/`, revision `C4a`; QSF = `C3-P6.qsf` with only top entity, output
  folder and RTL list changed; SDC = `C3.sdc` (40.000 ns) copied unchanged; default seed and settings.

**A2 - core negative control (2026-10-01, after the first core run, before any Quartus result).**
- V5/V7 reuse the Phase 4 core test `tb/ntt/test_ntt_core_c3.py` unchanged (runner `tb/arith/run_c4_core_tests.py`).
- The first C4 negative control (fold reducer, RdLat 1 + WrDly 7, P = 8) was **not** a valid negative control: the
  scoreboard tripped, but 0 of 5 NTT results were wrong on both simulators
  (`5a/negctl_first_attempt_rd1_wr7.txt`). Reason (INFERENCE): the memory performs a read RdLat cycles
  after the request, so the physical read-after-write hazard depends on **WrDly** (registers after the read),
  not on P; WrDly 7 is within the schedule slack of 7. Scoreboard check (a) flags at request time and is therefore
  conservative.
- The negative control is now RED_KIND 0 with RdLat 0 + WrDly 8 (the fold reducer has only 7 stage boundaries),
  i.e. Phase 4's negative control through the C4 core; it must trip the scoreboard and give 5/5 wrong results.
- Consequence outside Phase 5 (reported to the team; nothing changed in Phase 5): the stall table of
  `baseline/decision_package.md` (a) assumes the hazard depends on P and is therefore conservative;
  registers added **before** the read (RdLat) would not need stalls on this evidence. The later memory / P phase must
  confirm this in simulation and needs a scoreboard that models the read at request + RdLat (a new test file; the
  Phase 4 test stays frozen).

**A3 - 5b candidates, revisions C4b-B and C4b-M (2026-10-01, before any 5b compile).**
- Barrett `rtl/arith/modmul_barrett.sv` (RED_KIND 2): stages S_1 quotient estimate t = (x·5039) >> 24 (the product
  x·M is left to the tool), S_2 remainder r = x − t·q (t·q shift-and-add), S_3 select r or r − q. r < 2q for every
  24-bit x (largest r = 5,713, perhitungan tim over all 2^24 values; confirmed by V2).
- Montgomery `rtl/arith/modmul_montgomery.sv` (RED_KIND 3, R = 2^12): S_1 m = −769·(x mod 2^12) mod 2^12 (q' = 3327 ≡
  −769, shift-and-add), S_2 t = (x + m·q) >> 12 (m·q shift-and-add), S_3 select. t < 2q because x ≤ (q−1)² < q·R.
  Constant operands in Montgomery form: `rtl/arith/twiddle_rom_mont.sv` generated by
  `scripts/build/gen_twiddle_rom_mont.py` from `tb/golden/primitives.py`; INTT scaling constant 3303·2^12 mod q = 32
  (computed at elaboration in `ntt_core_c4.sv`). V7 = `tb/arith/check_mont_rom.py`.
- Register positions for both (3 registers, ADR 0011 D5): **X, S_1, S_2** (`REG_AFTER` bits 0, 1, 2 = 7). Segments:
  product → X; S_1 → reg; S_2 → reg; S_3 + butterfly `add_mod`/`sub_mod` + memory write. Same placement rule as A1
  (one select stage before the write path). Memory cuts unchanged.
- V2/V3 for Montgomery drive the second operand in Montgomery form through a simulation-only wrapper
  (`tb/arith/c4_tb_wrappers.sv`), so results are still compared against (a·b) mod q for every pair; the butterfly test
  converts ζ the same way.
- Wrappers `rtl/ntt/ntt_core_c4b_b.sv`, `rtl/ntt/ntt_core_c4b_m.sv`; Quartus revisions `C4b-B`, `C4b-M` and their seed
  copies `C4b-B-s2..s6`, `C4b-M-s2..s6` (only `SEED` and output folder differ), all at 40.000 ns, Quartus defaults.

**A4 - 5c lazy reduction, revision C4c (2026-10-01, ADR 0014, before any 5c RTL or compile).**
- Design: `rtl/arith/lazy_bfly_io.sv` (combinational input / output logic of the INTT lazy butterfly: u = b + q − a,
  s = a + b, output a' = s ≥ q ? s − q : s, b' = t; NTT mode as before), `rtl/arith/modmul_barrett_lazy.sv` (Barrett with
  a 13-bit second operand, 25-bit product, same constant M = 5039 and stages S_1..S_3; r < 2q for every product up to
  (q−1)·(2q−1) = 22,154,496, perhitungan tim over all values), `rtl/arith/butterfly_c4_lazy.sv` (I/O logic + reducer + 13-bit
  side delay), parameter `LAZY` of `rtl/ntt/ntt_core_c4.sv` (default 0 = unchanged), wrapper `rtl/ntt/ntt_core_c4c.sv`
  (RED_KIND 2 for the scaling multiplier, LAZY 1). Register positions as C4b-B: X, S_1, S_2; memory cuts A_4, A_11, M.
- Tests (both simulators where applicable):
  - V2-lazy: exhaustive `modmul_barrett_lazy` over z in [0, q) and u in [0, 2q) (22,164,482 pairs) against (z·u) mod q
    at REG_AFTER 0 and 7; info: all 12-bit z × 13-bit u; negative control (t·(q−1)) must fail;
  - V2 (D6 domain) also for `modmul_barrett_lazy` restricted to u < q, as a regression of 5b;
  - V4: the Phase 4 butterfly test (`tb/ntt/test_butterfly_pipe.py`) unchanged on `butterfly_c4_lazy`, plus INTT corners
    a = 0, b = q−1 (u = 2q−1); a = q−1, b = 0 (u = 1); a = b = q−1 (s = 2q−2) with every twiddle;
  - V5–V7: core tests unchanged on `ntt_core_c4c` (bit-exact, scoreboard, cycles exactly 119 / 375) and C4a / C4b-B /
    C4b-M / RED_KIND 0 again after the core change; negative controls as before;
  - V8-lazy (formal, §8): `lazy_bfly_io` with assumes a, b, t < q, prove u < 2q, s < 2q, (u ≥ q ? u − q : u) =
    sub_mod(b, a), a' < q, b' < q, a' = add_mod(a, b) in INTT; NTT outputs = add_mod / sub_mod of (a, t); negative
    control: a copy whose output does not reduce s must fail. The reducer itself is covered by V2-lazy (exhaustive), not
    by the formal proof (stated as the proof's scope);
  - V8 (control), V9 (regression) as before.
- Quartus: `C4c`, `C4c-s2..s6`; adoption by the rule of ADR 0014 §4, applied by script from evidence files.
