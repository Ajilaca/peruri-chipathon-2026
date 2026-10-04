<!-- claim-lint: skip-file (internal evidence, not proposal text) -->
# Critical paths of the 9M-1 core (MW, MW-20), 2026-10-04

MEASURED with `quartus_sta -t scripts/phase5m_top_paths.tcl` (300 worst setup paths, slow model, 1,100 mV, 100 C) on a copy of the compiled database of `quartus/phase09m1_core` (revisions MW: 40 ns, seed 1; MW-20: 20 ns, seed 1). The classification counts the source and destination hierarchy of each path (script output below). INFERENCE in the reading: everything not listed has more slack than the last listed path.

## MW-20
```
paths: 300, slack 4.355 .. 5.533 ns
  worst slack   4.355 ns,  195 paths: C5 Keccak (hash instance) -> C5 Keccak (hash instance)
  worst slack   4.361 ns,  105 paths: C5 Keccak (sampler sponge) -> C5 Keccak (sampler sponge)
```
## MW
```
paths: 300, slack 20.825 .. 22.954 ns
  worst slack  20.825 ns,   99 paths: C5 Keccak (sampler sponge) -> C5 Keccak (sampler sponge)
  worst slack  21.750 ns,  149 paths: C5 Keccak (hash instance) -> C5 Keccak (hash instance)
  worst slack  21.990 ns,    7 paths: sponge (hash instance, outside the permutation) -> byte buffer RAM
  worst slack  22.127 ns,   11 paths: NTT core / memory -> NTT core / memory
  worst slack  22.166 ns,   34 paths: sponge (hash instance, outside the permutation) -> register file rf_q
```

## Reading
- At 20 ns (MW-20) all 300 worst paths lie inside the two Keccak-f[1600] permutations of the C5 kind (two rounds per cycle): 195 in the hash instance, 105 in the sampler sponge of the engine. The worst path has a data arrival of 21.07 ns against a required time of 25.43 ns (slack 4.355 ns).
- INFERENCE: every other path of MW-20 has a slack above 5.533 ns, i.e. outside the two permutations the design would allow about 69 MHz in this compile; the next limit is not identified by this report.
- At 40 ns (MW) the same two permutations lead; the first other classes are the hash sponge output to the register file and the byte RAMs (slack about 22.0-22.9 ns) and the NTT core / memory (22.127 ns).
