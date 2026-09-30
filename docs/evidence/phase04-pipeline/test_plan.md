# Phase 4 test plan — butterfly pipeline sweep P = 0 / 2 / 4 / 6 (C3), written before any RTL is coded (CRG-4)

- Date (UTC): 2026-09-30. Branch `phase4-pipeline`. No Phase 4 RTL, testbench or Quartus project exists
  at the time of writing.
- Governing decisions: ADR 0005 (start from C2-K2-K1 at L = 8), ADR 0006 (Phase 4 constraint and
  milestone: 40.000 ns; 25 MHz is an experimental target, not a hardware or system requirement; end goal
  20.000 ns after Phase 5), ADR 0007 (P ∈ {0, 2, 4, 6}; registers allowed inside the memory access path
  and the divider; function must stay bit-exact; selection rule). ADR 0004 is unchanged (ALM budget
  10,478).
- Reference: `tb/golden/primitives.py` (`ntt`, `intt`), `tb/mem/bank_model.py`.
- Planning evidence: `k1_l8_worst_path_breakdown_2026-09-30.md` (MEASURED path of the starting point),
  `layer_boundary_slack_2026-09-30.txt` (schedule analysis, perhitungan tim).

## 1. What is built and what stays frozen
**Frozen, not edited in Phase 4:** `rtl/ntt/modmul_reduce.sv`, `butterfly.sv`, `butterfly_shared.sv`,
`twiddle_rom.sv`, `rtl/mem/bank_map_rom.sv`, `poly_mem_multiport.sv`, `ntt_core_c2*.sv` and their
wrappers, all Phase 1–3 evidence.

**P = 0 is not new RTL.** It is the frozen `rtl/ntt/ntt_core_c2_k2_k1_l8.sv` re-compiled with the Phase 4
constraint (revision `C3-P0`). Its simulation evidence is the existing Phase 3 regression, re-run.

**New files planned (names may be adjusted; the separation may not):**
| File | Content |
|---|---|
| `rtl/ntt/modmul_reduce_staged.sv` | (a·b) mod q with the reduction written as explicit conditional-subtract stages so that registers can sit between stages. Same results as `modmul_reduce.sv` for every a, b in [0, q). Parameter: after which stages a register is placed |
| `rtl/ntt/butterfly_shared_pipe.sv` | `butterfly_shared.sv`'s equations with the staged reducer and the operands that bypass the multiplier delayed by the same number of stages |
| `rtl/mem/poly_mem_multiport_pipe.sv` | Memory with separate read and write addressing per port; slot arbitration with optional register stages; the (bank, offset, slot) computed for a port's read is delayed and reused for its write |
| `rtl/ntt/ntt_core_c3.sv` | C2-K2-K1's FSM and schedule, parameter `PIPE ∈ {2, 4, 6}`, valid/address delay line, drain at the end |
| `rtl/ntt/ntt_core_c3_p2.sv`, `_p4.sv`, `_p6.sv` | Thin Quartus wrappers, L = 8 fixed |

The ×3303 INTT scaling pass keeps its own multiplier + staged reducer and uses port 0, with the same
pipeline depth as the butterflies. Sharing that multiplier with a lane is a different optimisation and
is out of scope.

## 2. Register positions per P (fixed here, before anything is measured)
P counts the register stages between the cycle a butterfly's addresses are issued and the cycle its
results are written (ADR 0007). Named cut points, from the measured path of the starting point:

