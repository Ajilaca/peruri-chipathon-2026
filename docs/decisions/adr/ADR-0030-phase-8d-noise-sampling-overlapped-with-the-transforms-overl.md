# ADR 0030: Phase 8d: noise sampling overlapped with the transforms (OVERLAP) adopted by the rule over STREAM; result

- Status: Accepted
- Date: 2026-10-03
- Decided by: Jo, Team J5, chat 2026-10-03: 'ya terima' (reply to the proposal to accept C5, W2, STREAM and OVERLAP because all were adopted by their rules and are measured) (header was 'Proposed / pending team decision')

## Context
- ADR 0026 (Accepted) sends sub-step 8d ahead: overlap of the sampler with the arithmetic. Chat 2026-10-03 (no name given): do 8b, 8c, 8d without stopping.
- Test plan and rule: `evidence/phase08/8d/test_plan_8d.md` (written before the RTL paths were exercised and before any 8d measurement; Amendment A1 records the findings). Baseline: STREAM (ADR 0029 Proposed). The change: a noise polynomial is sampled non-blocking while a transform computes, its beats are written when the store write port is free, and the sequencer has priority on that port (`OVERLAP` = 1, program set OVERLAP).
- The matrix is still streamed (`PWMS` needs the sampler), so matrix and noise sampling are sequential: one sampler.

## Options considered
(a) STREAM as it is: simpler control; the sampler idles while the NTT core runs.
(b) OVERLAP: five of six (KeyGen) and six of seven (Encrypt) noise polynomials hidden behind transforms.
(c) A second sampler (to hide the matrix too): not built; cost not estimated.

## Decision
Not taken by the team. The rule fixed before measuring gives: **OVERLAP adopted** (all four conditions hold). The team accepts or rejects it.

## Consequences
- Bit-exact against the model and the unmodified golden K-PKE on both simulators, in the OVERLAP programs and in the test-only STRESS program (a noise sample collides with an ADD pass; 763 sampler-beat cycles were held back by sequencer writes in the final run, so the arbitration was exercised; the NC-ARB control fails as required).
- MEASURED (simulation, mean over the same inputs): KeyGen 6,344.1 cycles (STREAM 7,089.1), Encrypt 7,654.6 (STREAM 8,548.6): 10.5 % and 10.5 % fewer ((7,089.1 - 6,344.1) / 7,089.1 and (8,548.6 - 7,654.6) / 8,548.6), against the ESTIMATE of about 11 %; Decrypt unchanged (3,109).
  MEASURED (Quartus, medians over seeds 1-6): OVERLAP 10,992.5 ALM (STREAM 10,995.5), 3,368-3,414 registers, 44 M10K (same), 26 DSP, Fmax 43.755 MHz (STREAM 43.355), timing met at 40 ns at every seed. t = cycles / Fmax: KeyGen 145.0 us against 163.5 us, Encrypt 174.9 against 197.2 (INFERENCE / perhitungan tim).
- Whole-program comparison with Phase 6 (arithmetic only, inputs given): KeyGen 5,475 -> 6,344 cycles with all sampling of the matrix and the noise included; Encrypt 6,789 -> 7,655; Decrypt 3,109 unchanged.
- Information at 20 ns (seed 1): OVERLAP met (setup +1.535 ns, 54.16 MHz); kernel-only.
- A finding of this step: a start of the sampler in the same cycle as the previous sample's `done` pulse cleared the PWMS marker (program hang), found only by the STRESS program; fixed (the done branch now comes before the start branch).
- Limits: the WAIT operations are a safety property of the schedule (the overlapped transform is longer than a noise sample, so ignoring them would not change the result); the static hazard checker of the golden model guards them. One sampler only. No hardware.

## Evidence
- `evidence/phase08/8d/selection_worksheet.md`, `quartus_SMP2*.md`, `formal.md`, `cycles_v2.json`, `cycles_v3_stress.json`, `evidence/phase08/8c/verify.md` (the single run that covers 8c and 8d), `test_plan_8d.md`.
