# MEASURED - Quartus results for revision `K1-s3`

- Generated: 2026-10-04 09:34 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09f1_core/output_files_K1-s3`
- Note: Phase 9F step S1: mlkem_core2 with SMP_C5 = 0, HASH_C5 = 0, CODEC_W2 = 1, revision K1-s3, kernel-only virtual pins; branch phase9m-optimisation

## Fitter (`K1-s3.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 14:31:51 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K1-s3 |
| Top-level Entity Name | mlkem_core2 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,033 / 41,910 ( 33 % ) |
| Total registers | 8376 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`K1-s3.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 21.273 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.326 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.709 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.136 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.591 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 21.772 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.208 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.889 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.999 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.558 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 28.269 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.173 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.647 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.625 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.946 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 30.585 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.091 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.912 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.479 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.943 | 0.000 |

- Worst setup slack: **21.273 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.091 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K1-s3.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 53.4 MHz | 53.4 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 54.86 MHz | 54.86 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 253
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

