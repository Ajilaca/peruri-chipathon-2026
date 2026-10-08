# MEASURED - Hasil Quartus untuk revisi `C5-s2`

- Dibuat: 2026-10-03 05:44 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase08_keccak/output_files_C5-s2`
- Catatan: Fase 8a C5: keccak_sponge_r2 (dua ronde Keccak per siklus), 40.000 ns (C.sdc), seed 2, kernel-only dengan virtual pin; RTL pada commit 4926b1a

## Fitter (`C5-s2.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 12:25:54 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | C5-s2 |
| Top-level Entity Name | keccak_sponge_r2 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 6,166 / 41,910 ( 15 % ) |
| Total registers | 1652 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 0 / 5,662,720 ( 0 % ) |
| Total RAM Blocks | 0 / 553 ( 0 % ) |
| Total DSP Blocks | 0 / 112 ( 0 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`C5-s2.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 20.648 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.416 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.242 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 21.299 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.439 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.147 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.677 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.563 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 30.054 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.162 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.554 | 0.000 |

- Slack setup terburuk: **20.648 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.162 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`C5-s2.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 51.67 MHz | 51.67 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 53.47 MHz | 53.47 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 6
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