| Cut | Where |
|---|---|
| A_k | inside the slot-arbitration ripple, after it has processed k of the 16 ports (control only: depends on `layer_q`, `t_q`, `mode_q`, never on polynomial data) |
| M | after slot arbitration is complete (per-port bank, offset, slot registered), before the read mux |
| X | after the multiplier (the 24-bit product), before the first reduction stage |
| D_n | inside the reducer, after n of its conditional-subtract stages (13 in the inferred divider of the starting point; the staged reducer's exact stage count N is fixed when it is written, and n scales as round(n·N/13)) |

| P | Cuts | Longest segment expected (ESTIMATE from the single measured path; not a prediction of Fmax) |
|---|---|---|
| 0 | none (frozen C2-K2-K1) | 129.6 ns data delay, MEASURED |
| 2 | A_13, D_3 | about 45 ns — **not expected to meet 40.000 ns** (three equal parts of this path would be about 44 ns); measured anyway, as ADR 0007 requires |
| 4 | A_7, M, X, D_7 | about 30 ns |
| 6 | A_4, A_11, M, X, D_5, D_11 | about 24 ns (the read mux + multiplier segment) |

Rule against tuning after the fact: these positions are used for the measured revisions. If a position
has to change for a correctness or tool reason, this plan is amended with the reason **before** the
Quartus revision concerned is compiled. If a position is changed after a Quartus result has been seen,
the new placement is a separately named revision (for example `C3-P4b`), both results are kept and
reported, and the selection rule is applied to the revisions named in this table unless the team decides
otherwise.

## 3. Hazards and cycle counts (expectations to be checked, not assumed)
- Within a layer every address is read once and written once, so no read-after-write hazard exists for
  any P. At layer boundaries the existing schedule has at least 7 cycles of slack at L = 8 in both
  directions, and 15 cycles before the INTT scaling pass (`layer_boundary_slack_2026-09-30.txt`), so
  P ≤ 6 needs **no stall**. This is an analysis of the Python schedule model; the RTL must demonstrate it.
- Expected cycle counts (ESTIMATE): NTT = 113 + P, INTT = 369 + P (C2-K2-K1 measured 113 / 369; the
  pipeline adds a drain of P cycles at the end). The measured values are what is recorded.
- Stall cycles per P are reported as: measured cycles − (7 × 16 + [256 for INTT] + 1 + P). Expected 0.
- With P > 0 a bank receives up to 2 reads and 2 writes of different addresses per cycle; the read
  schedule and the write schedule each keep the "at most 2 per bank" property separately.

## 4. Verification, per P ∈ {2, 4, 6} (and the existing regression for P = 0)
Every item is run on **both** simulators (Icarus and Verilator) unless stated; a disagreement between
them is investigated before either is trusted.

**V1. Lint / elaboration (CRG-1, CRG-2).** `verilator --lint-only -Wall` and `slang`, 0 warnings, for
each PIPE value and each wrapper. No comment line may begin with the word "synthesis" (Quartus pragma
trap found in Phase 3).

**V2. Staged reducer equals `modmul_reduce` (the "function must not change" check).**
- Exhaustive: every (a, b) in [0, q)², 3329² = 11,082,241 pairs, for every register configuration used
  by P = 2, 4, 6, comparing the staged output (after its latency) with `modmul_reduce` and with the
  integer formula (a·b) mod 3329. Verilator C++ harness, same pattern as `tb/ntt/k1_exhaustive/`.
- Corner cases also as a cocotb unit test: a = 0, b = 0; a = b = q−1; a = 1; b = 1; a = q−1, b = 1;
  products just below and just above multiples of q.
- Latency: the output for an input applied at cycle t appears exactly at t + (number of stages), for
  back-to-back inputs (no bubble needed between them).

**V3. Pipelined butterfly vs golden butterfly step.** Corners (a = b = 0; a = b = q−1; a = 0, b = q−1;
a = q−1, b = 0; zeta = first and last table entries) and 1,000 random (a, b, zeta) per mode with zeta from
the golden table, streamed back-to-back; each result compared at the expected latency.

**V4. Memory variant.** Write then read back every address through every port; simultaneous reads and
writes of different addresses on the same bank in one cycle; a read of an address in the cycle after it
was written returns the new value; `bank_overflow_o` never asserted for the scheduled traffic.

**V5. Core bit-exact (CRG-3).** For each P: `ntt(f)` and `intt(f)` equal `tb/golden/primitives.py` for the
five corner polynomials (all zero; all q−1; impulse at 0; impulse at 255; alternating 0 / q−1) and 100
random polynomials per direction; `intt(ntt(f)) == f` for 50 random polynomials.

**V6. Constant cycle count (CRG-7).** For each P and each direction the start-to-done cycle count is
identical for every corner and 20 random polynomials; the value is recorded and must be the same on both
simulators. This value is `cycles_NTT(P)` / `cycles_INTT(P)` of the selection rule.

**V7. Layer-boundary hazard tests.**
- A testbench scoreboard tracks, for every address, whether a write is still in the pipeline; it fails if
  any read is issued for such an address, or if a read and a write hit the same address in one cycle.
  It runs during all V5 tests.
- Directed data: polynomials whose coefficients differ only at the addresses with the tightest boundary
  slack (from `scripts/pipeline_hazard_slack.py`), so a stale read there changes the result.
- Negative control: a test-only elaboration with a depth beyond the slack (PIPE = 8, never compiled in
  Quartus, never a candidate) must trip the scoreboard and fail bit-exactness. If it does not, the
  scoreboard is not doing its job and V7 is void.

**V8. `bank_overflow_o`** is sampled every cycle of every core test and must stay 0.

**V9. Formal (CRG-8),** with the corrected flow (`formal/run_formal_slang.py`: yosys-slang frontend,
`memory_map -rom-only`), per P: the busy/done handshake; `bank_overflow_o` == 0; counter ranges; the
pipeline valid chain drains exactly P cycles after the last issue; no same-cycle read and write of one
address. Negative controls as in Phase 3 (a corrupted copy of `bank_map_rom` must fail). Scope stated in
the result: control and bank-capacity properties, not arithmetic.

**V10. Regression (CRG-5, CRG-6).** Phase 0 pytest, Phase 1–3 cocotb regressions (including `k2` and `k1`
variants) and `check_params.py` still pass; `run_formal_slang.py` still reports every existing proof as
expected.

**V11. Reference P = 0.** `python3 tb/ntt/run_ntt_c2_tests.py <sim> k1` on both simulators; L = 8 must
still give NTT 113 / INTT 369.

A P value has "bit-exact: PASS" (ADR 0007 condition 1) only if V2, V3, V5 and V7 all pass on both
simulators, and "constant cycle: PASS" (condition 2) only if V6 passes.

## 5. Quartus (CRG-9), all four revisions
- Project `quartus/phase04_pipeline_c3/`, revisions `C3-P0`, `C3-P2`, `C3-P4`, `C3-P6`. Device
  5CSEBA6U23I7, Quartus Prime Lite 25.1std, kernel-only with virtual pins, same assignments as the
  Phase 3 revisions; the QSFs differ only in top entity, output folder and RTL file list.
- One SDC for all four: `create_clock -name clk_i -period 40.000 [get_ports {clk_i}]`,
  `derive_clock_uncertainty`, `set_false_path -from [get_ports {rst_ni}]` — the Phase 3 SDC with only the
  period changed. Fitter seed: the default, as in Phases 1–3, the same for all four.
- `C3-P0` is compiled in the same session as the others; its result is **not** copied from the Phase 3
  evidence (that was at 20.000 ns).
- Evidence, one file per revision, via the `/quartus-report` extractor:
  `docs/evidence/phase04-pipeline/quartus_C3-P<n>_<UTCdate>.md`, plus a per-entity breakdown
  (`scripts/quartus_entity_breakdown.py`, extended for the new module names).
- Recorded per revision: ALM (with the fitter's denominator), registers, M10K, DSP; Fmax for every slow
  corner the Fmax Summary reports; worst setup slack and worst hold slack per corner; message counts.
- **Timing met at 40.000 ns** (ADR 0007 condition 4) = worst setup slack ≥ 0 **and** worst hold slack ≥ 0
  at every corner reported. Negative slack is reported as "timing not met", never softened.
- **ALM ≤ 10,478** (condition 3) uses the fitter's "Logic utilization (in ALMs)" figure.
- Critical warnings are listed and triaged in writing; new warning types relative to Phase 3 are
  explained before the result is used. No false path, multicycle or other exception is added to make a
  revision pass.
- Information only, no extra compile: whether each revision's Fmax would also satisfy the 20.000 ns end
  goal.

## 6. Selection (ADR 0007) — applied only after all four P are measured
Worksheet to be filled from the evidence files (no cell is filled from memory or estimate):

| P | bit-exact | constant cycle | ALM | ≤ 10,478? | worst setup / hold slack @ 40.000 ns | timing met? | cycles_NTT | cycles_INTT | Fmax per slow corner (MHz) | Fmax(P) = lowest | t_NTT (µs) | t_INTT (µs) | candidate? |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | | | | | | | | | | | | | |
| 2 | | | | | | | | | | | | | |
| 4 | | | | | | | | | | | | | |
| 6 | | | | | | | | | | | | | |

1. Candidate set C = the P values for which all four conditions hold: bit-exact PASS, constant-cycle
   PASS, ALM ≤ 10,478, timing met at 40.000 ns (setup and hold, all corners).
2. Fmax(P) = the lowest Fmax among the slow-corner results the Timing Analyzer's Fmax Summary reports for
   that revision (worst-case slow-corner value), as printed, in MHz.
3. t_NTT(P) = cycles_NTT(P) / Fmax(P) and t_INTT(P) = cycles_INTT(P) / Fmax(P), in microseconds; both are
   computed and reported for **every** P, candidate or not. t_INTT does not drive the selection.
4. t_min = min over P in C of t_NTT(P);  d(P) = (t_NTT(P) − t_min) / t_min.
   P_selected = the smallest P in C with d(P) ≤ 0.05 (near-tie: within 5% of the global minimum; the
   smaller P wins). Unrounded quotients are compared.
5. If C is empty, no P is selected automatically: every measured result is reported and the team is asked
   to decide.
6. The rule is applied by a small script that reads the worksheet values (so the arithmetic is
   reproducible), and the chosen P is recorded in a new ADR (ROADMAP Phase 4 PASS criterion), not by
   editing ADR 0007.

Expectation stated in advance so it cannot be mistaken for a result later: P = 0 and probably P = 2 will
not be candidates (timing at 40.000 ns); P = 4 and P = 6 may or may not be, depending on measured timing
and on the ALM budget, whose margin at the starting point is 724 ALM.

## 7. Order of work and stop points
1. This plan approved by the team.
2. Staged reducer + V2 (exhaustive) — nothing else is built on it until V2 passes.
3. Memory variant + V4; pipelined butterfly + V3.
4. Core for P = 2, 4, 6 + V1, V5–V8, V10, V11.
5. Formal V9.
6. Quartus: all four revisions; evidence extracted; critical warnings triaged.
7. Worksheet filled; selection rule applied; results reported to the team.
8. New ADR for the chosen P (or the "no candidate" report); `docs/results/result_phase4.md`; ROADMAP C3
   rows. Approval box left for a human.

Stop and report instead of continuing if: V2 finds any mismatch; the negative control in V7 does not
fail; a simulator disagreement cannot be explained; or a change to a frozen file appears necessary.

## 8. Explicitly out of scope for Phase 4
Any change to the reduction method's results or to q, n, the twiddle values or other FIPS 203 quantities;
Barrett / Montgomery / lazy reduction (Phase 5); M10K mapping; layer merging; Keccak; changing L or the
lane schedule; P values other than {0, 2, 4, 6} as measured candidates; sharing the scaling multiplier;
changing the clock constraint after the sweep has started; timing exceptions to turn a result green; any
speed-up claim against software or literature; any claim of hardware validation (no board attached).
