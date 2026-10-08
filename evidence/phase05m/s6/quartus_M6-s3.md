# MEASURED - Hasil Quartus untuk revisi `M6-s3`

- Dibuat: 2026-10-02 12:42 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase05m_memsched/output_files_M6-s3`
- Catatan: Fase 5M langkah S6 kandidat: rtl/ntt/ntt_core_m6_p6.sv (Barrett, INTT tanpa lintasan skala, pembagian dua di tiap layer; ADR 0017, test plan evidence/phase05m/test_plan.md); potongan seperti C4b-B (A_4, A_11, M; X, S_1, S_2); batasan 40.000 ns (quartus/phase05m_memsched/M.sdc); bawaan Quartus; fitter seed 3 (dikonfirmasi di laporan fit: baris Fitter Initial Placement Seed); RTL = working tree branch phase5m-memory-schedule di atas git f47efcc; kompilasi penuh dari db bersih

## Fitter (`M6-s3.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Fri Oct  2 19:02:45 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | M6-s3 |
| Top-level Entity Name | ntt_core_m6_p6 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,417 / 41,910 ( 22 % ) |
| Total registers | 4063 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,314 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 29 / 553 ( 5 % ) |
| Total DSP Blocks | 16 / 112 ( 14 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`M6-s3.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 10.721 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.398 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 36.663 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.163 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.585 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 10.860 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.415 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 36.870 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.991 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.532 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 24.073 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.181 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.027 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.691 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.908 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 26.568 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.143 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.379 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.501 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.910 | 0.000 |

- Slack setup terburuk: **10.721 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.143 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`M6-s3.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 34.15 MHz | 34.15 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 34.32 MHz | 34.32 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 19
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

