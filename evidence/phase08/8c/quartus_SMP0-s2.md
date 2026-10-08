# MEASURED - Hasil Quartus untuk revisi `SMP0-s2`

- Dibuat: 2026-10-03 13:26 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase08c_smp/output_files_SMP0-s2`
- Catatan: Fase 8c/8d: kpke_smp_top_s10 revisi SMP0-s2, kernel-only dengan virtual pin; dikompilasi di quartus/phase08c_smp; working tree di atas commit d965b4d

## Fitter (`SMP0-s2.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 18:26:30 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | SMP0-s2 |
| Top-level Entity Name | kpke_smp_top_s10 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 10,969 / 41,910 ( 26 % ) |
| Total registers | 3342 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 155,373 / 5,662,720 ( 3 % ) |
| Total RAM Blocks | 55 / 553 ( 10 % ) |
| Total DSP Blocks | 26 / 112 ( 23 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`SMP0-s2.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 17.213 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.258 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.907 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.027 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.571 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 16.417 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.244 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 38.072 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.886 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.527 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 26.400 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.142 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.804 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.532 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.902 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.111 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.098 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 39.037 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.397 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.906 | 0.000 |

- Slack setup terburuk: **16.417 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.098 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`SMP0-s2.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 43.88 MHz | 43.88 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 42.4 MHz | 42.4 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 243
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

