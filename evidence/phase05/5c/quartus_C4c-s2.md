# MEASURED — Quartus results for revision `C4c-s2`

- Generated: 2026-10-01 14:36 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase05_arith_c4/output_files_C4c-s2`
- Note: Phase 5c candidate: rtl/ntt/ntt_core_c4c.sv (Barrett RED_KIND=2, LAZY=1, lazy INTT inputs, ADR 0014; cuts X, S_1, S_2 as C4b-B; memory cuts A_4, A_11, M); constraint 40.000 ns (C4.sdc); Quartus defaults; fitter seed 2 (confirmed in the fit report: Fitter Initial Placement Seed line); RTL = working tree on branch phase5-arith on top of git 97f41a1

## Fitter (`C4c-s2.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Thu Oct  1 21:07:50 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | C4c-s2 |
| Top-level Entity Name | ntt_core_c4c |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,032 / 41,910 ( 22 % ) |
| Total registers | 4078 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,338 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 29 / 553 ( 5 % ) |
| Total DSP Blocks | 18 / 112 ( 16 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`C4c-s2.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 11.806 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.416 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.645 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.570 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.611 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 11.636 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.332 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.777 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.433 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.600 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 25.025 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.184 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.729 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.296 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.952 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 27.373 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.129 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.922 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.171 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.947 | 0.000 |

- Worst setup slack: **11.636 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.129 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`C4c-s2.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 35.47 MHz | 35.47 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 35.26 MHz | 35.26 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 23
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

