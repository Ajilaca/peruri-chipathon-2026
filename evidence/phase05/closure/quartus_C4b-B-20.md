# MEASURED - Hasil Quartus untuk revisi `C4b-B-20`

- Dibuat: 2026-10-01 17:04 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase05_arith_c4/output_files_C4b-B-20`
- Catatan: Penutup Fase 5, kompilasi INFORMASI (ADR 0011 D1): konfigurasi C4 akhir C4b-B (Barrett, ntt_core_c4b_b) pada 20.000 ns (quartus/phase05_arith_c4/C4-20.sdc); bawaan Quartus; seed bawaan 1; RTL = git b418d1e ditambah dokumen; bukan gerbang Fase 5 (ADR 0010)

## Fitter (`C4b-B-20.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Fri Oct  2 00:00:10 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | C4b-B-20 |
| Top-level Entity Name | ntt_core_c4b_b |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,305 / 41,910 ( 22 % ) |
| Total registers | 4272 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,314 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 29 / 553 ( 5 % ) |
| Total DSP Blocks | 18 / 112 ( 16 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`C4b-B-20.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | -2.557 | -461.653 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.424 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 17.094 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.867 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.606 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | -2.438 | -442.383 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.336 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 17.282 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.709 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.599 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 8.087 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.180 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 18.307 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.514 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.950 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 9.877 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.151 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 18.607 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.344 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.946 | 0.000 |

- Slack setup terburuk: **-2.557 ns** (Slow 1100mV 100C Model Setup 'clk_i')  **NEGATIVE: timing not met**
- Slack hold terburuk: **0.151 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`C4b-B-20.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 44.33 MHz | 44.33 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 44.57 MHz | 44.57 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 3
- Peringatan: 20
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

