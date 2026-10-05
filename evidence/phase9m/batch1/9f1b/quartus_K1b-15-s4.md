# MEASURED - Quartus results for revision `K1b-15-s4`

- Generated: 2026-10-04 12:08 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09f1b_core/output_files_K1b-15-s4`
- Note: Phase 9F step S1b: mlkem_core3 (background hash sidecar) with SMP_C5 = 0, HASH_C5 = 0, CODEC_W2 = 1, revision K1b-15-s4, kernel-only virtual pins; branch phase9m-optimisation

## Fitter (`K1b-15-s4.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 18:38:33 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K1b-15-s4 |
| Top-level Entity Name | mlkem_core3 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,390 / 41,910 ( 34 % ) |
| Total registers | 8213 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,270 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 53 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`K1b-15-s4.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 1.261 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.359 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.084 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 1.007 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.235 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.066 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 7.631 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.167 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.443 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 8.787 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.047 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.440 | 0.000 |

- Worst setup slack: **1.007 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.047 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K1b-15-s4.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 72.79 MHz | 72.79 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 71.46 MHz | 71.46 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 253
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

