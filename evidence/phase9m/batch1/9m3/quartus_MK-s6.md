# MEASURED — Quartus results for revision `MK-s6`

- Generated: 2026-10-04 06:47 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase09m3_core/output_files_MK-s6`
- Note: Phase 9M item 3: mlkem_core with HASH_C5 = 0 (K0 hash sponge), CODEC_W2 = 1, revision MK-s6, kernel-only virtual pins; branch phase9m-optimisation

## Fitter (`MK-s6.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sun Oct  4 13:30:28 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | MK-s6 |
| Top-level Entity Name | mlkem_core |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 15,940 / 41,910 ( 38 % ) |
| Total registers | 8382 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 120,350 / 5,662,720 ( 2 % ) |
| Total RAM Blocks | 54 / 553 ( 10 % ) |
| Total DSP Blocks | 28 / 112 ( 25 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`MK-s6.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 19.577 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.282 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 36.707 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.815 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.572 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 19.889 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.254 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 36.958 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.605 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.546 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.208 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.133 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 37.933 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 1.060 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.905 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.755 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.117 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.355 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.838 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.908 | 0.000 |

- Worst setup slack: **19.577 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.117 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`MK-s6.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 48.96 MHz | 48.96 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 49.72 MHz | 49.72 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 254
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

