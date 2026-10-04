# MEASURED — Quartus results for revision `K1-s5`

- Generated: 2026-10-04 09:34 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09f1_core/output_files_K1-s5`
- Note: Phase 9F step S1: mlkem_core2 with SMP_C5 = 0, HASH_C5 = 0, CODEC_W2 = 1, revision K1-s5, kernel-only virtual pins; branch phase9m-optimisation

## Fitter (`K1-s5.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 14:57:56 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K1-s5 |
| Top-level Entity Name | mlkem_core2 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,056 / 41,910 ( 34 % ) |
| Total registers | 8355 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`K1-s5.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 20.494 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.298 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.767 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.096 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.560 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 20.496 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.215 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.960 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.929 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.516 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.996 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.152 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.700 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.581 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.898 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 30.360 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.109 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.957 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.432 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.902 | 0.000 |

- Worst setup slack: **20.494 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.109 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K1-s5.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 51.27 MHz | 51.27 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 51.27 MHz | 51.27 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 253
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

