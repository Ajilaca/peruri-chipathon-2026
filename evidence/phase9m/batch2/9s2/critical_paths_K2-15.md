<!-- claim-lint: skip-file (internal evidence, not proposal text) -->
# Critical paths of K2 at 15 ns (K2-15-s5, a seed with the smallest slack at 100 C), 2026-10-04

MEASURED with `quartus_sta -t scripts/quartus/phase5m_top_paths.tcl` (300 worst setup paths, slow model, 1,100 mV, 100 C) on a copy of the compiled database of `quartus/phase09s2_core`; classified by `scripts/quartus/classify_paths_9f.py`; the field-level grouping was computed from the same report (raw report not stored). K2-15-s3 has an equal slack at the corner of the worksheet (1.237 against 1.236 ns); one seed is analysed.

```
## K2-15-s5_paths_slow100_summary.rpt
paths: 300, slack 1.404 .. 2.977 ns
  worst slack   1.404 ns,  286 paths: NTT core / memory / PWM -> NTT core / memory / PWM
  worst slack   2.505 ns,    9 paths: core controller / other -> register file
  worst slack   2.905 ns,    5 paths: hash wrapper / sponge control -> register file
```

Grouping of the 300 paths by start and end register (names shortened; "NTT|" is the NTT core inside the engine):
| Paths | Worst slack (ns) | From | To |
|---|---|---|---|
| 55 | 1.404 | `NTT|layer_q[*]` | the RAM write / address ports of the M10K banks (`poly_mem_m10k`) |
| 144 | 2.354 | `NTT|mode_q` | the Barrett reducer inside the butterflies |
| 45 | 2.102 | side-operand delay of the butterfly (`u_side`) | the M10K banks |
| 24 | 2.587 | read-position delay (`u_dly_pos`) | the Barrett reducer |
| 18 | 2.349 | the Barrett reducer | the M10K banks |
| 9 + 5 + 1 | 2.505 / 2.905 / 2.934 | core controller, hash sponge | register file |

## Reading
- The wall that S2 targeted moved: in K1b the reducer to M10K class was the worst (+1.170 ns, 182 of 300 paths, `../../batch1/9f1b/critical_paths_K1b-15.md` and its field breakdown); in K2 it is at **+2.349 ns** (18 paths). The new register works as designed.
- **The worst path of K2 is a different, already present one:** the layer counter (`layer_q`) through the address arithmetic of the issue stage (shifts by `log2len`, block and position, the bank map) to the M10K ports, +1.404 ns at 100 C in this seed. In K1b the same class was at +1.910 ns (20 paths): it was hidden behind the worst one. It limits K2 now.
- The next classes are at +2.1 to +2.6 ns (`mode_q` fanout into the reducer, the side-operand path, the read position). A step that removes only the `layer_q` class would move the wall to about the +2.1 .. +2.4 ns classes (INFERENCE from this table; the seed noise of the compiles is about 3 MHz, `selection_worksheet.md`).
