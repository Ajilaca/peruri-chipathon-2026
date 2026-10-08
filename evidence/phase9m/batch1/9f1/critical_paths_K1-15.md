<!-- claim-lint: skip-file (internal evidence, not proposal text) -->
# Jalur kritis K1 pada 15 ns (K1-15-s4, seed dengan slack terkecil), 2026-10-04

MEASURED dengan `quartus_sta -t scripts/quartus/phase5m_top_paths.tcl` (300 jalur setup terburuk, model slow, 1.100 mV, 100 C) pada salinan database terkompilasi `quartus/phase09f1_core`; diklasifikasikan oleh `scripts/quartus/classify_paths_9f.py`. Laporan mentah tidak disimpan (300 baris).

```
## K1-15-s4_paths_slow100_summary.rpt
paths: 300, slack 1.114 .. 2.447 ns
  worst slack   1.114 ns,  300 paths: NTT core / memory / PWM -> NTT core / memory / PWM
```

## Pembacaan
- Pada 15 ns semua 300 jalur setup terburuk K1 (sampler K0 dan hash K0) ada di kelas inti NTT / memori / PWM (slack +1,114 .. +2,447 ns); tidak ada jalur Keccak di antaranya. Permutasi C5 yang membatasi inti 9M-1 (S0, 14 ns) sudah hilang dari daftar kritis, dan kelas NTT / memori yang tersisa.
- Bersama S0 (kelas NTT berada dalam 0,2 ns dari permutasi C5 pada batas 13 ns) ini menunjukkan bahwa S1 menghapus batas permutasi tetapi menabrak dinding NTT / memori: kenaikan Fmax S1 kecil (bagian 3 result_9f1.md); S2 (pipeline lebih dalam di kelas ini) adalah tuas berikutnya bila tim menginginkan Fmax lebih tinggi; analisis kedalaman pipeline (`ntt_pipeline_depth_analysis.md`) menyatakan biaya siklusnya kecil (sekitar 8 % siklus adalah NTT).
