# MEASURED - Quartus results for revision `MW`

- Generated: 2026-10-04 02:05 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09m1_core/output_files_MW`
- Note: Phase 9M-1: mlkem_core with CODEC_W2 = 1 (two-byte load / store tasks), revision MW, kernel-only virtual pins; branch phase9m-optimisation, rtl/mlkem at the 9M-1 files

## Fitter (`MW.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 08:02:01 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MW |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 17,672 / 41,910 ( 42 % ) |
| Total registers | 8233 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`MW.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 20.825 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.358 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 38.661 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.562 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.563 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 21.516 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.296 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 38.750 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.481 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.527 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 28.136 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 39.329 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.245 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.899 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 30.347 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.116 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 39.441 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.162 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.906 | 0.000 |

- Worst setup slack: **20.825 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.116 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MW.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 52.15 MHz | 52.15 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 54.1 MHz | 54.1 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 253
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

