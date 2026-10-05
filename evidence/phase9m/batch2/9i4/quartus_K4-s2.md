# MEASURED — Quartus results for revision `K4-s2`

- Generated: 2026-10-04 19:15 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09i4_core/output_files_K4-s2`
- Note: Phase 9I item 4: mlkem_core4 (K3 parameters): revision K4-s2, kernel-only virtual pins, 40.000 ns; compiled in quartus/phase09i4_core; working tree on top of commit cf81581 (S2 / S2b / item 4 changes uncommitted)

## Fitter (`K4-s2.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Mon Oct  5 01:31:42 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K4-s2 |
| Top-level Entity Name | mlkem_core4 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,203 / 41,910 ( 34 % ) |
| Total registers | 8479 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,603 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`K4-s2.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 16.690 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.260 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 38.287 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.782 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.599 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 17.893 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.243 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 38.424 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.660 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.566 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 25.253 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.149 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 39.056 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.391 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.953 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 28.139 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.126 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 39.230 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.280 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.946 | 0.000 |

- Worst setup slack: **16.69 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.126 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K4-s2.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 42.9 MHz | 42.9 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 45.23 MHz | 45.23 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 255
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

