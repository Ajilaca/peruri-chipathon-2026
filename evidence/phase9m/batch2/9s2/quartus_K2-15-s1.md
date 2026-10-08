# MEASURED - Hasil Quartus untuk revisi `K2-15-s1`

- Dibuat: 2026-10-04 15:05 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09s2_core/output_files_K2-15-s1`
- Catatan: Fase 9F S2: mlkem_core3 revisi K2-15-s1 (K1b + NTT_P6 = 1), kernel-only dengan virtual pin, 15.000 ns; dikompilasi di quartus/phase09s2_core; working tree di atas commit cf81581 (perubahan S2 belum di-commit)

## Fitter (`K2-15-s1.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 21:26:58 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K2-15-s1 |
| Top-level Entity Name | mlkem_core3 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,308 / 41,910 ( 34 % ) |
| Total registers | 8383 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,507 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 53 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`K2-15-s1.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 1.959 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.361 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.087 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 1.624 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.267 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.069 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 7.538 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.177 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.445 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 8.879 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.117 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.442 | 0.000 |

- Slack setup terburuk: **1.624 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.117 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K2-15-s1.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 76.68 MHz | 76.68 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 74.76 MHz | 74.76 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 254
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

