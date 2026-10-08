# MEASURED - Hasil Quartus untuk revisi `MC`

- Dibuat: 2026-10-03 18:15 UTC oleh `extract_quartus_report.py` (nilai disalin dari laporan, tidak dihitung)
- Direktori sumber: `quartus/phase09c_core/output_files_MC`
- Catatan: Fase 9c: mlkem_core (KeyGen, Encaps, Decaps; mesin 8d, codec, hash dengan sponge C5, pembanding), revisi MC, kernel-only dengan virtual pin; working tree sebelum commit Fase 9

## Fitter (`MC.fit.summary`)

| Item | Nilai (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 00:11:03 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MC |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 17,613 / 41,910 ( 42 % ) |
| Total registers | 8210 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Penyebut di atas adalah penyebut fitter sendiri; kutip persis seperti tercetak.

## Timing (`MC.sta.summary`)

| Tipe | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 20.272 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.298 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.765 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.116 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.587 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 20.896 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.206 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.945 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.972 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.542 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.871 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.684 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.611 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.909 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 30.243 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.096 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.941 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.465 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.911 | 0.000 |

- Slack setup terburuk: **20.272 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Slack hold terburuk: **0.096 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MC.sta.rpt`, panel Fmax Summary)

| Model | Fmax | Fmax terbatas | Nama clock | Catatan |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 50.69 MHz | 50.69 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 52.35 MHz | 52.35 MHz | clk_i |  |

## Jumlah pesan log kompilasi

- Peringatan kritis: 1
- Peringatan: 253
- Kesalahan: 0

Peringatan kritis harus dibahas secara tertulis.

