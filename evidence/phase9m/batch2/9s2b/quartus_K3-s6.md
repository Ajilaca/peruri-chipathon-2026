# MEASURED - Hasil Quartus untuk revisi `K3-s6`

- Dibuat: 2026-10-04 19:15 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09s2b_core/output_files_K3-s6`
- Catatan: Fase 9F S2b: mlkem_core3 (K2 + NTT_AR = 1): revisi K3-s6, kernel-only dengan virtual pin, 40.000 ns; dikompilasi di quartus/phase09s2b_core; working tree di atas commit cf81581 (perubahan S2 / S2b / butir 4 belum di-commit)

## Fitter (`K3-s6.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 23:51:05 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K3-s6 |
| Top-level Entity Name | mlkem_core3 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,133 / 41,910 ( 34 % ) |
| Total registers | 8462 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,603 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`K3-s6.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 20.354 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.319 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 38.155 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.871 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.570 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 20.884 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.201 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 38.314 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.725 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.511 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.406 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.151 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.974 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.435 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.902 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.871 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.122 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 39.166 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.312 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.906 | 0.000 |

- Slack setup terburuk: **20.354 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.122 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K3-s6.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 50.9 MHz | 50.9 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 52.31 MHz | 52.31 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 255
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

