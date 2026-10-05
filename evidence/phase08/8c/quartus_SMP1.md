# MEASURED - Quartus results for revision `SMP1`

- Generated: 2026-10-03 13:26 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase08c_smp/output_files_SMP1`
- Note: Phases 8c/8d: kpke_smp_top_s10 revision SMP1, kernel-only virtual pins; compiled in quartus/phase08c_smp; working tree on top of commit d965b4d

## Fitter (`SMP1.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 18:01:24 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | SMP1 |
| Top-level Entity Name | kpke_smp_top_s10 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 10,975 / 41,910 ( 26 % ) |
| Total registers | 3385 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 81,694 / 5,662,720 ( 1 % ) |
| Total RAM Blocks | 44 / 553 ( 8 % ) |
| Total DSP Blocks | 26 / 112 ( 23 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`SMP1.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 18.139 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.348 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.602 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.576 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.590 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 17.441 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.146 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.765 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.438 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.546 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.123 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.669 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.319 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.911 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.630 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.091 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.888 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.181 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.913 | 0.000 |

- Worst setup slack: **17.441 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.091 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`SMP1.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 45.74 MHz | 45.74 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 44.33 MHz | 44.33 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 261
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

