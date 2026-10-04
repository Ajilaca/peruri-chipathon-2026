# MEASURED — Quartus results for revision `K4`

- Generated: 2026-10-04 19:15 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09i4_core/output_files_K4`
- Note: Phase 9I item 4: mlkem_core4 (K3 parameters): revision K4, kernel-only virtual pins, 40.000 ns; compiled in quartus/phase09i4_core; working tree on top of commit cf81581 (S2 / S2b / item 4 changes uncommitted)

## Fitter (`K4.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Mon Oct  5 01:22:31 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K4 |
| Top-level Entity Name | mlkem_core4 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,215 / 41,910 ( 34 % ) |
| Total registers | 8482 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,603 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`K4.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 20.902 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.319 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.347 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.404 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.577 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 21.700 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.307 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.541 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.219 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.527 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 28.291 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.168 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.448 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.730 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.902 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 30.460 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.115 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.751 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.561 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.906 | 0.000 |

- Worst setup slack: **20.902 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.115 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K4.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 52.36 MHz | 52.36 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 54.64 MHz | 54.64 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 255
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

