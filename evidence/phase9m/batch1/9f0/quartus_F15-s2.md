# MEASURED - Quartus results for revision `F15-s2`

- Generated: 2026-10-04 08:39 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09f0_core/output_files_F15-s2`
- Note: Phase 9F step S0: the 9M-1 core (CODEC_W2 = 1, C5 hash) at a tighter constraint, revision F15-s2, kernel-only virtual pins; branch phase9m-optimisation

## Fitter (`F15-s2.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 13:53:31 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | F15-s2 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 17,926 / 41,910 ( 43 % ) |
| Total registers | 8700 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,270 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 53 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`F15-s2.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 1.363 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.342 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.090 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 1.570 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.165 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.057 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 6.815 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.446 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 8.299 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.071 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.442 | 0.000 |

- Worst setup slack: **1.363 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.071 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`F15-s2.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 73.33 MHz | 73.33 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 74.46 MHz | 74.46 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 253
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

