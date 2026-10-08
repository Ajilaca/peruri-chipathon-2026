# MEASURED - Hasil Quartus untuk revisi `K2-s4`

- Dibuat: 2026-10-04 13:51 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09s2_core/output_files_K2-s4`
- Catatan: Fase 9F S2: mlkem_core3 revisi K2-s4 (K1b + NTT_P6 = 1), kernel-only dengan virtual pin, 40.000 ns; dikompilasi di quartus/phase09s2_core; working tree di atas commit cf81581 (perubahan S2 belum di-commit)

## Fitter (`K2-s4.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 20:21:43 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K2-s4 |
| Top-level Entity Name | mlkem_core3 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,194 / 41,910 ( 34 % ) |
| Total registers | 8327 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,603 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`K2-s4.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 21.174 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.297 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.164 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.859 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.554 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 21.389 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.315 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.351 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.701 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.520 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 28.055 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.128 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.360 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.503 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.897 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 30.429 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.109 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.644 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.342 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.903 | 0.000 |

- Slack setup terburuk: **21.174 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.109 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K2-s4.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 53.12 MHz | 53.12 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 53.73 MHz | 53.73 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 254
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

