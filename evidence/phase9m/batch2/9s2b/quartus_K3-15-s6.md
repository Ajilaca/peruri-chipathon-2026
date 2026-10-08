# MEASURED - Hasil Quartus untuk revisi `K3-15-s6`

- Dibuat: 2026-10-04 16:04 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09s2b_core/output_files_K3-15-s6`
- Catatan: Fase 9F S2b: mlkem_core3 revisi K3-15-s6 (K2 + NTT_AR = 1), kernel-only dengan virtual pin, 15.000 ns; dikompilasi di quartus/phase09s2b_core; working tree di atas commit cf81581 (perubahan S2 / S2b belum di-commit)

## Fitter (`K3-15-s6.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 23:03:14 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K3-15-s6 |
| Top-level Entity Name | mlkem_core3 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,329 / 41,910 ( 34 % ) |
| Total registers | 8448 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,507 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 53 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`K3-15-s6.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 2.777 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.353 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.085 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 2.400 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.140 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.042 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 7.674 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.411 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 8.964 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.086 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.412 | 0.000 |

- Slack setup terburuk: **2.4 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.086 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K3-15-s6.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 81.81 MHz | 81.81 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 79.37 MHz | 79.37 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 255
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

