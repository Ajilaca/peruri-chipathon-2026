# MEASURED — Quartus results for revision `SMP2`

- Generated: 2026-10-03 13:26 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase08c_smp/output_files_SMP2`
- Note: Phases 8c/8d: kpke_smp_top_s10 revision SMP2, kernel-only virtual pins; compiled in quartus/phase08c_smp; working tree on top of commit d965b4d

## Fitter (`SMP2.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 18:13:49 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | SMP2 |
| Top-level Entity Name | kpke_smp_top_s10 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 10,987 / 41,910 ( 26 % ) |
| Total registers | 3405 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 81,694 / 5,662,720 ( 1 % ) |
| Total RAM Blocks | 44 / 553 ( 8 % ) |
| Total DSP Blocks | 26 / 112 ( 23 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`SMP2.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 17.686 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.394 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 38.533 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.659 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.599 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 17.049 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.246 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 38.609 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.574 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.563 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 26.764 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 39.282 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.277 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.953 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.258 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.146 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 39.396 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.189 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.946 | 0.000 |

- Worst setup slack: **17.049 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.146 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`SMP2.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 44.81 MHz | 44.81 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 43.57 MHz | 43.57 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 250
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

