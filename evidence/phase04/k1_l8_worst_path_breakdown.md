<!-- claim-lint: skip-file (internal evidence record, not proposal text) -->
# Worst setup path of the Phase 4 starting point (C2-K2-K1, L = 8), by block

- Date (UTC): 2026-09-30
- Source: the existing Phase 3 compile of revision `C2-K2-K1-L8`
  (`evidence/quartus/C2-K2-K1-L8.md`); no new compile. Timing query only:
  `report_timing -setup -npaths 1 -detail full_path` at operating condition `7_slow_1100mv_100c`,
  provisional clock 20.000 ns. MEASURED (Quartus Timing Analyzer); the grouping into blocks is a
  classification of the reported path elements by hierarchy name, done by script.
- Purpose: input for the Phase 4 target-clock and pipeline-depth decisions (ADR 0006, ADR 0007).

## Path
- From `ntt_core_c2_k2_k1:u_dut|t_q[2]` to `...|poly_mem_multiport:u_mem|g_bank[6].mem[15][3]`
- Data arrival 135.696 ns, data required 25.527 ns, slack −110.169 ns (VIOLATED) at this corner
  (the worst corner overall is Slow −40C, −110.494 ns, in the evidence file above)
- Data delay 129.607 ns, 107 logic levels

## Delay by block (cell + interconnect increments summed along the path)
| Block | Delay (ns) | Share | Arrival at entry → exit (ns) |
|---|---|---|---|
| Core: address generation (`t_q`/`layer_q` → `j`, `jlen`), port mux | 10.0 (about 4.8 on the read side and 2.6 on the write side between entry and exit; the rest is interconnect into the block) | 7% | 5.5 → 10.3, and 126.0 → 128.6 |
| `bank_map_rom` | 1.5 | 1% | 11.3 → 11.8 |
| Memory access: bank slot arbitration across the 16 ports, read mux, read-data crossbar; and the write mux at the end | 64.0 (56.8 read side, 4.4 write side, rest interconnect between them) | 47% | 12.7 → 69.4, and 130.6 → 135.0 |
| Butterfly: sub/mux before the multiplier, add/sub after | 6.6 | 5% | 70.7 → 74.1, and 124.6 → 125.7 |
| Butterfly: multiplier (DSP) | 4.4 | 3% | 75.4 → 78.5 |
| Butterfly: divider (`%` in `modmul_reduce`) | 45.2 | 34% | 79.3 → 123.7 |
| Clock network to the launch register | 3.2 | 2% | — |

## Finer breakdown of the two long blocks (same path, same query)
Arrival times in ns along the path (clock network 0 → 3.2 included):

| Piece | Arrival at entry → exit | Length | Depends on data? |
|---|---|---|---|
| Address generation, port mux | 3.2 → 10.3 | 7.1 | no (only `layer_q`, `t_q`, `mode_q`) |
| `bank_map_rom` | 10.3 → 11.8 | 1.5 | no |
| Memory: slot arbitration, a ripple across the 16 ports (`count`/`slot` elements alternating with muxes) | 11.8 → 55.0 | 43.2 | no |
| Memory: per-bank sub-port select, read mux, read-data crossbar | 55.0 → 69.4 | 14.4 | yes (read data) |
| Butterfly: inverse-operand sub/mux, then multiplier (DSP) | 69.4 → 78.5 | 9.0 | yes |
| Butterfly: divider, 13 subtract stages (`op_4` … `op_17`), about 3.4 ns each; stage arrivals 79.3, 82.5, 86.4, 89.9, 93.3, 97.5, 101.4, 105.3, 108.6, 112.6, 115.2, 118.2, 121.1 | 78.5 → 123.7 | 45.2 | yes |
| Butterfly: add/sub after the divider | 123.7 → 125.7 | 2.0 | yes |
| Write side: port mux, per-bank sub-port select, write | 125.7 → 135.0 | 9.3 | yes |

The slot arbitration (about 43 ns) is control-only: it is a function of the schedule counters, not of
the polynomial data. That is what allows register stages inside it without touching the datapath.

## Reading
- The largest segment at L = 8 is the **memory access path (about 57 ns on the read side)**, not the
  divider (about 44 ns). At C0 (L = 1) the divider dominated
  (`evidence/phase01/quartus_C0_timing_analysis.md`); the multi-port slot
  arbitration and crossbar added in Phase 3 changed that.
- Consequence for pipelining (ESTIMATE, from the segment lengths above, ignoring register overhead
  and re-routing): registers placed only at block boundaries cannot give a clock period shorter than
  the longest single block, about 57 ns (about 17 MHz). Going below that needs a register inside the
  memory access path; going below about 44 ns (about 22 MHz) also needs one inside the divider chain.
  An even split of 129.6 ns would need about 7 stages for 20 ns and about 4 for 40 ns.
- These are single-path numbers from one compile; other near-critical paths exist and the fitter
  re-places logic when registers are added, so they bound expectations, they do not predict Fmax.

## Reproduce
```tcl
# quartus_sta -t <this script>, run in quartus/phase03_multilane_c2/ after compiling C2-K2-K1-L8
project_open phase03_multilane_c2 -revision C2-K2-K1-L8
create_timing_netlist
set_operating_conditions 7_slow_1100mv_100c
read_sdc
update_timing_netlist
report_timing -setup -npaths 1 -detail full_path -file k1_l8_worst.rpt
delete_timing_netlist
project_close
```
(`project_open` rewrites `phase03_multilane_c2.qpf`; restore it with `git checkout` afterwards.)
