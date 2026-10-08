# MEASURED - Hasil Quartus untuk revisi `S10-20-s6`

- Dibuat: 2026-10-02 20:27 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase06_sched/output_files_S10-20-s6`
- Catatan: Kandidat S10: rtl/ntt/ntt_core_s10_p5.sv (memori 16 bank 1R1W tanpa arbitrasi slot, P = 5; ADR 0024, test plan evidence/phase06/test_plan_s10.md); batasan 20.000 ns; bawaan Quartus; git 8d8cb6f

## Fitter (`S10-20-s6.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 03:26:10 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | S10-20-s6 |
| Top-level Entity Name | ntt_core_s10_p5 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 5,123 / 41,910 ( 12 % ) |
| Total registers | 567 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 4,069 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 24 / 553 ( 4 % ) |
| Total DSP Blocks | 16 / 112 ( 14 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`S10-20-s6.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 1.457 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.382 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 16.080 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.632 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.582 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 0.792 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.363 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 16.280 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.464 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.553 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 10.619 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.183 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 17.727 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.934 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.939 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 12.091 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.169 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 18.114 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.697 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.940 | 0.000 |

- Slack setup terburuk: **0.792 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.169 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`S10-20-s6.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 53.93 MHz | 53.93 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 52.06 MHz | 52.06 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 18
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

