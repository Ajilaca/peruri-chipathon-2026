# MEASURED — Quartus results for revision `SMP1-s6`

- Generated: 2026-10-03 13:26 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/par_d/output_files_SMP1-s6`
- Note: Phases 8c/8d: kpke_smp_top_s10 revision SMP1-s6, kernel-only virtual pins; compiled in quartus/par_d (a copy of quartus/phase08c_smp with identical .qsf, .sdc and sources, used to run compiles in parallel; not committed); working tree on top of commit d965b4d

## Fitter (`SMP1-s6.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 20:23:03 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | SMP1-s6 |
| Top-level Entity Name | kpke_smp_top_s10 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 11,018 / 41,910 ( 26 % ) |
| Total registers | 3385 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 81,694 / 5,662,720 ( 1 % ) |
| Total RAM Blocks | 44 / 553 ( 8 % ) |
| Total DSP Blocks | 26 / 112 ( 23 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`SMP1-s6.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 17.192 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.317 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 36.350 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.328 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.571 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 16.621 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.104 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 36.609 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.122 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.538 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.413 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 37.778 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.812 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.902 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.756 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.094 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.197 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.592 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.907 | 0.000 |

- Worst setup slack: **16.621 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.094 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`SMP1-s6.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 43.84 MHz | 43.84 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 42.77 MHz | 42.77 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 261
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

