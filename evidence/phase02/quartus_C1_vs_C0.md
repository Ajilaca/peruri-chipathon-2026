# MEASURED — Quartus C1 vs C0 comparison (Phase 2, config C1: banked memory at NUM_BANKS=1)

- Generated: 2026-09-29 UTC, from `evidence/quartus/C0.md`,
  `evidence/quartus/C1.md`, and a read-only `quartus_sta` drill-down
  (`quartus/phase02_mem_c1/report_worst_path.tcl`) on C1's existing post-fit netlist.
- Same provisional constraint as C0: `quartus/phase02_mem_c1/C1.sdc` = `quartus/phase01_ntt_c0/C0.sdc`
  verbatim (20.000 ns on `clk_i`), same device (5CSEBA6U23I7), same virtual-pin methodology.
- C1 = C0's FSM/butterfly/twiddle-ROM, byte-for-byte, with `rtl/ntt/poly_mem.sv` replaced by
  `rtl/mem/poly_mem_banked.sv #(.NUM_BANKS(1))` (`rtl/mem/ntt_core_c1.sv`).

## 1. Did every stage complete?

All four (Analysis & Synthesis, Fitter, Assembler, Timing Analyzer) completed with 0 errors, same
as C0. The Timing Analyzer's `Critical Warning (332148): Timing requirements not met` still fires
**4 times** (once per corner) -- unchanged from C0. (Note: `extract_quartus_report.py`'s automated
critical-warning count in `evidence/quartus/C1.md` reads 0 because it was pointed at
`C1.flow.rpt`, which does not carry the Timing-Analyzer-stage critical warnings; the correct count,
read directly from `C1.sta.rpt`, is 4 -- same as C0. Recorded here so the automated "0" is not
mistaken for "no critical warnings existed".)

## 2. Measured comparison

| Quantity | C0 (Phase 1) | C1 (Phase 2) | Change |
|---|---|---|---|
| ALM | 7,010 / 41,910 (17%) | 6,749 / 41,910 (16%) | **-261 ALM** |
| Registers | 3,104 | 3,105 | +1 |
| RAM Blocks (M10K) | 0 / 553 | 0 / 553 | **no change -- see Section 4** |
| Block memory bits | 0 / 5,662,720 | 0 / 5,662,720 | no change |
| DSP blocks | 3 / 112 | 3 / 112 | no change |
| Fmax, Slow 100C | 14.64 MHz | 14.99 MHz | +0.35 MHz |
| Fmax, Slow -40C | 14.69 MHz | 15.05 MHz | +0.36 MHz |
| Worst setup slack, Slow 100C | -48.323 ns | -46.720 ns | +1.603 ns (still failing) |
| Worst setup TNS, Slow 100C | -143,688.194 ns | -139,926.248 ns | improved, still very negative |
| Worst hold slack | 0.211 ns (met) | 0.168 ns (met) | still met |
| NTT / INTT cycles (simulation) | 897 / 1153 | 897 / 1153 | **0 -- identical, 0 stall cycles** |

Sources: `evidence/quartus/C0.md`, `evidence/quartus/C1.md`,
`evidence/phase01/quartus_C0_timing_analysis.md`,
`evidence/phase02/cocotb_regression.txt`.

## 3. Root cause -- unchanged from C0

The worst path is still register-to-register through the arithmetic, ending in a memory register:
`layer_q[0]` -> `poly_mem_banked:u_mem|g_bank[0].mem[28][1]`, data delay **66.087 ns** (vs C0's
67.684 ns), 46 logic levels, 252 references to the same combinational `lpm_divide` cells inferred
from `%` in `rtl/ntt/modmul_reduce.sv` on the path (`quartus/phase02_mem_c1/output_files/C1_worst_setup_path.rpt`).
**Phase 2 did not touch `rtl/ntt/modmul_reduce.sv` or any other arithmetic**, so this is expected,
not a new finding -- the small (~1.6 ns) slack improvement is attributed to a different
placement/routing outcome around the swapped memory module, not to any arithmetic or timing fix.
Fixing this is Phase 4 (pipelining) / Phase 5 (arithmetic) scope, per `docs/ROADMAP.md`.

## 4. Honest finding: M10K was NOT used, despite Phase 2's own title

`docs/ROADMAP.md` Phase 2's implementation scope says "M10K polynomial storage". The measured
result is **0 / 553 RAM Blocks used** -- identical to C0. From the Analysis & Synthesis log
(`quartus/phase02_mem_c1/output_files/C1.map.rpt`):

```
Info (276014): Found 5 instances of uninferred RAM logic
    Info (276007): RAM logic "poly_mem_banked:u_mem|bank_map_rom:u_map_b|Ram0" is uninferred due to asynchronous read logic
    Info (276007): RAM logic "poly_mem_banked:u_mem|bank_map_rom:u_map_b|Ram1" is uninferred due to asynchronous read logic
    Info (276007): RAM logic "poly_mem_banked:u_mem|bank_map_rom:u_map_a|Ram0" is uninferred due to asynchronous read logic
    Info (276007): RAM logic "poly_mem_banked:u_mem|bank_map_rom:u_map_a|Ram1" is uninferred due to asynchronous read logic
    Info (276004): RAM logic "twiddle_rom:u_rom|rom_zeta" is uninferred due to inappropriate RAM size
```

Only `bank_map_rom` and `twiddle_rom` are named here -- `poly_mem_banked`'s own 256-entry storage
array is not even *recognized* as a RAM candidate in this log, and the near-unchanged register
count (3104 -> 3105) confirms it is still built from flip-flops, exactly like C0's `poly_mem.sv`.
The `-261 ALM` change is therefore attributed to the (small, cheap) `bank_map_rom` logic and to
different flip-flop/mux packing around the swapped module, **not** to any RAM-block savings.

**Root cause**: both `rtl/ntt/poly_mem.sv` (C0) and `rtl/mem/poly_mem_banked.sv` (C1) use
*asynchronous* (combinational) read ports, so a single-cycle butterfly (read both operands,
compute, write both results, same cycle) can complete without a read-latency register stage.
Quartus's M10K inference requires a *synchronous* read for this exact reason (message 276007
above says so directly). Reaching M10K would need a design that reads its operands into a
register one cycle before they are used -- a scheduling change, not something to retrofit
quietly into C1 without team review, since it changes the FSM's cycle count (currently proven
identical to C0 at 897/1153 -- CRG-7's own requirement this phase).

This is recorded as a limitation, not corrected in this phase: `docs/ROADMAP.md`'s own Phase 2
PASS criteria ("Conflict-freedom proven for all four L values; measured stall cycles = 0 at
L = 1; bit-exact; constant cycle count; C1 row filled") do not require nonzero M10K usage, and
none of that criteria's wording is weakened here -- the honest 0 is what is filled into the C1
row (`docs/ROADMAP.md`).
