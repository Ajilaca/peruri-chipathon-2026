# MEASURED — Quartus results for revision `MW-20-s6`

- Generated: 2026-10-04 04:55 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09m2_core/output_files_MW-20-s6`
- Note: Phase 9M-2: mlkem_core at 20.000 ns, revision MW-20-s6, kernel-only virtual pins; branch phase9m-optimisation

## Fitter (`MW-20-s6.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 11:53:46 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MW-20-s6 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 17,728 / 41,910 ( 42 % ) |
| Total registers | 8407 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`MW-20-s6.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 4.389 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.346 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 17.830 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.047 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.573 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 4.852 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.245 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 17.983 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.936 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.568 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 10.562 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.166 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 18.719 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.575 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.943 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 12.264 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.080 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 18.966 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.446 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.938 | 0.000 |

- Worst setup slack: **4.389 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.08 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MW-20-s6.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 64.06 MHz | 64.06 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 66.02 MHz | 66.02 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 253
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

