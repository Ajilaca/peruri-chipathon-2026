# MEASURED — Quartus results for revision `C3-P6-s4`

- Generated: 2026-10-01 03:16 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase04_pipeline_c3/output_files_P6_s4`
- Note: Phase 4 seed sweep (input to ADR 0008): C3-P6 with fitter SEED 4; everything else identical to C3-P6 (RTL at git 7947c0c, C3.sdc 40.000 ns). Recompiled sequentially after the first attempt failed for a tool reason (see seed_sweep.md)

## Fitter (`C3-P6-s4.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Thu Oct  1 10:09:47 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | C3-P6-s4 |
| Top-level Entity Name | ntt_core_c3_p6 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 10,516 / 41,910 ( 25 % ) |
| Total registers | 4152 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,314 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 29 / 553 ( 5 % ) |
| Total DSP Blocks | 9 / 112 ( 8 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`C3-P6-s4.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 10.756 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.442 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.500 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.634 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.585 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 10.885 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.415 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.653 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.498 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.543 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 23.364 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.182 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.603 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.355 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.909 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 26.206 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.128 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.837 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.218 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.910 | 0.000 |

- Worst setup slack: **10.756 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.128 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`C3-P6-s4.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 34.2 MHz | 34.2 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 34.35 MHz | 34.35 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 19
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

