# MEASURED - Quartus results for revision `MC-20-s2`

- Generated: 2026-10-04 04:55 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09m2_core/output_files_MC-20-s2`
- Note: Phase 9M-2: mlkem_core at 20.000 ns, revision MC-20-s2, kernel-only virtual pins; branch phase9m-optimisation

## Fitter (`MC-20-s2.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 10:24:54 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MC-20-s2 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 17,780 / 41,910 ( 42 % ) |
| Total registers | 8465 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`MC-20-s2.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 4.155 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.311 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 18.583 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.594 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.583 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 4.399 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.107 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 18.681 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.516 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.540 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 10.328 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.155 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 19.297 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.248 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.906 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 12.138 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.102 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 19.414 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.167 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.909 | 0.000 |

- Worst setup slack: **4.155 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.102 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MC-20-s2.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 63.11 MHz | 63.11 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 64.1 MHz | 64.1 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 253
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

