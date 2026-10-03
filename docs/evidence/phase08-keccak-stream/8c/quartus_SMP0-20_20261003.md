# MEASURED — Quartus results for revision `SMP0-20`

- Generated: 2026-10-03 13:26 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/par_a/output_files_SMP0-20`
- Note: Phases 8c/8d: kpke_smp_top_s10 revision SMP0-20, kernel-only virtual pins; compiled in quartus/par_a (a copy of quartus/phase08c_smp with identical .qsf, .sdc and sources, used to run compiles in parallel; not committed); working tree on top of commit d965b4d

## Fitter (`SMP0-20.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 20:05:03 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | SMP0-20 |
| Top-level Entity Name | kpke_smp_top_s10 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 11,058 / 41,910 ( 26 % ) |
| Total registers | 3438 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 155,373 / 5,662,720 ( 3 % ) |
| Total RAM Blocks | 55 / 553 ( 10 % ) |
| Total DSP Blocks | 26 / 112 ( 23 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`SMP0-20.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 2.209 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.285 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 17.162 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.457 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.566 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 0.992 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.174 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 17.399 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.284 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.520 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 9.825 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.171 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 18.289 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.804 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.897 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 11.752 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.105 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 18.636 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.624 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.902 | 0.000 |

- Worst setup slack: **0.992 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.105 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`SMP0-20.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 56.21 MHz | 56.21 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 52.61 MHz | 52.61 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 243
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

