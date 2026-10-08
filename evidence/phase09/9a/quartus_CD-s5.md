# MEASURED - Hasil Quartus untuk revisi `CD-s5`

- Dibuat: 2026-10-03 14:38 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09a_codec/output_files_CD-s5`
- Catatan: Fase 9a: mlkem_codec_top (pengemas dan pembongkar), revisi CD-s5, kernel-only dengan virtual pin; working tree sebelum commit Fase 9

## Fitter (`CD-s5.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 21:34:00 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | CD-s5 |
| Top-level Entity Name | mlkem_codec_top |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 299 / 41,910 ( < 1 % ) |
| Total registers | 192 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 0 / 5,662,720 ( 0 % ) |
| Total RAM Blocks | 0 / 553 ( 0 % ) |
| Total DSP Blocks | 2 / 112 ( 2 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`CD-s5.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 30.762 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.432 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.259 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 30.716 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.450 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.149 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 35.088 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.181 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.568 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 35.833 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.167 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.558 | 0.000 |

- Slack setup terburuk: **30.716 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.167 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`CD-s5.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 108.25 MHz | 108.25 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 107.71 MHz | 107.71 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 5
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

