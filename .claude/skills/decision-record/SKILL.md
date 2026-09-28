---
name: decision-record
description: Record a project decision as a numbered ADR in docs/decisions and keep docs/decisions/PENDING.md in sync. Use when the team makes or asks to make a design or scope choice (card-side vs reader-side accelerator, DMA, randomness source, hybrid mode, declared subtheme, second baseline, licence), or when you notice a choice that has not been decided.
---

# decision-record

Decisions belong to the team (J5), not to Claude. This skill makes them explicit and
traceable so the proposal, the RTL, and the claims stay consistent.

## Rules

1. **Never decide on the team's behalf.** If a choice is open, list it in
   `docs/decisions/PENDING.md` and ask. Do not start RTL or write proposal text that
   assumes an undecided option.
2. Create records with the script; it numbers them and refuses `accepted` without a named
   decider:

   ```bash
   python3 .claude/skills/decision-record/scripts/new_adr.py "Short decision title"            # proposed
   python3 .claude/skills/decision-record/scripts/new_adr.py "Title" --status accepted --decided-by "team J5, <date/where>"
   ```
3. Fill **Context / Options / Decision / Consequences / Evidence** only from what was said
   or measured. Quote the source (chat, meeting, report path).
4. Never edit an accepted record to change history. Write a new ADR that supersedes it and
   set the old status to `Superseded by NNNN`.
5. After accepting a decision, list what it invalidates: proposal sentences, claim labels,
   `docs/proposal/CLAIMS_REGISTER.md` rows, roadmap items. Update them or flag them.
6. Move the item out of `PENDING.md` in the same change.

## Currently open (see PENDING.md for the live list)

Card-side vs reader-side target · DMA vs plain register access · randomness source ·
hybrid ECDH+ML-KEM mode · declared subtheme · second software baseline · DE10-Nano board
availability · repository licence · whether the Appendix counts toward the 6 pages · activating
rtl-agent-team hooks (`rat-init-project`).
