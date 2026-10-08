# MEASURED - Hasil Quartus untuk revisi `K3-15-s4`

- Dibuat: 2026-10-04 16:04 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09s2b_core/output_files_K3-15-s4`
- Catatan: Fase 9F S2b: mlkem_core3 revisi K3-15-s4 (K2 + NTT_AR = 1), kernel-only dengan virtual pin, 15.000 ns; dikompilasi di quartus/phase09s2b_core; working tree di atas commit cf81581 (perubahan S2 / S2b belum di-commit)

## Fitter (`K3-15-s4.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 22:48:23 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K3-15-s4 |
| Top-level Entity Name | mlkem_core3 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,139 / 41,910 ( 34 % ) |
| Total registers | 8441 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,507 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 53 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`K3-15-s4.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 1.666 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.332 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.074 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 1.305 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.163 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.046 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 8.034 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.144 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.406 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 9.133 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.090 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.410 | 0.000 |

- Slack setup terburuk: **1.305 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.09 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K3-15-s4.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 75.0 MHz | 75.0 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 73.02 MHz | 73.02 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 255
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

