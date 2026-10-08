# MEASURED - Hasil Quartus untuk revisi `S8-s4`

- Dibuat: 2026-10-02 17:38 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase05m_memsched/output_files_S8-s4`
- Catatan: Fase 5M langkah S8 kandidat: rtl/ntt/ntt_core_s8_p8.sv (S7 ditambah register jalur tulis WR_REG = 1, P = 8, satu bubble per arah; ADR 0017/0019/0020/0021, test plan evidence/phase05m/test_plan_s8.md); batasan 40.000 ns (quartus/phase05m_memsched/M.sdc); bawaan Quartus; git 300aaf3

## Fitter (`S8-s4.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Fri Oct  2 22:39:47 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | S8-s4 |
| Top-level Entity Name | ntt_core_s8_p8 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,402 / 41,910 ( 22 % ) |
| Total registers | 4137 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,942 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 33 / 553 ( 6 % ) |
| Total DSP Blocks | 16 / 112 ( 14 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`S8-s4.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 13.450 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.442 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 36.886 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.033 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.603 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 12.794 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.352 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.048 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.873 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.574 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 26.829 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.184 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.222 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.513 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.951 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 28.351 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.131 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.521 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.341 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.947 | 0.000 |

- Slack setup terburuk: **12.794 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.131 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`S8-s4.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 37.66 MHz | 37.66 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 36.76 MHz | 36.76 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 20
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

