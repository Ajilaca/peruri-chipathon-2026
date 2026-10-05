# MEASURED — Quartus results for revision `SM2-s4`

- Generated: 2026-10-03 10:59 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase08b_sampler/output_files_SM2-s4`
- Note: Phase 8b stage W2: keccak_sampler OUTW = 2 (streaming SampleNTT and CBD2, two coefficients per cycle), revision SM2-s4, kernel-only virtual pins; working tree on top of commit 794db0d (the W2 RTL is committed afterwards)

## Fitter (`SM2-s4.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 16:58:11 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | SM2-s4 |
| Top-level Entity Name | keccak_sampler |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 5,290 / 41,910 ( 13 % ) |
| Total registers | 1947 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 0 / 5,662,720 ( 0 % ) |
| Total RAM Blocks | 0 / 553 ( 0 % ) |
| Total DSP Blocks | 0 / 112 ( 0 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`SM2-s4.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 19.364 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.396 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.245 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 20.335 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.345 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.141 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 26.913 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.565 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.440 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.162 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.553 | 0.000 |

- Worst setup slack: **19.364 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.162 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`SM2-s4.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 48.46 MHz | 48.46 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 50.85 MHz | 50.85 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 7
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

