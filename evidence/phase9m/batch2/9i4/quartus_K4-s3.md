# MEASURED - Quartus results for revision `K4-s3`

- Generated: 2026-10-04 19:15 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09i4_core/output_files_K4-s3`
- Note: Phase 9I item 4: mlkem_core4 (K3 parameters): revision K4-s3, kernel-only virtual pins, 40.000 ns; compiled in quartus/phase09i4_core; working tree on top of commit cf81581 (S2 / S2b / item 4 changes uncommitted)

## Fitter (`K4-s3.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Mon Oct  5 01:40:55 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K4-s3 |
| Top-level Entity Name | mlkem_core4 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,249 / 41,910 ( 34 % ) |
| Total registers | 8500 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,603 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`K4-s3.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 21.047 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.247 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 38.147 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.839 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.579 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 21.710 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.231 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 38.278 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.735 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.530 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.858 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.135 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.942 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.439 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.908 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 30.191 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.117 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 39.142 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.322 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.909 | 0.000 |

- Worst setup slack: **21.047 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.117 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K4-s3.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 52.76 MHz | 52.76 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 54.67 MHz | 54.67 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 255
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

