# MEASURED — Quartus results for revision `K3-s2`

- Generated: 2026-10-04 19:15 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09s2b_core/output_files_K3-s2`
- Note: Phase 9F S2b: mlkem_core3 (K2 + NTT_AR = 1): revision K3-s2, kernel-only virtual pins, 40.000 ns; compiled in quartus/phase09s2b_core; working tree on top of commit cf81581 (S2 / S2b / item 4 changes uncommitted)

## Fitter (`K3-s2.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 23:17:39 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K3-s2 |
| Top-level Entity Name | mlkem_core3 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,106 / 41,910 ( 34 % ) |
| Total registers | 8462 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,603 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`K3-s2.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 20.302 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.295 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 38.633 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.547 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.589 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 21.053 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.136 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 38.725 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.479 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.561 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 26.918 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.149 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 39.347 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.258 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.945 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.607 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.091 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 39.453 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.175 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.945 | 0.000 |

- Worst setup slack: **20.302 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.091 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K3-s2.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 50.77 MHz | 50.77 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 52.78 MHz | 52.78 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 255
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

