# MEASURED — Quartus results for revision `MK`

- Generated: 2026-10-04 06:47 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09m3_core/output_files_MK`
- Note: Phase 9M item 3: mlkem_core with HASH_C5 = 0 (K0 hash sponge), CODEC_W2 = 1, revision MK, kernel-only virtual pins; branch phase9m-optimisation

## Fitter (`MK.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 12:35:18 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MK |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 15,923 / 41,910 ( 38 % ) |
| Total registers | 8249 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`MK.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 19.069 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.320 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.542 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.702 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.586 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 19.977 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.171 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.669 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.555 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.546 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 26.545 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.692 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.371 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.907 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.206 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.080 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.888 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.217 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.910 | 0.000 |

- Worst setup slack: **19.069 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.08 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MK.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 47.78 MHz | 47.78 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 49.94 MHz | 49.94 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 254
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

