# MEASURED - Quartus results for revision `SM1-K0`

- Generated: 2026-10-03 08:03 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase08b_sampler/output_files_SM1-K0`
- Note: Phase 8b stage W1: keccak_sampler (streaming SampleNTT and CBD2, one coefficient per cycle), revision SM1-K0, kernel-only virtual pins; RTL of rtl/sample at the working tree on top of commit dcae678 (committed afterwards)

## Fitter (`SM1-K0.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 15:01:58 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | SM1-K0 |
| Top-level Entity Name | keccak_sampler |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 3,470 / 41,910 ( 8 % ) |
| Total registers | 1914 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 0 / 5,662,720 ( 0 % ) |
| Total RAM Blocks | 0 / 553 ( 0 % ) |
| Total DSP Blocks | 0 / 112 ( 0 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`SM1-K0.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 23.928 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.414 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.243 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 24.496 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.438 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.136 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 30.287 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.562 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 32.052 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.162 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.553 | 0.000 |

- Worst setup slack: **23.928 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.162 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`SM1-K0.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 62.22 MHz | 62.22 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 64.5 MHz | 64.5 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 7
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

