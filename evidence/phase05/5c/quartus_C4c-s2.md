# MEASURED - Hasil Quartus untuk revisi `C4c-s2`

- Dibuat: 2026-10-01 14:36 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase05_arith_c4/output_files_C4c-s2`
- Catatan: Fase 5c kandidat: rtl/ntt/ntt_core_c4c.sv (Barrett RED_KIND=2, LAZY=1, masukan INTT malas, ADR 0014; potongan X, S_1, S_2 seperti C4b-B; potongan memori A_4, A_11, M); batasan 40.000 ns (C4.sdc); bawaan Quartus; fitter seed 2 (dikonfirmasi di laporan fit: baris Fitter Initial Placement Seed); RTL = working tree branch phase5-arith di atas git 97f41a1

## Fitter (`C4c-s2.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Thu Oct  1 21:07:50 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | C4c-s2 |
| Top-level Entity Name | ntt_core_c4c |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,032 / 41,910 ( 22 % ) |
| Total registers | 4078 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,338 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 29 / 553 ( 5 % ) |
| Total DSP Blocks | 18 / 112 ( 16 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`C4c-s2.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 11.806 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.416 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.645 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.570 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.611 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 11.636 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.332 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.777 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.433 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.600 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 25.025 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.184 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.729 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.296 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.952 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 27.373 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.129 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.922 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.171 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.947 | 0.000 |

- Slack setup terburuk: **11.636 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Slack hold terburuk: **0.129 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`C4c-s2.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 35.47 MHz | 35.47 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 35.26 MHz | 35.26 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 23
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

