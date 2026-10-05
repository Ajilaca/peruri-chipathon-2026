# MEASURED - Quartus results for revision `S8-s6`

- Generated: 2026-10-02 17:38 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase05m_memsched/output_files_S8-s6`
- Note: Phase 5M step S8 candidate: rtl/ntt/ntt_core_s8_p8.sv (S7 plus write-path register WR_REG = 1, P = 8, one bubble per direction; ADR 0017/0019/0020/0021, test plan evidence/phase05m/test_plan_s8.md); constraint 40.000 ns (quartus/phase05m_memsched/M.sdc); Quartus defaults; git 300aaf3

## Fitter (`S8-s6.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Fri Oct  2 22:50:51 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | S8-s6 |
| Top-level Entity Name | ntt_core_s8_p8 |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,419 / 41,910 ( 22 % ) |
| Total registers | 4130 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,942 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 33 / 553 ( 6 % ) |
| Total DSP Blocks | 16 / 112 ( 14 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`S8-s6.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | 14.137 | 0.000 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.453 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 36.034 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 1.058 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.585 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | 13.593 | 0.000 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.376 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 36.281 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.884 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.541 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 26.837 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.185 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 37.590 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.624 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 18.908 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 28.413 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.152 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 38.044 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.440 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 18.909 | 0.000 |

- Worst setup slack: **13.593 ns** (Slow 1100mV -40C Model Setup 'clk_i')
- Worst hold slack: **0.152 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`S8-s6.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 38.67 MHz | 38.67 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 37.87 MHz | 37.87 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 1
- Warnings: 20
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

