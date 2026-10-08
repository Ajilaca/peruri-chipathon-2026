# MEASURED - Hasil Quartus untuk revisi `S8-s5`

- Dibuat: 2026-10-02 17:38 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase05m_memsched/output_files_S8-s5`
- Catatan: Fase 5M langkah S8 kandidat: rtl/ntt/ntt_core_s8_p8.sv (S7 ditambah register jalur tulis WR_REG = 1, P = 8, satu bubble per arah; ADR 0017/0019/0020/0021, test plan evidence/phase05m/test_plan_s8.md); batasan 40.000 ns (quartus/phase05m_memsched/M.sdc); bawaan Quartus; git 300aaf3

## Fitter (`S8-s5.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Fri Oct  2 22:45:38 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | S8-s5 |
| Top-level Entity Name | ntt_core_s8_p8 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,469 / 41,910 ( 23 % ) |
| Total registers | 4138 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,942 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 33 / 553 ( 6 % ) |
| Total DSP Blocks | 16 / 112 ( 14 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`S8-s5.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 14.522 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.349 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.016 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.682 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.597 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 13.772 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.321 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.155 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.533 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.574 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.475 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.183 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.363 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.344 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.945 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 28.824 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.140 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.618 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.210 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.943 | 0.000 |

- Slack setup terburuk: **13.772 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.14 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`S8-s5.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 39.25 MHz | 39.25 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 38.13 MHz | 38.13 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 20
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

