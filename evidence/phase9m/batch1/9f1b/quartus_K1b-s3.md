# MEASURED - Hasil Quartus untuk revisi `K1b-s3`

- Dibuat: 2026-10-04 12:08 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09f1b_core/output_files_K1b-s3`
- Catatan: Fase 9F langkah S1b: mlkem_core3 (sidecar hash latar belakang) dengan SMP_C5 = 0, HASH_C5 = 0, CODEC_W2 = 1, revisi K1b-s3, kernel-only dengan virtual pin; branch phase9m-optimisation

## Fitter (`K1b-s3.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 17:28:54 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K1b-s3 |
| Top-level Entity Name | mlkem_core3 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,332 / 41,910 ( 34 % ) |
| Total registers | 8247 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`K1b-s3.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 20.776 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.292 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.108 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.518 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.590 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 21.079 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.277 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.308 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.348 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.557 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.744 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.151 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.281 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.813 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.947 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 30.184 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.113 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.620 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.634 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.945 | 0.000 |

- Slack setup terburuk: **20.776 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.113 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K1b-s3.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 52.02 MHz | 52.02 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 52.85 MHz | 52.85 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 253
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

