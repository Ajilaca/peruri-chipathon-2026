# MEASURED - Hasil Quartus untuk revisi `CD-s6`

- Dibuat: 2026-10-03 14:38 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09a_codec/output_files_CD-s6`
- Catatan: Fase 9a: mlkem_codec_top (pengemas dan pembongkar), revisi CD-s6, kernel-only dengan virtual pin; working tree sebelum commit Fase 9

## Fitter (`CD-s6.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 21:35:48 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | CD-s6 |
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

## Timing (`CD-s6.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 30.538 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.395 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.258 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 30.440 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.372 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.153 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 34.746 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.180 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.567 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 35.507 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.167 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.556 | 0.000 |

- Slack setup terburuk: **30.44 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.167 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`CD-s6.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 105.69 MHz | 105.69 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 104.6 MHz | 104.6 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 5
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

