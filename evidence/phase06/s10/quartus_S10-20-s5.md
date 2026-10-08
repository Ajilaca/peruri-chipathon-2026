# MEASURED - Hasil Quartus untuk revisi `S10-20-s5`

- Dibuat: 2026-10-02 20:27 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase06_sched/output_files_S10-20-s5`
- Catatan: Kandidat S10: rtl/ntt/ntt_core_s10_p5.sv (memori 16 bank 1R1W tanpa arbitrasi slot, P = 5; ADR 0024, test plan evidence/phase06/test_plan_s10.md); batasan 20.000 ns; bawaan Quartus; git 8d8cb6f

## Fitter (`S10-20-s5.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 03:22:49 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | S10-20-s5 |
| Top-level Entity Name | ntt_core_s10_p5 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 5,181 / 41,910 ( 12 % ) |
| Total registers | 563 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 4,069 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 24 / 553 ( 4 % ) |
| Total DSP Blocks | 16 / 112 ( 14 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`S10-20-s5.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 2.260 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.378 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 17.171 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.919 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.599 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 1.241 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.360 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 17.355 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.754 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.580 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 11.590 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.183 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 18.351 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.541 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.950 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 12.544 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.131 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 18.640 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.375 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.948 | 0.000 |

- Slack setup terburuk: **1.241 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.131 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`S10-20-s5.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 56.37 MHz | 56.37 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 53.31 MHz | 53.31 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 18
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

