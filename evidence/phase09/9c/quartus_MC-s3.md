# MEASURED - Hasil Quartus untuk revisi `MC-s3`

- Dibuat: 2026-10-03 18:15 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09c_core/output_files_MC-s3`
- Catatan: Fase 9c: mlkem_core (KeyGen, Encaps, Decaps; mesin 8d, codec, hash dengan sponge C5, pembanding), revisi MC-s3, kernel-only dengan virtual pin; working tree sebelum commit Fase 9

## Fitter (`MC-s3.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 00:30:36 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MC-s3 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 17,630 / 41,910 ( 42 % ) |
| Total registers | 8365 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`MC-s3.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 19.395 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.323 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.126 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.921 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.566 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 20.320 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.148 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.290 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.760 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.517 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 26.865 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.153 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.404 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.503 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.898 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.441 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.104 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.659 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.329 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.904 | 0.000 |

- Slack setup terburuk: **19.395 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.104 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MC-s3.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 48.53 MHz | 48.53 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 50.81 MHz | 50.81 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 253
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

