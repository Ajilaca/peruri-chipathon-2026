# MEASURED — Quartus results for revision `C5-s4`

- Generated: 2026-10-03 05:44 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase08_keccak/output_files_C5-s4`
- Note: Phase 8a C5: keccak_sponge_r2 (two Keccak rounds per cycle), 40.000 ns (C.sdc), seed 4, kernel-only virtual pins; RTL at commit 4926b1a

## Fitter (`C5-s4.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 12:34:54 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | C5-s4 |
| Top-level Entity Name | keccak_sponge_r2 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 6,169 / 41,910 ( 15 % ) |
| Total registers | 1652 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 0 / 5,662,720 ( 0 % ) |
| Total RAM Blocks | 0 / 553 ( 0 % ) |
| Total DSP Blocks | 0 / 112 ( 0 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`C5-s4.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 20.582 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.420 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.258 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 21.313 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.440 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.144 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.889 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 19.567 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 30.238 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.162 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 19.555 | 0.000 |

- Worst setup slack: **20.582 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.162 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`C5-s4.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 51.5 MHz | 51.5 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 53.51 MHz | 53.51 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 6
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

