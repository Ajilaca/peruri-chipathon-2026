# MEASURED - Hasil Quartus untuk revisi `MW-20-s4`

- Dibuat: 2026-10-04 04:55 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09m2_core/output_files_MW-20-s4`
- Catatan: Fase 9M-2: mlkem_core pada 20.000 ns, revisi MW-20-s4, kernel-only dengan virtual pin; branch phase9m-optimisation

## Fitter (`MW-20-s4.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 11:33:48 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MW-20-s4 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 17,759 / 41,910 ( 42 % ) |
| Total registers | 8460 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`MW-20-s4.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 4.498 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.347 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 17.998 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.039 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.568 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 4.894 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.302 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 18.108 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.911 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.540 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 10.739 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 18.959 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.492 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.901 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 12.350 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.112 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 19.126 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.357 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.907 | 0.000 |

- Slack setup terburuk: **4.498 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.112 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MW-20-s4.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 64.51 MHz | 64.51 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 66.2 MHz | 66.2 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 253
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

