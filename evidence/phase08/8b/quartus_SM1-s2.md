# MEASURED - Hasil Quartus untuk revisi `SM1-s2`

- Dibuat: 2026-10-03 08:03 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase08b_sampler/output_files_SM1-s2`
- Catatan: Fase 8b tahap W1: keccak_sampler (SampleNTT dan CBD2 streaming, satu koefisien per siklus), revisi SM1-s2, kernel-only dengan virtual pin; RTL rtl/sample pada working tree di atas commit dcae678 (di-commit sesudahnya)

## Fitter (`SM1-s2.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 14:27:58 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | SM1-s2 |
| Top-level Entity Name | keccak_sampler |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 5,271 / 41,910 ( 13 % ) |
| Total registers | 1913 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 0 / 5,662,720 ( 0 % ) |
| Total RAM Blocks | 0 / 553 ( 0 % ) |
| Total DSP Blocks | 0 / 112 ( 0 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`SM1-s2.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 20.470 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.415 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.241 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 21.127 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.435 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.148 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.716 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.562 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 30.082 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.162 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.554 | 0.000 |

- Slack setup terburuk: **20.47 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.162 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`SM1-s2.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 51.2 MHz | 51.2 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 52.99 MHz | 52.99 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 7
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

