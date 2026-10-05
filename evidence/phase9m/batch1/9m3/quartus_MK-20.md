# MEASURED - Quartus results for revision `MK-20`

- Generated: 2026-10-04 06:47 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09m3_core/output_files_MK-20`
- Note: Phase 9M item 3: mlkem_core with HASH_C5 = 0 (K0 hash sponge), CODEC_W2 = 1, revision MK-20, kernel-only virtual pins; branch phase9m-optimisation

## Fitter (`MK-20.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 13:43:55 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MK-20 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 16,007 / 41,910 ( 38 % ) |
| Total registers | 8327 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`MK-20.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 4.003 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.342 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 17.791 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.084 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.565 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 4.294 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.289 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 17.955 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.935 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.535 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 10.109 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.143 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 18.725 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.567 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.901 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 11.948 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.067 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 18.973 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.422 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.906 | 0.000 |

- Worst setup slack: **4.003 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.067 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MK-20.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 62.51 MHz | 62.51 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 63.67 MHz | 63.67 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 254
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

