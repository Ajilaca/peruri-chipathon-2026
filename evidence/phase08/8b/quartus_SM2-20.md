# MEASURED — Quartus results for revision `SM2-20`

- Generated: 2026-10-03 10:59 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase08b_sampler/output_files_SM2-20`
- Note: Phase 8b stage W2: keccak_sampler OUTW = 2 (streaming SampleNTT and CBD2, two coefficients per cycle), revision SM2-20, kernel-only virtual pins; working tree on top of commit 794db0d (the W2 RTL is committed afterwards)

## Fitter (`SM2-20.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 17:42:18 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | SM2-20 |
| Top-level Entity Name | keccak_sampler |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 5,320 / 41,910 ( 13 % ) |
| Total registers | 1947 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 0 / 5,662,720 ( 0 % ) |
| Total RAM Blocks | 0 / 553 ( 0 % ) |
| Total DSP Blocks | 0 / 112 ( 0 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`SM2-20.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 4.214 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.417 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 9.249 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 4.459 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.320 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 9.141 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 10.348 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 9.565 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 12.169 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.162 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 9.554 | 0.000 |

- Worst setup slack: **4.214 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.162 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`SM2-20.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 63.35 MHz | 63.35 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 64.35 MHz | 64.35 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 7
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

