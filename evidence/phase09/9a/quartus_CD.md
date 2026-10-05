# MEASURED - Quartus results for revision `CD`

- Generated: 2026-10-03 14:38 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09a_codec/output_files_CD`
- Note: Phase 9a: mlkem_codec_top (packer and unpacker), revision CD, kernel-only virtual pins; working tree before the Phase 9 commits

## Fitter (`CD.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 21:28:19 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | CD |
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

## Timing (`CD.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 30.388 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.436 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.251 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 30.143 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.446 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.145 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 35.016 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.182 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.566 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 35.725 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.168 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.558 | 0.000 |

- Worst setup slack: **30.143 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.168 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`CD.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 104.04 MHz | 104.04 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 101.45 MHz | 101.45 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 5
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

