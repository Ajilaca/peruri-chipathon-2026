<!-- claim-lint: skip-file (result artifact: internal status page, not proposal text) -->
# Result — Phase 0: Foundations

- Status: DONE
- Date (UTC): 2026-09-28 18:20
- Git commit (HEAD when verified): bac5637
- Environment: Ubuntu 24.04.4 LTS, Python 3.12.3 (`.venv`, pytest 9.1.1); oracle cross-check run
  with a separate throwaway venv (`~/.cache/chip2026-oracle/venv`, kyber-py 1.2.0)

## 1. Done-criteria (copied from docs/ROADMAP.md, unchanged)
| # | Criterion | Evidence (`path` under docs/evidence/ or tests, or `cmd: ...`) | Status |
|---|---|---|---|
| 1 | `check_params.py` passes (locked parameters), and k/eta/du/dv are confirmed against the FIPS 203 parameter table | `cmd: python3 .claude/skills/mlkem-guard/scripts/check_params.py` and `docs/evidence/golden/fips203_errata_2026-09-28.md` | PASS |
| 2 | Golden model reproduces the official ML-KEM-768 vectors (NIST ACVP, pinned commit in kat_sources.md; NIST sample sets; raw output in docs/evidence/golden/) | `docs/evidence/golden/kat_mlkem768_2026-09-28.txt` | PASS |
| 3 | Errata findings recorded (evidence file + ADR) | `docs/evidence/golden/fips203_errata_2026-09-28.md` and `docs/decisions/0003-fips-203-errata-findings-and-golden-model-handling.md` | PASS |
| 4 | Independent cross-check log on random inputs in docs/evidence/golden/ (oracle: kyber-py in a throwaway venv) | `docs/evidence/golden/crosscheck_kyberpy_2026-09-28.txt` | PASS |
| 5 | `docs/results/result_phase0.md` passes `check_result.py`, and a human has approved it | `cmd: python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/result_phase0.md` (this file; the human-approval half of this criterion is tracked separately by section 10's unticked checkbox, not by this row) | PASS |

Status is PASS, FAIL or MISSING. PASS needs at least one backticked evidence item that exists.
No RTL exists yet in this phase; nothing here is simulation-only vs. board-measured (that
distinction starts in Phase 1).

## 2. What was produced
| Path | Purpose |
|---|---|
| `tb/golden/params.py` | Locked ML-KEM-768 constants (Q N ZETA K ETA1 ETA2 DU DV EK_BYTES DK_BYTES CT_BYTES SS_BYTES) |
| `tb/golden/primitives.py` | FIPS 203 auxiliary algorithms: NTT/NTT⁻¹, MultiplyNTTs, BaseCaseMultiply, SampleNTT, SamplePolyCBD, ByteEncode/Decode, Compress/Decompress, hash/XOF wrappers |
| `tb/golden/kpke.py` | K-PKE.KeyGen/Encrypt/Decrypt (Algorithms 13-15) |
| `tb/golden/mlkem.py` | ML-KEM internal algorithms (16-18), input checks (§7.2, §7.3), randomized wrappers (19-21) |
| `tb/golden/conftest.py` | pytest sys.path setup so tests can `import params`/`import primitives` |
| `tb/golden/tests/test_primitives.py` | 19 property tests (NTT round-trip, NTT-vs-schoolbook, layer structure, encode/decode, compress/decompress, CBD range) |
| `tb/golden/tests/test_mlkem.py` | 4 tests: 500-trial round-trip, bit-flip implicit rejection, length checks, check_params.py re-run |
| `tb/golden/fetch_acvp_vectors.py` | Downloads + sha256-verifies the two pinned ACVP vector files |
| `tb/golden/run_kat.py` | Compares the model against the ML-KEM-768 ACVP groups |
| `tb/golden/crosscheck_kyberpy.py` | N=2000 deterministic cross-check against kyber-py (external oracle) |
| `docs/evidence/golden/fips203_errata_2026-09-28.md` | FIPS 203 source hashes, errata items quoted + impact analysis, Table 2/3 parameter cross-check |
| `docs/evidence/golden/kat_mlkem768_2026-09-28.txt` | Raw ACVP KAT comparison log (80/80 passed) |
| `docs/evidence/golden/crosscheck_kyberpy_2026-09-28.txt` | Raw kyber-py cross-check log (2000/2000 matched) |
| `docs/decisions/0003-fips-203-errata-findings-and-golden-model-handling.md` | ADR (Status: Proposed) on how the errata are handled |
| `.claude/skills/mlkem-guard/reference/kat_sources.md` | Pinned ACVP commit, sha256, vector layout, oracle note (provided, not authored by this session) |

## 3. Numbers (each labelled MEASURED, ESTIMATE, or cited [n])
| Quantity | Value | Label | Evidence |
|---|---|---|---|
| `check_params.py` result | 12/12 locked constants OK | MEASURED | `cmd: python3 .claude/skills/mlkem-guard/scripts/check_params.py` |
| `pytest tb/golden` result | 23/23 passed | MEASURED | `cmd: python3 -m pytest tb/golden/tests/ -q` |
| ACVP ML-KEM-768 KAT cases | 80/80 passed (keyGen 25, encapsulation 25, decapsulation 10, decapsulationKeyCheck 10, encapsulationKeyCheck 10) | MEASURED | `docs/evidence/golden/kat_mlkem768_2026-09-28.txt` |
| kyber-py cross-check trials | 2000/2000 matched (keygen_internal, encaps_internal, decaps_internal valid, decaps_internal modified-ciphertext) | MEASURED | `docs/evidence/golden/crosscheck_kyberpy_2026-09-28.txt` |
| FIPS 203 errata items found | 2, both non-normative (clarification / comment typo) | MEASURED | `docs/evidence/golden/fips203_errata_2026-09-28.md` |

## 4. Standards and sources pinned
- **FIPS 203** (Module-Lattice-Based Key-Encapsulation Mechanism Standard), published 2024-08-13,
  DOI 10.6028/NIST.FIPS.203. PDF fetched 2026-09-28 UTC from
  `https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf`,
  sha256 `fe1f12f32a7e44ec9fdebbf400cda843a40b506dee676725234dc6f7923b6cac`.
- **Errata state read**: NIST's "Potential Updates (Errata)" spreadsheet, fetched 2026-09-28 UTC
  from `https://csrc.nist.gov/files/pubs/fips/203/final/docs/fips-203-potential-updates.xlsx`,
  sha256 `edf899c89762449f43d7713883caeefc2e4ae9ae98d5a76b339547db22cb3ac7`. Contains 2 items as of
  that access date (2025-03-31 Appendix A zeta-table clarification; 2025-10-17 Section 5.3
  comment typo), both non-normative. Full quotes and impact analysis in
  `docs/evidence/golden/fips203_errata_2026-09-28.md`. Handling recorded in ADR 0003
  (**Status: Proposed**, not yet team-accepted -- see Section 7 below).
- **NIST ACVP-Server** test vectors: repository `https://github.com/usnistgov/ACVP-Server`,
  pinned commit `975de31eb83d87039ec88934fdc47d8c312b892d`. Files used:
  `gen-val/json-files/ML-KEM-keyGen-FIPS203/internalProjection.json`
  (sha256 `d7a62a2c3476957f56dd8d24f9004ea6776ccfe995ffe71a65bb9506dc9c7b1b`, top-level
  `isSample: false` as downloaded -- differs from the `kat_sources.md` assumption of
  `isSample: true`, see caveat below) and
  `gen-val/json-files/ML-KEM-encapDecap-FIPS203/internalProjection.json`
  (sha256 `a556952ce869bb89c3a3196a701dad89647c193a34c86eafb61a9d710d5b810f`, top-level
  `isSample: true`). Both hashes verified before use; see
  `docs/evidence/golden/kat_mlkem768_2026-09-28.txt`.
- **Independent oracle**: kyber-py 1.2.0 (`https://github.com/GiacomoPope/kyber-py`), license
  MIT OR Apache-2.0, Copyright Giacomo Pope. Installed only in a throwaway virtualenv outside
  this repository; not added to `scripts/requirements-dev.txt`, not copied into the repo.

## 5. Coverage and limits
- **NIST sample/shipped vector sets only.** ACVP KAT coverage is 80 ML-KEM-768 cases total (25
  keyGen AFT, 25 encapsulation AFT, 10 decapsulation VAL, 10 decapsulationKeyCheck VAL, 10
  encapsulationKeyCheck VAL) from one pinned commit -- not exhaustive coverage of every possible
  input, decapsulation-failure path, or invalid-key construction.
- **ML-KEM-512 and ML-KEM-1024 are entirely untested.** Only ML-KEM-768 groups were used from
  both ACVP files, and `tb/golden/params.py` defines ML-KEM-768 constants only (by design, see
  mlkem-guard SKILL.md).
- **This Python model is NOT a constant-time implementation and no such claim is made about
  it.** `tb/golden/mlkem.py`'s docstring states this explicitly (branches on secret/derived data
  in the implicit-rejection and input-check paths). Constant-time is an RTL-level property to be
  measured in later phases, separately from this golden model's correctness.
