# MEASURED - Hasil Quartus untuk revisi `C3-P2`

- Dibuat: 2026-09-30 16:10 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase04_pipeline_c3/output_files_P2`
- Catatan: Fase 4 P=2: rtl/ntt/ntt_core_c3_p2.sv (C3, L=8, potongan A_13, D_3 menurut test_plan.md bagian 2); batasan 40.000 ns (quartus/phase04_pipeline_c3/C3.sdc, ADR 0006); seed fitter bawaan; RTL = working tree di atas git c2cc16c, di-commit bersama file ini

## Fitter (`C3-P2.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Wed Sep 30 22:58:56 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | C3-P2 |
| Top-level Entity Name | ntt_core_c3_p2 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,696 / 41,910 ( 23 % ) |
| Total registers | 3817 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 22,784 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 16 / 553 ( 3 % ) |
| Total DSP Blocks | 9 / 112 ( 8 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`C3-P2.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 0.061 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.380 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.589 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | -0.368 | -2.430 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.360 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.540 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 19.955 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.184 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.911 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 22.551 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.174 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.911 | 0.000 |

- Slack setup terburuk: **-0.368 ns** (Slow 1100mV -40C Model Setup 'clk_i')  **NEGATIVE: timing not met**
- Slack hold terburuk: **0.174 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`C3-P2.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 25.04 MHz | 25.04 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 24.77 MHz | 24.77 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 2
- Peringatan: 19
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

