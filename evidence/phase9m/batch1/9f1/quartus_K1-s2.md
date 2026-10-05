# MEASURED - Quartus results for revision `K1-s2`

- Generated: 2026-10-04 09:34 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09f1_core/output_files_K1-s2`
- Note: Phase 9F step S1: mlkem_core2 with SMP_C5 = 0, HASH_C5 = 0, CODEC_W2 = 1, revision K1-s2, kernel-only virtual pins; branch phase9m-optimisation

## Fitter (`K1-s2.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 14:20:08 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K1-s2 |
| Top-level Entity Name | mlkem_core2 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,106 / 41,910 ( 34 % ) |
| Total registers | 8395 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`K1-s2.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 20.980 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.317 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.943 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.977 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.574 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 21.056 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.167 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 38.122 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.831 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.568 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 29.033 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.171 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.820 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.515 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.943 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 30.869 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.095 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 39.046 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.383 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.938 | 0.000 |

- Worst setup slack: **20.98 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.095 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K1-s2.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 52.58 MHz | 52.58 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 52.79 MHz | 52.79 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 253
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

