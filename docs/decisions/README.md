# Decision records (ADR)

One file per decision in [`adr/`](adr/): `ADR-NNNN-short-title.md`. [`SUMMARY.md`](SUMMARY.md) summarises all of them. Create them with
`python3 .claude/skills/decision-record/scripts/new_adr.py "Title"` (it writes to `docs/decisions/adr/`; add a row to `SUMMARY.md` afterwards).
Open choices live in `PENDING.md`. Decisions belong to the team; Claude records and
questions, it does not decide. Accepted records are never edited; supersede them instead.
