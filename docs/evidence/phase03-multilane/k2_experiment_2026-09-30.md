<!-- claim-lint: skip-file (internal experiment record, not proposal text) -->
# Phase 3 supplementary experiment K2 — narrow sub-cycle counter (`t_q`) on C2

- Date (UTC): 2026-09-30
- Branch: `phase3-multilane`, on top of `f155f32` (Phase 3 C2 sweep, unchanged)
- Status: **completed, accepted by the team as a finished experiment — valid but insufficient**
- Baseline kept frozen: `rtl/ntt/ntt_core_c2.sv` and every Phase 3 evidence file
  (`docs/evidence/quartus/C2-L{1,2,4,8}-20260929.md`, `docs/results/result_phase3.md`) are untouched.

## Why this experiment exists
C2-L8 measured 11,446 ALM, 968 ALM over ADR 0004's 10,478 ALM (25%) budget. The team asked whether
L=8 can be brought under budget while keeping everything that makes the comparison fair: NUM_LANES=8,
8 butterflies per cycle, bit-exact, NTT=113 / INTT=369 cycles, no pipelining (Phase 4), no change to
the modular arithmetic, no large memory-architecture change. The per-entity audit is in
`l8_opt_entity_breakdown_2026-09-30.txt` (C2-L4 vs C2-L8 section); K2 was its lowest-risk candidate.

## What changed
`rtl/ntt/ntt_core_c2_k2.sv` is a copy of `rtl/ntt/ntt_core_c2.sv` with exactly three logic edits
(module name, `TW`, and an explicit `8'(t_q)` zero-extension):

- C2: `t_q` is a fixed 8-bit register for every NUM_LANES.
- K2: `t_q` is `$clog2(128/NUM_LANES)` bits (7/6/5/4 bits for L=1/2/4/8) -- exactly wide enough for
  its reachable range 0..TMax. Same values, same FSM, same schedule.

Supporting files: `rtl/ntt/ntt_core_c2_k2_l8.sv` (Quartus wrapper), revision
`quartus/phase03_multilane_c2/C2-L8-K2` (QSF differs from C2-L8 only in top entity, output folder and
the two RTL files; SDC identical), `formal/phase03-multilane/ntt_core_c2_k2_*`,
`tb/ntt/run_ntt_c2_tests.py <sim> k2` (new optional argument; default still runs the frozen C2), and
`scripts/quartus_entity_breakdown.py` (groups the fitter's per-entity table).

## Results
| Check | Result | Evidence |
|---|---|---|
| Lint (Verilator `-Wall`, all four L) + slang | clean | `cmd: verilator --lint-only -Wall --timing -sv rtl/ntt/*.sv rtl/mem/*.sv --top-module ntt_core_c2_k2 -GNUM_LANES=<L>` |
| cocotb, Verilator + Icarus, L=1/2/4/8 | 16/16 + 16/16, bit-exact | `k2_cocotb_regression_2026-09-30.txt` |
| Cycle counts | identical to C2 for every L (L=8: NTT 113, INTT 369) | same file |
| Formal (SymbiYosys) | unchanged vs C2: L=1 PASS; L=2/4/8 UNKNOWN (same `bank_overflow_o` induction issue as C2) | `k2_formal_2026-09-30.txt`, `formal_verification_2026-09-29.txt` |
| Quartus C2-L8-K2 | see table below | `docs/evidence/quartus/C2-L8-K2-20260930.md` |

| MEASURED (Quartus) | C2-L8 | C2-L8-K2 | Delta |
|---|---|---|---|
| ALM | 11,446 / 41,910 | 11,232 / 41,910 | **−214** |
| ADR 0004 budget (10,478) | over by 968 | **over by 754** | |
| Registers | 3,100 | 3,095 | −5 |
| DSP | 17 / 112 | 17 / 112 | 0 |
| M10K | 0 / 553 | 0 / 553 | 0 |
| Fmax (Slow 100C) | 7.62 MHz | 7.85 MHz | +0.23 |
| Worst setup slack @ 20.000 ns | −111.219 ns | −107.314 ns | timing still **NOT met** |
| Critical warnings | 5 (15725, 332148) | 5 (same two) | |

Where the saving came from (`l8_opt_entity_breakdown_2026-09-30.txt`, K2 section): `ntt_core_c2`
own logic −132.6 ALM, `poly_mem_multiport` own logic −91.9 ALM; every other group moved by +0.1 to
+6.2 ALM (placement variation).

## Conclusion
K2 is functionally correct, cycle-identical and a real (small) improvement, but it is **insufficient**:
C2-L8-K2 is still 754 ALM over budget, so **L=8 remains ineligible under ADR 0004 and L=4 remains the
candidate**. This matches the audit's bound: the whole `ntt_core_c2` own-logic group is 768 ALM, so no
width fix there could reach 968 ALM on its own.

## Deviation noted during the experiment
The first K2 compile raised 9 × Warning 10335 ("Unrecognized synthesis attribute") because a header
comment line in `ntt_core_c2_k2.sv` began with the word "synthesis", which Quartus parses as a pragma.
The comment was reworded and the design recompiled; every number above is from that second compile
(identical ALM/registers/DSP to the first, 0 × Warning 10335). cocotb and formal were re-run on the
committed file as well.

## Next step (team decision, 2026-09-30)
K1 (one shared modular multiplier per butterfly instead of separate forward/inverse ones) is approved
as a separate, supplementary experiment `C2-K2-K1`, built on K2, measured for all four L (not only
L=8), because it changes the butterfly datapath and so deviates from the written Phase 3 scope
("butterfly, arithmetic and memory as in Phase 2"). Not started yet. ADR 0004 is not changed by this
experiment.