- **kyber-py cross-check is 2000 pseudorandom trials from one fixed seed** (reproducible, not
  exhaustive) -- explicitly labelled "not a proof" in its own log.
- **No FPGA/Quartus numbers exist yet** -- Phase 0 is Python-only; no ALM/register/M10K/DSP/Fmax
  or cycle-count claim is made or implied by this phase.
- **§7.1 "key pair check" (seed-consistency + pairwise-consistency) is not implemented or
  tested** -- only the per-call §7.2 encapsulation-key check and §7.3 decapsulation-input check
  are implemented (`tb/golden/mlkem.py`), matching what the ACVP `encapsulationKeyCheck` /
  `decapsulationKeyCheck` groups actually exercise.
- **Invalid-input rejection paths for our own `check_encapsulation_key` /
  `check_decapsulation_input`** were exercised only through the 20 ACVP key-check cases (10+10);
  no additional fuzzing of malformed lengths/hashes was done beyond that.
- **ADR 0003 (errata handling) is Proposed, not yet accepted** by a named team decider; see
  Section 7.

## 6. Deviations, failures and open issues
None. No test failed at any point in this phase; no tolerance, assertion, or comparison was
weakened to make a result pass.

One factual correction relative to an earlier assumption: `.claude/skills/mlkem-guard/reference/kat_sources.md`
states the ACVP vectors are NIST "sample sets (isSample: true)". As actually downloaded and
sha256-verified (2026-09-28), the **keyGen** file's own JSON says `"isSample": false` (only the
**encapDecap** file says `true`). This is reported as found, not silently corrected in that
reference file; see `docs/evidence/golden/kat_mlkem768_2026-09-28.txt` for the exact values.

