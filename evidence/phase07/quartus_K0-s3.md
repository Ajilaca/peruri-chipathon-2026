# MEASURED — Quartus results for revision `K0-s3`

- Generated: 2026-10-03 05:17 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase07_keccak/output_files_K0-s3`
- Note: Phase 7 K0 baseline for the 8a rule: same RTL as K0, 40.000 ns (K.sdc), seed 3, kernel-only virtual pins

## Fitter (`K0-s3.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 12:08:25 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | K0-s3 |
| Top-level Entity Name | keccak_sponge |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 3,566 / 41,910 ( 9 % ) |
| Total registers | 1653 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 0 / 5,662,720 ( 0 % ) |
| Total RAM Blocks | 0 / 553 ( 0 % ) |
| Total DSP Blocks | 0 / 112 ( 0 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`K0-s3.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 25.196 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.416 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.290 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 25.636 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.396 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.207 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 30.852 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.177 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.622 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 32.518 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.162 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.601 | 0.000 |

- Worst setup slack: **25.196 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.162 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`K0-s3.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 67.55 MHz | 67.55 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 69.62 MHz | 69.62 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 6
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

