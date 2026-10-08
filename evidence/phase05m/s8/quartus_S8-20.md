# MEASURED - Hasil Quartus untuk revisi `S8-20`

- Dibuat: 2026-10-02 17:38 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase05m_memsched/output_files_S8-20`
- Catatan: Fase 5M langkah S8 kompilasi informasi pada 20.000 ns (quartus/phase05m_memsched/M-20.sdc), RTL dan seed 1 sama dengan S8; bukan bagian aturan adopsi; git 300aaf3

## Fitter (`S8-20.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Fri Oct  2 22:56:51 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | S8-20 |
| Top-level Entity Name | ntt_core_s8_p8 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,443 / 41,910 ( 23 % ) |
| Total registers | 4142 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,942 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 33 / 553 ( 6 % ) |
| Total DSP Blocks | 16 / 112 ( 14 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`S8-20.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | -1.771 | -18.802 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.418 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 17.003 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.873 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.605 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | -2.242 | -32.118 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.330 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 17.155 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.731 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.578 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 9.383 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.183 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 18.385 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.489 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.950 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 10.588 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.125 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 18.635 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.342 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.946 | 0.000 |

- Slack setup terburuk: **-2.242 ns** (Slow 1100mV -40C Model Setup 'clk_i')  **NEGATIVE: timing not met**
- Slack hold terburuk: **0.125 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`S8-20.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 45.93 MHz | 45.93 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 44.96 MHz | 44.96 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 3
- Peringatan: 20
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

