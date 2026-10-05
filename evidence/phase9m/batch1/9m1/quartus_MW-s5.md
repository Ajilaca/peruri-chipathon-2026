# MEASURED - Quartus results for revision `MW-s5`

- Generated: 2026-10-04 02:05 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09m1_core/output_files_MW-s5`
- Note: Phase 9M-1: mlkem_core with CODEC_W2 = 1 (two-byte load / store tasks), revision MW-s5, kernel-only virtual pins; branch phase9m-optimisation, rtl/mlkem at the 9M-1 files

## Fitter (`MW-s5.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 08:44:30 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MW-s5 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 17,683 / 41,910 ( 42 % ) |
| Total registers | 8250 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`MW-s5.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 18.655 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.283 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.449 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.690 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.577 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 19.303 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.248 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.617 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.543 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.528 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.324 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.545 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.409 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.905 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.616 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.077 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.789 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.266 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.906 | 0.000 |

- Worst setup slack: **18.655 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.077 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MW-s5.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 46.85 MHz | 46.85 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 48.32 MHz | 48.32 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 253
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

