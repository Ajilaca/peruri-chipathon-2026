# MEASURED - Hasil Quartus untuk revisi `C3-P4-s6`

- Dibuat: 2026-10-01 03:00 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase04_pipeline_c3/output_files_P4_s6`
- Catatan: Sapuan seed Fase 4 (masukan untuk ADR 0008): C3-P4 dengan SEED fitter 6; semua yang lain identik dengan C3-P4 (RTL pada git 7947c0c, C3.sdc 40.000 ns)

## Fitter (`C3-P4-s6.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Thu Oct  1 09:55:02 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | C3-P4-s6 |
| Top-level Entity Name | ntt_core_c3_p4 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 10,468 / 41,910 ( 25 % ) |
| Total registers | 4149 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 27,428 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 26 / 553 ( 5 % ) |
| Total DSP Blocks | 9 / 112 ( 8 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`C3-P4-s6.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 9.701 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.445 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.630 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 9.704 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.399 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.601 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 23.194 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.182 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.961 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 26.046 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.130 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.953 | 0.000 |

- Slack setup terburuk: **9.701 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.13 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`C3-P4-s6.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 33.0 MHz | 33.0 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 33.01 MHz | 33.01 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 19
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

