<!-- claim-lint: skip-file (internal evidence, not proposal text) -->
# Critical paths of K3 at 15 ns (K3-15-s4), 2026-10-05

MEASURED with `quartus_sta -t scripts/quartus/phase5m_top_paths.tcl` (300 worst setup paths, slow model, 1,100 mV, 100 C) on a copy of the compiled database of `quartus/phase09s2b_core`, classified by `scripts/quartus/classify_paths_9f.py` and grouped by start and end register (the raw report is not stored). K3-15-s4 was the seed with the smallest setup slack of the six seeds of the rule (+1.305 ns over all corners; the seed with the lowest Fmax, 73.02 MHz). Written after the compile campaign of S2b; the seeds 7-9 were not analysed.

```
## K3-15-s4_paths_slow100_summary.rpt
paths: 300, slack 1.666 .. 3.883 ns
  worst slack   1.666 ns,  272 paths: NTT core / memory / PWM -> NTT core / memory / PWM
  worst slack   3.335 ns,   10 paths: engine sequencer -> sampler (outside the permutation)
  (the remaining classes at +3.4 .. +3.9 ns)
```
| Paths | Worst slack (ns) | From | To |
|---|---|---|---|
| 144 | 1.666 | read-position delay of the NTT core (`u_dly_pos`) | the Barrett reducer inside the butterflies |
| 126 | 2.368 | side-operand delay of the butterfly (`u_side`) | the M10K banks |

## Reading
- The `layer_q` to memory class of K2 (+1.404 ns) is gone from the 300 worst paths; the registered issue address works as designed. The worst class of this seed is the read-position / zeta path to the reducer (+1.666 ns).
- Not visible here but present in the design (found in the K4 seed with the smallest slack, `critical_paths_K4-15.md`, same S2b logic in `ntt_core_s10.sv`): the term `start_go` of S2b makes the address register depend on `host_we_i`, which the sequencer drives from `cnt_q != 0`; a path `cnt_q` -> `core_hwe_o` -> `mode_n` -> shifts and adders -> `jlen_r`. In K4-15-s6 it is the worst path (+0.736 ns). It is the likely reason for the low seeds of K3 (seeds 4, 8 and 9 at 73.0, 75.5 and 72.8 MHz) beside the six seeds at 77.0 to 79.4 MHz (INFERENCE: not checked in the K3 seeds with a path report).
