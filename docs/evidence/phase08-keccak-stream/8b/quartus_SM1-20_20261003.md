# MEASURED — Quartus results for revision `SM1-20`

- Generated: 2026-10-03 08:03 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase08b_sampler/output_files_SM1-20`
- Note: Phase 8b stage W1: keccak_sampler (streaming SampleNTT and CBD2, one coefficient per cycle), revision SM1-20, kernel-only virtual pins; RTL of rtl/sample at the working tree on top of commit dcae678 (committed afterwards)

## Fitter (`SM1-20.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 14:57:32 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | SM1-20 |
| Top-level Entity Name | keccak_sampler |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 5,296 / 41,910 ( 13 % ) |
| Total registers | 1913 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 0 / 5,662,720 ( 0 % ) |
| Total RAM Blocks | 0 / 553 ( 0 % ) |
| Total DSP Blocks | 0 / 112 ( 0 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`SM1-20.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 3.892 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.415 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 9.262 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 4.330 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.437 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 9.189 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 10.063 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 9.607 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 11.882 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.161 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 9.591 | 0.000 |

- Worst setup slack: **3.892 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.161 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`SM1-20.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 62.08 MHz | 62.08 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 63.82 MHz | 63.82 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 7
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

