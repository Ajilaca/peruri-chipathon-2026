# MEASURED - Hasil Quartus untuk revisi `HF`

- Dibuat: 2026-10-03 16:21 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09b_hashfo/output_files_HF`
- Catatan: Fase 9b: mlkem_hash_fo_top (pembungkus hash dan pembanding FO), revisi HF, kernel-only dengan virtual pin; working tree sebelum commit Fase 9

## Fitter (`HF.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 22:30:13 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | HF |
| Top-level Entity Name | mlkem_hash_fo_top |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 6,745 / 41,910 ( 16 % ) |
| Total registers | 1976 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 0 / 5,662,720 ( 0 % ) |
| Total RAM Blocks | 0 / 553 ( 0 % ) |
| Total DSP Blocks | 0 / 112 ( 0 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`HF.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 19.095 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.425 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.281 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 19.968 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.444 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.193 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 26.884 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.177 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.616 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.378 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.163 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.597 | 0.000 |

- Slack setup terburuk: **19.095 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.163 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`HF.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 47.84 MHz | 47.84 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 49.92 MHz | 49.92 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 6
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

