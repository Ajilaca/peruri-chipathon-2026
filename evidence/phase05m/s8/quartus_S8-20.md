# MEASURED — Quartus results for revision `S8-20`

- Generated: 2026-10-02 17:38 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase05m_memsched/output_files_S8-20`
- Note: Phase 5M step S8 information compile at 20.000 ns (quartus/phase05m_memsched/M-20.sdc), same RTL and seed 1 as S8; not part of the adoption rule; git 300aaf3

## Fitter (`S8-20.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Fri Oct  2 22:56:51 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | S8-20 |
| Top-level Entity Name | ntt_core_s8_p8 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,443 / 41,910 ( 23 % ) |
| Total registers | 4142 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,942 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 33 / 553 ( 6 % ) |
| Total DSP Blocks | 16 / 112 ( 14 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`S8-20.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | -1.771 | -18.802 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.418 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 17.003 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.873 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.605 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | -2.242 | -32.118 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.330 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 17.155 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.731 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.578 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 9.383 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.183 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 18.385 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.489 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.950 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 10.588 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.125 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 18.635 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.342 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.946 | 0.000 |

- Worst setup slack: **-2.242 ns** (Slow 1100mV -40C Model Setup 'clk_i')  **NEGATIVE: timing not met**
- Worst hold slack: **0.125 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`S8-20.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 45.93 MHz | 45.93 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 44.96 MHz | 44.96 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 3
- Warnings: 20
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