## 7. Decisions needed
- **ADR 0003** (`docs/decisions/0003-fips-203-errata-findings-and-golden-model-handling.md`,
  Status: Proposed) needs a named team decider to accept it. Until accepted,
  `docs/decisions/PENDING.md` item #9 stays open.
- No other `docs/decisions/PENDING.md` item blocks Phase 0 closure; items #1-#8 and #10-#13 all
  target later phases (see PENDING.md itself for the up-to-date list).

## 8. Claims made in this phase
None written for judges/proposal text in this phase. The only proposal artifact touched is
`docs/proposal/CLAIMS_REGISTER.md` row "Bit-exact match with official KATs", updated in this same
change from "not started" to a precise, evidenced statement (see Section 9's git log / diff);
`claim_lint.py` was run against `docs/results` and `docs/proposal` as required (see Section 9).

## 9. Reproduce
```bash
# from repo root
. scripts/env.sh

# 1. Golden model tests
python3 -m pytest tb/golden/tests/ -v

# 2. Locked parameters
python3 .claude/skills/mlkem-guard/scripts/check_params.py

# 3. Official NIST ACVP KAT comparison (downloads + sha256-verifies vectors first)
python3 tb/golden/fetch_acvp_vectors.py
python3 tb/golden/run_kat.py

# 4. Independent oracle cross-check (needs a throwaway venv with kyber-py==1.2.0
#    installed OUTSIDE this repo, e.g. ~/.cache/chip2026-oracle/venv)
~/.cache/chip2026-oracle/venv/bin/python3 tb/golden/crosscheck_kyberpy.py

# 5. Validate this result artifact
python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/result_phase0.md
python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal
```

## 10. Approval
- [ ] Human approver (name, date):
      Next phase starts only after a team member ticks this box.
