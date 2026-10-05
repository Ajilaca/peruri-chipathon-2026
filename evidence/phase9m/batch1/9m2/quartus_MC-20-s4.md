# MEASURED - Quartus results for revision `MC-20-s4`

- Generated: 2026-10-04 04:55 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09m2_core/output_files_MC-20-s4`
- Note: Phase 9M-2: mlkem_core at 20.000 ns, revision MC-20-s4, kernel-only virtual pins; branch phase9m-optimisation

## Fitter (`MC-20-s4.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 10:43:45 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MC-20-s4 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 17,729 / 41,910 ( 42 % ) |
| Total registers | 8369 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`MC-20-s4.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 3.730 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.347 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 17.367 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.861 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.567 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 4.452 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.269 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 17.508 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.702 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.521 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 9.691 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.177 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 18.570 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.456 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.898 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 11.638 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.121 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 18.787 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.298 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.903 | 0.000 |

- Worst setup slack: **3.73 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.121 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MC-20-s4.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 61.46 MHz | 61.46 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 64.32 MHz | 64.32 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 253
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

