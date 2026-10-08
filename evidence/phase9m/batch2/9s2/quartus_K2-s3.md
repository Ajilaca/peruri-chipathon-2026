# MEASURED - Hasil Quartus untuk revisi `K2-s3`

- Dibuat: 2026-10-04 13:51 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09s2_core/output_files_K2-s3`
- Catatan: Fase 9F S2: mlkem_core3 revisi K2-s3 (K1b + NTT_P6 = 1), kernel-only dengan virtual pin, 40.000 ns; dikompilasi di quartus/phase09s2_core; working tree di atas commit cf81581 (perubahan S2 belum di-commit)

## Fitter (`K2-s3.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 20:08:10 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K2-s3 |
| Top-level Entity Name | mlkem_core3 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,216 / 41,910 ( 34 % ) |
| Total registers | 8337 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,603 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`K2-s3.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 21.187 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.303 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.228 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.416 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.554 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 21.290 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.276 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.433 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.249 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.524 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 29.168 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.172 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.287 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.820 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.898 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 31.161 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.118 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.641 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.632 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.904 | 0.000 |

- Slack setup terburuk: **21.187 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.118 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K2-s3.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 53.15 MHz | 53.15 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 53.45 MHz | 53.45 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 254
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

