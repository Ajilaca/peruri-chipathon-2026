# MEASURED - Hasil Quartus untuk revisi `MW-s6`

- Dibuat: 2026-10-04 02:05 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09m1_core/output_files_MW-s6`
- Catatan: Fase 9M-1: mlkem_core dengan CODEC_W2 = 1 (tugas muat / simpan dua byte), revisi MW-s6, kernel-only dengan virtual pin; branch phase9m-optimisation, rtl/mlkem pada file 9M-1

## Fitter (`MW-s6.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 08:54:10 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MW-s6 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 17,653 / 41,910 ( 42 % ) |
| Total registers | 8376 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`MW-s6.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 19.504 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.292 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 38.170 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.878 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.580 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 20.150 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.263 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 38.319 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.750 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.536 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.119 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.141 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.982 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.451 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.908 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.615 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.114 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 39.173 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.332 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.909 | 0.000 |

- Slack setup terburuk: **19.504 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.114 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MW-s6.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 48.79 MHz | 48.79 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 50.38 MHz | 50.38 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 253
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

