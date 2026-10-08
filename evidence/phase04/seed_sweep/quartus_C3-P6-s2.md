# MEASURED - Hasil Quartus untuk revisi `C3-P6-s2`

- Dibuat: 2026-10-01 03:00 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase04_pipeline_c3/output_files_P6_s2`
- Catatan: Sapuan seed Fase 4 (masukan untuk ADR 0008): C3-P6 dengan SEED fitter 2; semua yang lain identik dengan C3-P6 (RTL pada git 7947c0c, C3.sdc 40.000 ns)

## Fitter (`C3-P6-s2.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Wed Sep 30 23:32:24 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | C3-P6-s2 |
| Top-level Entity Name | ntt_core_c3_p6 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 10,508 / 41,910 ( 25 % ) |
| Total registers | 4153 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,314 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 29 / 553 ( 5 % ) |
| Total DSP Blocks | 9 / 112 ( 8 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`C3-P6-s2.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 9.773 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.443 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.373 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.375 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.564 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 9.940 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.416 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.541 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.241 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.535 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 23.219 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.183 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.420 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.770 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.901 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 26.101 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.139 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.733 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.605 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.906 | 0.000 |

- Slack setup terburuk: **9.773 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.139 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`C3-P6-s2.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 33.08 MHz | 33.08 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 33.27 MHz | 33.27 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 19
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

