# MEASURED - Hasil Quartus untuk revisi `C4c-s6`

- Dibuat: 2026-10-01 14:36 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase05_arith_c4/output_files_C4c-s6`
- Catatan: Fase 5c kandidat: rtl/ntt/ntt_core_c4c.sv (Barrett RED_KIND=2, LAZY=1, masukan INTT malas, ADR 0014; potongan X, S_1, S_2 seperti C4b-B; potongan memori A_4, A_11, M); batasan 40.000 ns (C4.sdc); bawaan Quartus; fitter seed 6 (dikonfirmasi di laporan fit: baris Fitter Initial Placement Seed); RTL = working tree branch phase5-arith di atas git 97f41a1

## Fitter (`C4c-s6.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Thu Oct  1 21:24:15 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | C4c-s6 |
| Top-level Entity Name | ntt_core_c4c |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,084 / 41,910 ( 22 % ) |
| Total registers | 4091 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,338 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 29 / 553 ( 5 % ) |
| Total DSP Blocks | 18 / 112 ( 16 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`C4c-s6.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 9.895 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.381 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.533 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.328 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.584 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 10.294 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.347 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.667 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.202 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.556 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 23.394 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.175 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.620 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.690 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.905 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 26.121 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.095 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.862 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.524 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.911 | 0.000 |

- Slack setup terburuk: **9.895 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.095 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`C4c-s6.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 33.22 MHz | 33.22 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 33.66 MHz | 33.66 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 23
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

