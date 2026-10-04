<!-- claim-lint: skip-file (internal evidence, not proposal text) -->
# Critical paths of K4 at 15 ns (K4-15-s6, the seed with the smallest slack), 2026-10-05

MEASURED with `quartus_sta -t scripts/phase5m_top_paths.tcl` (300 worst setup paths, slow model, 1,100 mV, 100 C) on a copy of the compiled database of `quartus/phase09i4_core`, classified by `scripts/classify_paths_9f.py` (the raw report is not stored). K4-15-s6: setup slack +0.596 ns over all corners, Fmax 69.43 MHz, the lowest seed.

```
## K4-15-s6_paths_slow100_summary.rpt
paths: 300, slack 0.736 .. 2.434 ns
  worst slack   0.736 ns,   29 paths: engine sequencer -> NTT core / memory / PWM
  worst slack   1.759 ns,  207 paths: engine sequencer -> Keccak permutation (sampler sponge)
  worst slack   1.971 ns,   60 paths: NTT core / memory / PWM -> NTT core / memory / PWM
  worst slack   2.083 ns,    4 paths: hash wrapper / sponge control -> register file
```
| Paths | Worst slack (ns) | From | To |
|---|---|---|---|
| 21 + 3 + 5 | 0.736 | engine sequencer `cnt_q` | the registered issue address `jlen_r` / `j_r` of the NTT core (S2b) |
| 189 + 18 | 1.759 | engine sequencer `opc_q` | the Keccak state of the sampler sponge |
| 48 | 1.990 | read-position delay of the NTT core | the Barrett reducer |
| 8 | 1.971 | side-operand delay | the M10K banks |

## Reading
- **The worst path of K4 is not new to item 4: it belongs to S2b.** Element by element (MEASURED, full report of the worst path): `cnt_q[6]` -> `Equal8~0` (`cnt_q != 0`) -> `core_hwe_o` -> `mode_q~1` (the `start_go` term of `mode_n`) -> `ShiftRight8` / `ShiftLeft14` (block and start address) -> `Add23`, `Add25` (j, j + len) -> `jlen_r`. The sequencer drives the NTT host write enable from its counter, and S2b made the registered address depend on it through `start_go`.
- **Item 4 itself (the host-write grant, the interlock, `pend_q`) does not appear among the 300 worst paths**; the nearest class at +1.759 ns is the existing path from the engine opcode register to the sampler Keccak state (207 paths), which is the same class that was already 2.4 ns behind in K1b.
