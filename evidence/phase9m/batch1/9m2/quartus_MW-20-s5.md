# MEASURED - Hasil Quartus untuk revisi `MW-20-s5`

- Dibuat: 2026-10-04 04:55 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09m2_core/output_files_MW-20-s5`
- Catatan: Fase 9M-2: mlkem_core pada 20.000 ns, revisi MW-20-s5, kernel-only dengan virtual pin; branch phase9m-optimisation

## Fitter (`MW-20-s5.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 11:43:42 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MW-20-s5 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 17,845 / 41,910 ( 43 % ) |
| Total registers | 8481 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`MW-20-s5.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 4.184 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.358 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 17.349 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.786 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.597 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 4.740 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.291 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 17.528 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.628 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.571 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 10.073 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 18.480 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.458 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.950 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 12.003 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.100 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 18.741 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.307 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.946 | 0.000 |

- Slack setup terburuk: **4.184 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.1 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MW-20-s5.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 63.23 MHz | 63.23 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 65.53 MHz | 65.53 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 253
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

