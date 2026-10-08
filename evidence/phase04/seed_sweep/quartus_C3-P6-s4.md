# MEASURED - Hasil Quartus untuk revisi `C3-P6-s4`

- Dibuat: 2026-10-01 03:16 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase04_pipeline_c3/output_files_P6_s4`
- Catatan: Sapuan seed Fase 4 (masukan untuk ADR 0008): C3-P6 dengan SEED fitter 4; semua yang lain identik dengan C3-P6 (RTL pada git 7947c0c, C3.sdc 40.000 ns). Dikompilasi ulang berurutan setelah percobaan pertama gagal karena masalah alat (lihat seed_sweep.md)

## Fitter (`C3-P6-s4.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Thu Oct  1 10:09:47 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | C3-P6-s4 |
| Top-level Entity Name | ntt_core_c3_p6 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 10,516 / 41,910 ( 25 % ) |
| Total registers | 4152 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,314 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 29 / 553 ( 5 % ) |
| Total DSP Blocks | 9 / 112 ( 8 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`C3-P6-s4.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 10.756 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.442 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.500 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.634 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.585 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 10.885 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.415 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.653 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.498 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.543 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 23.364 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.182 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.603 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.355 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.909 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 26.206 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.128 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.837 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.218 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.910 | 0.000 |

- Slack setup terburuk: **10.756 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.128 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`C3-P6-s4.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 34.2 MHz | 34.2 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 34.35 MHz | 34.35 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 19
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

