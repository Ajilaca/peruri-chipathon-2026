# MEASURED — Quartus results for revision `S7-20-s2`

- Generated: 2026-10-02 20:02 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase05m_memsched/output_files_S7-20-s2`
- Note: 50 MHz question option 2: S7 RTL (rtl/ntt/ntt_core_s7_p7.sv) at 20.000 ns (quartus/phase05m_memsched/M-20.sdc), information only; Quartus defaults; git 8133e08

## Fitter (`S7-20-s2.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Sat Oct  3 02:16:57 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | S7-20-s2 |
| Top-level Entity Name | ntt_core_s7_p7 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,358 / 41,910 ( 22 % ) |
| Total registers | 4350 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,423 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 31 / 553 ( 6 % ) |
| Total DSP Blocks | 16 / 112 ( 14 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`S7-20-s2.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | -0.932 | -9.409 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.426 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 16.599 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.339 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.594 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | -1.655 | -20.449 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.356 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 16.818 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.145 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.563 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 9.433 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.179 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 17.908 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.778 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.946 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 10.675 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.127 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 18.325 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.591 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.945 | 0.000 |

- Worst setup slack: **-1.655 ns** (Slow 1100mV -40C Model Setup 'clk_i')  **NEGATIVE: timing not met**
- Worst hold slack: **0.127 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`S7-20-s2.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 47.77 MHz | 47.77 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 46.18 MHz | 46.18 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 3
- Warnings: 19
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

