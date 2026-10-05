# MEASURED — Quartus results for revision `CD-s4`

- Generated: 2026-10-03 14:38 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09a_codec/output_files_CD-s4`
- Note: Phase 9a: mlkem_codec_top (packer and unpacker), revision CD-s4, kernel-only virtual pins; working tree before the Phase 9 commits

## Fitter (`CD-s4.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 21:32:22 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | CD-s4 |
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

## Timing (`CD-s4.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 30.959 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.399 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.256 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 30.624 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.376 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.148 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 35.570 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.179 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.567 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 36.085 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.167 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.558 | 0.000 |

- Worst setup slack: **30.624 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.167 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`CD-s4.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 110.61 MHz | 110.61 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 106.66 MHz | 106.66 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 5
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

