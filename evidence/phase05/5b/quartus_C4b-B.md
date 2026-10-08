# MEASURED - Hasil Quartus untuk revisi `C4b-B`

- Dibuat: 2026-10-01 12:31 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase05_arith_c4/output_files_C4b-B`
- Catatan: Fase 5b kandidat: rtl/ntt/ntt_core_c4b_b.sv (Barrett RED_KIND=2; potongan jalur pengali X, S_1, S_2; potongan memori A_4, A_11, M seperti C3-P6; test_plan.md amandemen A3); batasan 40.000 ns (quartus/phase05_arith_c4/C4.sdc); bawaan Quartus; fitter seed 1 (dikonfirmasi di laporan fit: Fitter Initial Placement Seed = 1); RTL = working tree branch phase5-arith di atas git 5a1eec0

## Fitter (`C4b-B.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Thu Oct  1 18:37:03 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | C4b-B |
| Top-level Entity Name | ntt_core_c4b_b |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,208 / 41,910 ( 22 % ) |
| Total registers | 4115 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,314 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 29 / 553 ( 5 % ) |
| Total DSP Blocks | 18 / 112 ( 16 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`C4b-B.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 11.221 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.436 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 38.028 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.903 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.564 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 11.044 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.324 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 38.164 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.787 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.531 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 24.304 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.181 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.901 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.447 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.901 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 26.883 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.120 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 39.115 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.323 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.905 | 0.000 |

- Slack setup terburuk: **11.044 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.12 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`C4b-B.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 34.75 MHz | 34.75 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 34.54 MHz | 34.54 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 20
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

