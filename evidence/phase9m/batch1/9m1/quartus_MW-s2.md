# MEASURED - Quartus results for revision `MW-s2`

- Generated: 2026-10-04 02:05 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09m1_core/output_files_MW-s2`
- Note: Phase 9M-1: mlkem_core with CODEC_W2 = 1 (two-byte load / store tasks), revision MW-s2, kernel-only virtual pins; branch phase9m-optimisation, rtl/mlkem at the 9M-1 files

## Fitter (`MW-s2.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 08:13:10 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MW-s2 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 17,641 / 41,910 ( 42 % ) |
| Total registers | 8299 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`MW-s2.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 20.048 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.324 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.958 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.981 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.580 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 20.701 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.173 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 38.122 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.853 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.536 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.337 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.799 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.543 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.908 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.826 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.111 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 39.032 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.408 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.909 | 0.000 |

- Worst setup slack: **20.048 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.111 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MW-s2.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 50.12 MHz | 50.12 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 51.82 MHz | 51.82 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 253
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

