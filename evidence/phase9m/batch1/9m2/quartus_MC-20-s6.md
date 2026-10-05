# MEASURED — Quartus results for revision `MC-20-s6`

- Generated: 2026-10-04 04:55 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09m2_core/output_files_MC-20-s6`
- Note: Phase 9M-2: mlkem_core at 20.000 ns, revision MC-20-s6, kernel-only virtual pins; branch phase9m-optimisation

## Fitter (`MC-20-s6.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 11:04:10 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MC-20-s6 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 17,723 / 41,910 ( 42 % ) |
| Total registers | 8504 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`MC-20-s6.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 3.831 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.331 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 17.924 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.025 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.571 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 4.526 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.194 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 18.091 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.905 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.525 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 9.919 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.163 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 18.770 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.572 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.902 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 11.833 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.077 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 19.011 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.434 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.906 | 0.000 |

- Worst setup slack: **3.831 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.077 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MC-20-s6.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 61.85 MHz | 61.85 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 64.62 MHz | 64.62 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 253
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

