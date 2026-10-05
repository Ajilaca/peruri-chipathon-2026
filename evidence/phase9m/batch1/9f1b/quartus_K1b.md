# MEASURED - Quartus results for revision `K1b`

- Generated: 2026-10-04 12:08 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09f1b_core/output_files_K1b`
- Note: Phase 9F step S1b: mlkem_core3 (background hash sidecar) with SMP_C5 = 0, HASH_C5 = 0, CODEC_W2 = 1, revision K1b, kernel-only virtual pins; branch phase9m-optimisation

## Fitter (`K1b.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 17:11:51 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K1b |
| Top-level Entity Name | mlkem_core3 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 14,338 / 41,910 ( 34 % ) |
| Total registers | 8254 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`K1b.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 20.857 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.285 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.802 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.496 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.579 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 21.642 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.272 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.935 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.361 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.525 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.666 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.149 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.837 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.241 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.904 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 30.084 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.110 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 39.010 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.126 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.908 | 0.000 |

- Worst setup slack: **20.857 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.11 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K1b.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 52.24 MHz | 52.24 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 54.47 MHz | 54.47 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 253
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

