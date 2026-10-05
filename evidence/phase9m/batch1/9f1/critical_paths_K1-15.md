<!-- claim-lint: skip-file (internal evidence, not proposal text) -->
# Critical paths of K1 at 15 ns (K1-15-s4, the seed with the smallest slack), 2026-10-04

MEASURED with `quartus_sta -t scripts/quartus/phase5m_top_paths.tcl` (300 worst setup paths, slow model, 1,100 mV, 100 C) on a copy of the compiled database of `quartus/phase09f1_core`; classified by `scripts/quartus/classify_paths_9f.py`. The raw report is not stored (300 lines).

```
## K1-15-s4_paths_slow100_summary.rpt
paths: 300, slack 1.114 .. 2.447 ns
  worst slack   1.114 ns,  300 paths: NTT core / memory / PWM -> NTT core / memory / PWM
```

## Reading
- At 15 ns all 300 worst setup paths of K1 (K0 sampler and K0 hash) lie in the **NTT core / memory / PWM** class (slack +1.114 .. +2.447 ns); no Keccak path is among them. The C5 permutations that limited the 9M-1 core (S0, 14 ns) are gone from the critical list, and the NTT / memory class is what remains.
- Together with S0 (the NTT class was within 0.2 ns of the C5 permutations at the 13 ns limit) this shows that S1 removes the permutation limit but meets the NTT / memory wall: the Fmax gain of S1 is small (section 3 of result_9f1.md); S2 (a deeper pipeline in this class) is the next lever if the team wants more Fmax; the pipeline-depth analysis (`ntt_pipeline_depth_analysis.md`) says its cycle cost is small (about 8 % of cycles are NTT).
