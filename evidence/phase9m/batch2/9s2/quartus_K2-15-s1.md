# MEASURED — Quartus results for revision `K2-15-s1`

- Generated: 2026-10-04 15:05 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09s2_core/output_files_K2-15-s1`
- Note: Phase 9F S2: mlkem_core3 revision K2-15-s1 (K1b + NTT_P6 = 1), kernel-only virtual pins, 15.000 ns; compiled in quartus/phase09s2_core; working tree on top of commit cf81581 (S2 changes uncommitted)

## Fitter (`K2-15-s1.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 21:26:58 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K2-15-s1 |
| Top-level Entity Name | mlkem_core3 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,308 / 41,910 ( 34 % ) |
| Total registers | 8383 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,507 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 53 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`K2-15-s1.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 1.959 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.361 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.087 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 1.624 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.267 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.069 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 7.538 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.177 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.445 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 8.879 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.117 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.442 | 0.000 |

- Worst setup slack: **1.624 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.117 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K2-15-s1.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 76.68 MHz | 76.68 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 74.76 MHz | 74.76 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 254
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

