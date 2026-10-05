<!-- claim-lint: skip-file (internal analysis record, not proposal text) -->
# 5c pre-check: is `sub_mod` on the critical segment of C4b-B? (before any 5c RTL)

Labels: **MEASURED** (Quartus Timing Analyzer on a copy of the C4b-B seed-1 database), **INFERENCE**, **ESTIMATE**.
Database: revision `C4b-B` (seed 1, 40.000 ns, Quartus defaults), the compile of
`evidence/phase05/5b/quartus_C4b-B.md` (worst setup slack +11.044 ns, matches). Scripts:
`scripts/quartus/phase5_top_paths.tcl` (full path of the worst path) and a `get_timing_paths -to *u_bfly|u_side|*` query (worst
path into the butterfly's side delay line). Corner: Slow 1100mV 100C only.

## 1. Worst path (MEASURED, slack +11.044 ns): memory → `mul_in` → multiplier
| Segment (cumulative arrival, ns) | Delay (ns) | Block |
|---|---:|---|
| 6.030 → 27.062 | 21.03 | memory read decode + read mux (`raddr0`, `Mux206`, `Mux365`, `Mux357`) |
| 27.062 → 31.279 | **4.22** | butterfly input `sub_mod(b, a)` (`Add1`, `LessThan0`, `mul_in` select) |
| 31.279 → 34.869 | 3.59 | routing into the DSP + Barrett product to cut X |

**Answer: yes — `sub_mod` is on the critical segment** (4.22 of 28.84 ns data path).

## 2. Second path class (MEASURED, slack +12.102 ns): memory → `side_in` → side delay line
The `a + b` side operand of the INTT butterfly passes the same read mux, then `add_mod(a, b)`, into the butterfly's
side delay line, which Quartus implemented as a shift register in M10K (`pipe_delay:u_side|altshift_taps`):
| Segment (cumulative arrival, ns) | Delay (ns) | Block |
|---|---:|---|
| 6.030 → 27.136 | 21.11 | memory read decode + read mux |
| 27.136 → 31.099 | **3.96** | butterfly input `add_mod(a, b)` (`Add3`, `LessThan1`, `side_in` select) |
| 31.099 → 33.362 | 2.26 | routing into the M10K data input |

## 3. Reading (INFERENCE / ESTIMATE)
- Removing only `sub_mod` from the multiplier path leaves the side path (§2) as the worst path: about 40 − 12.102 =
  27.9 ns of the period at seed 1, i.e. an Fmax cap near 35.8 MHz (INFERENCE, one seed). The adoption threshold for 5c
  is a median Fmax above 34.84 MHz (top of Barrett's 5b seed range), so a `sub_mod`-only change could at best clear it
  by a small margin.
- Making **both** INTT butterfly inputs lazy — multiplier input `b + q − a` in [1, 2q) and side operand `a + b` in
  [0, 2q), the latter reduced once at the output (one conditional subtraction in the write segment, which has slack
  +17.125 ns, `5b/c4b_segments_slow100.txt`) — removes the compare/select from both paths. ESTIMATE: worst path about
  21 + 1 + 3.6 ≈ 26 ns (≈ 38 MHz); not a prediction of Fmax; only a compile can tell.
- Either way the memory read part (≈ 21 ns) stays; 50 MHz is not reachable in 5c (ADR 0010).
