# Proposal workspace

The proposal text is written in Indonesian and submitted as PDF/Word; keep source text or
notes here as Markdown (`.md`) so the claim checker can read them.

**Constraints (from the organisers' template and the team)**
- Maximum 6 pages; cover page and reference list are not counted (whether the Appendix
  counts is unknown; see `docs/decisions/PENDING.md` #12).
- Pages 1-3: Section 1 (Ringkasan Ide) and Section 2 (Latar Belakang & Rumusan Masalah).
  Pages 4-6: Section 3 (Proposed Chip Design). Section 3 is **not written yet**.
- Keep the template headings verbatim. Formal Indonesian; foreign terms in italics.
- Numbers `[1]`-`[31]` refer to `references.md`; do not renumber silently.
- Every quantitative statement is cited, `ESTIMATE`, `MEASURED` (with an evidence path) or
  "perhitungan tim". See `CLAIMS_REGISTER.md`.
- No personal contact data in this public repository.

**Check before you commit anything here**
`python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/proposal README.md`

**Files**
- `references.md`: numbered reference list (matches the submitted Sections 1-2).
- `CLAIMS_REGISTER.md`: every claim in the proposal, its source, and its evidence status.
