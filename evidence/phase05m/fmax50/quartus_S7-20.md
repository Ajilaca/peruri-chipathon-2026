# MEASURED — Quartus results for revision `S7-20`

- Generated: 2026-10-02 20:02 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase05m_memsched/output_files_S7-20`
- Note: 50 MHz question option 2: S7 RTL (rtl/ntt/ntt_core_s7_p7.sv) at 20.000 ns (quartus/phase05m_memsched/M-20.sdc), information only; Quartus defaults; git 8133e08

## Fitter (`S7-20.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 02:09:42 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | S7-20 |
| Top-level Entity Name | ntt_core_s7_p7 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,365 / 41,910 ( 22 % ) |
| Total registers | 4327 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,423 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 31 / 553 ( 6 % ) |
| Total DSP Blocks | 16 / 112 ( 14 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`S7-20.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | -0.836 | -8.565 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.442 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 15.836 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.396 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.599 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | -1.388 | -16.724 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.401 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 16.124 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.242 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.582 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 9.734 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.183 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 17.371 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.797 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.949 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 10.833 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.151 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 17.888 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.624 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.947 | 0.000 |

- Worst setup slack: **-1.388 ns** (Slow 1100mV -40C Model Setup 'clk_i')  **NEGATIVE: timing not met**
- Worst hold slack: **0.151 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`S7-20.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 47.99 MHz | 47.99 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 46.76 MHz | 46.76 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 3
- Warnings: 19
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

