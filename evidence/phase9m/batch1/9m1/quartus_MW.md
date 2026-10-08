# MEASURED - Hasil Quartus untuk revisi `MW`

- Dibuat: 2026-10-04 02:05 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09m1_core/output_files_MW`
- Catatan: Fase 9M-1: mlkem_core dengan CODEC_W2 = 1 (tugas muat / simpan dua byte), revisi MW, kernel-only dengan virtual pin; branch phase9m-optimisation, rtl/mlkem pada file 9M-1

## Fitter (`MW.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 08:02:01 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MW |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 17,672 / 41,910 ( 42 % ) |
| Total registers | 8233 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`MW.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 20.825 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.358 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 38.661 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.562 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.563 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 21.516 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.296 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 38.750 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.481 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.527 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 28.136 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 39.329 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.245 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.899 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 30.347 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.116 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 39.441 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.162 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.906 | 0.000 |

- Slack setup terburuk: **20.825 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.116 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MW.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 52.15 MHz | 52.15 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 54.1 MHz | 54.1 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 253
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

