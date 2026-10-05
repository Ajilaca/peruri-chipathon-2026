# MEASURED — Quartus results for revision `K2-s2`

- Generated: 2026-10-04 13:51 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09s2_core/output_files_K2-s2`
- Note: Phase 9F S2: mlkem_core3 revision K2-s2 (K1b + NTT_P6 = 1), kernel-only virtual pins, 40.000 ns; compiled in quartus/phase09s2_core; working tree on top of commit cf81581 (S2 changes uncommitted)

## Fitter (`K2-s2.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 19:55:23 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K2-s2 |
| Top-level Entity Name | mlkem_core3 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,171 / 41,910 ( 34 % ) |
| Total registers | 8375 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,603 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`K2-s2.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 20.849 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.316 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.957 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.979 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.578 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 21.481 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.168 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 38.121 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.856 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.553 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 28.312 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.161 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.843 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.504 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.945 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 30.471 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.128 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 39.067 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.377 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.941 | 0.000 |

- Worst setup slack: **20.849 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.128 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K2-s2.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 52.22 MHz | 52.22 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 54.0 MHz | 54.0 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 254
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

