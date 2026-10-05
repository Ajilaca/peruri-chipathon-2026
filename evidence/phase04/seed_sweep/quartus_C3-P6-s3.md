# MEASURED — Quartus results for revision `C3-P6-s3`

- Generated: 2026-10-01 03:00 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase04_pipeline_c3/output_files_P6_s3`
- Note: Phase 4 seed sweep (input to ADR 0008): C3-P6 with fitter SEED 3; everything else identical to C3-P6 (RTL at git 7947c0c, C3.sdc 40.000 ns)

## Fitter (`C3-P6-s3.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Wed Sep 30 23:37:38 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | C3-P6-s3 |
| Top-level Entity Name | ntt_core_c3_p6 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 10,511 / 41,910 ( 25 % ) |
| Total registers | 4160 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,314 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 29 / 553 ( 5 % ) |
| Total DSP Blocks | 9 / 112 ( 8 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`C3-P6-s3.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 9.328 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.437 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 36.904 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.091 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.575 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 9.602 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.386 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.068 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.915 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.527 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 22.943 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.179 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.278 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.598 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.904 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 25.671 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.132 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.553 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.413 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.909 | 0.000 |

- Worst setup slack: **9.328 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.132 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`C3-P6-s3.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 32.6 MHz | 32.6 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 32.9 MHz | 32.9 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 19
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

