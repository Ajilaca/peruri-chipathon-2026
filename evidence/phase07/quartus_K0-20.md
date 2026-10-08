# MEASURED - Hasil Quartus untuk revisi `K0-20`

- Dibuat: 2026-10-03 04:47 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase07_keccak/output_files_K0-20`
- Catatan: Fase 7 K0-20: RTL sama dengan K0, 20.000 ns (K-20.sdc, informasi, bukan gerbang), seed 1, kernel-only dengan virtual pin

## Fitter (`K0-20.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 11:46:32 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K0-20 |
| Top-level Entity Name | keccak_sponge |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 3,573 / 41,910 ( 9 % ) |
| Total registers | 1653 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 0 / 5,662,720 ( 0 % ) |
| Total RAM Blocks | 0 / 553 ( 0 % ) |
| Total DSP Blocks | 0 / 112 ( 0 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`K0-20.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 6.893 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.408 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 9.279 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 7.445 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.344 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 9.196 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 11.908 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.177 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 9.611 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 13.400 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.164 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 9.596 | 0.000 |

- Slack setup terburuk: **6.893 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.164 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K0-20.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 76.3 MHz | 76.3 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 79.65 MHz | 79.65 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 6
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

