# ADR 0033: Phase 9: C7-core as built (ML-KEM-768 in simulation, ACVP 100 percent) and the hash sponge core

- Status: Proposed
- Date: 2026-10-04
- Decided by: pending team decision

## Context
- Phase 9 built the ML-KEM-768 core in three blocks (ADR 0032): 9a codec, 9b hash wrapper and FO comparison, 9c the controller `mlkem_core` (`docs/results/phase09.md`, `evidence/phase09/`). Every pinned ACVP vector of ML-KEM-768 passes on both simulators (keyGen 25, encapsulation 25, decapsulation 10 including the modified ciphertexts). The FIPS 203 input checks are on the HPS (ADR 0031). Nothing here is a board result.
- There was no adoption rule in Phase 9 (nothing was chosen between measured alternatives), so the result is recorded as a configuration for the team to accept; the one open design choice is the sponge core of the hash instance (the sampler inside the engine uses C5 by ADR 0027).
- MEASURED (kernel-only Quartus, seeds 1-6; simulation cycles): `mlkem_core` 17,620.5 ALM median (42 % of 41,910), 54 RAM blocks, 28 DSP, Fmax median 49.280 MHz, timing met at 40.000 ns at every seed; KeyGen 9,035-9,076, Encaps 10,691, Decaps 16,623 cycles. The hash instance with the C5 sponge (wrapper and comparison) is 6,734.5 ALM; with the K0 sponge it is 4,221 ALM (seed 1, information, 9b).

## Options considered
(a) Accept the configuration as built: hash instance on the C5 sponge (the default of ADR 0027), serial encode and decode, input checks on the HPS.
(b) Accept it with the K0 sponge in the hash instance (`HASH_C5 = 0`): about 2,500 ALM fewer in the 9b blocks (seed 1; not yet compiled for the whole core), 26 cycles per permutation instead of 14: about 100 cycles more per hash of a 1,184-byte key (MEASURED 389 against 282 for H(ek) at 9b), small against the 9,000-16,600 cycles of an operation.
(c) Ask for an optimisation before the freeze (for example overlapping the encode or decode of polynomials with the engine, or a wider codec): not started; its cost is the team's time, the gain is a smaller cycle count (the pack and unpack of the polynomials is about 2,300-2,400 cycles of a KeyGen or Decaps, INFERENCE).
(d) Reopen ADR 0031 and put the FIPS 203 input checks into the RTL.

## Decision
Pending team decision (PENDING #33). The assistant's recommendation, not a decision: (a) or (b); (c) and (d) only if time remains and a board or a reason appears.

## Consequences
- Accepting (a) or (b) fixes the architecture for the proposal's Section 3 and for Phase 10 (HPS integration, blocked on a board, PENDING #8). Accepting does not allow any claim about the board, a speed-up against software, power or side-channel resistance: constant-time means a cycle count that does not depend on a secret (shown in simulation for a fixed encapsulation key; the length of the matrix sampling depends on the public rho).
- (b) needs one more compile of the whole core (seeds 1-6, about an hour) and a rerun of the vector tests with `HASH_C5 = 0`.

## Evidence
`docs/results/phase09.md`, `evidence/phase09/9a/result_9a.md`, `9b/result_9b.md`, `9c/result_9c.md`, `9c/selection_worksheet.md`, `9b/selection_worksheet.md`, `9c/sim_verilator.md`, `9c/sim_icarus.md`; ADR 0027, 0031, 0032.
