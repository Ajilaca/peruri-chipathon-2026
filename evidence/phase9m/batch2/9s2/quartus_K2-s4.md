# MEASURED — Quartus results for revision `K2-s4`

- Generated: 2026-10-04 13:51 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09s2_core/output_files_K2-s4`
- Note: Phase 9F S2: mlkem_core3 revision K2-s4 (K1b + NTT_P6 = 1), kernel-only virtual pins, 40.000 ns; compiled in quartus/phase09s2_core; working tree on top of commit cf81581 (S2 changes uncommitted)

## Fitter (`K2-s4.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 20:21:43 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K2-s4 |
| Top-level Entity Name | mlkem_core3 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,194 / 41,910 ( 34 % ) |
| Total registers | 8327 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,603 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`K2-s4.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 21.174 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.297 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.164 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.859 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.554 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 21.389 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.315 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.351 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.701 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.520 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 28.055 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.128 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.360 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.503 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.897 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 30.429 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.109 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.644 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.342 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.903 | 0.000 |

- Worst setup slack: **21.174 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.109 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K2-s4.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 53.12 MHz | 53.12 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 53.73 MHz | 53.73 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 254
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

