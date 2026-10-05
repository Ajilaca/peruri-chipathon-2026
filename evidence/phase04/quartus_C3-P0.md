# MEASURED — Quartus results for revision `C3-P0`

- Generated: 2026-09-30 15:59 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase04_pipeline_c3/output_files_P0`
- Note: Phase 4 P=0 reference: frozen rtl/ntt/ntt_core_c2_k2_k1_l8.sv (C2-K2-K1, L=8) re-compiled with the Phase 4 constraint 40.000 ns (quartus/phase04_pipeline_c3/C3.sdc, ADR 0006); RTL at git c2cc16c; default fitter seed

## Fitter (`C3-P0.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Wed Sep 30 22:49:24 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | C3-P0 |
| Top-level Entity Name | ntt_core_c2_k2_k1_l8 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,723 / 41,910 ( 23 % ) |
| Total registers | 3097 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 0 / 5,662,720 ( 0 % ) |
| Total RAM Blocks | 0 / 553 ( 0 % ) |
| Total DSP Blocks | 9 / 112 ( 8 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`C3-P0.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | -90.653 | -272774.468 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.547 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.267 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | -90.157 | -271522.803 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.502 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.184 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | -30.081 | -88799.618 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.220 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.609 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | -19.769 | -57570.377 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.207 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.597 | 0.000 |

- Worst setup slack: **-90.653 ns** (Slow 1100mV 100C Model Setup 'clk_i')  **NEGATIVE: timing not met**
- Worst hold slack: **0.207 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`C3-P0.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 7.65 MHz | 7.65 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 7.68 MHz | 7.68 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 5
- Warnings: 11
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

