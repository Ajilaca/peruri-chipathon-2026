# MEASURED - Hasil Quartus untuk revisi `SMP0-s5`

- Dibuat: 2026-10-03 13:26 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/par_b/output_files_SMP0-s5`
- Catatan: Fase 8c/8d: kpke_smp_top_s10 revisi SMP0-s5, kernel-only dengan virtual pin; dikompilasi di quartus/par_b (salinan quartus/phase08c_smp dengan .qsf, .sdc, dan sumber identik, dipakai untuk menjalankan kompilasi paralel; tidak di-commit); working tree di atas commit d965b4d

## Fitter (`SMP0-s5.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 19:37:01 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | SMP0-s5 |
| Top-level Entity Name | kpke_smp_top_s10 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 10,941 / 41,910 ( 26 % ) |
| Total registers | 3354 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 155,373 / 5,662,720 ( 3 % ) |
| Total RAM Blocks | 55 / 553 ( 10 % ) |
| Total DSP Blocks | 26 / 112 ( 23 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`SMP0-s5.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 16.703 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.307 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 36.775 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.070 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.577 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 16.272 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.283 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 36.996 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.898 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.524 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.333 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.158 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.037 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.677 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.905 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.467 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.134 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.403 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.483 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.907 | 0.000 |

- Slack setup terburuk: **16.272 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.134 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`SMP0-s5.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 42.92 MHz | 42.92 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 42.14 MHz | 42.14 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 243
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

