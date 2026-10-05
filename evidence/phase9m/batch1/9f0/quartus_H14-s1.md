# MEASURED — Quartus results for revision `H14-s1`

- Generated: 2026-10-04 08:39 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09f0_core/output_files_H14-s1`
- Note: Phase 9F step S0: the 9M-1 core (CODEC_W2 = 1, C5 hash) at a tighter constraint, revision H14-s1, kernel-only virtual pins; branch phase9m-optimisation

## Fitter (`H14-s1.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 15:06:12 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | H14-s1 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 18,876 / 41,910 ( 45 % ) |
| Total registers | 10966 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 119,608 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 49 / 553 ( 9 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`H14-s1.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 0.826 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.325 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 5.575 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 1.273 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.243 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 5.550 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 5.913 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 5.906 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 7.474 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.090 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 5.909 | 0.000 |

- Worst setup slack: **0.826 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.09 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`H14-s1.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 75.91 MHz | 75.91 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 78.57 MHz | 78.57 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 254
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

