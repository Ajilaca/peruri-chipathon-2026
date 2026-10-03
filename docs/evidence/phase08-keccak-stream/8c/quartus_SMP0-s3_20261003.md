# MEASURED — Quartus results for revision `SMP0-s3`

- Generated: 2026-10-03 13:26 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase08c_smp/output_files_SMP0-s3`
- Note: Phases 8c/8d: kpke_smp_top_s10 revision SMP0-s3, kernel-only virtual pins; compiled in quartus/phase08c_smp; working tree on top of commit d965b4d

## Fitter (`SMP0-s3.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 18:57:50 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | SMP0-s3 |
| Top-level Entity Name | kpke_smp_top_s10 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 10,959 / 41,910 ( 26 % ) |
| Total registers | 3362 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 155,373 / 5,662,720 ( 3 % ) |
| Total RAM Blocks | 55 / 553 ( 10 % ) |
| Total DSP Blocks | 26 / 112 ( 23 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`SMP0-s3.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 16.488 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.318 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 35.308 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 2.052 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.590 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 15.789 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.168 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 35.618 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.829 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.557 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 26.813 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.170 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 36.978 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 1.337 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.945 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.466 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.094 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 37.583 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 1.046 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.943 | 0.000 |

- Worst setup slack: **15.789 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.094 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`SMP0-s3.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 42.53 MHz | 42.53 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 41.3 MHz | 41.3 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 243
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

