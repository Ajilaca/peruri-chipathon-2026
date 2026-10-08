# MEASURED - Hasil Quartus untuk revisi `K2-15-s6`

- Dibuat: 2026-10-04 15:05 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09s2_core/output_files_K2-15-s6`
- Catatan: Fase 9F S2: mlkem_core3 revisi K2-15-s6 (K1b + NTT_P6 = 1), kernel-only dengan virtual pin, 15.000 ns; dikompilasi di quartus/phase09s2_core; working tree di atas commit cf81581 (perubahan S2 belum di-commit)

## Fitter (`K2-15-s6.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 21:59:49 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K2-15-s6 |
| Top-level Entity Name | mlkem_core3 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,391 / 41,910 ( 34 % ) |
| Total registers | 8343 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,507 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 53 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`K2-15-s6.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 1.929 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.310 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.073 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 1.782 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.128 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.049 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 8.119 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.147 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.401 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 9.137 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.098 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.406 | 0.000 |

- Slack setup terburuk: **1.782 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.098 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K2-15-s6.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 76.51 MHz | 76.51 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 75.65 MHz | 75.65 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 254
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

