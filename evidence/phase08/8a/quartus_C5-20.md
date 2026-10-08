# MEASURED - Hasil Quartus untuk revisi `C5-20`

- Dibuat: 2026-10-03 05:49 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase08_keccak/output_files_C5-20`
- Catatan: Fase 8a C5-20: RTL sama dengan C5, 20.000 ns (C-20.sdc, informasi, bukan gerbang), seed 1, kernel-only dengan virtual pin

## Fitter (`C5-20.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 12:48:40 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | C5-20 |
| Top-level Entity Name | keccak_sponge_r2 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 6,178 / 41,910 ( 15 % ) |
| Total registers | 1652 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 0 / 5,662,720 ( 0 % ) |
| Total RAM Blocks | 0 / 553 ( 0 % ) |
| Total DSP Blocks | 0 / 112 ( 0 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`C5-20.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 4.591 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.418 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 9.258 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 5.042 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.441 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 9.182 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 10.433 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.177 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 9.603 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 12.195 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.162 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 9.589 | 0.000 |

- Slack setup terburuk: **4.591 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.162 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`C5-20.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 64.9 MHz | 64.9 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 66.85 MHz | 66.85 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 6
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

