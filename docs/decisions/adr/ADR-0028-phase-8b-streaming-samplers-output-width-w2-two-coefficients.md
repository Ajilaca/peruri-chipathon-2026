# ADR 0028: Phase 8b: streaming samplers, output width W2 (two coefficients per cycle) chosen by the rule over W1; result

- Status: Accepted
- Date: 2026-10-03
- Decided by: Jo, Team J5, chat 2026-10-03: 'ya terima' (reply to the proposal to accept C5, W2, STREAM and OVERLAP because all were adopted by their rules and are measured) (header was 'Proposed / pending team decision')

## Context
- ADR 0026 (Accepted) sends sub-step 8b ahead: samplers that take the Keccak stream straight into SampleNTT and CBD with no store in between. Chat 2026-10-03 (no name given) asked for two output widths, tested one after the other: W1 (one coefficient per cycle), then W2 (two per cycle), then the choice.
- The test plan with the acceptance gate (section 4) and the W1-versus-W2 rule (section 5) was written and committed before any RTL and any measurement: `evidence/phase08/8b/test_plan_8b.md` (Amendment A1 records the changes made after the first runs: the permutation-counter criterion and the formal controls).
- The C5 sponge (ADR 0027, Proposed; PENDING #29 open) is the core of the measured top; the wrapper also takes the K0 sponge through a parameter and both were simulated.

## Options considered
(a) W1, one coefficient per cycle: the simplest interface; floor of 256 cycles per polynomial.
(b) W2, two coefficients per cycle: a pool of up to three candidates with one carried coefficient; 128 cycles per CBD polynomial, about one cycle per triple for SampleNTT.
(c) neither (keep a buffered sampler): not built; the gate needs M10K = 0, which the buffered design cannot meet by construction.

## Decision
Not taken by the team. The rule fixed before measuring gives: both widths pass the gate and W2 is chosen (it passes the gate and t = cycles / median Fmax is lower than W1's for SampleNTT and for CBD). The team accepts or rejects W2 as the 8b sampler; until then W2 is the default for 8c and 8d (the plan of 8c names it).

## Consequences
- 8c and 8d use the sampler with `OUTW` = 2. W1 stays in the same files (`OUTW` = 1, verified again after W2 was added).
- Sampling time per polynomial is MEASURED in simulation: SampleNTT 206.48 cycles on average (194-231) and CBD 152 with the C5 sponge (W1: 305.23 and 280). With W2 the SampleNTT cycles equal the number of triples plus 49 (3 XOF blocks) or 61 (4 blocks) at every one of 500 polynomials.
- The permutation counter of the sponge can be one above the golden count when the sampler's byte window has already taken the last word of the final block while the output was held back (seen once in 500 K0 cases, W1): benign (the result is never read, the sponge is stopped and wiped); Amendment A1 of the plan.
- What this does not show: nothing on hardware; a sampler hidden behind other work is 8d; the two sponge cores are ADR 0027.

## Evidence
- `evidence/phase08/8b/selection_worksheet.md` (gate per width and the rule), `quartus_SM1*.md`, `quartus_SM2*.md` (MEASURED, kernel-only, seeds 1-6 each; seed 1 also at 20 ns and with the K0 sponge as information), `verify_W1.md`, `verify_W2.md`, `formal_W1.md`, `formal_W2.md`, `sampler_cycles_W1.md`, `sampler_cycles_W2.md`.
- MEASURED (Quartus, medians over seeds 1-6): W1 5,279 ALM, 1,913 registers, M10K 0, DSP 0, Fmax 51.220 MHz (50.10-55.79); W2 5,290 ALM, 1,947 registers, M10K 0, DSP 0, Fmax 50.220 MHz (48.46-53.42); timing met at 40 ns at every seed of both; the S10 median used by the gate is 44.320 MHz (Phase 6).
- ESTIMATE misses written before measuring (recorded in the plan): the ALM added by W2 was estimated at 100-300 and measured about +11 (median); the top is smaller than the 8a sponge alone (6,167 ALM) for reasons not investigated (INFERENCE: constant mode bits and the resynthesis of the second round differ between the two compiles); neither is a defect.
