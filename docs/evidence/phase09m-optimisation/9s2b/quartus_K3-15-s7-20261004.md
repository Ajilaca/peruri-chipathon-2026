# MEASURED — Quartus results for revision `K3-15-s7`

- Generated: 2026-10-04 19:15 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09s2b_core/output_files_K3-15-s7`
- Note: Phase 9F S2b: mlkem_core3 (K2 + NTT_AR = 1): revision K3-15-s7, kernel-only virtual pins, 15.000 ns; compiled in quartus/phase09s2b_core; working tree on top of commit cf81581 (S2 / S2b / item 4 changes uncommitted)

## Fitter (`K3-15-s7.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 23:59:37 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K3-15-s7 |
| Top-level Entity Name | mlkem_core3 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,216 / 41,910 ( 34 % ) |
| Total registers | 8481 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,507 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 53 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`K3-15-s7.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 2.150 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.371 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.080 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 2.018 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.289 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.033 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 8.221 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.404 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 9.354 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.137 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.408 | 0.000 |

- Worst setup slack: **2.018 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.137 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K3-15-s7.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 77.82 MHz | 77.82 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 77.03 MHz | 77.03 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 255
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

