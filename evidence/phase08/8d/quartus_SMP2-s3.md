# MEASURED — Quartus results for revision `SMP2-s3`

- Generated: 2026-10-03 13:26 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase08c_smp/output_files_SMP2-s3`
- Note: Phases 8c/8d: kpke_smp_top_s10 revision SMP2-s3, kernel-only virtual pins; compiled in quartus/phase08c_smp; working tree on top of commit d965b4d

## Fitter (`SMP2-s3.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 19:21:28 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | SMP2-s3 |
| Top-level Entity Name | kpke_smp_top_s10 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 11,009 / 41,910 ( 26 % ) |
| Total registers | 3402 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 81,694 / 5,662,720 ( 1 % ) |
| Total RAM Blocks | 44 / 553 ( 8 % ) |
| Total DSP Blocks | 26 / 112 ( 23 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`SMP2-s3.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 18.984 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.307 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 38.475 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.704 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.597 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 18.440 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.211 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 38.606 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.607 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.572 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 26.822 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.133 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 39.183 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.346 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.953 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.519 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.086 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 39.325 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.251 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.947 | 0.000 |

- Worst setup slack: **18.44 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.086 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`SMP2-s3.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 47.58 MHz | 47.58 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 46.38 MHz | 46.38 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 250
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

