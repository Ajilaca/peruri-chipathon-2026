# MEASURED - Quartus results for revision `SMP2-s5`

- Generated: 2026-10-03 13:26 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/par_c/output_files_SMP2-s5`
- Note: Phases 8c/8d: kpke_smp_top_s10 revision SMP2-s5, kernel-only virtual pins; compiled in quartus/par_c (a copy of quartus/phase08c_smp with identical .qsf, .sdc and sources, used to run compiles in parallel; not committed); working tree on top of commit d965b4d

## Fitter (`SMP2-s5.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 20:03:59 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | SMP2-s5 |
| Top-level Entity Name | kpke_smp_top_s10 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 10,998 / 41,910 ( 26 % ) |
| Total registers | 3399 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 81,694 / 5,662,720 ( 1 % ) |
| Total RAM Blocks | 44 / 553 ( 8 % ) |
| Total DSP Blocks | 26 / 112 ( 23 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`SMP2-s5.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 17.328 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.310 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 36.909 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.705 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.574 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 17.037 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.192 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.119 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.522 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.524 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.314 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.162 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.094 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.972 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.903 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.326 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.075 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.479 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.767 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.907 | 0.000 |

- Worst setup slack: **17.037 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.075 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`SMP2-s5.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 44.11 MHz | 44.11 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 43.55 MHz | 43.55 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 250
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

