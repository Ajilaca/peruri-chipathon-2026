# MEASURED — Quartus results for revision `CD-20`

- Generated: 2026-10-03 14:38 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09a_codec/output_files_CD-20`
- Note: Phase 9a: mlkem_codec_top (packer and unpacker), revision CD-20, kernel-only virtual pins; working tree before the Phase 9 commits

## Fitter (`CD-20.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 21:37:36 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | CD-20 |
| Top-level Entity Name | mlkem_codec_top |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 298 / 41,910 ( < 1 % ) |
| Total registers | 192 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 0 / 5,662,720 ( 0 % ) |
| Total RAM Blocks | 0 / 553 ( 0 % ) |
| Total DSP Blocks | 2 / 112 ( 2 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`CD-20.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 11.193 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.437 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 9.257 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 10.952 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.451 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 9.147 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 15.458 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.182 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 9.567 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 16.060 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.167 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 9.559 | 0.000 |

- Worst setup slack: **10.952 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.167 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`CD-20.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 113.55 MHz | 113.55 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 110.52 MHz | 110.52 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 5
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

