# MEASURED - Hasil Quartus untuk revisi `CD`

- Dibuat: 2026-10-03 14:38 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09a_codec/output_files_CD`
- Catatan: Fase 9a: mlkem_codec_top (pengemas dan pembongkar), revisi CD, kernel-only dengan virtual pin; working tree sebelum commit Fase 9

## Fitter (`CD.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 21:28:19 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | CD |
| Top-level Entity Name | mlkem_codec_top |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 298 / 41,910 ( < 1 % ) |
| Total registers | 192 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 0 / 5,662,720 ( 0 % ) |
| Total RAM Blocks | 0 / 553 ( 0 % ) |
| Total DSP Blocks | 2 / 112 ( 2 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`CD.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 30.388 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.436 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.251 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 30.143 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.446 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.145 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 35.016 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.182 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.566 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 35.725 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.168 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.558 | 0.000 |

- Slack setup terburuk: **30.143 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.168 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`CD.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 104.04 MHz | 104.04 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 101.45 MHz | 101.45 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 5
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

