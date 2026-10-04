# MEASURED — Quartus results for revision `HF-20`

- Generated: 2026-10-03 16:21 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09b_hashfo/output_files_HF-20`
- Note: Phase 9b: mlkem_hash_fo_top (hash wrapper and FO comparison), revision HF-20, kernel-only virtual pins; working tree before the Phase 9 commits

## Fitter (`HF-20.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 22:59:49 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | HF-20 |
| Top-level Entity Name | mlkem_hash_fo_top |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 6,745 / 41,910 ( 16 % ) |
| Total registers | 1976 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 0 / 5,662,720 ( 0 % ) |
| Total RAM Blocks | 0 / 553 ( 0 % ) |
| Total DSP Blocks | 0 / 112 ( 0 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`HF-20.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 3.843 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.428 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 9.274 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 4.356 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.455 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 9.178 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 9.880 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 9.608 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 11.829 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.162 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 9.594 | 0.000 |

- Worst setup slack: **3.843 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.162 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`HF-20.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 61.89 MHz | 61.89 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 63.92 MHz | 63.92 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 6
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

