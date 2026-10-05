# MEASURED - Quartus results for revision `K3-15-s9`

- Generated: 2026-10-04 19:15 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09s2b_core/output_files_K3-15-s9`
- Note: Phase 9F S2b: mlkem_core3 (K2 + NTT_AR = 1): revision K3-15-s9, kernel-only virtual pins, 15.000 ns; compiled in quartus/phase09s2b_core; working tree on top of commit cf81581 (S2 / S2b / item 4 changes uncommitted)

## Fitter (`K3-15-s9.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Mon Oct  5 00:17:39 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K3-15-s9 |
| Top-level Entity Name | mlkem_core3 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,258 / 41,910 ( 34 % ) |
| Total registers | 8502 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,507 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 53 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`K3-15-s9.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 1.422 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.352 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.088 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 1.263 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.186 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.074 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 7.979 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.443 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 9.195 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.070 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.441 | 0.000 |

- Worst setup slack: **1.263 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.07 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K3-15-s9.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 73.65 MHz | 73.65 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 72.8 MHz | 72.8 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 255
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

