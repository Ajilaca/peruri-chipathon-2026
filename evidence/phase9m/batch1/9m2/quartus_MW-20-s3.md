# MEASURED - Hasil Quartus untuk revisi `MW-20-s3`

- Dibuat: 2026-10-04 04:55 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09m2_core/output_files_MW-20-s3`
- Catatan: Fase 9M-2: mlkem_core pada 20.000 ns, revisi MW-20-s3, kernel-only dengan virtual pin; branch phase9m-optimisation

## Fitter (`MW-20-s3.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 11:23:58 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MW-20-s3 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 17,800 / 41,910 ( 42 % ) |
| Total registers | 8447 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`MW-20-s3.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 4.236 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.336 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 18.662 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.548 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.586 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 4.581 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.326 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 18.760 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.463 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.545 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 10.438 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 19.344 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.221 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.909 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 12.175 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.131 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 19.453 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.143 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.911 | 0.000 |

- Slack setup terburuk: **4.236 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.131 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MW-20-s3.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 63.44 MHz | 63.44 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 64.86 MHz | 64.86 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 253
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

