# MEASURED - Hasil Quartus untuk revisi `P6`

- Dibuat: 2026-10-02 19:27 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase06_sched/output_files_P6`
- Catatan: Top Fase 6 rtl/sched/kpke_sched_top.sv (sequencer aritmetika K-PKE, poly_store 24 slot, pwm_unit, inti NTT S7); batasan 40.000 ns (quartus/phase06_sched/P.sdc); bawaan Quartus; seed 1; git 016bff0

## Fitter (`P6.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 02:25:00 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | P6 |
| Top-level Entity Name | kpke_sched_top |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,840 / 41,910 ( 23 % ) |
| Total registers | 4589 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 181,222 / 5,662,720 ( 3 % ) |
| Total RAM Blocks | 58 / 553 ( 10 % ) |
| Total DSP Blocks | 26 / 112 ( 23 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`P6.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 14.005 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.434 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 36.765 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.267 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.559 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 13.395 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.307 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 36.988 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.053 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.529 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 26.809 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.179 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 37.967 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.682 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.902 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 28.421 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.123 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.377 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.475 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.904 | 0.000 |

- Slack setup terburuk: **13.395 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.123 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`P6.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 38.47 MHz | 38.47 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 37.59 MHz | 37.59 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 23
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

