# MEASURED - Hasil Quartus untuk revisi `S7-s3`

- Dibuat: 2026-10-02 15:18 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase05m_memsched/output_files_S7-s3`
- Catatan: Fase 5M langkah S7 kandidat: rtl/ntt/ntt_core_s7_p7.sv (M6 ditambah pembelahan jalur baca memori RD_SPLIT = 1, P = 7; ADR 0017/0019/0020, test plan evidence/phase05m/test_plan_s7.md); batasan 40.000 ns (quartus/phase05m_memsched/M.sdc); bawaan Quartus; git b53309d

## Fitter (`S7-s3.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Fri Oct  2 21:58:40 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | S7-s3 |
| Top-level Entity Name | ntt_core_s7_p7 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,361 / 41,910 ( 22 % ) |
| Total registers | 4302 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,423 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 31 / 553 ( 6 % ) |
| Total DSP Blocks | 16 / 112 ( 14 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`S7-s3.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 14.398 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.364 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.659 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.511 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.585 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 13.894 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.335 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.822 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.372 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.541 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 26.846 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.182 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.710 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.277 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.909 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 28.595 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.113 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.925 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.148 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.909 | 0.000 |

- Slack setup terburuk: **13.894 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.113 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`S7-s3.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 39.06 MHz | 39.06 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 38.31 MHz | 38.31 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 19
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

