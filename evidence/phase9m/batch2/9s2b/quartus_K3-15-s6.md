# MEASURED — Quartus results for revision `K3-15-s6`

- Generated: 2026-10-04 16:04 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09s2b_core/output_files_K3-15-s6`
- Note: Phase 9F S2b: mlkem_core3 revision K3-15-s6 (K2 + NTT_AR = 1), kernel-only virtual pins, 15.000 ns; compiled in quartus/phase09s2b_core; working tree on top of commit cf81581 (S2 / S2b changes uncommitted)

## Fitter (`K3-15-s6.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 23:03:14 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K3-15-s6 |
| Top-level Entity Name | mlkem_core3 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,329 / 41,910 ( 34 % ) |
| Total registers | 8448 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,507 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 53 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`K3-15-s6.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 2.777 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.353 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.085 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 2.400 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.140 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.042 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 7.674 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.411 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 8.964 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.086 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.412 | 0.000 |

- Worst setup slack: **2.4 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.086 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K3-15-s6.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 81.81 MHz | 81.81 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 79.37 MHz | 79.37 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 255
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

