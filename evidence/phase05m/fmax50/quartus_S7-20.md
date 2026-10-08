# MEASURED - Hasil Quartus untuk revisi `S7-20`

- Dibuat: 2026-10-02 20:02 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase05m_memsched/output_files_S7-20`
- Catatan: Pertanyaan 50 MHz opsi 2: RTL S7 (rtl/ntt/ntt_core_s7_p7.sv) pada 20.000 ns (quartus/phase05m_memsched/M-20.sdc), hanya informasi; bawaan Quartus; git 8133e08

## Fitter (`S7-20.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 02:09:42 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | S7-20 |
| Top-level Entity Name | ntt_core_s7_p7 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,365 / 41,910 ( 22 % ) |
| Total registers | 4327 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,423 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 31 / 553 ( 6 % ) |
| Total DSP Blocks | 16 / 112 ( 14 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`S7-20.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | -0.836 | -8.565 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.442 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 15.836 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.396 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.599 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | -1.388 | -16.724 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.401 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 16.124 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.242 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.582 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 9.734 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.183 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 17.371 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.797 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.949 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 10.833 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.151 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 17.888 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.624 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.947 | 0.000 |

- Slack setup terburuk: **-1.388 ns** (Slow 1100mV -40C Model Setup 'clk_i')  **NEGATIVE: timing not met**
- Slack hold terburuk: **0.151 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`S7-20.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 47.99 MHz | 47.99 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 46.76 MHz | 46.76 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 3
- Peringatan: 19
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

