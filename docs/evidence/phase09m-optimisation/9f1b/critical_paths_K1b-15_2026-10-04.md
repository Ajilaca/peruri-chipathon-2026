<!-- claim-lint: skip-file (internal evidence, not proposal text) -->
# Critical paths of K1b at 15 ns (K1b-15-s1, the seed with the smallest 100 C slack), 2026-10-04

MEASURED with `quartus_sta -t scripts/phase5m_top_paths.tcl` (300 worst setup paths, slow model, 1,100 mV, 100 C) on a copy of the compiled database of `quartus/phase09f1b_core`; classified by `scripts/classify_paths_9f.py`. The raw report is not stored.

```
## K1b-15-s1_paths_slow100_summary.rpt
paths: 300, slack 1.170 .. 2.457 ns
  worst slack   1.170 ns,  298 paths: NTT core / memory / PWM -> NTT core / memory / PWM
  worst slack   2.420 ns,    2 paths: engine sequencer -> Keccak permutation (sampler sponge)
```

## Reading
- 298 of the 300 worst paths are in the NTT core / memory / PWM class (+1.170 .. about +2.4 ns); the sidecar (new in K1b) does not appear among them; the next class is the engine sequencer to the sampler sponge at +2.420 ns (2 paths). The wall of K1b at 15 ns is the same as that of K1 (`../9f1/critical_paths_K1-15_2026-10-04.md`): the NTT core / memory.
