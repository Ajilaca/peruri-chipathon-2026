---
name: proposal-claims
description: Check and write proposal / README / report text under this project's claim rules (no overclaims, every number labelled ESTIMATE, MEASURED, cited, or team-calculated; 6-page limit). Use whenever the user edits or drafts text for judges (proposal sections, README, slides, video script), asks "is this claim OK", or before any commit that touches docs/proposal or README.md.
---

# proposal-claims

The proposal is scored on evidence. One unsupported claim costs more than a missing one.

## Run the checker

```bash
python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/proposal README.md --words
```

Exit 1 = at least one ERROR. WARNs are for a human decision. A clean run only means these
known problems are absent; it does not prove the text is right. `--selftest` verifies
the rules themselves.

## Claim labels (every quantitative statement gets exactly one)

| Label | Meaning | Requirement |
|---|---|---|
| `[n]` | From a cited source | Reference `n` exists in `docs/proposal/references.md` |
| `ESTIMATE` | Analytical guess | State method and assumptions in the same paragraph |
| `MEASURED` | Produced by a tool run in this repo | Path to evidence under `evidence/` |
| `perhitungan tim` | Simple arithmetic from cited facts | Show the inputs |

Literature numbers are context, never our result. Example: "OCAKE takes 1.39 s on a
20 MHz STM32 [11]" is motivation; it is not a claim about the DE10-Nano.

## Claims this project does NOT make (until evidence exists)

1. "Quantum-proof / kebal kuantum". Say: *dirancang mengikuti standar pasca-kuantum*.
2. Side-channel (power/EM) protection. Core stage claims constant-time by construction,
   proven by cycle-count invariance. TVLA with the oscilloscope and masking are *later
   stage*. See `docs/decisions/adr/ADR-0002-scope-and-claims.md`.
3. Speed-up versus software. The HPS Cortex-A9 is far stronger than the microcontroller
   in the literature, and bridge overhead may cancel gains. Needs a MEASURED baseline on
   the same board.
4. Power or energy savings ("boros daya", "hemat daya"): no measurement plan exists yet.
5. Novelty absolutes ("pertama", "belum pernah ada"). Prior art exists (Kyber NTT on
   Cyclone V, Xilinx ML-KEM cores, Adams Bridge). Scope with *sejauh penelusuran kami*
   only after a documented search.
6. Yosys/generic-synthesis area as Cyclone V resources. Quartus only.
7. Anything about e-KTP cryptography (no source). e-passport (ICAO Doc 9303) is sourced.
8. The template's 415,000 flip-flops. Cyclone V 5CSEBA6U23I7 has 166,036 registers.

## Format constraints (from the organisers' template and the team)

- Maximum 6 pages, cover and reference list not counted (Appendix counting unknown;
  ask the team, do not assume). Sections 1-2 get pages 1-3; Section 3 gets pages 4-6.
- Proposal text is Indonesian, formal. Foreign terms in italics.
- Keep the template's section headings verbatim.
- Do not put personal contact data (email, phone) in this public repository.

## When you edit text

1. Change the smallest thing that fixes the problem; keep the team's wording otherwise.
2. Re-run the linter; then re-check the reference numbers still match.
3. If a rule blocks a sentence the team wants, explain the rule and offer scoped wording.
   Do not weaken the checker to make text pass.
