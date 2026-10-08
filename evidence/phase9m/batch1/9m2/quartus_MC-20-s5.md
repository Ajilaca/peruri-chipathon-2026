# MEASURED - Hasil Quartus untuk revisi `MC-20-s5`

- Dibuat: 2026-10-04 04:55 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09m2_core/output_files_MC-20-s5`
- Catatan: Fase 9M-2: mlkem_core pada 20.000 ns, revisi MC-20-s5, kernel-only dengan virtual pin; branch phase9m-optimisation

## Fitter (`MC-20-s5.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 10:53:50 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MC-20-s5 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 17,682 / 41,910 ( 42 % ) |
| Total registers | 8461 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`MC-20-s5.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 4.522 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.364 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 17.251 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.400 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.577 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 5.055 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.228 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 17.462 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.240 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.531 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 10.779 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 18.305 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.818 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.904 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 12.424 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.109 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 18.645 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.631 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.906 | 0.000 |

- Slack setup terburuk: **4.522 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.109 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MC-20-s5.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 64.61 MHz | 64.61 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 66.91 MHz | 66.91 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 253
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

