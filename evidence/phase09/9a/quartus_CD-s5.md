# MEASURED - Quartus results for revision `CD-s5`

- Generated: 2026-10-03 14:38 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09a_codec/output_files_CD-s5`
- Note: Phase 9a: mlkem_codec_top (packer and unpacker), revision CD-s5, kernel-only virtual pins; working tree before the Phase 9 commits

## Fitter (`CD-s5.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 21:34:00 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | CD-s5 |
| Top-level Entity Name | mlkem_codec_top |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 299 / 41,910 ( < 1 % ) |
| Total registers | 192 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 0 / 5,662,720 ( 0 % ) |
| Total RAM Blocks | 0 / 553 ( 0 % ) |
| Total DSP Blocks | 2 / 112 ( 2 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`CD-s5.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 30.762 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.432 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.259 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 30.716 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.450 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.149 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 35.088 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.181 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.568 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 35.833 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.167 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.558 | 0.000 |

- Worst setup slack: **30.716 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.167 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`CD-s5.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 108.25 MHz | 108.25 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 107.71 MHz | 107.71 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 5
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

