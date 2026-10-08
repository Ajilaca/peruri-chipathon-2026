# MEASURED - Hasil Quartus untuk revisi `K1-15-s4`

- Dibuat: 2026-10-04 09:34 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09f1_core/output_files_K1-15-s4`
- Catatan: Fase 9F langkah S1: mlkem_core2 dengan SMP_C5 = 0, HASH_C5 = 0, CODEC_W2 = 1, revisi K1-15-s4, kernel-only dengan virtual pin; branch phase9m-optimisation

## Fitter (`K1-15-s4.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 16:00:19 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K1-15-s4 |
| Top-level Entity Name | mlkem_core2 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,194 / 41,910 ( 34 % ) |
| Total registers | 8378 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,270 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 53 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`K1-15-s4.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 1.114 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.341 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.075 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 1.147 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.264 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.048 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 7.476 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.177 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.438 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 8.704 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.142 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.438 | 0.000 |

- Slack setup terburuk: **1.114 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.142 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K1-15-s4.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 72.01 MHz | 72.01 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 72.19 MHz | 72.19 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 253
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

