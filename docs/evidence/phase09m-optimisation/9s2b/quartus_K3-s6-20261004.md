# MEASURED — Quartus results for revision `K3-s6`

- Generated: 2026-10-04 19:15 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09s2b_core/output_files_K3-s6`
- Note: Phase 9F S2b: mlkem_core3 (K2 + NTT_AR = 1): revision K3-s6, kernel-only virtual pins, 40.000 ns; compiled in quartus/phase09s2b_core; working tree on top of commit cf81581 (S2 / S2b / item 4 changes uncommitted)

## Fitter (`K3-s6.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 23:51:05 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K3-s6 |
| Top-level Entity Name | mlkem_core3 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,133 / 41,910 ( 34 % ) |
| Total registers | 8462 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,603 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`K3-s6.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 20.354 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.319 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 38.155 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.871 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.570 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 20.884 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.201 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 38.314 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.725 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.511 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.406 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.151 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.974 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.435 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.902 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.871 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.122 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 39.166 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.312 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.906 | 0.000 |

- Worst setup slack: **20.354 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.122 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K3-s6.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 50.9 MHz | 50.9 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 52.31 MHz | 52.31 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 255
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

