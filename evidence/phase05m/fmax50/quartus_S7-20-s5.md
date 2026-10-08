# MEASURED - Hasil Quartus untuk revisi `S7-20-s5`

- Dibuat: 2026-10-02 20:02 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase05m_memsched/output_files_S7-20-s5`
- Catatan: Pertanyaan 50 MHz opsi 2: RTL S7 (rtl/ntt/ntt_core_s7_p7.sv) pada 20.000 ns (quartus/phase05m_memsched/M-20.sdc), hanya informasi; bawaan Quartus; git 8133e08

## Fitter (`S7-20-s5.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 02:50:40 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | S7-20-s5 |
| Top-level Entity Name | ntt_core_s7_p7 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,369 / 41,910 ( 22 % ) |
| Total registers | 4354 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,423 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 31 / 553 ( 6 % ) |
| Total DSP Blocks | 16 / 112 ( 14 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`S7-20-s5.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | -1.412 | -17.961 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.388 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 15.823 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.913 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.602 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | -1.933 | -28.792 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.370 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 16.101 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.768 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.580 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 9.453 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.183 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 17.402 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.463 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.950 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 10.680 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.124 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 17.903 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.339 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.947 | 0.000 |

- Slack setup terburuk: **-1.933 ns** (Slow 1100mV -40C Model Setup 'clk_i')  **NEGATIVE: timing not met**
- Slack hold terburuk: **0.124 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`S7-20-s5.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 46.7 MHz | 46.7 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 45.59 MHz | 45.59 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 3
- Peringatan: 19
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

