# ADR 0013: Phase 5b choice: Barrett reducer selected by the ADR 0011 rule

- Status: Accepted
- Date: 2026-10-01
- Decided by: Jevan, Team J5 (chat 2026-10-02, answered the three ADR questions)

## Context
- `docs/ROADMAP.md` Phase 5b: Montgomery versus Barrett behind the same interface, both measured, "choice by ADR".
- ADR 0011 (Accepted) fixed the selection rule (D8) and the seeds (D7, seeds 1–6) before any 5b compile.
- Both candidates were built, verified and compiled (test plan `evidence/phase05/test_plan.md`, amendment A3):
  - correctness (MEASURED, both simulators): exhaustive reducer test 0 mismatches over all a, b in [0, q) for each;
    unit tests 40/40; core tests 22/22 incl. cycles exactly 119 / 375, Montgomery ROM check and negative controls;
    formal 9/9 as expected (`evidence/phase05/5b/verify.txt`, `formal.md`);
  - Quartus, 40.000 ns, Quartus defaults, seeds 1–6 (MEASURED, `evidence/phase05/5b/quartus_C4b-*.md`),
    rule applied by `scripts/quartus/phase5_select_5b.py` (`evidence/phase05/5b/selection_worksheet.md`):

| Candidate | Qualifies at all 6 seeds | ALM median (min–max) | Fmax median, lowest slow corner (min–max) | DSP | t_NTT at median Fmax |
|---|---|---:|---:|---:|---:|
| Barrett (C4b-B) | yes | 9,171.0 (9,166–9,208) | 34.515 MHz (33.46–34.84) | 18 / 112 | 3.448 µs |
| Montgomery (C4b-M) | yes | 9,286.5 (9,249–9,297) | 33.780 MHz (32.81–34.25) | 9 / 112 | 3.523 µs |

## Options considered
1. Accept the rule result: Barrett. Rule steps (ADR 0011 D8): both qualify; Barrett has the higher median Fmax and
   Montgomery is 2.13 % lower, a near tie (≤ 5 %); in a near tie the lower median ALM wins; the ALM medians differ by
   115.5 ALM (≥ 32), so the rule selects Barrett without a team tie-break.
2. Override the rule in favour of Montgomery because of DSP use (9 instead of 18). ADR 0011 D2 sets no DSP limit, so
   the rule does not weigh DSP; an override would be a team decision with its own reason.

## Decision
*(Accepted 2026-10-02 by Jevan, Team J5: Barrett, as selected by the rule; the DSP cost below was shown before the choice.)* Barrett (`rtl/arith/modmul_barrett.sv`, RED_KIND 2, revision C4b-B)
is the Phase 5b choice, as selected by the ADR 0011 rule.

Recorded explicitly: DSP use doubles from 9 to 18 (of 112, fitter denominator). Per entity (MEASURED, seed 1,
`quartus/phase05_arith_c4/output_files_C4b-B/C4b-B.fit.rpt`): each of the nine Barrett reducers uses 2 DSP blocks
and 20.5–26.5 ALM, 225.3 ALM in total (INFERENCE: the second DSP holds the quotient estimate x·5039, the only
multiplication besides a·b that the RTL leaves to the tool); Montgomery uses 1 DSP and 37.7–42.1 ALM each (352.0 ALM in total; its q' multiplication is shift-and-add).
C3-P6 and C4a use 9 DSP.

## Consequences
- The C4 configuration carried into 5c / 5d and into the 20.000 ns information compile (ADR 0011 D1) is C4b-B,
  unless the team rejects this ADR.
- DSP: 18 of 112 for the NTT core (MEASURED). No DSP budget exists; Keccak, samplers and other blocks are NOT MEASURED,
  so whether DSPs become scarce later is unknown. If a DSP limit is set later, Montgomery (9 DSP, +115.5 ALM median)
  is the measured alternative, or Barrett with x·5039 written as shift-and-add (not built, NOT MEASURED).
- Montgomery files (`modmul_montgomery.sv`, `twiddle_rom_mont.sv`, generator, ROM check) stay in the repository as the
  measured candidate.
- Compared with C3-P6 (INFERENCE): median ALM 9,171 vs 10,484–10,516 (about −1,330); median Fmax 34.515 MHz vs
  C3-P6's seed range 32.60–34.20 MHz (median 33.11, `evidence/phase04/seed_sweep.md`). The
  critical path stays in the memory read path (`5b/C4b-B_top300_path_classes_slow100.txt`); 50 MHz is not reached
  (ADR 0010).

## Evidence
- `evidence/phase05/5b/selection_worksheet.md`, `verification_status.json`,
  `verify.txt`, `formal.md`, `quartus_C4b-{B,M}[-s2..s6].md`,
  `C4b-{B,M}_top300_path_classes_slow100.txt`, `c4b_segments_slow100.txt`
- `docs/decisions/adr/ADR-0011-phase-5-plan-decisions-d1-d8-and-the-5b-selection-rule.md`
- `evidence/phase05/test_plan.md` (amendment A3)
