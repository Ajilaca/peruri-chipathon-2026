# ADR 0031: Phase 9: FIPS 203 input checks are done by the HPS, not in the RTL (no board access for now)

- Status: Accepted
- Date: 2026-10-03
- Decided by: Jo, Team J5, chat 2026-10-03: 'HPS untuk sekarang karena papan tidak ada aksesnya' (reply to the suggestion: on the HPS, with the note that it is not tested on a board)

## Context
- `docs/ROADMAP.md` Phase 9 item 2 requires a decision before the phase starts: the FIPS 203 input checks (encapsulation-key check, decapsulation-input check) run in hardware or on the HPS. PENDING #25 (suggestion in the pending list: on the HPS for the deadline scope).
- No DE10-Nano is accessible to the team (PENDING #8 open; `jtagconfig` showed no board on 2026-09-24; chat 2026-10-03: the team has no access to a board). The HPS cannot be run, so anything placed on the HPS stays untested on a board.
- The golden model already has both checks as software functions: `check_encapsulation_key` and `check_decapsulation_input` in `tb/golden/mlkem.py`.
- The deadline is 2026-10-08 (evidence freeze 2026-10-07 night); ADR 0019 tiers: T3 is not guaranteed.

## Options considered
(a) Checks in the RTL (hardware): adds RTL (re-encode and compare of the key, a hash of the secret key, length checks) and the ACVP key-check groups (10 + 10) to the Phase 9 vector runs; more area and more verification work before the deadline; testable in simulation.
(b) Checks on the HPS (software): no RTL; the accelerator assumes inputs that passed the checks; the software function exists in the golden model; cannot be run on the HPS without a board.

## Decision
(b). The FIPS 203 input checks are done by the HPS (software), not in the RTL, for now. Chat 2026-10-03 (Jo, Team J5): 'HPS untuk sekarang karena papan tidak ada aksesnya'. The words "for now" are the team's: the question can be reopened if a board becomes available or time remains.

## Consequences
- Phase 9 (C7-core) has no key-check RTL. The vector runs cover the ACVP groups keyGen, encapsulation and decapsulation (decapsulation with modified ciphertexts included); the key-check groups (10 + 10) are **not** run against the RTL. Whether they are run against the software function of the golden model is a separate, optional step and must be labelled as software only.
- The RTL core states the assumption in its specification: the caller (HPS) has checked the inputs. The proposal must not say that the hardware performs the FIPS 203 input checks.
- NOT tested on a board: the HPS-side checks stay a design intent until Phase 10 (blocked on PENDING #8). No claim of hardware validation (C8). The implicit rejection of Decaps (FO) stays in the RTL and is part of Phase 9.
- The constant-cycle evidence for Decaps is unaffected (valid and modified ciphertexts, different secret keys).
- If a board never becomes available, the proposal describes the HPS checks as a planned software step, with the golden-model function as the reference.

## Evidence
- `docs/ROADMAP.md` Phase 9 item 2 and 3; `docs/decisions/PENDING.md` #25 and #8; `tb/golden/mlkem.py` (the two check functions); ADR 0019 (tiers, deadline).
- No measurement is involved in this decision.
