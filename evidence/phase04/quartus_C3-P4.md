# MEASURED - Quartus results for revision `C3-P4`

- Generated: 2026-09-30 16:10 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase04_pipeline_c3/output_files_P4`
- Note: Phase 4 P=4: rtl/ntt/ntt_core_c3_p4.sv (C3, L=8, cuts A_7, M, X, D_7 per test_plan.md section 2); constraint 40.000 ns (quartus/phase04_pipeline_c3/C3.sdc, ADR 0006); default fitter seed; RTL = working tree on top of git c2cc16c, committed together with this file

## Fitter (`C3-P4.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Wed Sep 30 23:04:32 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | C3-P4 |
| Top-level Entity Name | ntt_core_c3_p4 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 10,439 / 41,910 ( 25 % ) |
| Total registers | 4145 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 27,428 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 26 / 553 ( 5 % ) |
| Total DSP Blocks | 9 / 112 ( 8 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`C3-P4.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 9.322 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.400 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.622 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 8.734 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.347 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.615 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 23.368 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.183 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.974 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 26.089 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.157 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.978 | 0.000 |

- Worst setup slack: **8.734 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.157 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`C3-P4.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 32.6 MHz | 32.6 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 31.98 MHz | 31.98 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 19
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

