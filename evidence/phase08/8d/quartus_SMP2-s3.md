# MEASURED - Hasil Quartus untuk revisi `SMP2-s3`

- Dibuat: 2026-10-03 13:26 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase08c_smp/output_files_SMP2-s3`
- Catatan: Fase 8c/8d: kpke_smp_top_s10 revisi SMP2-s3, kernel-only dengan virtual pin; dikompilasi di quartus/phase08c_smp; working tree di atas commit d965b4d

## Fitter (`SMP2-s3.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 19:21:28 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | SMP2-s3 |
| Top-level Entity Name | kpke_smp_top_s10 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 11,009 / 41,910 ( 26 % ) |
| Total registers | 3402 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 81,694 / 5,662,720 ( 1 % ) |
| Total RAM Blocks | 44 / 553 ( 8 % ) |
| Total DSP Blocks | 26 / 112 ( 23 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`SMP2-s3.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 18.984 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.307 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 38.475 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.704 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.597 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 18.440 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.211 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 38.606 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.607 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.572 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 26.822 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.133 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 39.183 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.346 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.953 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.519 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.086 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 39.325 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.251 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.947 | 0.000 |

- Slack setup terburuk: **18.44 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.086 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`SMP2-s3.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 47.58 MHz | 47.58 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 46.38 MHz | 46.38 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 250
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

