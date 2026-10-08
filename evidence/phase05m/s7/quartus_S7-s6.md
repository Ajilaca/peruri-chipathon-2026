# MEASURED - Hasil Quartus untuk revisi `S7-s6`

- Dibuat: 2026-10-02 15:18 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase05m_memsched/output_files_S7-s6`
- Catatan: Fase 5M langkah S7 kandidat: rtl/ntt/ntt_core_s7_p7.sv (M6 ditambah pembelahan jalur baca memori RD_SPLIT = 1, P = 7; ADR 0017/0019/0020, test plan evidence/phase05m/test_plan_s7.md); batasan 40.000 ns (quartus/phase05m_memsched/M.sdc); bawaan Quartus; git b53309d

## Fitter (`S7-s6.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Fri Oct  2 22:16:34 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | S7-s6 |
| Top-level Entity Name | ntt_core_s7_p7 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,396 / 41,910 ( 22 % ) |
| Total registers | 4324 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,423 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 31 / 553 ( 6 % ) |
| Total DSP Blocks | 16 / 112 ( 14 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`S7-s6.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 16.082 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.440 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 36.597 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.100 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.564 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 15.178 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.302 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 36.835 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.928 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.523 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.240 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.181 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 37.937 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.583 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.900 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.346 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.088 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.324 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.431 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.905 | 0.000 |

- Slack setup terburuk: **15.178 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.088 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`S7-s6.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 41.81 MHz | 41.81 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 40.29 MHz | 40.29 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 19
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

