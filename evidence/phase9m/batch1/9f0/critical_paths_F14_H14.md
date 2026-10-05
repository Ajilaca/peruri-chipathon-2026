<!-- claim-lint: skip-file (internal evidence, not proposal text) -->
# Critical paths of the 9M-1 core at 14 ns (F14-s1, H14-s2), 2026-10-04

MEASURED with `quartus_sta -t scripts/quartus/phase5m_top_paths.tcl` (300 worst setup paths, slow model, 1,100 mV, 100 C) on a copy of the compiled database of `quartus/phase09f0_core` (revisions F14-s1: defaults, and H14-s2: high performance effort, both 14.000 ns); classified by `scripts/quartus/classify_paths_9f.py` from the hierarchy names of the From and To nodes (the same script reproduces the classes of `../../critical_paths_MW.md`). The raw report files were kept in the scratch copy and are not stored (300 lines each).

```
## F14-s1_paths_slow100_summary.rpt
paths: 300, slack 0.721 .. 1.689 ns
  worst slack   0.721 ns,  133 paths: Keccak permutation (hash instance) -> Keccak permutation (hash instance)
  worst slack   1.055 ns,   84 paths: NTT core / memory / PWM -> NTT core / memory / PWM
  worst slack   1.266 ns,   83 paths: Keccak permutation (sampler sponge) -> Keccak permutation (sampler sponge)
## H14-s2_paths_slow100_summary.rpt
paths: 300, slack 0.423 .. 1.184 ns
  worst slack   0.423 ns,  126 paths: Keccak permutation (hash instance) -> Keccak permutation (hash instance)
  worst slack   0.453 ns,  146 paths: Keccak permutation (sampler sponge) -> Keccak permutation (sampler sponge)
  worst slack   0.906 ns,   19 paths: hash wrapper / sponge control -> register file
  worst slack   1.024 ns,    3 paths: hash wrapper / sponge control -> byte buffer RAM
  worst slack   1.063 ns,    6 paths: Keccak permutation (hash instance) -> register file
```

## Reading
- At 14 ns with the defaults the worst paths are still inside the C5 Keccak permutation of the hash instance (+0.721 ns, 133 of 300 paths); the NTT core / memory / PWM class follows at +1.055 ns (84 paths) and the sampler-sponge permutation at +1.266 ns (83 paths). The three classes lie within 0.55 ns of each other: no single block dominates at this constraint.
- With the high performance effort the two Keccak permutations lead (+0.423 ns hash, +0.453 ns sampler) and the next classes (hash wrapper to register file, +0.906 ns) are about 0.5 ns behind.
- INFERENCE: replacing the C5 permutations by K0 (S1) removes the permutation classes from the critical list; the NTT core / memory / PWM class (+1.055 ns at 14 ns, i.e. a path of about 12.9 ns for this fitter run) would then be the next limit, so S1 may not raise Fmax much beyond the NTT wall. S1 measures this (test plan V9).

## Added after amendment A2: 13 ns (F13-s2: first constraint not met; F13-s1: met)
```
## F13-s2_paths_slow100_summary.rpt
paths: 300, slack -0.185 .. 0.532 ns
  worst slack  -0.185 ns,  171 paths: NTT core / memory / PWM -> NTT core / memory / PWM
  worst slack  -0.030 ns,   33 paths: Keccak permutation (hash instance) -> Keccak permutation (hash instance)
  worst slack   0.178 ns,   96 paths: Keccak permutation (sampler sponge) -> Keccak permutation (sampler sponge)
## F13-s1_paths_slow100_summary.rpt
paths: 300, slack 0.227 .. 1.086 ns
  worst slack   0.227 ns,  130 paths: Keccak permutation (hash instance) -> Keccak permutation (hash instance)
  worst slack   0.571 ns,   65 paths: NTT core / memory / PWM -> NTT core / memory / PWM
  worst slack   0.716 ns,  105 paths: Keccak permutation (sampler sponge) -> Keccak permutation (sampler sponge)
```
- At 13 ns seed 2 (not met, -0.185 ns) the worst class is **NTT core / memory / PWM** (171 of 300 paths); the hash-instance Keccak permutation is also negative (-0.030 ns) and the sampler-sponge permutation is +0.178 ns. At seed 1 (met, +0.227 ns) the hash-instance permutation leads and the NTT class follows at +0.571 ns.
- So at the limit the NTT core / memory and the C5 permutations fail together within 0.2 ns: the NTT wall is about 13.2 ns (about 75 MHz) for this design and these settings. INFERENCE for S1: replacing the permutations does not lift the wall of the NTT class; S1 measures it.
