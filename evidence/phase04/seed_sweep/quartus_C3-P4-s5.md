# MEASURED - Hasil Quartus untuk revisi `C3-P4-s5`

- Dibuat: 2026-10-01 03:16 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase04_pipeline_c3/output_files_P4_s5`
- Catatan: Sapuan seed Fase 4 (masukan untuk ADR 0008): C3-P4 dengan SEED fitter 5; semua yang lain identik dengan C3-P4 (RTL pada git 7947c0c, C3.sdc 40.000 ns). Dikompilasi ulang berurutan setelah percobaan pertama gagal karena masalah alat (lihat seed_sweep.md)

## Fitter (`C3-P4-s5.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Thu Oct  1 10:14:25 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | C3-P4-s5 |
| Top-level Entity Name | ntt_core_c3_p4 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 10,467 / 41,910 ( 25 % ) |
| Total registers | 4160 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 27,428 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 26 / 553 ( 5 % ) |
| Total DSP Blocks | 9 / 112 ( 8 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`C3-P4-s5.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 8.497 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.403 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.712 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 7.580 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.371 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.686 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 22.687 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.183 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.028 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 25.484 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.118 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.994 | 0.000 |

- Slack setup terburuk: **7.58 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.118 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`C3-P4-s5.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 31.74 MHz | 31.74 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 30.85 MHz | 30.85 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 19
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

