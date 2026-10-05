# MEASURED - Quartus results for revision `S10-s2`

- Generated: 2026-10-02 20:27 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase06_sched/output_files_S10-s2`
- Note: S10 candidate: rtl/ntt/ntt_core_s10_p5.sv (16-bank 1R1W memory without slot arbitration, P = 5; ADR 0024, test plan evidence/phase06/test_plan_s10.md); constraint 40.000 ns; Quartus defaults; git 8d8cb6f

## Fitter (`S10-s2.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 02:40:28 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | S10-s2 |
| Top-level Entity Name | ntt_core_s10_p5 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 5,088 / 41,910 ( 12 % ) |
| Total registers | 543 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 4,069 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 24 / 553 ( 4 % ) |
| Total DSP Blocks | 16 / 112 ( 14 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`S10-s2.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 16.919 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.293 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 37.298 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.818 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.607 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 16.382 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.278 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 37.456 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.672 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.587 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.592 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.153 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 38.485 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.444 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.957 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.442 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.132 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.736 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.303 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.950 | 0.000 |

- Worst setup slack: **16.382 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.132 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`S10-s2.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 43.33 MHz | 43.33 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 42.34 MHz | 42.34 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 18
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

