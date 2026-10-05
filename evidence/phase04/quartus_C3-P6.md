# MEASURED — Quartus results for revision `C3-P6`

- Generated: 2026-09-30 16:10 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase04_pipeline_c3/output_files_P6`
- Note: Phase 4 P=6: rtl/ntt/ntt_core_c3_p6.sv (C3, L=8, cuts A_4, A_11, M, X, D_5, D_11 per test_plan.md section 2); constraint 40.000 ns (quartus/phase04_pipeline_c3/C3.sdc, ADR 0006); default fitter seed; RTL = working tree on top of git c2cc16c, committed together with this file

## Fitter (`C3-P6.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Wed Sep 30 23:09:32 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | C3-P6 |
| Top-level Entity Name | ntt_core_c3_p6 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 10,505 / 41,910 ( 25 % ) |
| Total registers | 4168 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,314 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 29 / 553 ( 5 % ) |
| Total DSP Blocks | 9 / 112 ( 8 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`C3-P6.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 10.753 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.442 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 35.035 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 2.198 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.575 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 11.016 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.343 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 35.316 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 2.004 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.528 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 23.331 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.183 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 36.794 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 1.435 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.903 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 26.219 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.140 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 37.434 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 1.123 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.905 | 0.000 |

- Worst setup slack: **10.753 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.14 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`C3-P6.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 34.19 MHz | 34.19 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 34.5 MHz | 34.5 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 19
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

