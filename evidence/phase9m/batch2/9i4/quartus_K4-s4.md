# MEASURED - Hasil Quartus untuk revisi `K4-s4`

- Dibuat: 2026-10-04 19:15 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09i4_core/output_files_K4-s4`
- Catatan: Fase 9I butir 4: mlkem_core4 (parameter K3): revisi K4-s4, kernel-only dengan virtual pin, 40.000 ns; dikompilasi di quartus/phase09i4_core; working tree di atas commit cf81581 (perubahan S2 / S2b / butir 4 belum di-commit)

## Fitter (`K4-s4.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Mon Oct  5 01:49:59 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K4-s4 |
| Top-level Entity Name | mlkem_core4 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,229 / 41,910 ( 34 % ) |
| Total registers | 8510 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,603 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`K4-s4.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 20.622 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.267 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.820 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.071 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.574 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 21.284 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.127 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.985 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.930 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.533 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 28.195 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.145 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.738 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.575 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.902 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 30.352 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.110 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.978 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.433 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.906 | 0.000 |

- Slack setup terburuk: **20.622 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.11 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K4-s4.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 51.6 MHz | 51.6 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 53.43 MHz | 53.43 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 255
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

