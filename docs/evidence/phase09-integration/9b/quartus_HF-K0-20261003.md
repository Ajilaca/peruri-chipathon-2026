# MEASURED — Quartus results for revision `HF-K0`

- Generated: 2026-10-03 16:21 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09b_hashfo/output_files_HF-K0`
- Note: Phase 9b: mlkem_hash_fo_top (hash wrapper and FO comparison), revision HF-K0, kernel-only virtual pins; working tree before the Phase 9 commits

## Fitter (`HF-K0.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 23:02:23 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | HF-K0 |
| Top-level Entity Name | mlkem_hash_fo_top |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 4,221 / 41,910 ( 10 % ) |
| Total registers | 1977 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 0 / 5,662,720 ( 0 % ) |
| Total RAM Blocks | 0 / 553 ( 0 % ) |
| Total DSP Blocks | 0 / 112 ( 0 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`HF-K0.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 25.719 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.425 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.257 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 26.325 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.451 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.149 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 31.135 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.177 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.568 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 32.781 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.163 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.558 | 0.000 |

- Worst setup slack: **25.719 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.163 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`HF-K0.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 70.02 MHz | 70.02 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 73.13 MHz | 73.13 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 6
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

