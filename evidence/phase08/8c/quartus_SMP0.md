# MEASURED — Quartus results for revision `SMP0`

- Generated: 2026-10-03 13:26 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase08c_smp/output_files_SMP0`
- Note: Phases 8c/8d: kpke_smp_top_s10 revision SMP0, kernel-only virtual pins; compiled in quartus/phase08c_smp; working tree on top of commit d965b4d

## Fitter (`SMP0.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 17:45:44 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | SMP0 |
| Top-level Entity Name | kpke_smp_top_s10 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 10,967 / 41,910 ( 26 % ) |
| Total registers | 3364 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 155,373 / 5,662,720 ( 3 % ) |
| Total RAM Blocks | 55 / 553 ( 10 % ) |
| Total DSP Blocks | 26 / 112 ( 23 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`SMP0.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 15.917 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.329 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 36.029 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.709 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.580 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 15.734 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.155 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 36.266 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.485 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.557 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 26.917 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.177 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 37.546 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 1.048 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.939 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 28.884 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.131 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.018 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.799 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.940 | 0.000 |

- Worst setup slack: **15.734 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.131 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`SMP0.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 41.52 MHz | 41.52 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 41.21 MHz | 41.21 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 243
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

