# MEASURED - Hasil Quartus untuk revisi `K1b-s5`

- Dibuat: 2026-10-04 12:08 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09f1b_core/output_files_K1b-s5`
- Catatan: Fase 9F langkah S1b: mlkem_core3 (sidecar hash latar belakang) dengan SMP_C5 = 0, HASH_C5 = 0, CODEC_W2 = 1, revisi K1b-s5, kernel-only dengan virtual pin; branch phase9m-optimisation

## Fitter (`K1b-s5.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 17:46:40 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K1b-s5 |
| Top-level Entity Name | mlkem_core3 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,374 / 41,910 ( 34 % ) |
| Total registers | 8211 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`K1b-s5.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 18.043 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.294 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 38.069 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.919 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.574 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 18.723 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.276 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 38.199 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.795 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.528 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 26.427 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.160 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.936 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.449 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.903 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 28.918 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.100 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 39.129 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.330 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.907 | 0.000 |

- Slack setup terburuk: **18.043 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.1 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K1b-s5.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 45.54 MHz | 45.54 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 47.0 MHz | 47.0 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 253
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

