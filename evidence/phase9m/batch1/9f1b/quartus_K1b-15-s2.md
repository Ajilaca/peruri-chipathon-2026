# MEASURED — Quartus results for revision `K1b-15-s2`

- Generated: 2026-10-04 12:08 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09f1b_core/output_files_K1b-15-s2`
- Note: Phase 9F step S1b: mlkem_core3 (background hash sidecar) with SMP_C5 = 0, HASH_C5 = 0, CODEC_W2 = 1, revision K1b-15-s2, kernel-only virtual pins; branch phase9m-optimisation

## Fitter (`K1b-15-s2.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 18:16:39 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K1b-15-s2 |
| Top-level Entity Name | mlkem_core3 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,450 / 41,910 ( 34 % ) |
| Total registers | 8256 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,270 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 53 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`K1b-15-s2.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 1.434 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.352 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.077 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 1.414 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.239 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.030 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 7.628 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.174 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 6.405 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 8.912 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.120 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 6.409 | 0.000 |

- Worst setup slack: **1.414 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.12 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K1b-15-s2.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 73.71 MHz | 73.71 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 73.61 MHz | 73.61 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 253
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

