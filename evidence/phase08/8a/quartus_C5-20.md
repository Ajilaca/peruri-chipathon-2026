# MEASURED - Quartus results for revision `C5-20`

- Generated: 2026-10-03 05:49 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase08_keccak/output_files_C5-20`
- Note: Phase 8a C5-20: same RTL as C5, 20.000 ns (C-20.sdc, information, not a gate), seed 1, kernel-only virtual pins

## Fitter (`C5-20.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 12:48:40 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | C5-20 |
| Top-level Entity Name | keccak_sponge_r2 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 6,178 / 41,910 ( 15 % ) |
| Total registers | 1652 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 0 / 5,662,720 ( 0 % ) |
| Total RAM Blocks | 0 / 553 ( 0 % ) |
| Total DSP Blocks | 0 / 112 ( 0 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`C5-20.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 4.591 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.418 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 9.258 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 5.042 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.441 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 9.182 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 10.433 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.177 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 9.603 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 12.195 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.162 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 9.589 | 0.000 |

- Worst setup slack: **4.591 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.162 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`C5-20.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 64.9 MHz | 64.9 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 66.85 MHz | 66.85 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 6
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

