# MEASURED — Quartus results for revision `C4c-s6`

- Generated: 2026-10-01 14:36 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase05_arith_c4/output_files_C4c-s6`
- Note: Phase 5c candidate: rtl/ntt/ntt_core_c4c.sv (Barrett RED_KIND=2, LAZY=1, lazy INTT inputs, ADR 0014; cuts X, S_1, S_2 as C4b-B; memory cuts A_4, A_11, M); constraint 40.000 ns (C4.sdc); Quartus defaults; fitter seed 6 (confirmed in the fit report: Fitter Initial Placement Seed line); RTL = working tree on branch phase5-arith on top of git 97f41a1

## Fitter (`C4c-s6.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Thu Oct  1 21:24:15 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | C4c-s6 |
| Top-level Entity Name | ntt_core_c4c |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,084 / 41,910 ( 22 % ) |
| Total registers | 4091 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,338 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 29 / 553 ( 5 % ) |
| Total DSP Blocks | 18 / 112 ( 16 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`C4c-s6.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 9.895 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.381 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.533 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.328 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.584 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 10.294 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.347 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.667 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.202 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.556 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 23.394 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.175 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.620 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.690 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.905 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 26.121 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.095 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.862 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.524 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.911 | 0.000 |

- Worst setup slack: **9.895 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.095 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`C4c-s6.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 33.22 MHz | 33.22 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 33.66 MHz | 33.66 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 23
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

