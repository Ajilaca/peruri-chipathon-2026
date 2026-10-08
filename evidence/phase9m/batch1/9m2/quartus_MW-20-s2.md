# MEASURED - Hasil Quartus untuk revisi `MW-20-s2`

- Dibuat: 2026-10-04 04:55 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09m2_core/output_files_MW-20-s2`
- Catatan: Fase 9M-2: mlkem_core pada 20.000 ns, revisi MW-20-s2, kernel-only dengan virtual pin; branch phase9m-optimisation

## Fitter (`MW-20-s2.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 11:14:03 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MW-20-s2 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 17,756 / 41,910 ( 42 % ) |
| Total registers | 8411 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`MW-20-s2.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 4.972 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.339 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 18.401 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.715 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.573 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 5.325 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.139 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 18.542 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.620 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.528 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 10.844 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 19.129 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.350 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.904 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 12.546 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.088 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 19.289 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.255 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.907 | 0.000 |

- Slack setup terburuk: **4.972 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.088 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MW-20-s2.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 66.54 MHz | 66.54 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 68.14 MHz | 68.14 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 253
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

