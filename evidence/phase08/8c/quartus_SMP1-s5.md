# MEASURED - Hasil Quartus untuk revisi `SMP1-s5`

- Dibuat: 2026-10-03 13:26 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/par_b/output_files_SMP1-s5`
- Catatan: Fase 8c/8d: kpke_smp_top_s10 revisi SMP1-s5, kernel-only dengan virtual pin; dikompilasi di quartus/par_b (salinan quartus/phase08c_smp dengan .qsf, .sdc, dan sumber identik, dipakai untuk menjalankan kompilasi paralel; tidak di-commit); working tree di atas commit d965b4d

## Fitter (`SMP1-s5.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 19:21:34 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | SMP1-s5 |
| Top-level Entity Name | kpke_smp_top_s10 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 11,032 / 41,910 ( 26 % ) |
| Total registers | 3391 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 81,694 / 5,662,720 ( 1 % ) |
| Total RAM Blocks | 44 / 553 ( 8 % ) |
| Total DSP Blocks | 26 / 112 ( 23 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`SMP1-s5.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 15.754 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.293 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 38.321 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.763 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.576 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 15.231 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.242 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 38.463 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.641 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.547 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.307 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.126 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 39.086 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.375 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.939 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.039 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.103 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 39.254 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.264 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.938 | 0.000 |

- Slack setup terburuk: **15.231 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.103 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`SMP1-s5.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 41.24 MHz | 41.24 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 40.37 MHz | 40.37 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 261
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

