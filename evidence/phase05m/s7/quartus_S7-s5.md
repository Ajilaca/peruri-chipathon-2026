# MEASURED - Hasil Quartus untuk revisi `S7-s5`

- Dibuat: 2026-10-02 15:18 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase05m_memsched/output_files_S7-s5`
- Catatan: Fase 5M langkah S7 kandidat: rtl/ntt/ntt_core_s7_p7.sv (M6 ditambah pembelahan jalur baca memori RD_SPLIT = 1, P = 7; ADR 0017/0019/0020, test plan evidence/phase05m/test_plan_s7.md); batasan 40.000 ns (quartus/phase05m_memsched/M.sdc); bawaan Quartus; git b53309d

## Fitter (`S7-s5.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Fri Oct  2 22:10:55 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | S7-s5 |
| Top-level Entity Name | ntt_core_s7_p7 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,362 / 41,910 ( 22 % ) |
| Total registers | 4298 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,423 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 31 / 553 ( 6 % ) |
| Total DSP Blocks | 16 / 112 ( 14 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`S7-s5.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 15.205 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.288 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 36.819 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.041 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.583 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 14.545 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.295 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.032 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.899 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.539 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.167 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.182 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.106 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.544 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.907 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 28.826 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.130 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.444 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.418 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.909 | 0.000 |

- Slack setup terburuk: **14.545 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.13 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`S7-s5.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 40.33 MHz | 40.33 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 39.29 MHz | 39.29 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 19
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

