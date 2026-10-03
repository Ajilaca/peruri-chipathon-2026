<!-- claim-lint: skip-file (internal evidence record, not proposal text) -->
# 50 MHz question, option 1: critical-path analysis of S7 and S8 (2026-10-03, team request "jalankan opsi 1 dan 2")

Method (read-only, MEASURED): `scripts/phase5m_top_paths.tcl` run with `quartus_sta` on a **copy** of `quartus/phase05m_memsched/` (the database of revisions S7 and S8, seed 1, 40.000 ns; the repository
`.qpf` is never opened by the analysis), 300 worst setup paths per corner (Slow 1100 mV 100 C and -40 C), three in full detail; grouped by start and end block with `scripts/phase5_path_classes.py`
(bit indices collapsed). Files: `S7_top300_path_classes_slow{100,-40}.txt`, `S8_top300_path_classes_slow{100,-40}.txt`, `S7_worst_path_slow-40_2026-10-03.txt`.

## Worst path classes (slack at 40.000 ns; path delay = 40 - slack, INFERENCE)
| Rev / corner | Worst class | Slack (ns) | Next class |
|---|---|---|---|
| S7 / -40 C | bank map ROM (inferred as M10K, `bank_map_rom:g_map[4]`) -> slot-arbitration ripple ports 4..10 -> cut register `g_arb[10].count_q` (cut A_11) | 14.439 (16 paths) | multiplier cut 2 (`u_mul.cut2`) -> memory write (storage flip-flops): 17.711 (269 paths) |
| S7 / 100 C | same | 14.617 | same, 17.770 |
| S8 / -40 C | same arbitration class | 15.135 | `layer_q` -> RAM; `bank_rdata_q` -> multiplier cut 0: 19.015 (the S7 write-path class is gone) |

Worst S7 path in detail (`S7_worst_path_slow-40_2026-10-03.txt`): clock to the M10K 7.043 ns, M10K clock-to-out 1.080 ns, then about 22.6 ns of mux / add cells of the arbitration ripple (`Mux7` ... `Mux18`,
`count_c` of ports 4 to 10) up to `g_arb[10].count_q`; data path 23.932 ns, clock skew -1.569 ns.

## Reading (INFERENCE)
- After S7 the limit is **the slot arbitration between the cuts A_4 and A_11** (seven ports of the ripple), fed by the bank-map ROM that Quartus placed in an M10K block (this also explains part of
  the M10K count of 31 / 33: the bank-map ROMs are inferred as RAM blocks; not decomposed further).
- For 50 MHz (20 ns) both the arbitration segment (about 25.6 ns at -40 C) and the multiplier-to-write segment (about 22.3 ns) must drop below about 19-20 ns. S8's write register removed the second
  class but not the first, which is why S8 did not raise Fmax.
- The arbitration depends only on addresses, i.e. on the fixed schedule, never on data. Two ways to remove it, both new steps for the team: (a) **S10** (16 x 1R1W banks, ADR 0022): no slot arbitration at all;
  (b) a precomputed arbitration table (slot and offset per port and cycle from a ROM indexed by mode, layer and t) in place of the ripple. More arbitration cuts are a third way, with stalls (P > 7).
- Quartus option without RTL: keeping the bank-map ROM out of M10K (logic ROM) would replace the RAM block clock-to-out (1.080 ns) and its clock-path skew (-1.569 ns) at the start of the path by a logic ROM delay (effect not measured).

## Option 2: S7 at 20.000 ns, seeds 1-6 (MEASURED, `quartus_S7-20[-s2..s6]_20261002.md`, `quartus/phase05m_memsched/run_s7_20_sweep.sh`)
| Seed | ALM | Worst setup (ns, all corners) | Worst hold (ns) | Fmax lowest slow corner (MHz) |
|---|---|---|---|---|
| 1 | 9,365 | -1.388 | 0.151 | 46.76 |
| 2 | 9,358 | -1.655 | 0.127 | 46.18 |
| 3 | 9,359 | -2.296 | 0.136 | 44.85 |
| 4 | 9,383 | -2.431 | 0.125 | 44.58 |
| 5 | 9,369 | -1.933 | 0.124 | 45.59 |
| 6 | 9,355 | -1.615 | 0.150 | 46.26 |

Timing at 20.000 ns met at **0 of 6 seeds**; median lowest-corner Fmax 45.885 MHz (INFERENCE: median). Under the 20 ns constraint the fitter works harder than at 40 ns, so these Fmax values are not comparable
with the 40 ns figures. Note: a status message of 2026-10-03 quoted "-0.836 ns" for seed 1; that was the Slow 100 C setup line only; the worst over all corners is -1.388 ns (corrected here).
