# MEASURED — Quartus results for revision `MC-s2`

- Generated: 2026-10-03 18:15 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09c_core/output_files_MC-s2`
- Note: Phase 9c: mlkem_core (KeyGen, Encaps, Decaps; engine of 8d, codec, hash with the C5 sponge, comparison), revision MC-s2, kernel-only virtual pins; working tree before the Phase 9 commits

## Fitter (`MC-s2.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 00:20:16 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MC-s2 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 17,636 / 41,910 ( 42 % ) |
| Total registers | 8272 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`MC-s2.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 19.010 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.329 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.001 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.606 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.592 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 19.920 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.215 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.216 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.457 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.559 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 26.850 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.162 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.104 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.962 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.947 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.372 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.075 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.496 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.760 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.944 | 0.000 |

- Worst setup slack: **19.01 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.075 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MC-s2.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 47.64 MHz | 47.64 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 49.8 MHz | 49.8 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 253
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

