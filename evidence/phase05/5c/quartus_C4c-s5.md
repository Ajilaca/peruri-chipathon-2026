# MEASURED — Quartus results for revision `C4c-s5`

- Generated: 2026-10-01 14:36 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase05_arith_c4/output_files_C4c-s5`
- Note: Phase 5c candidate: rtl/ntt/ntt_core_c4c.sv (Barrett RED_KIND=2, LAZY=1, lazy INTT inputs, ADR 0014; cuts X, S_1, S_2 as C4b-B; memory cuts A_4, A_11, M); constraint 40.000 ns (C4.sdc); Quartus defaults; fitter seed 5 (confirmed in the fit report: Fitter Initial Placement Seed line); RTL = working tree on branch phase5-arith on top of git 97f41a1

## Fitter (`C4c-s5.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Thu Oct  1 21:20:13 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | C4c-s5 |
| Top-level Entity Name | ntt_core_c4c |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,068 / 41,910 ( 22 % ) |
| Total registers | 4081 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,338 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 29 / 553 ( 5 % ) |
| Total DSP Blocks | 18 / 112 ( 16 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`C4c-s5.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 11.154 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.405 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.713 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.131 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.586 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 11.011 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.307 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.903 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.976 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.541 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 24.331 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.183 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.618 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.643 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.909 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 26.870 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.133 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.898 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.486 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.911 | 0.000 |

- Worst setup slack: **11.011 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.133 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`C4c-s5.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 34.67 MHz | 34.67 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 34.5 MHz | 34.5 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 23
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

