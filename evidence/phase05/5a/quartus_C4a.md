# MEASURED — Quartus results for revision `C4a`

- Generated: 2026-10-01 08:49 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase05_arith_c4/output_files_C4a`
- Note: Phase 5a: rtl/ntt/ntt_core_c4a.sv (C4, fold reducer RED_KIND=1, multiplier-path cuts X, F_3, F_5; memory cuts A_4, A_11, M as C3-P6; test_plan.md amendment A1); constraint 40.000 ns (quartus/phase05_arith_c4/C4.sdc, ADR 0011 D1); Quartus defaults, default fitter seed; RTL = working tree on branch phase5-arith on top of git 5a1eec0

## Fitter (`C4a.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Thu Oct  1 15:47:27 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | C4a |
| Top-level Entity Name | ntt_core_c4a |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,847 / 41,910 ( 23 % ) |
| Total registers | 4109 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,314 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 29 / 553 ( 5 % ) |
| Total DSP Blocks | 9 / 112 ( 8 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`C4a.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 10.352 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.449 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.404 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.686 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.586 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 10.463 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.388 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.613 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.509 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.545 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 23.763 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.182 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.532 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.383 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.909 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 26.349 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.107 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.789 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.230 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.911 | 0.000 |

- Worst setup slack: **10.352 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.107 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`C4a.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 33.73 MHz | 33.73 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 33.86 MHz | 33.86 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 20
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

