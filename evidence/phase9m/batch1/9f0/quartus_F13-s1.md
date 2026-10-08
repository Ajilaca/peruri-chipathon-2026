# MEASURED - Hasil Quartus untuk revisi `F13-s1`

- Dibuat: 2026-10-04 09:34 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09f0_core/output_files_F13-s1`
- Catatan: Fase 9F langkah S0 amandemen A2: inti 9M-1 pada 13.000 ns, revisi F13-s1, kernel-only dengan virtual pin; branch phase9m-optimisation

## Fitter (`F13-s1.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 16:07:39 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | F13-s1 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 17,900 / 41,910 ( 43 % ) |
| Total registers | 8807 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,270 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 53 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`F13-s1.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 0.227 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.327 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 5.078 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 0.609 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.214 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 5.068 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 5.230 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 5.443 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 6.652 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.112 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 5.440 | 0.000 |

- Slack setup terburuk: **0.227 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.112 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`F13-s1.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 78.29 MHz | 78.29 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 80.7 MHz | 80.7 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 253
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

