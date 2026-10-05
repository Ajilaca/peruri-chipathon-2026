# MEASURED - Quartus results for revision `MC`

- Generated: 2026-10-03 18:15 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09c_core/output_files_MC`
- Note: Phase 9c: mlkem_core (KeyGen, Encaps, Decaps; engine of 8d, codec, hash with the C5 sponge, comparison), revision MC, kernel-only virtual pins; working tree before the Phase 9 commits

## Fitter (`MC.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 00:11:03 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MC |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 17,613 / 41,910 ( 42 % ) |
| Total registers | 8210 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`MC.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 20.272 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.298 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.765 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.116 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.587 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 20.896 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.206 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.945 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.972 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.542 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.871 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.684 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.611 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.909 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 30.243 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.096 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.941 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.465 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.911 | 0.000 |

- Worst setup slack: **20.272 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.096 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MC.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 50.69 MHz | 50.69 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 52.35 MHz | 52.35 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 253
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

