# MEASURED - Hasil Quartus untuk revisi `SMP1-20`

- Dibuat: 2026-10-03 13:26 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/par_a/output_files_SMP1-20`
- Catatan: Fase 8c/8d: kpke_smp_top_s10 revisi SMP1-20, kernel-only dengan virtual pin; dikompilasi di quartus/par_a (salinan quartus/phase08c_smp dengan .qsf, .sdc, dan sumber identik, dipakai untuk menjalankan kompilasi paralel; tidak di-commit); working tree di atas commit d965b4d

## Fitter (`SMP1-20.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 19:43:12 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | SMP1-20 |
| Top-level Entity Name | kpke_smp_top_s10 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 11,031 / 41,910 ( 26 % ) |
| Total registers | 3474 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 81,694 / 5,662,720 ( 1 % ) |
| Total RAM Blocks | 44 / 553 ( 8 % ) |
| Total DSP Blocks | 26 / 112 ( 23 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`SMP1-20.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 2.498 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.310 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 16.295 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.555 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.567 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 1.783 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.185 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 16.475 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.367 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.531 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 10.473 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.170 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 17.920 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.838 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.901 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 12.195 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.095 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 18.258 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.612 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.904 | 0.000 |

- Slack setup terburuk: **1.783 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.095 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`SMP1-20.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 57.14 MHz | 57.14 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 54.89 MHz | 54.89 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 261
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

