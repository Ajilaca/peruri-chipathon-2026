# MEASURED — Quartus results for revision `C4b-B-20`

- Generated: 2026-10-01 17:04 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `quartus/phase05_arith_c4/output_files_C4b-B-20`
- Note: Phase 5 closure, INFORMATION compile (ADR 0011 D1): final C4 configuration C4b-B (Barrett, ntt_core_c4b_b) at 20.000 ns (quartus/phase05_arith_c4/C4-20.sdc); Quartus defaults; default seed 1; RTL = git b418d1e plus docs; not a Phase 5 gate (ADR 0010)

## Fitter (`C4b-B-20.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Fri Oct  2 00:00:10 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | C4b-B-20 |
| Top-level Entity Name | ntt_core_c4b_b |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 9,305 / 41,910 ( 22 % ) |
| Total registers | 4272 |
| Total pins | 0 / 314 ( 0 % ) |
| Total block memory bits | 30,314 / 5,662,720 ( < 1 % ) |
| Total RAM Blocks | 29 / 553 ( 5 % ) |
| Total DSP Blocks | 18 / 112 ( 16 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 0 / 4 ( 0 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`C4b-B-20.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | -2.557 | -461.653 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.424 | 0.000 |
| Slow 1100mV 100C Model Recovery 'clk_i' | 17.094 | 0.000 |
| Slow 1100mV 100C Model Removal 'clk_i' | 0.867 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.606 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | -2.438 | -442.383 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.336 | 0.000 |
| Slow 1100mV -40C Model Recovery 'clk_i' | 17.282 | 0.000 |
| Slow 1100mV -40C Model Removal 'clk_i' | 0.709 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.599 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | 8.087 | 0.000 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.180 | 0.000 |
| Fast 1100mV 100C Model Recovery 'clk_i' | 18.307 | 0.000 |
| Fast 1100mV 100C Model Removal 'clk_i' | 0.514 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 8.950 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | 9.877 | 0.000 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.151 | 0.000 |
| Fast 1100mV -40C Model Recovery 'clk_i' | 18.607 | 0.000 |
| Fast 1100mV -40C Model Removal 'clk_i' | 0.344 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 8.946 | 0.000 |

- Worst setup slack: **-2.557 ns** (Slow 1100mV 100C Model Setup 'clk_i')  **NEGATIVE: timing not met**
- Worst hold slack: **0.151 ns** (Fast 1100mV -40C Model Hold 'clk_i')

## Fmax (`C4b-B-20.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 44.33 MHz | 44.33 MHz | clk_i |  |
| Slow 1100mV -40C Model Fmax Summary | 44.57 MHz | 44.57 MHz | clk_i |  |

## Compile log message counts

- Critical warnings: 3
- Warnings: 20
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

