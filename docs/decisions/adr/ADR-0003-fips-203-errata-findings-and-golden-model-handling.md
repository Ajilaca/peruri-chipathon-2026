# ADR 0003: FIPS 203 errata findings and golden-model handling

- Status: Accepted
- Date: 2026-09-29
- Decided by: Faza Dzil (Team J5), 2026-09-29, via Claude Code session instruction "accept adr3"

## Context

`docs/decisions/PENDING.md` item #9 blocked Phase 0: the content of NIST's FIPS 203
"planning note" (dated 2025-11-17, seen on the publication page) about an issue to be
corrected was not yet read. Phase 0 requires locking `tb/golden/params.py` and official
KAT vectors before any RTL work, and the mlkem-guard verification process requires
reading the errata before locking vectors. This ADR records what was found so the team
can confirm the golden model may proceed as planned.

## Options considered

1. Implement FIPS 203 literally as published (13 Aug 2024), treat the two errata items
   as non-normative - cost: none if the errata truly change nothing testable; risk is
   that a future NIST errata *update* (not yet issued) could add normative changes we'd
   need to re-check.
2. Wait for NIST to issue a formal errata update/revision before writing the golden
   model - cost: indefinitely blocks Phase 0 with no announced timeline from NIST.
3. Pre-emptively adopt the two potential corrections as if final - cost: unnecessary,
   since NIST explicitly states these are not official changes and introduce no new
   technical requirements; would add process overhead for zero behavioural difference.

Evidence: `evidence/phase00/fips203_errata.md` (full quotes, source
URLs, SHA-256 of the fetched PDF and errata spreadsheet, and the Table 2 parameter
cross-check for ML-KEM-768).

## Decision

Option 1: implement FIPS 203 literally as published, with no deviation motivated by the
current errata. Findings:

- The "Potential Updates (Errata)" spreadsheet (accessed 2026-09-28 UTC) lists 2
  items, both explicitly labelled by NIST as clarifications/typo corrections that "DO
  NOT introduce new technical requirements" and "ARE NOT official changes":
  1. Appendix A - clarifies why the zeta table includes the i=0 entry (value 1), used by
     Algorithms 9/10 (NTT/NTT⁻¹) only for i=1..127. No algorithm step changes.
  2. Section 5.3, Algorithm 15, line 7 - comment text says "polynomial v" but should say
     "polynomial w"; the algorithm body already uses `w` correctly. Comment-only fix.
- Neither item changes an algorithm step, a parameter, or a test vector. Neither affects
  our golden model as planned: the NTT will compute zeta values from the BitRev_7 formula
  (not copy an Appendix A table row-by-row), so it already agrees with the Appendix A
  clarification for i=0 without any code change; K-PKE.Decrypt will follow the algorithm
  body (`w`), not the erroneous comment.
- Table 2 (Section 8) parameter values for ML-KEM-768 were read directly from the PDF and
  cross-checked against the planned `tb/golden/params.py` values: k=3, η1=2, η2=2, du=10,
  dv=4 - exact match, no discrepancy. n=256 and q=3329 confirmed as fixed constants.
  Table 3 sizes (ek 1184 B, dk 2400 B, ct 1088 B, ss 32 B) also match.

Accepted 2026-09-29 by Faza Dzil (Team J5). Phase 0 golden-model work (`tb/golden/params.py`
and the NTT/K-PKE golden model, already written against the literal FIPS 203 text without
waiting on NIST) stands confirmed under this decision.

## Consequences

- `docs/decisions/PENDING.md` item #9 is closed by this acceptance.
- No proposal text, claim, or roadmap item needs to change: no parameter or algorithm
  deviates from FIPS 203 as published.
- If NIST later issues a formal errata *update* or revision (beyond this "potential
  updates" list), this ADR must be revisited and, if it changes anything normative,
  superseded by a new ADR.
- Re-check trigger: re-read the NIST FIPS 203 publication page before locking any KAT
  vector batch, in case the list has grown since 2026-09-28.

## Evidence

- `evidence/phase00/fips203_errata.md` - MEASURED: source URLs, access
  date, SHA-256 of the fetched FIPS 203 PDF and errata spreadsheet, full quoted errata
  items with per-item impact analysis, and the Table 2/Table 3 parameter cross-check.
