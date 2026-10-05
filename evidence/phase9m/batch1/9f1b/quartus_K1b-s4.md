# MEASURED - Quartus results for revision `K1b-s4`

- Generated: 2026-10-04 12:08 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09f1b_core/output_files_K1b-s4`
- Note: Phase 9F step S1b: mlkem_core3 (background hash sidecar) with SMP_C5 = 0, HASH_C5 = 0, CODEC_W2 = 1, revision K1b-s4, kernel-only virtual pins; branch phase9m-optimisation

## Fitter (`K1b-s4.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 17:37:13 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K1b-s4 |
| Top-level Entity Name | mlkem_core3 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,330 / 41,910 ( 34 % ) |
| Total registers | 8243 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`K1b-s4.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 20.559 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.334 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 35.937 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.695 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.587 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 21.168 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.236 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 36.251 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.414 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.562 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.231 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.170 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 37.540 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.974 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.946 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.912 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.095 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.021 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.717 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.943 | 0.000 |

- Worst setup slack: **20.559 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.095 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K1b-s4.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 51.44 MHz | 51.44 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 53.1 MHz | 53.1 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 253
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

