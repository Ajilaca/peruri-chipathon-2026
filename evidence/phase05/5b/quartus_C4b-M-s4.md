# MEASURED - Quartus results for revision `C4b-M-s4`

- Generated: 2026-10-01 12:31 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase05_arith_c4/output_files_C4b-M-s4`
- Note: Phase 5b candidate: rtl/ntt/ntt_core_c4b_m.sv (Montgomery RED_KIND=3, Montgomery-form ROM and scaling constant; multiplier-path cuts X, S_1, S_2; memory cuts A_4, A_11, M as C3-P6; test_plan.md amendment A3); constraint 40.000 ns (quartus/phase05_arith_c4/C4.sdc); Quartus defaults; fitter seed 4 (confirmed in the fit report: Fitter Initial Placement Seed = 4); RTL = working tree on branch phase5-arith on top of git 5a1eec0

## Fitter (`C4b-M-s4.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Thu Oct  1 19:09:23 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | C4b-M-s4 |
| Top-level Entity Name | ntt_core_c4b_m |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,286 / 41,910 ( 22 % ) |
| Total registers | 4294 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,314 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 29 / 553 ( 5 % ) |
| Total DSP Blocks | 9 / 112 ( 8 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`C4b-M-s4.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 9.884 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.399 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.721 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.165 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.576 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 10.007 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.307 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.837 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.038 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.530 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 23.377 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.181 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.782 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.558 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.903 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 26.126 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.112 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.985 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.414 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.906 | 0.000 |

- Worst setup slack: **9.884 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.112 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`C4b-M-s4.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 33.2 MHz | 33.2 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 33.34 MHz | 33.34 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 20
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

