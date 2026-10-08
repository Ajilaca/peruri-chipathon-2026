# MEASURED - Hasil Quartus untuk revisi `SMP2-20`

- Dibuat: 2026-10-03 13:26 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/par_a/output_files_SMP2-20`
- Catatan: Fase 8c/8d: kpke_smp_top_s10 revisi SMP2-20, kernel-only dengan virtual pin; dikompilasi di quartus/par_a (salinan quartus/phase08c_smp dengan .qsf, .sdc, dan sumber identik, dipakai untuk menjalankan kompilasi paralel; tidak di-commit); working tree di atas commit d965b4d

## Fitter (`SMP2-20.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 19:26:26 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | SMP2-20 |
| Top-level Entity Name | kpke_smp_top_s10 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 11,049 / 41,910 ( 26 % ) |
| Total registers | 3404 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 81,694 / 5,662,720 ( 1 % ) |
| Total RAM Blocks | 44 / 553 ( 8 % ) |
| Total DSP Blocks | 26 / 112 ( 23 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`SMP2-20.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 2.768 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.325 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 18.260 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.808 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.578 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 1.535 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.139 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 18.402 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.682 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.541 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 10.549 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 19.032 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.413 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.904 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 12.315 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.108 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 19.214 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.297 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.909 | 0.000 |

- Slack setup terburuk: **1.535 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.108 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`SMP2-20.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 58.03 MHz | 58.03 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 54.16 MHz | 54.16 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 250
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

