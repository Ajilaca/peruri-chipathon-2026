# MEASURED - Hasil Quartus untuk revisi `K1-s6`

- Dibuat: 2026-10-04 09:34 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09f1_core/output_files_K1-s6`
- Catatan: Fase 9F langkah S1: mlkem_core2 dengan SMP_C5 = 0, HASH_C5 = 0, CODEC_W2 = 1, revisi K1-s6, kernel-only dengan virtual pin; branch phase9m-optimisation

## Fitter (`K1-s6.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 15:10:23 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K1-s6 |
| Top-level Entity Name | mlkem_core2 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,108 / 41,910 ( 34 % ) |
| Total registers | 8386 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`K1-s6.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 19.063 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.338 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.056 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.934 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.573 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 19.376 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.235 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.250 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.758 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.542 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 26.990 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.301 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.532 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.905 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.493 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.096 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.602 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.363 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.908 | 0.000 |

- Slack setup terburuk: **19.063 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.096 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K1-s6.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 47.76 MHz | 47.76 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 48.49 MHz | 48.49 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 253
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

