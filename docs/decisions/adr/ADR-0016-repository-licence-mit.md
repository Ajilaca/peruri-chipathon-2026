# ADR 0016: Repository licence: MIT

- Status: Accepted
- Date: 2026-10-02
- Decided by: Faza Dzil, Team J5 (chat 2026-10-02: 'isi lisensi dengan MIT')

## Context
- PENDING #11: the repository is public (constraint C7); without a licence the default copyright applies and reuse is
  not permitted.
- The team lead asked on 2026-10-02 to fill the licence with MIT.

## Options considered
Only MIT was named in the request; no alternative licence was evaluated.

## Decision
The repository is licensed under the MIT License (`LICENSE`). The copyright line reads "Team J5 (Institut Teknologi
Bandung), CHIP 2026 Hackathon" (wording chosen by the assistant, to be corrected by the team if a different holder
name is wanted). Third-party material that carries its own licence (for example Intel/Terasic GHRD files, if
vendored, and downloaded test vectors) keeps that licence; MIT applies to the team's own files.

## Consequences
- `README.md` licence section updated; `docs/decisions/PENDING.md` item #11 closed.
- Anyone may reuse the code under the MIT terms; no patent grant is included (MIT has none).
- The proposal text should state the licence only as written in `LICENSE`.

## Evidence
- `LICENSE`; chat 2026-10-02 (Faza Dzil): "isi lisensi dengan MIT".
