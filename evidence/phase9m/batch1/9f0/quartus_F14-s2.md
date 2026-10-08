# MEASURED - Hasil Quartus untuk revisi `F14-s2`

- Dibuat: 2026-10-04 08:39 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09f0_core/output_files_F14-s2`
- Catatan: Fase 9F langkah S0: inti 9M-1 (CODEC_W2 = 1, hash C5) pada batasan lebih ketat, revisi F14-s2, kernel-only dengan virtual pin; branch phase9m-optimisation

## Fitter (`F14-s2.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 14:29:16 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | F14-s2 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 17,889 / 41,910 ( 43 % ) |
| Total registers | 8669 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,270 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 53 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`F14-s2.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 1.062 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.343 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 5.563 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 1.213 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.325 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 5.532 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 6.110 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 5.901 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 7.561 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.108 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 5.906 | 0.000 |

- Slack setup terburuk: **1.062 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.108 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`F14-s2.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 77.29 MHz | 77.29 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 78.2 MHz | 78.2 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 253
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

