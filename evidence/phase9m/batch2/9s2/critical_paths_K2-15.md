<!-- claim-lint: skip-file (internal evidence, not proposal text) -->
# Jalur kritis K2 pada 15 ns (K2-15-s5, seed dengan slack terkecil pada 100 C), 2026-10-04

MEASURED dengan `quartus_sta -t scripts/quartus/phase5m_top_paths.tcl` (300 jalur setup terburuk, model slow, 1.100 mV, 100 C) pada salinan database terkompilasi `quartus/phase09s2_core`; diklasifikasikan oleh `scripts/quartus/classify_paths_9f.py`; pengelompokan tingkat field dihitung dari laporan yang sama (laporan mentah tidak disimpan). K2-15-s3 punya slack sama pada corner worksheet (1,237 lawan 1,236 ns); satu seed dianalisis.

```
## K2-15-s5_paths_slow100_summary.rpt
paths: 300, slack 1.404 .. 2.977 ns
  worst slack   1.404 ns,  286 paths: NTT core / memory / PWM -> NTT core / memory / PWM
  worst slack   2.505 ns,    9 paths: core controller / other -> register file
  worst slack   2.905 ns,    5 paths: hash wrapper / sponge control -> register file
```

Pengelompokan 300 jalur menurut register awal dan akhir (nama dipendekkan; "NTT|" adalah inti NTT di dalam mesin):
| Jalur | Slack terburuk (ns) | Dari | Ke |
|---|---|---|---|
| 55 | 1.404 | `NTT|layer_q[*]` | port tulis / alamat RAM bank M10K (`poly_mem_m10k`) |
| 144 | 2.354 | `NTT|mode_q` | reducer Barrett di dalam butterfly |
| 45 | 2.102 | delay operand sisi butterfly (`u_side`) | bank M10K |
| 24 | 2.587 | delay posisi baca (`u_dly_pos`) | reducer Barrett |
| 18 | 2.349 | reducer Barrett | bank M10K |
| 9 + 5 + 1 | 2.505 / 2.905 / 2.934 | pengendali inti, sponge hash | register file |

## Pembacaan
- Dinding yang disasar S2 berpindah: di K1b kelas reducer ke M10K adalah yang terburuk (+1,170 ns, 182 dari 300 jalur, `../../batch1/9f1b/critical_paths_K1b-15.md` dan rincian field-nya); di K2 ia ada pada +2,349 ns (18 jalur). Register baru bekerja seperti dirancang.
- Jalur terburuk K2 adalah jalur lain yang sudah ada: penghitung layer (`layer_q`) lewat aritmetika alamat tahap issue (geser dengan `log2len`, blok dan posisi, peta bank) ke port M10K, +1,404 ns pada 100 C di seed ini. Di K1b kelas yang sama ada pada +1,910 ns (20 jalur): ia tersembunyi di balik yang terburuk. Kini ia membatasi K2.
- Kelas berikutnya ada pada +2,1 sampai +2,6 ns (fanout `mode_q` ke reducer, jalur operand sisi, posisi baca). Langkah yang hanya menghapus kelas `layer_q` akan memindahkan dinding ke kelas sekitar +2,1 .. +2,4 ns (INFERENCE dari tabel ini; derau seed kompilasi sekitar 3 MHz, `selection_worksheet.md`).
