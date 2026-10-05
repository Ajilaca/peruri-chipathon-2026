# ADR 0009: Phase 4 final decision: L = 8, P = 6 (C3-P6) and a 30% ALM design budget for the NTT core

- Status: Accepted
- Date: 2026-10-01
- Decided by: Faza Dzil, Team J5

## Context
- ADR 0004 (Accepted 2026-09-29) set an ALM budget of 25% of the device (10,478 ALM) for the lane-count selection.
  The review of 2026-10-01 found that 25% was a self-chosen design budget, not a documented requirement: the
  number entered as an example ("misal 25%") in the question that produced ADR 0004, and no estimate of the rest
  of the fabric content existed at the time.
- ADR 0007 (Accepted) fixed the Phase 4 candidate depths, the candidate conditions (with "ALM <= 10,478") and the
  selection rule. ADR 0008 (Proposed, never accepted) applied that rule with the 25% budget and proposed P = 4.
- Evidence gathered after ADR 0008 (all in `evidence/phase04/`, MEASURED unless marked):
  - seed sweep, seeds 1–6 (`seed_sweep.md`): P = 6 uses 10,484–10,516 ALM and is over 10,478 at every
    seed; P = 4 uses 10,439–10,503 ALM and is within 10,478 at 4 of 6 seeds; all 12 compiles meet 40.000 ns;
    lowest-slow-corner Fmax P = 4 30.60–33.00 MHz, P = 6 32.60–34.20 MHz;
  - DE10-Nano GHRD shell alone (`ghrd_shell_measured.md`): 1,304–1,309 ALM, 35 M10K, 0 DSP; the HPS
    hard block uses 0 fabric ALM;
  - GHRD + C3-P4 in one compile (`ghrd_plus_c3p4_integration.md`): 12,754 ALM; integration delta +18 ALM
    against the standalone parts compiled with the same settings; 40.000 ns met; packing difficulty Low; peak
    interconnect 48.2 %. This is integration evidence with P = 4 as baseline; P = 6 + GHRD was not compiled.
  - fabric-content draft (`fabric_estimate_DRAFT.md`, ESTIMATE, low confidence).

## Options considered
1. Keep 25% and accept ADR 0008 (P = 4). P = 4 is within budget at only 4 of 6 seeds; the P = 4 / P = 6 split rests
   on a few tens of ALM, within fitter noise.
2. Raise the NTT-core design budget to 30% (12,573 ALM) and select by the ADR 0007 rule. Both P = 4 and P = 6
   are within budget at every measured seed (margin ≥ 2,057 ALM).
3. Larger budgets (35–40%). No additional P becomes a candidate; only the headroom for later phases changes, and no
   estimate supports a specific larger number.

## Decision
1. Design budget: 30% of the device's ALMs for the NTT core = 12,573 ALM (41,910 × 0.30, fitter denominator),
   using the fitter's "Logic utilization (ALMs needed)" figure as in Phase 4. This replaces the 25% value of ADR 0004
   for the NTT core from Phase 4 onward. It is a design budget for the NTT core, not a limit for the final
   system, and it does not state that the remaining 70% is sufficient for the rest of ML-KEM.
2. Selected configuration: L = 8 lanes, pipeline depth P = 6, implementation C3-P6
   (`rtl/ntt/ntt_core_c3_p6.sv`, Quartus revision `C3-P6`). Phase 5 starts from C3-P6.
3. Timing targets unchanged (ADR 0006): Phase 4 milestone 40.000 ns (25 MHz, experimental target, met by C3-P6);
   Phase 5 target 20.000 ns (50 MHz, not yet met).

Check against the ADR 0007 rule with the 30% budget (perhitungan tim from `selection_worksheet.md` and
`seed_sweep.md`): at the default seed the candidates are {4, 6}; t_NTT(6) = 3.481 µs is the minimum and
d(4) = 0.051 > 0.05, so the rule selects P = 6. Stated plainly: across seeds 1–6 the same rule selects P = 6 at
seeds 1, 4, 5 and P = 4 at seeds 2, 3, 6 (the two are near the 5% tie line). The team's choice of P = 6 is
consistent with the rule at the default seed used for all measured revisions; it is not claimed to be seed-independent.

## Relation to earlier ADRs (nothing rewritten)
- ADR 0004: its 25% value is superseded for the NTT core from Phase 4 on by this ADR; ADR 0004's text and the
  Phase 3 decisions taken under it (ADR 0005, L = 8) stay as recorded.
- ADR 0007: rule, candidate set and conditions unchanged except that condition 3 now reads "ALM <= 12,573".
- ADR 0008: Proposed, not accepted; superseded by this ADR. Its measurements remain valid evidence.
- ADR 0006: unchanged.

## Consequences
- C3-P6 measured margin to 12,573 ALM: 2,057–2,089 ALM (seeds 1–6).
- System-level resources are not settled: P = 6 + GHRD has not been compiled; Keccak, samplers, the KEM controller,
  encode/compress, storage, bridge and SignalTap are not measured. The integration figures above use P = 4.
- Compile settings matter: the GHRD's global settings raised C3-P4 from 10,439 to 11,432 ALM (MEASURED). Under those
  settings C3-P6 has not been measured; a system build may need its own budget check.
- Phase 5 (arithmetic) must keep C3-P6 within 12,573 ALM or record a new decision.

## Evidence
- `evidence/phase04/selection_worksheet.md`, `seed_sweep.md`,
  `quartus_C3-P6.md`, `seed_sweep/quartus_C3-P6-s{2..6}.md`
- `evidence/phase04/ghrd_shell_measured.md`, `quartus_GHRD-de10-nano-base.md`,
  `ghrd_plus_c3p4_integration.md`, `fabric_estimate_DRAFT.md`
- `docs/decisions/0004-*.md`, `0006-*.md`, `0007-*.md`, `0008-*.md`; `docs/results/phase04.md`
