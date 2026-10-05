# MEASURED - Quartus results for revision `K1-15-s1`

- Generated: 2026-10-04 09:34 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09f1_core/output_files_K1-15-s1`
- Note: Phase 9F step S1: mlkem_core2 with SMP_C5 = 0, HASH_C5 = 0, CODEC_W2 = 1, revision K1-15-s1, kernel-only virtual pins; branch phase9m-optimisation

## Fitter (`K1-15-s1.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 15:24:20 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K1-15-s1 |
| Top-level Entity Name | mlkem_core2 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,233 / 41,910 ( 34 % ) |
| Total registers | 8332 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,270 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 53 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`K1-15-s1.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 1.251 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.348 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.093 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 1.172 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.157 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.051 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 7.583 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.443 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 8.852 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.095 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.442 | 0.000 |

- Worst setup slack: **1.172 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.095 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K1-15-s1.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 72.73 MHz | 72.73 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 72.32 MHz | 72.32 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 253
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

