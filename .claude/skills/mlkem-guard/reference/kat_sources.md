# Verified known-answer-test sources (checked 2026-09-28)

## NIST ACVP vectors (official)
- Repository: https://github.com/usnistgov/ACVP-Server  (path `gen-val/json-files/`)
- Pinned commit: `975de31eb83d87039ec88934fdc47d8c312b892d`
- Files (each file holds inputs and expected outputs together; `isSample: true`):

| File (under `gen-val/json-files/`) | sha256 |
|---|---|
| `ML-KEM-keyGen-FIPS203/internalProjection.json` | `d7a62a2c3476957f56dd8d24f9004ea6776ccfe995ffe71a65bb9506dc9c7b1b` |
| `ML-KEM-encapDecap-FIPS203/internalProjection.json` | `a556952ce869bb89c3a3196a701dad89647c193a34c86eafb61a9d710d5b810f` |

Pinned URL form:
`https://raw.githubusercontent.com/usnistgov/ACVP-Server/975de31eb83d87039ec88934fdc47d8c312b892d/gen-val/json-files/<dir>/internalProjection.json`
Fetching these pinned URLs returned files with the sha256 above. If a later fetch differs, stop and report.

## Structure of the ML-KEM-768 groups (as inspected)
| Set / function | Tests | Fields | Notes |
|---|---|---|---|
| keyGen (AFT) | 25 | `d`, `z` -> `ek`, `dk` | seeds 32 B; ek 1184 B; dk 2400 B |
| encapDecap, `encapsulation` (AFT) | 25 | `ek`, `m` -> `c`, `k` | m 32 B; c 1088 B; k 32 B |
| encapDecap, `decapsulation` (VAL) | 10 | `dk`, `c` -> `k`, `reason` | 5 `valid decapsulation`, 5 `modified ciphertext` (implicit rejection) |
| encapDecap, `encapsulationKeyCheck` | 10 | `ek` -> `testPassed`, `reason` | 5 valid, 5 invalid keys |
| encapDecap, `decapsulationKeyCheck` | 10 | `dk` -> `testPassed`, `reason` | |

Hex strings are compared case-insensitively. Use only the `ML-KEM-768` groups. These are NIST's sample
sets (25 cases per group), not exhaustive coverage; say so in every result.

## Independent oracle for random cross-checks
- `kyber-py` 1.2.0 (pure Python ML-KEM, FIPS 203), MIT licence (Copyright 2025 Giacomo Pope).
- Exposes deterministic `_keygen_internal(d, z)`, `_encaps_internal(ek, m)`, `_decaps_internal(dk, c)`.
- Verified 2026-09-28: it reproduces all 60 ML-KEM-768 vectors above (25 + 25 + 10).
- Use it as a test-time oracle in a throwaway virtualenv outside the repository. Do not copy its code
  into this repository and do not add it to `requirements-dev.txt` without an ADR.

## Still to read (not verified from here)
- FIPS 203 PDF and the "Errata (potential updates)" spreadsheet linked on
  https://csrc.nist.gov/pubs/fips/203/final (its planning note is dated 17 Nov 2025; contents unread).
- NIST SP 800-227 (KEM usage guidance) is optional background.
