<!-- claim-lint: skip-file (internal evidence, not proposal text) -->
# Jalur kritis K3 pada 15 ns (K3-15-s4), 2026-10-05

MEASURED dengan `quartus_sta -t scripts/quartus/phase5m_top_paths.tcl` (300 jalur setup terburuk, model slow, 1.100 mV, 100 C) pada salinan database terkompilasi `quartus/phase09s2b_core`, diklasifikasikan oleh `scripts/quartus/classify_paths_9f.py` dan dikelompokkan menurut register awal dan akhir (laporan mentah tidak disimpan). K3-15-s4 adalah seed dengan slack setup terkecil dari enam seed aturan (+1,305 ns pada semua corner; seed dengan Fmax terendah, 73,02 MHz). Ditulis setelah kampanye kompilasi S2b; seed 7-9 tidak dianalisis.

```
## K3-15-s4_paths_slow100_summary.rpt
paths: 300, slack 1.666 .. 3.883 ns
  worst slack   1.666 ns,  272 paths: NTT core / memory / PWM -> NTT core / memory / PWM
  worst slack   3.335 ns,   10 paths: engine sequencer -> sampler (outside the permutation)
  (the remaining classes at +3.4 .. +3.9 ns)
```
| Jalur | Slack terburuk (ns) | Dari | Ke |
|---|---|---|---|
| 144 | 1.666 | delay posisi baca inti NTT (`u_dly_pos`) | reducer Barrett di dalam butterfly |
| 126 | 2.368 | delay operand sisi butterfly (`u_side`) | bank M10K |

## Pembacaan
- Kelas `layer_q` ke memori K2 (+1,404 ns) hilang dari 300 jalur terburuk; alamat issue terregistrasi bekerja seperti dirancang. Kelas terburuk seed ini adalah jalur posisi baca / zeta ke reducer (+1,666 ns).
- Tidak terlihat di sini tetapi ada di desain (ditemukan pada seed K4 dengan slack terkecil, `critical_paths_K4-15.md`, logika S2b yang sama di `ntt_core_s10.sv`): suku `start_go` S2b membuat register alamat bergantung pada `host_we_i`, yang digerakkan sequencer dari `cnt_q != 0`; jalur `cnt_q` -> `core_hwe_o` -> `mode_n` -> geser dan penjumlah -> `jlen_r`. Pada K4-15-s6 ia adalah jalur terburuk (+0,736 ns). Itu kemungkinan sebab seed rendah K3 (seed 4, 8, dan 9 pada 73,0, 75,5, dan 72,8 MHz) di samping enam seed pada 77,0 sampai 79,4 MHz (INFERENCE: tidak diperiksa pada seed K3 dengan laporan jalur).
