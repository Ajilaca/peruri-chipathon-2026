<!-- claim-lint: skip-file (internal evidence, not proposal text) -->
# Jalur kritis K1b pada 15 ns (K1b-15-s1, seed dengan slack 100 C terkecil), 2026-10-04

MEASURED dengan `quartus_sta -t scripts/quartus/phase5m_top_paths.tcl` (300 jalur setup terburuk, model slow, 1.100 mV, 100 C) pada salinan database terkompilasi `quartus/phase09f1b_core`; diklasifikasikan oleh `scripts/quartus/classify_paths_9f.py`. Laporan mentah tidak disimpan.

```
## K1b-15-s1_paths_slow100_summary.rpt
paths: 300, slack 1.170 .. 2.457 ns
  worst slack   1.170 ns,  298 paths: NTT core / memory / PWM -> NTT core / memory / PWM
  worst slack   2.420 ns,    2 paths: engine sequencer -> Keccak permutation (sampler sponge)
```

## Pembacaan
- 298 dari 300 jalur terburuk ada di kelas inti NTT / memori / PWM (+1,170 .. sekitar +2,4 ns); sidecar (baru di K1b) tidak muncul di antaranya; kelas berikutnya adalah sequencer mesin ke sponge sampler pada +2,420 ns (2 jalur). Dinding K1b pada 15 ns sama dengan K1 (`../9f1/critical_paths_K1-15.md`): inti NTT / memori.
