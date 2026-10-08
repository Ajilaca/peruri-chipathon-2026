# MEASURED - Hasil Quartus untuk revisi `SMP1`

- Dibuat: 2026-10-03 13:26 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase08c_smp/output_files_SMP1`
- Catatan: Fase 8c/8d: kpke_smp_top_s10 revisi SMP1, kernel-only dengan virtual pin; dikompilasi di quartus/phase08c_smp; working tree di atas commit d965b4d

## Fitter (`SMP1.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 18:01:24 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | SMP1 |
| Top-level Entity Name | kpke_smp_top_s10 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 10,975 / 41,910 ( 26 % ) |
| Total registers | 3385 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 81,694 / 5,662,720 ( 1 % ) |
| Total RAM Blocks | 44 / 553 ( 8 % ) |
| Total DSP Blocks | 26 / 112 ( 23 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`SMP1.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 18.139 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.348 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.602 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.576 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.590 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 17.441 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.146 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.765 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.438 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.546 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.123 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.669 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.319 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.911 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.630 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.091 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.888 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.181 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.913 | 0.000 |

- Slack setup terburuk: **17.441 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.091 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`SMP1.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 45.74 MHz | 45.74 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 44.33 MHz | 44.33 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 261
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

