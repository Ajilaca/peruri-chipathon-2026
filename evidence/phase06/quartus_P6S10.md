# MEASURED - Hasil Quartus untuk revisi `P6S10`

- Dibuat: 2026-10-02 21:22 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase06_sched/output_files_P6S10`
- Catatan: Kompilasi informasi: top Fase 6 dengan inti S10 (rtl/sched/kpke_sched_top_s10.sv); batasan 40.000 ns; bawaan Quartus; seed 1; git 70e2938

## Fitter (`P6S10.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 04:18:37 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | P6S10 |
| Top-level Entity Name | kpke_sched_top_s10 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 5,553 / 41,910 ( 13 % ) |
| Total registers | 840 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 154,861 / 5,662,720 ( 3 % ) |
| Total RAM Blocks | 51 / 553 ( 9 % ) |
| Total DSP Blocks | 26 / 112 ( 23 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`P6S10.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 17.735 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.432 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 36.054 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.542 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.579 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 16.886 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.355 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 36.310 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.338 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.572 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 28.612 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.180 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 37.599 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.925 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.943 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 30.187 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.140 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.050 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.696 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.939 | 0.000 |

- Slack setup terburuk: **16.886 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.14 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`P6S10.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 44.91 MHz | 44.91 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 43.26 MHz | 43.26 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 22
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

