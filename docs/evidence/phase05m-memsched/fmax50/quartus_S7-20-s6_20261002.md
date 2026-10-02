# MEASURED — Quartus results for revision `S7-20-s6`

- Generated: 2026-10-02 20:02 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase05m_memsched/output_files_S7-20-s6`
- Note: 50 MHz question option 2: S7 RTL (rtl/ntt/ntt_core_s7_p7.sv) at 20.000 ns (quartus/phase05m_memsched/M-20.sdc), information only; Quartus defaults; git 8133e08

## Fitter (`S7-20-s6.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 03:00:20 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | S7-20-s6 |
| Top-level Entity Name | ntt_core_s7_p7 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,355 / 41,910 ( 22 % ) |
| Total registers | 4311 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,423 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 31 / 553 ( 6 % ) |
| Total DSP Blocks | 16 / 112 ( 14 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`S7-20-s6.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | -1.080 | -14.330 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.402 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 17.529 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.929 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.592 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | -1.615 | -22.122 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.306 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 17.699 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.778 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.550 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 9.272 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.183 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 18.607 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.440 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.908 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 10.610 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.150 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 18.860 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.319 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.911 | 0.000 |

- Worst setup slack: **-1.615 ns** (Slow 1100mV -40C Model Setup 'clk_i')  **NEGATIVE: timing not met**
- Worst hold slack: **0.15 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`S7-20-s6.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 47.44 MHz | 47.44 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 46.26 MHz | 46.26 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 3
- Warnings: 19
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

