# MEASURED - Quartus results for revision `K1b-15-s6`

- Generated: 2026-10-04 12:08 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09f1b_core/output_files_K1b-15-s6`
- Note: Phase 9F step S1b: mlkem_core3 (background hash sidecar) with SMP_C5 = 0, HASH_C5 = 0, CODEC_W2 = 1, revision K1b-15-s6, kernel-only virtual pins; branch phase9m-optimisation

## Fitter (`K1b-15-s6.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 19:02:38 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K1b-15-s6 |
| Top-level Entity Name | mlkem_core3 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,459 / 41,910 ( 35 % ) |
| Total registers | 8231 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,270 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 53 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`K1b-15-s6.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 1.559 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.315 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.091 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 1.570 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.268 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.060 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 7.874 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.173 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.444 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 8.979 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.110 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.445 | 0.000 |

- Worst setup slack: **1.559 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.11 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K1b-15-s6.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 74.4 MHz | 74.4 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 74.46 MHz | 74.46 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 253
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

