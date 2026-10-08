# MEASURED - Hasil Quartus untuk revisi `F15-s2`

- Dibuat: 2026-10-04 08:39 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09f0_core/output_files_F15-s2`
- Catatan: Fase 9F langkah S0: inti 9M-1 (CODEC_W2 = 1, hash C5) pada batasan lebih ketat, revisi F15-s2, kernel-only dengan virtual pin; branch phase9m-optimisation

## Fitter (`F15-s2.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 13:53:31 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | F15-s2 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 17,926 / 41,910 ( 43 % ) |
| Total registers | 8700 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,270 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 53 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`F15-s2.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 1.363 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.342 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.090 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 1.570 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.165 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.057 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 6.815 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.446 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 8.299 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.071 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.442 | 0.000 |

- Slack setup terburuk: **1.363 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.071 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`F15-s2.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 73.33 MHz | 73.33 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 74.46 MHz | 74.46 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 253
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

