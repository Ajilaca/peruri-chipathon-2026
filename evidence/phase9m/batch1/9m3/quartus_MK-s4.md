# MEASURED - Quartus results for revision `MK-s4`

- Generated: 2026-10-04 06:47 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09m3_core/output_files_MK-s4`
- Note: Phase 9M item 3: mlkem_core with HASH_C5 = 0 (K0 hash sponge), CODEC_W2 = 1, revision MK-s4, kernel-only virtual pins; branch phase9m-optimisation

## Fitter (`MK-s4.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 13:06:31 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MK-s4 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 15,912 / 41,910 ( 38 % ) |
| Total registers | 8261 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`MK-s4.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 19.754 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.327 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.047 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.614 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.590 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 20.336 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.256 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.263 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.436 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.554 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.659 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.174 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.934 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.946 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.894 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.107 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.545 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.731 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.943 | 0.000 |

- Worst setup slack: **19.754 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.107 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MK-s4.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 49.39 MHz | 49.39 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 50.85 MHz | 50.85 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 254
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

