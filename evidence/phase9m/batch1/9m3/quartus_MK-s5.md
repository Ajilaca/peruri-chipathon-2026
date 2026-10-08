# MEASURED - Hasil Quartus untuk revisi `MK-s5`

- Dibuat: 2026-10-04 06:47 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09m3_core/output_files_MK-s5`
- Catatan: Fase 9M butir 3: mlkem_core dengan HASH_C5 = 0 (sponge hash K0), CODEC_W2 = 1, revisi MK-s5, kernel-only dengan virtual pin; branch phase9m-optimisation

## Fitter (`MK-s5.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 13:18:19 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MK-s5 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 15,926 / 41,910 ( 38 % ) |
| Total registers | 8263 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`MK-s5.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 18.934 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.336 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 38.621 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.572 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.588 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 19.792 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.240 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 38.716 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.482 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.560 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 26.719 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 39.311 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.242 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.941 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.283 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.132 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 39.423 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.161 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.942 | 0.000 |

- Slack setup terburuk: **18.934 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.132 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MK-s5.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 47.47 MHz | 47.47 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 49.49 MHz | 49.49 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 254
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

