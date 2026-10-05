# ADR 0002: Scope and claim policy - the mathematics is locked

- Status: Accepted
- Date: 2026-09-28
- Decided by: team J5 (basis: statements in the team's proposal Sections 1-2: design principles, "Batasan", core / later-stage / out-of-scope table)

## Context
The proposal claims FIPS 203 conformance and constant-time behaviour, and separates a core
stage from later-stage work. Judges score evidence; unsupported claims are costly.

## Decision
1. ML-KEM-768 parameters (q, n, k, eta, du, dv, root of unity) and all arithmetic
   definitions are not modified. Innovation is in hardware architecture only.
2. Security wording: "designed to follow post-quantum standards", never "quantum-proof".
3. Side-channel (power/EM) resistance is not claimed at core stage. Core claim:
   constant-time by construction, shown by cycle-count invariance. TVLA and masking are
   later stage.
4. All resource, timing and performance numbers come from Quartus reports or board
   measurements (`evidence/`); otherwise they are labelled ESTIMATE.
5. Scope tiers as in `docs/PROJECT_BRIEF.md` (core / later / out of scope).

## Consequences
`/mlkem-guard` (parameter lock), `/proposal-claims` (claim lint) and CLAUDE.md §3 enforce this.
Any request to change a locked item requires a new ADR that supersedes this one.

## Evidence
Proposal Sections 1-2; `docs/AI_TOOLING_RESEARCH.md`.
