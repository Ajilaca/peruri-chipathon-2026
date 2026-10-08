# MEASURED - Hasil Quartus untuk revisi `MW-20`

- Dibuat: 2026-10-04 02:05 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09m1_core/output_files_MW-20`
- Catatan: Fase 9M-1: mlkem_core dengan CODEC_W2 = 1 (tugas muat / simpan dua byte), revisi MW-20, kernel-only dengan virtual pin; branch phase9m-optimisation, rtl/mlkem pada file 9M-1

## Fitter (`MW-20.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 09:03:52 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MW-20 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 17,808 / 41,910 ( 42 % ) |
| Total registers | 8487 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`MW-20.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 4.355 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.340 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 18.627 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.566 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.573 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 4.673 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.199 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 18.728 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.481 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.542 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 10.309 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.148 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 19.318 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.233 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.906 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 12.131 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.081 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 19.430 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.152 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.909 | 0.000 |

- Slack setup terburuk: **4.355 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.081 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MW-20.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 63.92 MHz | 63.92 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 65.24 MHz | 65.24 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 253
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

