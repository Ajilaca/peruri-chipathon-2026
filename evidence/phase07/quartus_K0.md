# MEASURED - Quartus results for revision `K0`

- Generated: 2026-10-03 04:44 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase07_keccak/output_files_K0`
- Note: Phase 7 K0: keccak_sponge (iterative Keccak-f[1600], 1 round/cycle), 40.000 ns (K.sdc), seed 1, kernel-only virtual pins; RTL at commit 361be68 plus Phase 7 working tree (rtl/keccak/*.sv)

## Fitter (`K0.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 11:43:53 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K0 |
| Top-level Entity Name | keccak_sponge |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 3,572 / 41,910 ( 9 % ) |
| Total registers | 1653 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 0 / 5,662,720 ( 0 % ) |
| Total RAM Blocks | 0 / 553 ( 0 % ) |
| Total DSP Blocks | 0 / 112 ( 0 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`K0.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 22.452 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.421 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.276 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 23.217 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.444 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.178 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 29.190 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.609 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 31.244 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.163 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.593 | 0.000 |

- Worst setup slack: **22.452 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.163 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K0.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 56.99 MHz | 56.99 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 59.58 MHz | 59.58 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 6
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

