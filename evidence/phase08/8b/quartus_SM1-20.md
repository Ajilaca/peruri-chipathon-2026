# MEASURED - Hasil Quartus untuk revisi `SM1-20`

- Dibuat: 2026-10-03 08:03 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase08b_sampler/output_files_SM1-20`
- Catatan: Fase 8b tahap W1: keccak_sampler (SampleNTT dan CBD2 streaming, satu koefisien per siklus), revisi SM1-20, kernel-only dengan virtual pin; RTL rtl/sample pada working tree di atas commit dcae678 (di-commit sesudahnya)

## Fitter (`SM1-20.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 14:57:32 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | SM1-20 |
| Top-level Entity Name | keccak_sampler |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 5,296 / 41,910 ( 13 % ) |
| Total registers | 1913 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 0 / 5,662,720 ( 0 % ) |
| Total RAM Blocks | 0 / 553 ( 0 % ) |
| Total DSP Blocks | 0 / 112 ( 0 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`SM1-20.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 3.892 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.415 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 9.262 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 4.330 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.437 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 9.189 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 10.063 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 9.607 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 11.882 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.161 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 9.591 | 0.000 |

- Slack setup terburuk: **3.892 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.161 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`SM1-20.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 62.08 MHz | 62.08 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 63.82 MHz | 63.82 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 7
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

