# MEASURED — Quartus results for revision `SMP0-s5`

- Generated: 2026-10-03 13:26 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/par_b/output_files_SMP0-s5`
- Note: Phases 8c/8d: kpke_smp_top_s10 revision SMP0-s5, kernel-only virtual pins; compiled in quartus/par_b (a copy of quartus/phase08c_smp with identical .qsf, .sdc and sources, used to run compiles in parallel; not committed); working tree on top of commit d965b4d

## Fitter (`SMP0-s5.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 19:37:01 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | SMP0-s5 |
| Top-level Entity Name | kpke_smp_top_s10 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 10,941 / 41,910 ( 26 % ) |
| Total registers | 3354 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 155,373 / 5,662,720 ( 3 % ) |
| Total RAM Blocks | 55 / 553 ( 10 % ) |
| Total DSP Blocks | 26 / 112 ( 23 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`SMP0-s5.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 16.703 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.307 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 36.775 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.070 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.577 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 16.272 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.283 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 36.996 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.898 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.524 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.333 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.158 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.037 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.677 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.905 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.467 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.134 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.403 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.483 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.907 | 0.000 |

- Worst setup slack: **16.272 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.134 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`SMP0-s5.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 42.92 MHz | 42.92 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 42.14 MHz | 42.14 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 243
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

