# Artefak hasil per fase

Satu file per fase yang selesai: `phase<NN>.md` (NN mengikuti `docs/ROADMAP.md`; `phase05m` dan `phase9m` untuk sub-fase), dibuat dari
`TEMPLATE.md`. Ini satu halaman yang dibaca peninjau untuk memutuskan "apakah fase ini benar-benar selesai?".

- Hanya fakta, dari file di repository ini. `PASS` memerlukan bukti yang ada.
- `python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase<NN>.md` harus melaporkan 0 error
  sebelum meminta persetujuan.
- Kotak persetujuan dicentang manusia. Bukan Claude, bukan skrip.
- Fase yang jujur berstatus `PARTIAL` boleh; `DONE` dengan bukti yang hilang tidak boleh.
