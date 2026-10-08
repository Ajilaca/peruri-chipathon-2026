# MEASURED - Hasil Quartus untuk revisi `MC-20-s2`

- Dibuat: 2026-10-04 04:55 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09m2_core/output_files_MC-20-s2`
- Catatan: Fase 9M-2: mlkem_core pada 20.000 ns, revisi MC-20-s2, kernel-only dengan virtual pin; branch phase9m-optimisation

## Fitter (`MC-20-s2.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 10:24:54 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MC-20-s2 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 17,780 / 41,910 ( 42 % ) |
| Total registers | 8465 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`MC-20-s2.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 4.155 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.311 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 18.583 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.594 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.583 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 4.399 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.107 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 18.681 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.516 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.540 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 10.328 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.155 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 19.297 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.248 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.906 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 12.138 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.102 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 19.414 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.167 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.909 | 0.000 |

- Slack setup terburuk: **4.155 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.102 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MC-20-s2.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 63.11 MHz | 63.11 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 64.1 MHz | 64.1 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 253
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

