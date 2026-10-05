# MEASURED - Quartus results for revision `MW-s4`

- Generated: 2026-10-04 02:05 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09m1_core/output_files_MW-s4`
- Note: Phase 9M-1: mlkem_core with CODEC_W2 = 1 (two-byte load / store tasks), revision MW-s4, kernel-only virtual pins; branch phase9m-optimisation, rtl/mlkem at the 9M-1 files

## Fitter (`MW-s4.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 08:33:59 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MW-s4 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 17,655 / 41,910 ( 42 % ) |
| Total registers | 8189 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`MW-s4.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 18.957 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.353 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 38.216 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.854 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.574 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 19.694 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.278 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 38.358 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.723 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.525 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 26.779 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.160 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 39.006 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.437 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.903 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.295 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.083 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 39.191 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.319 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.907 | 0.000 |

- Worst setup slack: **18.957 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.083 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MW-s4.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 47.52 MHz | 47.52 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 49.25 MHz | 49.25 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 253
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

