# MEASURED - Quartus results for revision `P6`

- Generated: 2026-10-02 19:27 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase06_sched/output_files_P6`
- Note: Phase 6 top rtl/sched/kpke_sched_top.sv (K-PKE arithmetic sequencer, poly_store 24 slots, pwm_unit, S7 NTT core); constraint 40.000 ns (quartus/phase06_sched/P.sdc); Quartus defaults; seed 1; git 016bff0

## Fitter (`P6.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 02:25:00 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | P6 |
| Top-level Entity Name | kpke_sched_top |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,840 / 41,910 ( 23 % ) |
| Total registers | 4589 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 181,222 / 5,662,720 ( 3 % ) |
| Total RAM Blocks | 58 / 553 ( 10 % ) |
| Total DSP Blocks | 26 / 112 ( 23 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`P6.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 14.005 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.434 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 36.765 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.267 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.559 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 13.395 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.307 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 36.988 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.053 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.529 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 26.809 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.179 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 37.967 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.682 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.902 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 28.421 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.123 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.377 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.475 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.904 | 0.000 |

- Worst setup slack: **13.395 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.123 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`P6.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 38.47 MHz | 38.47 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 37.59 MHz | 37.59 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 23
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

