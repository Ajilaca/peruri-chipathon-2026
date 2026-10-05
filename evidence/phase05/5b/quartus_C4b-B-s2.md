# MEASURED - Quartus results for revision `C4b-B-s2`

- Generated: 2026-10-01 12:31 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase05_arith_c4/output_files_C4b-B-s2`
- Note: Phase 5b candidate: rtl/ntt/ntt_core_c4b_b.sv (Barrett RED_KIND=2; multiplier-path cuts X, S_1, S_2; memory cuts A_4, A_11, M as C3-P6; test_plan.md amendment A3); constraint 40.000 ns (quartus/phase05_arith_c4/C4.sdc); Quartus defaults; fitter seed 2 (confirmed in the fit report: Fitter Initial Placement Seed = 2); RTL = working tree on branch phase5-arith on top of git 5a1eec0

## Fitter (`C4b-B-s2.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Thu Oct  1 18:46:07 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | C4b-B-s2 |
| Top-level Entity Name | ntt_core_c4b_b |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,168 / 41,910 ( 22 % ) |
| Total registers | 4102 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,314 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 29 / 553 ( 5 % ) |
| Total DSP Blocks | 18 / 112 ( 16 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`C4b-B-s2.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 10.970 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.416 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.955 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.920 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.561 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 10.832 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.330 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 38.141 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.775 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.532 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 24.105 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.181 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.793 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.505 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.900 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 26.674 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.130 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 39.034 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.371 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.906 | 0.000 |

- Worst setup slack: **10.832 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.13 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`C4b-B-s2.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 34.45 MHz | 34.45 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 34.28 MHz | 34.28 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 20
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

