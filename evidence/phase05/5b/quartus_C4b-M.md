# MEASURED - Hasil Quartus untuk revisi `C4b-M`

- Dibuat: 2026-10-01 12:31 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase05_arith_c4/output_files_C4b-M`
- Catatan: Fase 5b kandidat: rtl/ntt/ntt_core_c4b_m.sv (Montgomery RED_KIND=3, ROM bentuk Montgomery dan konstanta skala; potongan jalur pengali X, S_1, S_2; potongan memori A_4, A_11, M seperti C3-P6; test_plan.md amandemen A3); batasan 40.000 ns (quartus/phase05_arith_c4/C4.sdc); bawaan Quartus; fitter seed 1 (dikonfirmasi di laporan fit: Fitter Initial Placement Seed = 1); RTL = working tree branch phase5-arith di atas git 5a1eec0

## Fitter (`C4b-M.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Thu Oct  1 18:41:36 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | C4b-M |
| Top-level Entity Name | ntt_core_c4b_m |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,249 / 41,910 ( 22 % ) |
| Total registers | 4297 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,314 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 29 / 553 ( 5 % ) |
| Total DSP Blocks | 9 / 112 ( 8 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`C4b-M.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 9.526 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.432 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.052 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.930 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.564 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 9.855 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.311 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.232 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.766 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.527 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 23.217 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.184 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.291 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.552 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.901 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 26.021 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.107 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.596 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.376 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.905 | 0.000 |

- Slack setup terburuk: **9.526 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.107 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`C4b-M.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 32.81 MHz | 32.81 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 33.17 MHz | 33.17 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 20
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

