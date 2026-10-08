# MEASURED - Hasil Quartus untuk revisi `K0-s2`

- Dibuat: 2026-10-03 05:17 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase07_keccak/output_files_K0-s2`
- Catatan: Fase 7 baseline K0 untuk aturan 8a: RTL sama dengan K0, 40.000 ns (K.sdc), seed 2, kernel-only dengan virtual pin

## Fitter (`K0-s2.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 12:05:09 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K0-s2 |
| Top-level Entity Name | keccak_sponge |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 3,569 / 41,910 ( 9 % ) |
| Total registers | 1653 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 0 / 5,662,720 ( 0 % ) |
| Total RAM Blocks | 0 / 553 ( 0 % ) |
| Total DSP Blocks | 0 / 112 ( 0 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`K0-s2.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 24.373 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.418 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.272 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 25.142 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.374 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.186 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 29.953 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.177 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.611 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 31.957 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.164 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.595 | 0.000 |

- Slack setup terburuk: **24.373 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.164 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K0-s2.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 63.99 MHz | 63.99 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 67.3 MHz | 67.3 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 6
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

