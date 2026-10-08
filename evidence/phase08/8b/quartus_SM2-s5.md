# MEASURED - Hasil Quartus untuk revisi `SM2-s5`

- Dibuat: 2026-10-03 10:59 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase08b_sampler/output_files_SM2-s5`
- Catatan: Fase 8b tahap W2: keccak_sampler OUTW = 2 (SampleNTT dan CBD2 streaming, dua koefisien per siklus), revisi SM2-s5, kernel-only dengan virtual pin; working tree di atas commit 794db0d (RTL W2 di-commit sesudahnya)

## Fitter (`SM2-s5.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 17:11:31 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | SM2-s5 |
| Top-level Entity Name | keccak_sampler |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 5,305 / 41,910 ( 13 % ) |
| Total registers | 1947 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 0 / 5,662,720 ( 0 % ) |
| Total RAM Blocks | 0 / 553 ( 0 % ) |
| Total DSP Blocks | 0 / 112 ( 0 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`SM2-s5.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 20.187 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.372 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.250 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 21.166 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.358 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.143 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.304 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.567 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.785 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.162 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.553 | 0.000 |

- Slack setup terburuk: **20.187 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.162 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`SM2-s5.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 50.47 MHz | 50.47 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 53.1 MHz | 53.1 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 7
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

