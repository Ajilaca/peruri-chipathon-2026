# MEASURED - Hasil Quartus untuk revisi `H14-s1`

- Dibuat: 2026-10-04 08:39 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09f0_core/output_files_H14-s1`
- Catatan: Fase 9F langkah S0: inti 9M-1 (CODEC_W2 = 1, hash C5) pada batasan lebih ketat, revisi H14-s1, kernel-only dengan virtual pin; branch phase9m-optimisation

## Fitter (`H14-s1.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 15:06:12 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | H14-s1 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 18,876 / 41,910 ( 45 % ) |
| Total registers | 10966 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 119,608 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 49 / 553 ( 9 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`H14-s1.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 0.826 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.325 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 5.575 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 1.273 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.243 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 5.550 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 5.913 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 5.906 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 7.474 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.090 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 5.909 | 0.000 |

- Slack setup terburuk: **0.826 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.09 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`H14-s1.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 75.91 MHz | 75.91 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 78.57 MHz | 78.57 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 254
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

