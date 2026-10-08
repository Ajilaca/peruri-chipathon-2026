# MEASURED - Hasil Quartus untuk revisi `MK-s3`

- Dibuat: 2026-10-04 06:47 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09m3_core/output_files_MK-s3`
- Catatan: Fase 9M butir 3: mlkem_core dengan HASH_C5 = 0 (sponge hash K0), CODEC_W2 = 1, revisi MK-s3, kernel-only dengan virtual pin; branch phase9m-optimisation

## Fitter (`MK-s3.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 12:53:14 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MK-s3 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 15,911 / 41,910 ( 38 % ) |
| Total registers | 8266 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`MK-s3.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 19.727 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.329 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 38.115 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.893 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.569 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 20.201 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.288 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 38.241 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.798 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.529 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.014 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.141 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.945 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.456 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.904 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.527 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.110 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 39.139 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.343 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.910 | 0.000 |

- Slack setup terburuk: **19.727 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.11 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MK-s3.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 49.33 MHz | 49.33 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 50.51 MHz | 50.51 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 254
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

