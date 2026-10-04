# MEASURED — Quartus results for revision `K1b-s6`

- Generated: 2026-10-04 12:08 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09f1b_core/output_files_K1b-s6`
- Note: Phase 9F step S1b: mlkem_core3 (background hash sidecar) with SMP_C5 = 0, HASH_C5 = 0, CODEC_W2 = 1, revision K1b-s6, kernel-only virtual pins; branch phase9m-optimisation

## Fitter (`K1b-s6.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 17:55:46 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K1b-s6 |
| Top-level Entity Name | mlkem_core3 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,376 / 41,910 ( 34 % ) |
| Total registers | 8258 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`K1b-s6.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 19.219 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.301 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 38.075 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.894 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.571 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 19.896 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.268 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 38.208 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.788 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.526 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.326 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.156 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.909 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.467 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.902 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.663 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.132 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 39.113 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.350 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.906 | 0.000 |

- Worst setup slack: **19.219 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.132 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K1b-s6.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 48.12 MHz | 48.12 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 49.74 MHz | 49.74 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 253
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

