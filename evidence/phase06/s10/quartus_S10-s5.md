# MEASURED - Quartus results for revision `S10-s5`

- Generated: 2026-10-02 20:27 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase06_sched/output_files_S10-s5`
- Note: S10 candidate: rtl/ntt/ntt_core_s10_p5.sv (16-bank 1R1W memory without slot arbitration, P = 5; ADR 0024, test plan evidence/phase06/test_plan_s10.md); constraint 40.000 ns; Quartus defaults; git 8d8cb6f

## Fitter (`S10-s5.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 02:58:38 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | S10-s5 |
| Top-level Entity Name | ntt_core_s10_p5 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 5,045 / 41,910 ( 12 % ) |
| Total registers | 552 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 4,069 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 24 / 553 ( 4 % ) |
| Total DSP Blocks | 16 / 112 ( 14 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`S10-s5.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 18.186 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.327 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.412 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.749 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.595 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 17.205 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.304 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.576 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.605 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.540 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.965 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.178 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.568 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.411 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.913 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.943 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.106 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.795 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.260 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.912 | 0.000 |

- Worst setup slack: **17.205 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.106 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`S10-s5.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 45.84 MHz | 45.84 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 43.87 MHz | 43.87 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 18
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

