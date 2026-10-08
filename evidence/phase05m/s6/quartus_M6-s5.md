# MEASURED - Hasil Quartus untuk revisi `M6-s5`

- Dibuat: 2026-10-02 12:42 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase05m_memsched/output_files_M6-s5`
- Catatan: Fase 5M langkah S6 kandidat: rtl/ntt/ntt_core_m6_p6.sv (Barrett, INTT tanpa lintasan skala, pembagian dua di tiap layer; ADR 0017, test plan evidence/phase05m/test_plan.md); potongan seperti C4b-B (A_4, A_11, M; X, S_1, S_2); batasan 40.000 ns (quartus/phase05m_memsched/M.sdc); bawaan Quartus; fitter seed 5 (dikonfirmasi di laporan fit: baris Fitter Initial Placement Seed); RTL = working tree branch phase5m-memory-schedule di atas git f47efcc; kompilasi penuh dari db bersih

## Fitter (`M6-s5.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Fri Oct  2 19:10:40 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | M6-s5 |
| Top-level Entity Name | ntt_core_m6_p6 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,441 / 41,910 ( 23 % ) |
| Total registers | 4049 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,314 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 29 / 553 ( 5 % ) |
| Total DSP Blocks | 16 / 112 ( 14 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`M6-s5.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 11.464 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.353 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.520 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.723 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.591 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 11.559 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.307 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.612 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.593 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.567 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 24.113 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.183 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.715 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.367 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.946 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 26.653 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.126 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.885 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.218 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.941 | 0.000 |

- Slack setup terburuk: **11.464 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.126 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`M6-s5.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 35.04 MHz | 35.04 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 35.16 MHz | 35.16 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 19
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

