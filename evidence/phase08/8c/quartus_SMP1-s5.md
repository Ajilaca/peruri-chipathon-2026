# MEASURED - Quartus results for revision `SMP1-s5`

- Generated: 2026-10-03 13:26 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/par_b/output_files_SMP1-s5`
- Note: Phases 8c/8d: kpke_smp_top_s10 revision SMP1-s5, kernel-only virtual pins; compiled in quartus/par_b (a copy of quartus/phase08c_smp with identical .qsf, .sdc and sources, used to run compiles in parallel; not committed); working tree on top of commit d965b4d

## Fitter (`SMP1-s5.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 19:21:34 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | SMP1-s5 |
| Top-level Entity Name | kpke_smp_top_s10 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 11,032 / 41,910 ( 26 % ) |
| Total registers | 3391 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 81,694 / 5,662,720 ( 1 % ) |
| Total RAM Blocks | 44 / 553 ( 8 % ) |
| Total DSP Blocks | 26 / 112 ( 23 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`SMP1-s5.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 15.754 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.293 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 38.321 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.763 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.576 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 15.231 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.242 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 38.463 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.641 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.547 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.307 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.126 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 39.086 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.375 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.939 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.039 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.103 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 39.254 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.264 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.938 | 0.000 |

- Worst setup slack: **15.231 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.103 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`SMP1-s5.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 41.24 MHz | 41.24 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 40.37 MHz | 40.37 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 261
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

