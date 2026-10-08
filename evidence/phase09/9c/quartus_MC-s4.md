# MEASURED - Hasil Quartus untuk revisi `MC-s4`

- Dibuat: 2026-10-03 18:15 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09c_core/output_files_MC-s4`
- Catatan: Fase 9c: mlkem_core (KeyGen, Encaps, Decaps; mesin 8d, codec, hash dengan sponge C5, pembanding), revisi MC-s4, kernel-only dengan virtual pin; working tree sebelum commit Fase 9

## Fitter (`MC-s4.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 00:40:59 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MC-s4 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 17,623 / 41,910 ( 42 % ) |
| Total registers | 8232 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`MC-s4.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 19.815 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.308 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 38.473 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.654 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.574 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 20.364 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.281 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 38.605 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.529 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.543 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 26.959 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.158 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 39.201 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.296 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.934 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.564 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.133 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 39.343 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.197 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.935 | 0.000 |

- Slack setup terburuk: **19.815 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.133 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MC-s4.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 49.54 MHz | 49.54 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 50.93 MHz | 50.93 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 253
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

