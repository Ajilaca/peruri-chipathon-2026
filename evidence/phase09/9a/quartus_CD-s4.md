# MEASURED - Hasil Quartus untuk revisi `CD-s4`

- Dibuat: 2026-10-03 14:38 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09a_codec/output_files_CD-s4`
- Catatan: Fase 9a: mlkem_codec_top (pengemas dan pembongkar), revisi CD-s4, kernel-only dengan virtual pin; working tree sebelum commit Fase 9

## Fitter (`CD-s4.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 21:32:22 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | CD-s4 |
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

## Timing (`CD-s4.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 30.959 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.399 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.256 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 30.624 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.376 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.148 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 35.570 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.179 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.567 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 36.085 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.167 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.558 | 0.000 |

- Slack setup terburuk: **30.624 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.167 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`CD-s4.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 110.61 MHz | 110.61 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 106.66 MHz | 106.66 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 5
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

