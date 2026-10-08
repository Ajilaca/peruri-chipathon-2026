# MEASURED - Hasil Quartus untuk revisi `C5-s4`

- Dibuat: 2026-10-03 05:44 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase08_keccak/output_files_C5-s4`
- Catatan: Fase 8a C5: keccak_sponge_r2 (dua ronde Keccak per siklus), 40.000 ns (C.sdc), seed 4, kernel-only dengan virtual pin; RTL pada commit 4926b1a

## Fitter (`C5-s4.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 12:34:54 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | C5-s4 |
| Top-level Entity Name | keccak_sponge_r2 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 6,169 / 41,910 ( 15 % ) |
| Total registers | 1652 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 0 / 5,662,720 ( 0 % ) |
| Total RAM Blocks | 0 / 553 ( 0 % ) |
| Total DSP Blocks | 0 / 112 ( 0 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`C5-s4.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 20.582 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.420 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.258 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 21.313 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.440 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.144 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.889 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.567 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 30.238 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.162 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.555 | 0.000 |

- Slack setup terburuk: **20.582 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.162 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`C5-s4.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 51.5 MHz | 51.5 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 53.51 MHz | 53.51 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 6
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

