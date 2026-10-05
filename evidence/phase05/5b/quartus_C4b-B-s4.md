# MEASURED — Quartus results for revision `C4b-B-s4`

- Generated: 2026-10-01 12:31 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase05_arith_c4/output_files_C4b-B-s4`
- Note: Phase 5b candidate: rtl/ntt/ntt_core_c4b_b.sv (Barrett RED_KIND=2; multiplier-path cuts X, S_1, S_2; memory cuts A_4, A_11, M as C3-P6; test_plan.md amendment A3); constraint 40.000 ns (quartus/phase05_arith_c4/C4.sdc); Quartus defaults; fitter seed 4 (confirmed in the fit report: Fitter Initial Placement Seed = 4); RTL = working tree on branch phase5-arith on top of git 5a1eec0

## Fitter (`C4b-B-s4.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Thu Oct  1 19:04:42 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | C4b-B-s4 |
| Top-level Entity Name | ntt_core_c4b_b |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,174 / 41,910 ( 22 % ) |
| Total registers | 4089 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,314 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 29 / 553 ( 5 % ) |
| Total DSP Blocks | 18 / 112 ( 16 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`C4b-B-s4.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 10.112 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.415 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.794 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.081 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.564 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 10.202 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.332 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.965 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.928 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.527 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 23.221 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.182 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.738 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.558 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.900 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 25.951 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.134 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.983 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.415 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.905 | 0.000 |

- Worst setup slack: **10.112 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.134 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`C4b-B-s4.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 33.46 MHz | 33.46 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 33.56 MHz | 33.56 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 20
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

