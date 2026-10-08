# MEASURED - Hasil Quartus untuk revisi `K1b-15-s5`

- Dibuat: 2026-10-04 12:08 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09f1b_core/output_files_K1b-15-s5`
- Catatan: Fase 9F langkah S1b: mlkem_core3 (sidecar hash latar belakang) dengan SMP_C5 = 0, HASH_C5 = 0, CODEC_W2 = 1, revisi K1b-15-s5, kernel-only dengan virtual pin; branch phase9m-optimisation

## Fitter (`K1b-15-s5.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 18:54:27 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K1b-15-s5 |
| Top-level Entity Name | mlkem_core3 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,455 / 41,910 ( 34 % ) |
| Total registers | 8276 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,270 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 53 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`K1b-15-s5.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 1.576 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.325 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.065 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 1.508 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.174 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.036 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 7.805 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.402 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 8.831 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.085 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.408 | 0.000 |

- Slack setup terburuk: **1.508 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.085 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K1b-15-s5.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 74.49 MHz | 74.49 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 74.12 MHz | 74.12 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 253
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

