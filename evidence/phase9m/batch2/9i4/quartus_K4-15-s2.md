# MEASURED - Hasil Quartus untuk revisi `K4-15-s2`

- Dibuat: 2026-10-04 19:15 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09i4_core/output_files_K4-15-s2`
- Catatan: Fase 9I butir 4: mlkem_core4 (parameter K3): revisi K4-15-s2, kernel-only dengan virtual pin, 15.000 ns; dikompilasi di quartus/phase09i4_core; working tree di atas commit cf81581 (perubahan S2 / S2b / butir 4 belum di-commit)

## Fitter (`K4-15-s2.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Mon Oct  5 00:36:41 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K4-15-s2 |
| Top-level Entity Name | mlkem_core4 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,493 / 41,910 ( 35 % ) |
| Total registers | 8564 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,507 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 53 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`K4-15-s2.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 1.915 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.303 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.074 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 1.662 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.123 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.028 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 7.457 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.156 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.400 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 8.867 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.085 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.403 | 0.000 |

- Slack setup terburuk: **1.662 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.085 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K4-15-s2.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 76.42 MHz | 76.42 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 74.97 MHz | 74.97 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 255
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

