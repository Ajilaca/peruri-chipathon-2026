# MEASURED - Hasil Quartus untuk revisi `S10-20-s4`

- Dibuat: 2026-10-02 20:27 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase06_sched/output_files_S10-20-s4`
- Catatan: Kandidat S10: rtl/ntt/ntt_core_s10_p5.sv (memori 16 bank 1R1W tanpa arbitrasi slot, P = 5; ADR 0024, test plan evidence/phase06/test_plan_s10.md); batasan 20.000 ns; bawaan Quartus; git 8d8cb6f

## Fitter (`S10-20-s4.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 03:19:16 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | S10-20-s4 |
| Top-level Entity Name | ntt_core_s10_p5 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 5,094 / 41,910 ( 12 % ) |
| Total registers | 562 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 4,069 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 24 / 553 ( 4 % ) |
| Total DSP Blocks | 16 / 112 ( 14 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`S10-20-s4.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 2.121 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.442 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 16.462 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.220 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.603 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 1.050 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.415 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 16.722 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.011 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.592 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 11.357 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.183 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 17.806 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.792 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.952 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 12.373 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.148 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 18.228 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.576 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.947 | 0.000 |

- Slack setup terburuk: **1.05 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.148 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`S10-20-s4.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 55.93 MHz | 55.93 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 52.77 MHz | 52.77 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 18
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

