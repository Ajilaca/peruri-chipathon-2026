# ADR 0021: Phase 5M S7: split memory read path (RD_SPLIT, P = 7) - rule result and base for S8

- Status: Superseded by 0025
- Date: 2026-10-02
- Decided by: not accepted as the configuration; superseded by ADR 0025 (Jevan, Team J5, chat 2026-10-03: 'kan udah di adaptasi dan kita menggambil s10'; header was 'Proposed / pending team decision')

## Context
- ADR 0017 step S7 (lever 1 of the decision package: one register stage inside the memory read, P 6 -> 7, no stall, +1 cycle); ADR 0019 amendment note 2 (S7 and S8 planned
  before Phase 7); ADR 0020 (M6 is the base). Test plan and adoption rule were written and committed before any S7 RTL and before any S7 measurement
  (`evidence/phase05m/test_plan_s7.md`, commit f39b074).
- The S7 change is new files only (`rtl/mem/poly_mem_multiport_split.sv`, `rtl/ntt/ntt_core_s7.sv`, `ntt_core_s7_p7.sv`); no existing file was modified.

## Options considered
(a) Adopt S7 as the base for S8 and for the later phases (the rule below says it passes).
(b) Keep M6 (P = 6) as the NTT/INTT configuration and treat S7 as a measured experiment.
(c) Another base chosen by the team.

## Decision
Result of the pre-fixed rule (`scripts/quartus/phase5m_select_s7.py`, no tolerance): S7 is adopted by the rule (all four conditions PASS). Whether the team accepts it as the
configuration is not decided here (C5): status stays Proposed. For schedule reasons the S8 work was started on the S7 base (S8 is defined as lever 4 on top of the split read, ADR 0017
table) following the team's working instruction of 2026-10-02 (chat: "kerjakan sesuai dengan agenda hari ini ... s7-s8 selesai"); if the team picks (b) or (c), S8's verdict is
then read as a measured experiment on S7.

## Consequences
- MEASURED (Quartus, seeds 1-6, 40.000 ns; `evidence/phase05m/s7/selection_worksheet.md`): ALM 9,361-9,405 (median 9,391.0; M6 median 9,421.5), registers 4,296-4,324,
  M10K 31 (M6 29), DSP 16, timing met at every seed, Fmax median 38.720 MHz (37.89-40.29) versus M6 34.430 MHz (32.35-35.04); cycles NTT = INTT = 120 (simulation).
- INFERENCE (perhitungan tim): t_NTT = t_INTT = 120 / 38.720 = 3.099 us versus M6 3.456 us (-10.3 %). The lowest S7 seed (37.89 MHz) is above the highest M6 seed (35.04 MHz), so
  the Fmax gain is larger than the seed spread seen so far (S7 spread 2.40 MHz). Worst setup slack at 40 ns rose to 13.6-15.2 ns (M6 about 11 ns in C4b-B terms).
- The threshold printed in the test plan (34.720 MHz) is the rounded value of 120 x 34.430 / 119 = 34.7193; the rounding has no effect on the verdict.
- The gain was not predicted to this size in the plan's ESTIMATE (about 40 MHz for a worst path of 25 ns; measured median 38.7 MHz is inside that bound).
- ALM did not rise (median -30 versus M6, inside the seed spread of 44 ALM, INFERENCE) although about 270 registers were added; M10K rose from 29 to 31 (tool-inferred, not analysed).
- Not covered: hardware, other seeds or constraints, path analysis after S7 (the new critical path was not examined; it is the input of S8's expectation only as a hypothesis), the Phase 0-5
  regression (runs once at S8, Amendment A1).
- Verification (MEASURED): V1-V6 PASS on Verilator and Icarus (`s7/verify.md`), formal H, O, R, A, B, C PASS with NC-O and NC-A failing (`s7/formal.md`); negative controls
  NCD (write control one cycle short) and NCS (output select not delayed) fail as required; RD_SPLIT = 0 equals the frozen memory cycle by cycle (V3). The cocotb Verilator builds print
  `WIDTHEXPAND` for the runner's 32-bit ARB_REG parameter value; the RTL lint (V1) is clean.

## Evidence
- `evidence/phase05m/test_plan_s7.md`, `s7/verify.md`, `s7/formal.md`, `s7/verification_status.json`, `s7/selection_worksheet.md`,
  `s7/quartus_S7[-s2..s6].md`, `s6/quartus_M6[-s2..s6].md` (baseline), `scripts/quartus/phase5m_select_s7.py`.

## Amendment note 1 (2026-10-03, Jevan, Team J5)
Consequence of ADR 0025 (Accepted 2026-10-03, Jevan, Team J5, chat 2026-10-03: 'kan udah di adaptasi dan kita menggambil s10'): S10 is the NTT/INTT core for the following phases. S7 is not used as the configuration; it stays on record as the measured base of S8 and as the baseline of the S10 comparison (`evidence/phase06/s10/selection_worksheet.md`).
The rule result and the measurements above are unchanged.
