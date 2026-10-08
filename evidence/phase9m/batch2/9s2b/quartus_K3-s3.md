# MEASURED - Hasil Quartus untuk revisi `K3-s3`

- Dibuat: 2026-10-04 19:15 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09s2b_core/output_files_K3-s3`
- Catatan: Fase 9F S2b: mlkem_core3 (K2 + NTT_AR = 1): revisi K3-s3, kernel-only dengan virtual pin, 40.000 ns; dikompilasi di quartus/phase09s2b_core; working tree di atas commit cf81581 (perubahan S2 / S2b / butir 4 belum di-commit)

## Fitter (`K3-s3.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 23:26:16 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K3-s3 |
| Top-level Entity Name | mlkem_core3 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,125 / 41,910 ( 34 % ) |
| Total registers | 8483 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,603 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`K3-s3.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 20.620 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.250 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.850 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.055 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.583 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 21.406 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.165 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 38.003 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.931 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.554 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.412 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.135 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.762 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.557 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.944 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.954 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.111 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.993 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.423 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.943 | 0.000 |

- Slack setup terburuk: **20.62 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.111 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K3-s3.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 51.6 MHz | 51.6 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 53.78 MHz | 53.78 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 255
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

