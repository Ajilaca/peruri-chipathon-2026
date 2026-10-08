# MEASURED - Hasil Quartus untuk revisi `HF-s5`

- Dibuat: 2026-10-03 16:21 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09b_hashfo/output_files_HF-s5`
- Catatan: Fase 9b: mlkem_hash_fo_top (pembungkus hash dan pembanding FO), revisi HF-s5, kernel-only dengan virtual pin; working tree sebelum commit Fase 9

## Fitter (`HF-s5.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 22:49:03 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | HF-s5 |
| Top-level Entity Name | mlkem_hash_fo_top |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 6,737 / 41,910 ( 16 % ) |
| Total registers | 1976 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 0 / 5,662,720 ( 0 % ) |
| Total RAM Blocks | 0 / 553 ( 0 % ) |
| Total DSP Blocks | 0 / 112 ( 0 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`HF-s5.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 20.794 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.419 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.243 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 21.559 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.442 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.139 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.764 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.563 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 30.182 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.162 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.553 | 0.000 |

- Slack setup terburuk: **20.794 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.162 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`HF-s5.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 52.07 MHz | 52.07 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 54.23 MHz | 54.23 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 6
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

