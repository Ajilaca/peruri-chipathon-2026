# MEASURED - Hasil Quartus untuk revisi `MK-s4`

- Dibuat: 2026-10-04 06:47 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09m3_core/output_files_MK-s4`
- Catatan: Fase 9M butir 3: mlkem_core dengan HASH_C5 = 0 (sponge hash K0), CODEC_W2 = 1, revisi MK-s4, kernel-only dengan virtual pin; branch phase9m-optimisation

## Fitter (`MK-s4.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 13:06:31 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MK-s4 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 15,912 / 41,910 ( 38 % ) |
| Total registers | 8261 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`MK-s4.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 19.754 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.327 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.047 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.614 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.590 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 20.336 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.256 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.263 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.436 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.554 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.659 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.174 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.934 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.946 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.894 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.107 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.545 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.731 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.943 | 0.000 |

- Slack setup terburuk: **19.754 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.107 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MK-s4.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 49.39 MHz | 49.39 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 50.85 MHz | 50.85 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 254
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

