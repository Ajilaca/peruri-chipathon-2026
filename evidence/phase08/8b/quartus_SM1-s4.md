# MEASURED - Hasil Quartus untuk revisi `SM1-s4`

- Dibuat: 2026-10-03 08:03 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase08b_sampler/output_files_SM1-s4`
- Catatan: Fase 8b tahap W1: keccak_sampler (SampleNTT dan CBD2 streaming, satu koefisien per siklus), revisi SM1-s4, kernel-only dengan virtual pin; RTL rtl/sample pada working tree di atas commit dcae678 (di-commit sesudahnya)

## Fitter (`SM1-s4.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 14:40:41 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | SM1-s4 |
| Top-level Entity Name | keccak_sampler |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 5,311 / 41,910 ( 13 % ) |
| Total registers | 1913 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 0 / 5,662,720 ( 0 % ) |
| Total RAM Blocks | 0 / 553 ( 0 % ) |
| Total DSP Blocks | 0 / 112 ( 0 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`SM1-s4.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 20.038 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.419 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.275 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 20.816 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.427 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.192 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.544 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.177 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.611 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.886 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.163 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.595 | 0.000 |

- Slack setup terburuk: **20.038 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.163 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`SM1-s4.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 50.1 MHz | 50.1 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 52.13 MHz | 52.13 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 7
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

