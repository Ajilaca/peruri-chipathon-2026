# MEASURED - Quartus results for revision `MC-20`

- Generated: 2026-10-03 18:15 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09c_core/output_files_MC-20`
- Note: Phase 9c: mlkem_core (KeyGen, Encaps, Decaps; engine of 8d, codec, hash with the C5 sponge, comparison), revision MC-20, kernel-only virtual pins; working tree before the Phase 9 commits

## Fitter (`MC-20.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 01:13:19 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MC-20 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 17,650 / 41,910 ( 42 % ) |
| Total registers | 8374 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`MC-20.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 4.419 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.352 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 18.564 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.605 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.552 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 4.747 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.197 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 18.676 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.505 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.530 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 10.624 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.174 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 19.260 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.271 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.898 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 12.292 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.113 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 19.387 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.185 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.903 | 0.000 |

- Worst setup slack: **4.419 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.113 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MC-20.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 64.18 MHz | 64.18 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 65.56 MHz | 65.56 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 253
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

