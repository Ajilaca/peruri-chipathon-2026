# MEASURED - Hasil Quartus untuk revisi `K0-s5`

- Dibuat: 2026-10-03 05:17 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase07_keccak/output_files_K0-s5`
- Catatan: Fase 7 baseline K0 untuk aturan 8a: RTL sama dengan K0, 40.000 ns (K.sdc), seed 5, kernel-only dengan virtual pin

## Fitter (`K0-s5.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 12:14:26 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K0-s5 |
| Top-level Entity Name | keccak_sponge |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 3,567 / 41,910 ( 9 % ) |
| Total registers | 1653 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 0 / 5,662,720 ( 0 % ) |
| Total RAM Blocks | 0 / 553 ( 0 % ) |
| Total DSP Blocks | 0 / 112 ( 0 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`K0-s5.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 25.646 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.418 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.274 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 26.413 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.407 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.177 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 31.181 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.177 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.610 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 32.856 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.163 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.593 | 0.000 |

- Slack setup terburuk: **25.646 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.163 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K0-s5.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 69.67 MHz | 69.67 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 73.6 MHz | 73.6 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 6
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

