# MEASURED - Hasil Quartus untuk revisi `K1b`

- Dibuat: 2026-10-04 12:08 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09f1b_core/output_files_K1b`
- Catatan: Fase 9F langkah S1b: mlkem_core3 (sidecar hash latar belakang) dengan SMP_C5 = 0, HASH_C5 = 0, CODEC_W2 = 1, revisi K1b, kernel-only dengan virtual pin; branch phase9m-optimisation

## Fitter (`K1b.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 17:11:51 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K1b |
| Top-level Entity Name | mlkem_core3 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,338 / 41,910 ( 34 % ) |
| Total registers | 8254 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`K1b.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 20.857 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.285 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.802 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.496 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.579 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 21.642 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.272 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.935 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.361 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.525 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.666 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.149 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.837 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.241 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.904 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 30.084 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.110 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 39.010 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.126 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.908 | 0.000 |

- Slack setup terburuk: **20.857 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.11 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K1b.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 52.24 MHz | 52.24 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 54.47 MHz | 54.47 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 253
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

