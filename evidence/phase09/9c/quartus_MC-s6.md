# MEASURED — Quartus results for revision `MC-s6`

- Generated: 2026-10-03 18:15 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09c_core/output_files_MC-s6`
- Note: Phase 9c: mlkem_core (KeyGen, Encaps, Decaps; engine of 8d, codec, hash with the C5 sponge, comparison), revision MC-s6, kernel-only virtual pins; working tree before the Phase 9 commits

## Fitter (`MC-s6.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 01:01:54 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MC-s6 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 17,618 / 41,910 ( 42 % ) |
| Total registers | 8248 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`MC-s6.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 19.599 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.361 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.378 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.737 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.573 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 20.424 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.220 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.577 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.558 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.527 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 26.870 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.529 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.406 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.903 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.415 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.104 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.768 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.261 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.908 | 0.000 |

- Worst setup slack: **19.599 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.104 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MC-s6.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 49.02 MHz | 49.02 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 51.08 MHz | 51.08 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 253
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

