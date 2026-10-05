# MEASURED - Quartus results for revision `SMP1-s2`

- Generated: 2026-10-03 13:26 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase08c_smp/output_files_SMP1-s2`
- Note: Phases 8c/8d: kpke_smp_top_s10 revision SMP1-s2, kernel-only virtual pins; compiled in quartus/phase08c_smp; working tree on top of commit d965b4d

## Fitter (`SMP1-s2.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 18:38:08 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | SMP1-s2 |
| Top-level Entity Name | kpke_smp_top_s10 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 10,989 / 41,910 ( 26 % ) |
| Total registers | 3389 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 81,694 / 5,662,720 ( 1 % ) |
| Total RAM Blocks | 44 / 553 ( 8 % ) |
| Total DSP Blocks | 26 / 112 ( 23 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`SMP1-s2.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 18.598 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.308 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 38.495 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.676 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.586 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 18.100 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.129 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 38.593 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.576 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.541 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.514 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.167 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 39.234 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.304 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.907 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.937 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.096 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 39.359 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.208 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.911 | 0.000 |

- Worst setup slack: **18.1 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.096 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`SMP1-s2.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 46.72 MHz | 46.72 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 45.66 MHz | 45.66 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 261
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

