# MEASURED - Hasil Quartus untuk revisi `S8-s6`

- Dibuat: 2026-10-02 17:38 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase05m_memsched/output_files_S8-s6`
- Catatan: Fase 5M langkah S8 kandidat: rtl/ntt/ntt_core_s8_p8.sv (S7 ditambah register jalur tulis WR_REG = 1, P = 8, satu bubble per arah; ADR 0017/0019/0020/0021, test plan evidence/phase05m/test_plan_s8.md); batasan 40.000 ns (quartus/phase05m_memsched/M.sdc); bawaan Quartus; git 300aaf3

## Fitter (`S8-s6.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Fri Oct  2 22:50:51 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | S8-s6 |
| Top-level Entity Name | ntt_core_s8_p8 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,419 / 41,910 ( 22 % ) |
| Total registers | 4130 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,942 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 33 / 553 ( 6 % ) |
| Total DSP Blocks | 16 / 112 ( 14 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`S8-s6.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 14.137 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.453 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 36.034 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.058 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.585 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 13.593 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.376 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 36.281 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.884 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.541 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 26.837 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.185 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 37.590 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.624 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.908 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 28.413 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.152 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.044 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.440 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.909 | 0.000 |

- Slack setup terburuk: **13.593 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.152 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`S8-s6.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 38.67 MHz | 38.67 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 37.87 MHz | 37.87 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 20
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

