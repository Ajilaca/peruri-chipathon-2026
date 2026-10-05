# MEASURED - Quartus results for revision `MC-s5`

- Generated: 2026-10-03 18:15 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09c_core/output_files_MC-s5`
- Note: Phase 9c: mlkem_core (KeyGen, Encaps, Decaps; engine of 8d, codec, hash with the C5 sponge, comparison), revision MC-s5, kernel-only virtual pins; working tree before the Phase 9 commits

## Fitter (`MC-s5.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 00:51:44 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MC-s5 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 17,608 / 41,910 ( 42 % ) |
| Total registers | 8272 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`MC-s5.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 20.671 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.306 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.419 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.693 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.579 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 21.295 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.272 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.582 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.549 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.535 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.965 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.523 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.406 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.904 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 30.203 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.106 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.778 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.259 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.906 | 0.000 |

- Worst setup slack: **20.671 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.106 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MC-s5.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 51.74 MHz | 51.74 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 53.46 MHz | 53.46 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 253
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

