# MEASURED - Quartus results for revision `C3-P6-s5`

- Generated: 2026-10-01 03:00 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase04_pipeline_c3/output_files_P6_s5`
- Note: Phase 4 seed sweep (input to ADR 0008): C3-P6 with fitter SEED 5; everything else identical to C3-P6 (RTL at git 7947c0c, C3.sdc 40.000 ns)

## Fitter (`C3-P6-s5.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Thu Oct  1 09:55:00 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | C3-P6-s5 |
| Top-level Entity Name | ntt_core_c3_p6 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 10,504 / 41,910 ( 25 % ) |
| Total registers | 4139 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,314 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 29 / 553 ( 5 % ) |
| Total DSP Blocks | 9 / 112 ( 8 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`C3-P6-s5.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 9.873 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.387 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 36.770 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.789 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.576 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 9.824 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.313 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 36.956 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.610 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.530 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 23.218 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.178 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.079 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.989 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.904 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 25.980 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.144 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.443 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.778 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.907 | 0.000 |

- Worst setup slack: **9.824 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.144 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`C3-P6-s5.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 33.19 MHz | 33.19 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 33.14 MHz | 33.14 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 19
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

