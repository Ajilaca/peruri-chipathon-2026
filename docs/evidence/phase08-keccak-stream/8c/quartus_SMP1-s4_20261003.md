# MEASURED — Quartus results for revision `SMP1-s4`

- Generated: 2026-10-03 13:26 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase08c_smp/output_files_SMP1-s4`
- Note: Phases 8c/8d: kpke_smp_top_s10 revision SMP1-s4, kernel-only virtual pins; compiled in quartus/phase08c_smp; working tree on top of commit d965b4d

## Fitter (`SMP1-s4.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 19:53:26 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | SMP1-s4 |
| Top-level Entity Name | kpke_smp_top_s10 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 11,002 / 41,910 ( 26 % ) |
| Total registers | 3395 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 81,694 / 5,662,720 ( 1 % ) |
| Total RAM Blocks | 44 / 553 ( 8 % ) |
| Total DSP Blocks | 26 / 112 ( 23 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`SMP1-s4.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 17.695 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.359 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 35.390 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 2.066 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.592 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 17.243 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.277 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 35.704 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.824 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.558 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.553 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.176 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 37.179 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 1.239 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.945 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 29.849 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.130 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 37.711 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.940 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.942 | 0.000 |

- Worst setup slack: **17.243 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.13 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`SMP1-s4.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 44.83 MHz | 44.83 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 43.94 MHz | 43.94 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 261
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

