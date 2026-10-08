# MEASURED - Hasil Quartus untuk revisi `S7-20-s4`

- Dibuat: 2026-10-02 20:02 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase05m_memsched/output_files_S7-20-s4`
- Catatan: Pertanyaan 50 MHz opsi 2: RTL S7 (rtl/ntt/ntt_core_s7_p7.sv) pada 20.000 ns (quartus/phase05m_memsched/M-20.sdc), hanya informasi; bawaan Quartus; git 8133e08

## Fitter (`S7-20-s4.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 02:40:47 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | S7-20-s4 |
| Top-level Entity Name | ntt_core_s7_p7 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,383 / 41,910 ( 22 % ) |
| Total registers | 4321 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,423 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 31 / 553 ( 6 % ) |
| Total DSP Blocks | 16 / 112 ( 14 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`S7-20-s4.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | -1.903 | -23.687 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.443 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 16.279 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.880 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.587 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | -2.431 | -32.632 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.361 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 16.517 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.766 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.551 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 9.006 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.182 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 17.721 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.460 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.906 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 10.295 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.125 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 18.145 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.345 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.912 | 0.000 |

- Slack setup terburuk: **-2.431 ns** (Slow 1100mV -40C Model Setup 'clk_i')  **NEGATIVE: timing not met**
- Slack hold terburuk: **0.125 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`S7-20-s4.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 45.66 MHz | 45.66 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 44.58 MHz | 44.58 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 3
- Peringatan: 19
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

