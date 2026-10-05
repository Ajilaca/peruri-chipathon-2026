# MEASURED — Quartus results for revision `S10`

- Generated: 2026-10-02 20:27 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase06_sched/output_files_S10`
- Note: S10 candidate: rtl/ntt/ntt_core_s10_p5.sv (16-bank 1R1W memory without slot arbitration, P = 5; ADR 0024, test plan evidence/phase06/test_plan_s10.md); constraint 40.000 ns; Quartus defaults; git 8d8cb6f

## Fitter (`S10.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 02:33:27 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | S10 |
| Top-level Entity Name | ntt_core_s10_p5 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 5,091 / 41,910 ( 12 % ) |
| Total registers | 545 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 4,069 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 24 / 553 ( 4 % ) |
| Total DSP Blocks | 16 / 112 ( 14 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`S10.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 18.551 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.347 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.223 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.389 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.580 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 17.662 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.307 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.447 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.243 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.546 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 29.174 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.167 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.283 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.806 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.904 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 30.716 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.089 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.632 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.627 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.910 | 0.000 |

- Worst setup slack: **17.662 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.089 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`S10.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 46.62 MHz | 46.62 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 44.77 MHz | 44.77 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 18
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

