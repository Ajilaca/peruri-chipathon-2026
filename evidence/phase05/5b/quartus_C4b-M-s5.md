# MEASURED - Hasil Quartus untuk revisi `C4b-M-s5`

- Dibuat: 2026-10-01 12:31 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase05_arith_c4/output_files_C4b-M-s5`
- Catatan: Fase 5b kandidat: rtl/ntt/ntt_core_c4b_m.sv (Montgomery RED_KIND=3, ROM bentuk Montgomery dan konstanta skala; potongan jalur pengali X, S_1, S_2; potongan memori A_4, A_11, M seperti C3-P6; test_plan.md amandemen A3); batasan 40.000 ns (quartus/phase05_arith_c4/C4.sdc); bawaan Quartus; fitter seed 5 (dikonfirmasi di laporan fit: Fitter Initial Placement Seed = 5); RTL = working tree branch phase5-arith di atas git 5a1eec0

## Fitter (`C4b-M-s5.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Thu Oct  1 19:19:14 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | C4b-M-s5 |
| Top-level Entity Name | ntt_core_c4b_m |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,297 / 41,910 ( 22 % ) |
| Total registers | 4299 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,314 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 29 / 553 ( 5 % ) |
| Total DSP Blocks | 9 / 112 ( 8 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`C4b-M-s5.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 10.645 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.258 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.518 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.221 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.576 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 10.387 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.243 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.739 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.061 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.528 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 24.036 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.152 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.472 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.718 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.903 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 26.649 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.102 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.791 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.548 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.908 | 0.000 |

- Slack setup terburuk: **10.387 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.102 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`C4b-M-s5.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 34.07 MHz | 34.07 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 33.77 MHz | 33.77 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 20
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

