<!-- claim-lint: skip-file (internal analysis record, not proposal text) -->
# C3-P6 critical-path analysis (Phase 5 baseline, before any Phase 5 RTL)

Labels: **MEASURED** = printed by the Quartus Timing Analyzer for the database listed below; **INFERENCE** = derived
from measured numbers; **ESTIMATE** = projection, not measured.

## 1. Source and method
- Database: the Phase 4 compile of revision `C3-P6` (default seed, 40.000 ns, Quartus Prime Lite 25.1std.0 Build 1129),
  the same compile as `evidence/phase04/quartus_C3-P6.md`. Its `db/C3-P6.*` files and
  `output_files_P6/` were **copied** to a folder outside the repository and analysed there (running `project_open` on
  the repository's `.qpf` rewrites it). No compile was run; nothing in the repository's Quartus folder was changed.
- Check that the copy is the measured compile (MEASURED): worst setup slack at Slow 1100mV 100C = **10.753 ns**,
  identical to the evidence file above.
- Scripts (in the repository): `scripts/quartus/phase5_top_paths.tcl` (300 worst setup paths, summary + 3 full paths, Slow
  1100mV 100C), `scripts/quartus/phase5_path_classes.py` (groups the 300 paths by start/end block; output
  `c3p6_top300_path_classes_slow100.txt` in this folder). Per-segment worst paths were taken with
  `get_timing_paths -from <cut registers> -to <next cut>` in the same session.
- Only the Slow 1100mV 100C corner was analysed (the corner with the worst setup slack). Other corners: NOT MEASURED.

## 2. The 300 worst setup paths (MEASURED, Slow 1100mV 100C)
| Start | End | Worst slack | Paths among the 300 |
|---|---|---:|---:|
| memory slot-arbitration register (cut M: `g_arb[*].g_reg.slot_q`) | multiplier output register (cut X, `u_mul.cut0`) | **10.753 ns** | 168 |
| memory slot-arbitration register (cut M: `g_arb[*].g_reg.bank_q`) | cut X | 11.654 ns | 24 |
| cut M | M10K write-data registers (Quartus-inferred RAM) | 11.495–15.022 ns | 96 |
| M10K write-enable register | arbitration counter `count_q` | 15.469 ns | 12 |

Slack range of the 300 paths: 10.753 to 15.566 ns. **No path inside the reducer** (`modmul_reduce_staged` stages
after cut X) is among the 300 worst.

## 3. Worst path broken down by block (MEASURED incremental delays from the full-path report)
Path: `g_arb[15].g_reg.slot_q[26]` → lane 6 `u_mul|g_cut[0]` (INTT input `sub_mod(b, a)` → DSP multiplier),
data path 29.345 ns.

| Segment (cumulative arrival, ns) | Delay (ns) | Block |
|---|---:|---|
| 6.045 → 27.337 | 21.292 | read-address decode and read mux of `poly_mem_multiport_pipe` (`raddr0`, `Mux111`, `Mux376`, `Mux368`) |
| 27.337 → 31.685 | 4.348 | butterfly input `sub_mod(b, a)` (two carry chains + select) |
| 31.685 → 35.390 | 3.705 | routing into the DSP block + DSP multiplier to cut X |

Segment boundaries are the block names in the report (INFERENCE on which element belongs to which block).

## 4. Worst path per register segment of the multiplier path (MEASURED slack; delay column INFERENCE)
| Segment | Worst slack @ 40.000 ns | ≈ period consumed (40 − slack) |
|---|---:|---:|
| cut M → cut X (read mux + `sub_mod` + multiplier) | 10.753 | ≈ 29.2 ns |
| lane cut X → cut D_5 (5 reduction stages) | 24.457 | ≈ 15.5 ns |
| lane cut D_5 → cut D_11 (6 reduction stages) | 23.592 | ≈ 16.4 ns |
| lane cut D_11 → memory (2 reduction stages + `add_mod`/`sub_mod` + write) | 16.382 | ≈ 23.6 ns |
| scale cut X → D_5 / D_5 → D_11 / D_11 → memory | 24.457 / 24.781 / 19.994 | ≈ 15.5 / 15.2 / 20.0 ns |

"40 − slack" includes clock skew, uncertainty and setup time; it is an approximation of the segment's share of the
period, not a pure logic delay.

## 5. Reading (INFERENCE)
- At P = 6 the clock is limited by the **memory read path plus the butterfly input and the multiplier**, not by the
  reduction. The reduction segments use about 15–16 ns of the 40 ns period; the D_11 → memory segment about 23.6 ns.
- The memory read part alone (about 21.3 ns of data delay) is longer than a 20.000 ns period. A reducer change cannot
  shorten it, and Phase 5 keeps the memory, schedule, L and P fixed (`docs/ROADMAP.md` Phase 5). On this evidence,
  **20.000 ns (50 MHz) is not reachable by Phase 5 arithmetic changes alone**; ADR 0006 expected Phase 5 to be needed
  for 50 MHz, based on the P = 0 breakdown in which the divider was about 44 ns.
- What arithmetic can still affect on the critical segment: the `sub_mod(b, a)` before the multiplier (about 4.3 ns)
  and the multiplier itself (about 3.7 ns). Removing all of it would leave the M → X segment at about 25 ns
  (ESTIMATE: 29.2 − 4.3; ignores re-placement), i.e. about 40 MHz, still short of 50 MHz.
- What the reducer change can affect: ALM, the D_11 → memory segment, and - only if the team allows the register
  positions inside P = 6 to move - the balance between segments. Per entity in `C3-P6.fit.rpt` (MEASURED): lane
  reducers `modmul_reduce_staged:u_mul` 153.2–157.2 ALM each (305 ALUTs, 1 DSP each), scaling reducer `u_scale_mul`
  148.9 ALM; butterfly logic outside the reducer 103.8–112.8 ALM per lane; `poly_mem_multiport_pipe` 7,660.7 ALM;
  `ntt_core_c3` 10,484.5 ALM. Sum of the nine reducers: 1,395.8 ALM (INFERENCE), the upper bound of what replacing
  the reducer alone could save.
- One seed, one corner, one revision. Phase 4 seed spread: 32.60–34.20 MHz for C3-P6.
