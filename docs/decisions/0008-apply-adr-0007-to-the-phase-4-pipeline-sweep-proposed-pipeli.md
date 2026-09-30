# ADR 0008: Apply ADR 0007 to the Phase 4 pipeline sweep: proposed pipeline depth P

- Status: Proposed
- Date: 2026-09-30
- Decided by: (pending: Team J5; not decided by the assistant)

## Context
ADR 0007 fixed, before anything was measured, the candidate depths P in {0, 2, 4, 6}, the four candidate
conditions (bit-exact PASS, constant-cycle PASS, ALM <= 10,478, timing met at 40.000 ns at every reported
corner) and the selection rule (Fmax(P) = lowest slow-corner Fmax; t_NTT = cycles_NTT / Fmax; smallest P
within 5% of the minimum t_NTT). ADR 0006 fixed the constraint (40.000 ns, an experimental milestone target,
not a hardware or system requirement). All four revisions were then compiled with one SDC and the default
seed (`quartus/phase04_pipeline_c3/`), and the rule was applied by `scripts/phase4_select_p.py`, which reads
the evidence files (`docs/evidence/phase04-pipeline/selection_worksheet_2026-09-30.md`).

## Options considered
Measured results (MEASURED, `docs/evidence/phase04-pipeline/quartus_C3-P<n>_20260930.md`; cycles from
simulation, `cocotb_regression_2026-09-30.txt`):

| P | ALM (of 41,910) | <= 10,478? | Worst setup / hold slack @ 40.000 ns | Timing met? | Fmax(P), lowest slow corner (MHz) | NTT / INTT cycles | t_NTT / t_INTT (us) | Candidate? |
|---|---|---|---|---|---|---|---|---|
| 0 | 9,723 | yes | -90.653 / 0.207 | no | 7.65 | 113 / 369 | 14.771 / 48.235 | no |
| 2 | 9,696 | yes | -0.368 / 0.174 | no (slow -40C corner; slow 100C is +0.061) | 24.77 | 115 / 371 | 4.643 / 14.978 | no |
| 4 | 10,439 | yes (39 below) | 8.734 / 0.157 | yes | 31.98 | 117 / 373 | 3.659 / 11.664 | yes |
| 6 | 10,505 | **no (27 over)** | 10.753 / 0.140 | yes | 34.19 | 119 / 375 | 3.481 / 10.968 | no (ALM) |

Registers 3,097 / 3,817 / 4,145 / 4,168, DSP 9 / 112 in all four, M10K 0 / 16 / 26 / 29 of 553.
Candidate set C = {4}; t_min = t_NTT(4); the rule yields **P_selected = 4**. P = 6 would have the lowest
t_NTT of all (3.481 us, 4.9% below P = 4; equivalently P = 4 is 5.1% above P = 6) but is excluded by the ALM condition by 27 ALM.

## Decision
**Not decided.** The rule of ADR 0007, applied as written, gives P = 4. This record is Proposed until the
team accepts it, changes it, or asks for more measurement. Nothing else in the repository treats P = 4 as
selected.

## Consequences
Points the team should weigh before accepting (stated, not resolved here):
- **Margins are thinner than the swing of the tool.** P = 4 is 39 ALM under the budget and P = 6 is 27 ALM
  over it. Fitter packing has varied by up to ~370 ALM between compiles of identical logic (Phase 3,
  no seed sweep run). With the default seed the rule is unambiguous, but a different seed could move P = 4
  over, or P = 6 under, the budget. A fitter seed sweep on P = 4 and P = 6 would quantify this; it was not
  run because ADR 0007 and the test plan fix the default seed for all four revisions.
- **A tool effect changed the resource picture, not only the pipeline.** With registers in the memory path
  Quartus inferred `bank_map_rom` and some register chains (`altshift_taps`) into M10K blocks (16 / 26 / 29
  blocks; 0 for P = 0). This is why P = 2 uses fewer ALM than P = 0 despite ~700 more registers. It was not
  designed or requested (M10K mapping is out of scope for Phase 4) and is reported as observed; a different
  inference in a later phase would change the ALM figures.
- **The 5% near-tie is on t_NTT only, and it is close.** P = 6 is excluded by the ALM condition, so the near-tie
  rule is not exercised. Were the ALM condition relaxed, C would be {4, 6}, t_min = t_NTT(6) = 3.481 us and
  d(4) = 0.051 > 0.05, so the rule would then select P = 6, not P = 4. The selection therefore depends on a
  27-ALM difference; this is the strongest reason to consider the seed sweep above.
- 40.000 ns is met by P = 4 and P = 6 per Quartus static timing analysis only; no board run exists
  and none is claimed. Fmax figures are kernel-only with virtual pins.
- The P = 2 miss is small (-0.368 ns at one corner) and was measured as it stands; no exception was added.
- If accepted, Phase 5 starts from C3-P4 and its 20.000 ns end goal (ADR 0006) is a separate check:
  Fmax 31.98 MHz does not reach 50 MHz.

## Evidence
- `docs/evidence/phase04-pipeline/selection_worksheet_2026-09-30.md`, `scripts/phase4_select_p.py`,
  `docs/evidence/phase04-pipeline/verification_status.json`
- `docs/evidence/phase04-pipeline/quartus_C3-P0_20260930.md`, `quartus_C3-P2_20260930.md`,
  `quartus_C3-P4_20260930.md`, `quartus_C3-P6_20260930.md`
- `docs/evidence/phase04-pipeline/cocotb_regression_2026-09-30.txt`,
  `docs/evidence/phase04-pipeline/v2_modmul_staged_exhaustive_2026-09-30.txt`,
  `docs/evidence/phase04-pipeline/formal_2026-09-30.md`, `docs/evidence/phase04-pipeline/regression_2026-09-30.txt`
- `docs/decisions/0006-phase-4-target-clock.md`, `docs/decisions/0007-phase-4-pipeline-depth-p-and-selection-criterion.md`,
  `docs/decisions/0004-phase-3-lane-count-l-selection-criterion.md`
