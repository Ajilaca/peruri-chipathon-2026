# MEASURED — Quartus results for revision `K4-15-s1`

- Generated: 2026-10-04 19:15 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09i4_core/output_files_K4-15-s1`
- Note: Phase 9I item 4: mlkem_core4 (K3 parameters): revision K4-15-s1, kernel-only virtual pins, 15.000 ns; compiled in quartus/phase09i4_core; working tree on top of commit cf81581 (S2 / S2b / item 4 changes uncommitted)

## Fitter (`K4-15-s1.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Mon Oct  5 00:27:31 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K4-15-s1 |
| Top-level Entity Name | mlkem_core4 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,453 / 41,910 ( 34 % ) |
| Total registers | 8502 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,507 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 53 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`K4-15-s1.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 2.653 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.351 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.057 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 2.826 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.165 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.022 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 7.709 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.399 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 8.978 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.105 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.404 | 0.000 |

- Worst setup slack: **2.653 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.105 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K4-15-s1.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 80.99 MHz | 80.99 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 82.14 MHz | 82.14 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 255
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

