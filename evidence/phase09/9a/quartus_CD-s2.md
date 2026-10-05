# MEASURED - Quartus results for revision `CD-s2`

- Generated: 2026-10-03 14:38 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09a_codec/output_files_CD-s2`
- Note: Phase 9a: mlkem_codec_top (packer and unpacker), revision CD-s2, kernel-only virtual pins; working tree before the Phase 9 commits

## Fitter (`CD-s2.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 21:29:39 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | CD-s2 |
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

## Timing (`CD-s2.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 30.250 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.429 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.266 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 30.046 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.428 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.148 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 34.666 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.181 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.571 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 35.506 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.167 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.559 | 0.000 |

- Worst setup slack: **30.046 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.167 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`CD-s2.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 102.56 MHz | 102.56 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 100.46 MHz | 100.46 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 5
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

