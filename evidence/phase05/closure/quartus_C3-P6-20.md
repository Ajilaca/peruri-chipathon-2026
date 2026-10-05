# MEASURED — Quartus results for revision `C3-P6-20`

- Generated: 2026-10-01 17:08 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase05_arith_c4/output_files_C3-P6-20`
- Note: Phase 5 closure, INFORMATION compile (ADR 0011 D1): C3-P6 (ntt_core_c3_p6, Phase 4 RTL unchanged, QSF = C3-P6.qsf with only output folder and SDC changed) at 20.000 ns (quartus/phase05_arith_c4/C4-20.sdc); Quartus defaults; default seed 1; not a Phase 5 gate (ADR 0010)

## Fitter (`C3-P6-20.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Fri Oct  2 00:07:37 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | C3-P6-20 |
| Top-level Entity Name | ntt_core_c3_p6 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 10,557 / 41,910 ( 25 % ) |
| Total registers | 4316 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,314 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 29 / 553 ( 5 % ) |
| Total DSP Blocks | 9 / 112 ( 8 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`C3-P6-20.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | -2.022 | -393.097 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.435 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 16.157 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.634 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.607 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | -2.059 | -413.397 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.358 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 16.415 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.396 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.585 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 7.945 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.183 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 17.686 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.972 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.954 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 10.040 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.147 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 18.104 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.723 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.950 | 0.000 |

- Worst setup slack: **-2.059 ns** (Slow 1100mV -40C Model Setup 'clk_i')  **NEGATIVE: timing not met**
- Worst hold slack: **0.147 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`C3-P6-20.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 45.41 MHz | 45.41 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 45.33 MHz | 45.33 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 3
- Warnings: 19
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

