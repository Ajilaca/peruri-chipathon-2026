# MEASURED — Quartus results for revision `MW-20-s3`

- Generated: 2026-10-04 04:55 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09m2_core/output_files_MW-20-s3`
- Note: Phase 9M-2: mlkem_core at 20.000 ns, revision MW-20-s3, kernel-only virtual pins; branch phase9m-optimisation

## Fitter (`MW-20-s3.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 11:23:58 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MW-20-s3 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 17,800 / 41,910 ( 42 % ) |
| Total registers | 8447 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`MW-20-s3.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 4.236 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.336 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 18.662 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.548 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.586 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 4.581 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.326 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 18.760 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.463 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.545 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 10.438 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 19.344 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.221 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.909 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 12.175 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.131 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 19.453 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.143 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.911 | 0.000 |

- Worst setup slack: **4.236 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.131 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MW-20-s3.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 63.44 MHz | 63.44 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 64.86 MHz | 64.86 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 253
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

