# Catatan keputusan (ADR)

Satu file per keputusan di [`adr/`](adr/): `ADR-NNNN-judul-singkat.md`. [`decision_summary.md`](decision_summary.md) memuat keputusan yang membentuk desain akhir;
[`SUMMARY.md`](SUMMARY.md) meringkas semuanya. Buat ADR baru dengan
`python3 .claude/skills/decision-record/scripts/new_adr.py "Judul"` (menulis ke `docs/decisions/adr/`; tambahkan satu baris ke `SUMMARY.md` sesudahnya).
Pilihan yang masih terbuka ada di `PENDING.md`. Keputusan milik tim; Claude mencatat dan bertanya, tidak memutuskan.
ADR yang sudah *Accepted* tidak diedit; gantikan dengan ADR baru.
