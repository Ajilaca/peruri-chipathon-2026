# MEASURED — Quartus results for revision `K0-s6`

- Generated: 2026-10-03 05:17 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase07_keccak/output_files_K0-s6`
- Note: Phase 7 K0 baseline for the 8a rule: same RTL as K0, 40.000 ns (K.sdc), seed 6, kernel-only virtual pins

## Fitter (`K0-s6.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 12:17:01 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K0-s6 |
| Top-level Entity Name | keccak_sponge |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 3,561 / 41,910 ( 8 % ) |
| Total registers | 1653 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 0 / 5,662,720 ( 0 % ) |
| Total RAM Blocks | 0 / 553 ( 0 % ) |
| Total DSP Blocks | 0 / 112 ( 0 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`K0-s6.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 25.251 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.402 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.273 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 25.880 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.421 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.169 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 30.607 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.178 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.575 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 32.418 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.164 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.562 | 0.000 |

- Worst setup slack: **25.251 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.164 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K0-s6.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 67.8 MHz | 67.8 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 70.82 MHz | 70.82 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 6
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

