# MEASURED - Hasil Quartus untuk revisi `SMP0-s4`

- Dibuat: 2026-10-03 13:26 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase08c_smp/output_files_SMP0-s4`
- Catatan: Fase 8c/8d: kpke_smp_top_s10 revisi SMP0-s4, kernel-only dengan virtual pin; dikompilasi di quartus/phase08c_smp; working tree di atas commit d965b4d

## Fitter (`SMP0-s4.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 19:36:49 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | SMP0-s4 |
| Top-level Entity Name | kpke_smp_top_s10 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 10,944 / 41,910 ( 26 % ) |
| Total registers | 3345 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 155,373 / 5,662,720 ( 3 % ) |
| Total RAM Blocks | 55 / 553 ( 10 % ) |
| Total DSP Blocks | 26 / 112 ( 23 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`SMP0-s4.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 18.089 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.287 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.854 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.057 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.590 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 17.415 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.272 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 38.000 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.933 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.571 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.934 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.151 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.767 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.555 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.946 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.844 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.125 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.999 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.425 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.945 | 0.000 |

- Slack setup terburuk: **17.415 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.125 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`SMP0-s4.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 45.64 MHz | 45.64 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 44.28 MHz | 44.28 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 243
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

