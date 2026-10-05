# ADR 0029: Phase 8c: matrix A streamed from the sampler into the PWM unit (STREAM) adopted by the rule over storing it (STORE); result

- Status: Accepted
- Date: 2026-10-03
- Decided by: Jo, Team J5, chat 2026-10-03: 'ya terima' (reply to the proposal to accept C5, W2, STREAM and OVERLAP because all were adopted by their rules and are measured) (header was 'Proposed / pending team decision')

## Context
- ADR 0026 (Accepted) sends sub-step 8c ahead: matrix A generated on the fly, not stored. Chat 2026-10-03 (no name given): do 8b, 8c, 8d without stopping.
- Test plan and adoption rule were written before the RTL and before any measurement: `evidence/phase08/8c/test_plan_8c.md` (committed together with the RTL; Amendment A1 lists what changed after the first runs). Both builds use the same sequencer, the same S10 core (ADR 0025 Proposed), the same 8b sampler (W2, ADR 0028 Proposed) and the C5 sponge (ADR 0027 Proposed).
- STORE is the baseline: the nine entries are sampled into slots 0-8 (blocking `SMPA`) and the Phase 6 PWM passes read them from the store (24 slots). STREAM: the sampler's beats feed the PWM unit directly (`PWMS`); the matrix slots do not exist (12 slots).

## Options considered
(a) STORE: fewer new hardware paths; nine polynomials stored.
(b) STREAM: no storage of A, the PWM pass runs at the speed of the sampler.
(c) Keep the Phase 6 interface with A written by the testbench: no sampler in the system (not a design).

## Decision
Not taken by the team. The rule fixed before measuring gives: **STREAM adopted** (all four conditions hold). The team accepts or rejects STREAM; 8d is built on it.

## Consequences
- Whole K-PKE programs with sampling are bit-exact against the golden model and the unmodified golden K-PKE (KeyGen, Encrypt, Decrypt) on both simulators; counters 6/0/9, 3/4/12, 3/1/3 plus 6 and 7 sampling operations; Decrypt is unchanged (3,109 cycles).
- MEASURED (simulation, mean over the same inputs): KeyGen 7,089.1 cycles (STORE 8,268.1), Encrypt 8,548.6 (STORE 9,727.6). MEASURED (Quartus, medians over seeds 1-6): STREAM 10,995.5 ALM, 3,377-3,395 registers, **44 M10K** (STORE 10,958 ALM, 3,342-3,378 registers, 55 M10K), 26 DSP both, Fmax 43.355 MHz (STORE 42.270), timing met at 40 ns at every seed of both.
  t = cycles / Fmax: KeyGen 163.5 us against 195.6 us, Encrypt 197.2 against 230.1 (INFERENCE / perhitungan tim: simulation cycles with the Fmax of a kernel-only compile).
- Eleven M10K blocks fewer (the store holds 12 slots instead of 24); the ESTIMATE written before measuring was 10-14 fewer blocks and about 15 % fewer cycles: both inside: 11 fewer blocks, 14.3 % fewer KeyGen cycles and 12.1 % fewer Encrypt cycles ((8,268.1 - 7,089.1) / 8,268.1 and (9,727.6 - 8,548.6) / 9,727.6).
- Information at 20 ns (seed 1): STREAM met (setup +1.783 ns, 54.89 MHz), STORE met (+0.992 ns, 52.61 MHz); kernel-only, not a system at 50 MHz.
- A finding: the valid tags of the PWMS pipeline had no reset (found by the first formal run, fixed); the sampler cores' constant `Q` was renamed `QC` for lint (8b evidence note).
- What this does not show: nothing on hardware; hashing of the keys and the whole KEM are not in the system; the seeds are written by the testbench.

## Evidence
- `evidence/phase08/8c/selection_worksheet.md` (per seed table and the rule), `quartus_SMP0*.md`, `quartus_SMP1*.md`, `verify.md`, `formal.md`, `cycles_v0.json`, `cycles_v1.json`, `evidence/phase08/8c/test_plan_8c.md`.
