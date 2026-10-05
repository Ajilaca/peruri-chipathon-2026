# MEASURED — Quartus results for revision `S7-s2`

- Generated: 2026-10-02 15:18 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase05m_memsched/output_files_S7-s2`
- Note: Phase 5M step S7 candidate: rtl/ntt/ntt_core_s7_p7.sv (M6 plus memory read path split RD_SPLIT = 1, P = 7; ADR 0017/0019/0020, test plan evidence/phase05m/test_plan_s7.md); constraint 40.000 ns (quartus/phase05m_memsched/M.sdc); Quartus defaults; git b53309d

## Fitter (`S7-s2.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Fri Oct  2 21:53:45 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | S7-s2 |
| Top-level Entity Name | ntt_core_s7_p7 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,388 / 41,910 ( 22 % ) |
| Total registers | 4317 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,423 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 31 / 553 ( 6 % ) |
| Total DSP Blocks | 16 / 112 ( 14 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`S7-s2.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 14.804 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.419 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 36.662 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.181 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.602 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 13.906 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.374 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 36.885 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 1.005 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.577 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 27.655 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.182 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 37.995 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.742 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.950 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 28.977 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.118 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.360 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.546 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.947 | 0.000 |

- Worst setup slack: **13.906 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.118 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`S7-s2.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 39.69 MHz | 39.69 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 38.32 MHz | 38.32 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 19
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

