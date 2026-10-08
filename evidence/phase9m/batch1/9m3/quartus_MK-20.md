# MEASURED - Hasil Quartus untuk revisi `MK-20`

- Dibuat: 2026-10-04 06:47 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09m3_core/output_files_MK-20`
- Catatan: Fase 9M butir 3: mlkem_core dengan HASH_C5 = 0 (sponge hash K0), CODEC_W2 = 1, revisi MK-20, kernel-only dengan virtual pin; branch phase9m-optimisation

## Fitter (`MK-20.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 13:43:55 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MK-20 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 16,007 / 41,910 ( 38 % ) |
| Total registers | 8327 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`MK-20.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 4.003 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.342 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 17.791 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.084 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.565 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 4.294 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.289 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 17.955 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.935 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.535 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 10.109 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.143 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 18.725 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.567 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.901 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 11.948 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.067 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 18.973 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.422 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.906 | 0.000 |

- Slack setup terburuk: **4.003 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.067 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MK-20.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 62.51 MHz | 62.51 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 63.67 MHz | 63.67 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 254
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

