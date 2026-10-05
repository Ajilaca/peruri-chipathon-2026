# MEASURED - Quartus results for revision `F16-s2`

- Generated: 2026-10-04 08:39 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09f0_core/output_files_F16-s2`
- Note: Phase 9F step S0: the 9M-1 core (CODEC_W2 = 1, C5 hash) at a tighter constraint, revision F16-s2, kernel-only virtual pins; branch phase9m-optimisation

## Fitter (`F16-s2.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 13:22:46 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | F16-s2 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 17,888 / 41,910 ( 43 % ) |
| Total registers | 8575 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,270 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 53 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`F16-s2.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 2.092 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.345 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.571 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 2.075 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.212 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.528 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 7.412 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.902 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 9.067 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.108 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.906 | 0.000 |

- Worst setup slack: **2.075 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.108 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`F16-s2.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 71.9 MHz | 71.9 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 71.81 MHz | 71.81 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 253
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

