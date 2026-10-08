# MEASURED - Hasil Quartus untuk revisi `K3-s5`

- Dibuat: 2026-10-04 19:15 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09s2b_core/output_files_K3-s5`
- Catatan: Fase 9F S2b: mlkem_core3 (K2 + NTT_AR = 1): revisi K3-s5, kernel-only dengan virtual pin, 40.000 ns; dikompilasi di quartus/phase09s2b_core; working tree di atas commit cf81581 (perubahan S2 / S2b / butir 4 belum di-commit)

## Fitter (`K3-s5.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 23:43:11 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K3-s5 |
| Top-level Entity Name | mlkem_core3 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,081 / 41,910 ( 34 % ) |
| Total registers | 8508 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,603 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`K3-s5.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 21.067 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.332 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.796 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.081 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.582 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 21.845 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.270 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.944 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.960 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.532 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 28.009 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.143 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.702 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.596 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.909 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 30.336 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.098 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.951 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.456 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.911 | 0.000 |

- Slack setup terburuk: **21.067 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.098 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K3-s5.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 52.82 MHz | 52.82 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 55.08 MHz | 55.08 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 255
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

