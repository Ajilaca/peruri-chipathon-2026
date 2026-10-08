# MEASURED - Hasil Quartus untuk revisi `SMP0`

- Dibuat: 2026-10-03 13:26 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase08c_smp/output_files_SMP0`
- Catatan: Fase 8c/8d: kpke_smp_top_s10 revisi SMP0, kernel-only dengan virtual pin; dikompilasi di quartus/phase08c_smp; working tree di atas commit d965b4d

## Fitter (`SMP0.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 17:45:44 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | SMP0 |
| Top-level Entity Name | kpke_smp_top_s10 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 10,967 / 41,910 ( 26 % ) |
| Total registers | 3364 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 155,373 / 5,662,720 ( 3 % ) |
| Total RAM Blocks | 55 / 553 ( 10 % ) |
| Total DSP Blocks | 26 / 112 ( 23 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`SMP0.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 15.917 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.329 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 36.029 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.709 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.580 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 15.734 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.155 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 36.266 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.485 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.557 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 26.917 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.177 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 37.546 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 1.048 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.939 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 28.884 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.131 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.018 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.799 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.940 | 0.000 |

- Slack setup terburuk: **15.734 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.131 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`SMP0.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 41.52 MHz | 41.52 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 41.21 MHz | 41.21 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 243
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

