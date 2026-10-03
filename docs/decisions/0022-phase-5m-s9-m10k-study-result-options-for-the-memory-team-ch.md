# ADR 0022: Phase 5M S9: M10K study result, options for the memory (team choice)

- Status: Superseded by 0025
- Date: 2026-10-03
- Decided by: option (A) built as S10 and accepted in ADR 0025 (Jevan, Team J5, chat 2026-10-03: 'kan udah di adaptasi dan kita menggambil s10'; header was 'Proposed / pending team decision')

## Context
- ADR 0017 defines S9 as a documentation-only study with no adoption rule ("the team chooses"); ADR 0019 had dropped it for the deadline; the team asked for it in chat on 2026-10-03
  ("s9 sekalian dikerjain", recorded in ADR 0019 amendment note 3). Plan: `docs/evidence/phase05m-memsched/test_plan_s9.md` (written before the analysis script).
- The measured limit of the core is the memory read path (ADR 0010; S7 confirmed it: median Fmax 34.430 -> 38.720 MHz with one register in the read). Storage is flip-flops (no M10K).

## Options considered
(A) 16 x 1R1W banks with the map `bank = (a1^a2^a3^a4, a7, a6, a5)`, `offset = a[3:0]`, one M10K per bank, crossbars, no slot arbitration (new step, "S10").
(B) two coefficients per word (not useful: one layer per direction benefits); (C) double-pumping (needs a second clock domain and the M10K maximum frequency, NOT VERIFIED); (D) fewer lanes (cycles double);
(E) keep the flip-flop memory of S7 and continue with Phase 6 / 7.

## Decision
None made here (C5). Suggestion (not a decision): (E) now; open (A) as its own step after the deadline-critical blocks (Keccak, samplers), with a test plan and the ADR 0012 rule.

## Consequences
- MEASURED by the model of the real address schedule (`docs/evidence/phase05m-memsched/s9/port_analysis_2026-10-03.txt`): the current 8-bank map needs 2 reads + 2 writes per bank in some cycles, which does not fit one
  true-dual-port M10K per bank (device mode facts not re-verified here); the 16-bank map above needs exactly 1 read + 1 write per bank per cycle over the whole timeline of both directions, bijective and balanced;
  the first hand-derived map was wrong and was refuted by the script (test plan Amendment A1); two negative controls conflict as required.
- ESTIMATE (method in the study): option A uses 16 M10K (2.9 % of 553), removes about 3,000 storage flip-flops, adds crossbars of at most about 1,920 ALM (upper bound by LUT counting, not measured); Fmax effect NOT MEASURED.
- Nothing in RTL, tests or proofs changed by S9; no regression needed for it.
- Open before any RTL: M10K read-during-write mode, synchronous-read latency, Cyclone V Device Handbook check, crossbar ROM, new formal bank property.

## Evidence
- `docs/evidence/phase05m-memsched/test_plan_s9.md`, `s9/study_m10k_2026-10-03.md`, `s9/port_analysis_2026-10-03.txt`, `scripts/phase5m_s9_port_analysis.py`.

## Amendment note 1 (2026-10-03, Jevan, Team J5)
Consequence of ADR 0025 (Accepted 2026-10-03, Jevan, Team J5, chat 2026-10-03: 'kan udah di adaptasi dan kita menggambil s10'): S10 is the NTT/INTT core for the following phases. Option (A) of this study was built and measured as S10 (ADR 0024 order, ADR 0025 result). The study's crossbar ESTIMATE was too low (measured memory entity 3,343 ALM,
`docs/evidence/phase06-scheduling/s10/resource_breakdown_2026-10-03.md`). The study text above is unchanged.
