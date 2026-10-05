# MEASURED — Quartus results for revision `M6`

- Generated: 2026-10-02 12:42 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase05m_memsched/output_files_M6`
- Note: Phase 5M step S6 candidate: rtl/ntt/ntt_core_m6_p6.sv (Barrett, INTT without the scaling pass, halving in every layer; ADR 0017, test plan evidence/phase05m/test_plan.md); cuts as C4b-B (A_4, A_11, M; X, S_1, S_2); constraint 40.000 ns (quartus/phase05m_memsched/M.sdc); Quartus defaults; fitter seed 1 (confirmed in the fit report: Fitter Initial Placement Seed line); RTL = branch phase5m-memory-schedule working tree on top of git f47efcc; full compile from a clean db

## Fitter (`M6.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Fri Oct  2 18:54:45 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | M6 |
| Top-level Entity Name | ntt_core_m6_p6 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,426 / 41,910 ( 22 % ) |
| Total registers | 4041 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,314 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 29 / 553 ( 5 % ) |
| Total DSP Blocks | 16 / 112 ( 14 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`M6.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 11.161 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.422 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 36.664 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.209 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.588 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 11.388 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.407 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 36.860 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.052 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.559 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 23.957 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.181 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 37.974 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.756 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.940 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 26.589 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.145 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.345 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.559 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.940 | 0.000 |

- Worst setup slack: **11.161 ns** (Slow 1100mV 100C Model Setup 'clk_i')
- Worst hold slack: **0.145 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`M6.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 34.68 MHz | 34.68 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 34.95 MHz | 34.95 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 19
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

