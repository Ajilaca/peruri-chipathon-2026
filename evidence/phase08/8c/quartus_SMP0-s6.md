# MEASURED - Hasil Quartus untuk revisi `SMP0-s6`

- Dibuat: 2026-10-03 13:26 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/par_c/output_files_SMP0-s6`
- Catatan: Fase 8c/8d: kpke_smp_top_s10 revisi SMP0-s6, kernel-only dengan virtual pin; dikompilasi di quartus/par_c (salinan quartus/phase08c_smp dengan .qsf, .sdc, dan sumber identik, dipakai untuk menjalankan kompilasi paralel; tidak di-commit); working tree di atas commit d965b4d

## Fitter (`SMP0-s6.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 20:21:50 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | SMP0-s6 |
| Top-level Entity Name | kpke_smp_top_s10 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 10,957 / 41,910 ( 26 % ) |
| Total registers | 3378 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 155,373 / 5,662,720 ( 3 % ) |
| Total RAM Blocks | 55 / 553 ( 10 % ) |
| Total DSP Blocks | 26 / 112 ( 23 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`SMP0-s6.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 18.078 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.395 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 36.905 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.116 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.590 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 17.119 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.223 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.042 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.961 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.559 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 26.400 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.178 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.276 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.608 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.945 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.046 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.091 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.553 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.422 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.943 | 0.000 |

- Slack setup terburuk: **17.119 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.091 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`SMP0-s6.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 45.62 MHz | 45.62 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 43.7 MHz | 43.7 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 243
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

