# MEASURED - Quartus results for revision `HF-s2`

- Generated: 2026-10-03 16:21 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09b_hashfo/output_files_HF-s2`
- Note: Phase 9b: mlkem_hash_fo_top (hash wrapper and FO comparison), revision HF-s2, kernel-only virtual pins; working tree before the Phase 9 commits

## Fitter (`HF-s2.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 22:34:47 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | HF-s2 |
| Top-level Entity Name | mlkem_hash_fo_top |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 6,728 / 41,910 ( 16 % ) |
| Total registers | 1976 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 0 / 5,662,720 ( 0 % ) |
| Total RAM Blocks | 0 / 553 ( 0 % ) |
| Total DSP Blocks | 0 / 112 ( 0 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`HF-s2.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 19.122 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.419 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.270 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 19.665 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.440 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.185 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 26.992 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.609 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.503 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.161 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.590 | 0.000 |

- Worst setup slack: **19.122 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.161 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`HF-s2.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 47.9 MHz | 47.9 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 49.18 MHz | 49.18 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 6
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

