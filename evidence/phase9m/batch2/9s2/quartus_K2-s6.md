# MEASURED - Quartus results for revision `K2-s6`

- Generated: 2026-10-04 13:51 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09s2_core/output_files_K2-s6`
- Note: Phase 9F S2: mlkem_core3 revision K2-s6 (K1b + NTT_P6 = 1), kernel-only virtual pins, 40.000 ns; compiled in quartus/phase09s2_core; working tree on top of commit cf81581 (S2 changes uncommitted)

## Fitter (`K2-s6.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 20:46:58 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K2-s6 |
| Top-level Entity Name | mlkem_core3 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,235 / 41,910 ( 34 % ) |
| Total registers | 8370 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,603 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`K2-s6.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 20.730 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.268 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 38.500 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.655 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.588 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 21.339 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.252 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 38.631 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.556 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.573 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.825 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.144 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 39.189 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.318 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.945 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 30.175 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.115 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 39.336 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.223 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.941 | 0.000 |

- Worst setup slack: **20.73 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.115 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K2-s6.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 51.89 MHz | 51.89 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 53.59 MHz | 53.59 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 254
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

