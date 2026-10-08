# MEASURED - Hasil Quartus untuk revisi `K4-s6`

- Dibuat: 2026-10-04 19:15 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09i4_core/output_files_K4-s6`
- Catatan: Fase 9I butir 4: mlkem_core4 (parameter K3): revisi K4-s6, kernel-only dengan virtual pin, 40.000 ns; dikompilasi di quartus/phase09i4_core; working tree di atas commit cf81581 (perubahan S2 / S2b / butir 4 belum di-commit)

## Fitter (`K4-s6.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Mon Oct  5 02:08:52 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K4-s6 |
| Top-level Entity Name | mlkem_core4 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,189 / 41,910 ( 34 % ) |
| Total registers | 8494 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,603 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`K4-s6.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 20.220 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.237 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 36.595 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.251 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.570 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 21.060 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.075 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 36.814 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.065 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.518 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.214 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.137 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 37.951 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.761 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.900 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.745 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.037 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.325 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.561 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.902 | 0.000 |

- Slack setup terburuk: **20.22 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.037 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K4-s6.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 50.56 MHz | 50.56 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 52.8 MHz | 52.8 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 255
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

