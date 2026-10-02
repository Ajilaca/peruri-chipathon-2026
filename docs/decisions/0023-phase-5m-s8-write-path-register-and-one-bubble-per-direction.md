# ADR 0023: Phase 5M S8: write-path register and one bubble per direction (P = 8) - rule result

- Status: Proposed
- Date: 2026-10-03
- Decided by: pending team decision

## Context
- ADR 0017 step S8 (lever 4: register in the write path, P 7 -> 8, one data-independent stall per transform, 20 ns information compile); ADR 0019 amendment note 2 (S7 and S8 before Phase 7); base S7 (ADR 0021 Proposed;
  S8 was started on that base by the team's working instruction of 2026-10-02/03). Test plan and rule: `docs/evidence/phase05m-memsched/test_plan_s8.md` (commit 01c8fb1, before any S8 simulation or compile).
- New files only (`rtl/ntt/ntt_core_s8.sv`, `ntt_core_s8_p8.sv`); the memory file of S7 is reused with `WR_DELAY = WrDly + WR_REG`. Bubble: NTT after layer 3, INTT after layer 2 (position depends on mode and layer only).

## Options considered
(a) Adopt S8 as the final Phase 5M core. (b) Keep S7 (P = 7, 120 / 120 cycles) as the configuration for Phase 6 and 7; S8 stays a measured experiment. (c) Keep M6 or another base.

## Decision
Result of the pre-fixed rule (`scripts/phase5m_select_s8.py`, no tolerance): **S8 is NOT adopted by the rule**: conditions 1-3 pass; condition 4 fails (t = 122 / 37.990 = 3.211 us versus S7's 120 / 38.720 = 3.099 us;
S8 needed a median Fmax above 39.365 MHz). The choice of the configuration for later phases is the team's (C5): this record stays Proposed. Suggestion (not a decision): (b).

## Consequences
- MEASURED (Quartus, seeds 1-6, 40.000 ns; `docs/evidence/phase05m-memsched/s8/selection_worksheet_2026-10-03.md`): ALM 9,402-9,471 (median 9,443.5; S7 9,391.0), registers 4,130-4,144 (S7 4,296-4,324), M10K 33, DSP 16,
  timing met at every seed, Fmax median 37.990 MHz (36.76-40.22) versus S7 38.720 (37.89-40.29); cycles NTT = INTT = 122 (simulation, as predicted: 113 + 8 + 1).
- INFERENCE: the median difference (0.73 MHz, -1.9 %) is inside the seed spread of both steps (S7 2.40 MHz, S8 3.46 MHz), so S8 is "not better", not "measurably worse"; with two more cycles (+1.7 %) it loses the rule either way.
  Hypothesis, not analysed: after S7 the write segment is no longer the limiting path, so one more register adds cycles without shortening the worst path. The register count went down although 192 bits were added: not attributed.
- 20 ns information compile (MEASURED, `s8/quartus_S8-20_20261002.md`): 9,443 ALM, setup -2.242 ns (Slow -40C), Fmax 44.96 MHz, timing not met; critical warnings 15725 and 332148 x2 triaged as in earlier phases, nothing waived.
- Verification (MEASURED): V1-V4 and V6 on Verilator and Icarus (12/12 each), negative controls NC-B (no bubble) and NC-W (write control not delayed) fail as required, formal H, O, R, A, B, C PASS with NC-O and NC-A failing (3/3),
  and the one full regression on the final tree (Amendment A1): Phase 0-5, S6, S7 all OVERALL PASS, 95 files added, 2 documents modified since 288a78c (`s8/regression_2026-10-03.md`).
- Not covered: hardware, path analysis after S7 or S8, other seeds or constraints.

## Evidence
- `docs/evidence/phase05m-memsched/test_plan_s8.md`, `s8/verify_2026-10-03.md`, `s8/formal_2026-10-03.md`, `s8/regression_2026-10-03.md`, `s8/verification_status.json`, `s8/selection_worksheet_2026-10-03.md`,
  `s8/quartus_S8[-s2..s6]_20261002.md`, `s8/quartus_S8-20_20261002.md`, `s7/quartus_S7[-s2..s6]_20261002.md` (baseline), `scripts/phase5m_select_s8.py`.
