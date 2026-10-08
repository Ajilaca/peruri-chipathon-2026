# ADR 0032: Protokol checkpoint sampai 2026-10-08: satu STOP per blok (Fase 9 dan seterusnya)

- Status: Accepted
- Tanggal: 2026-10-03
- Diputuskan oleh: Jo, Team J5, chat 2026-10-03: "b" (opsi B, satu STOP per blok), dan "jangan commit terlebih dahulu" (commit dibuat di akhir pekerjaan, dikelompokkan per blok)

## Konteks
- PENDING #26: seberapa sering asisten berhenti dan menunggu tim sampai batas waktu (2026-10-08, pembekuan evidence
  malam 2026-10-07). Tim punya sekitar 6-8 jam perhatian per hari (ADR 0019). Di Fase 8 tim meminta 8b, 8c, dan 8d
  dijalankan tanpa berhenti (chat 2026-10-03); pertanyaan tetap terbuka untuk fase berikutnya.

## Opsi yang dipertimbangkan
(A) STOP setelah setiap langkah (gaya ADR 0012): kendali paling banyak, menunggu paling banyak. (B) satu STOP per
blok: laporan setelah tiap kelompok pekerjaan. (C) tanpa STOP sampai akhir fase: menunggu paling sedikit, kendali
paling sedikit.

## Keputusan
(B), satu STOP per blok. Chat 2026-10-03 (Jo, Team J5): "b". Blok Fase 9 adalah usulan asisten dan bukan bagian
keputusan: 9a encode/decode dan compress/decompress; 9b bagian FO (enkripsi ulang, pembandingan waktu konstan,
implicit rejection); 9c pengendali KeyGen, Encaps, dan Decaps dengan semua grup ACVP terpatok dan kompilasi Quartus.
Chat 2026-10-03 (Jo): "jangan commit terlebih dahulu": commit dibuat ketika pekerjaan selesai, dikelompokkan per blok
(bukan satu commit per langkah-blok selama pekerjaan).

## Konsekuensi
- Setelah tiap blok asisten menulis laporan singkat dan berhenti; tim menyatakan lanjut atau tidak. Di dalam blok
  tidak ada stop. Tiap blok tetap punya test plan dan aturan adopsi yang ditulis sebelum RTL dan sebelum mengukur.
- Tidak berubah oleh keputusan ini: asisten tidak pernah mencentang kotak Approval, tidak pernah push, tidak pernah
  memutuskan butir PENDING yang terbuka (ia mencatat ADR Proposed), dan tidak pernah meng-commit dokumen status tanpa
  diminta.
- Sampai tim menyuruh commit, pekerjaan tetap tidak di-commit di working tree; riwayat commit yang dibuat sesudahnya
  harus mengikuti urutan nyata pekerjaan (rencana, model acuan, RTL, test, evidence, ADR, hasil) dan tidak boleh
  menyiratkan waktu yang tidak terjadi.

## Bukti
- `docs/decisions/PENDING.md` #26; `docs/decisions/adr/ADR-0019-*.md` (konteks checkpoint); `docs/decisions/adr/ADR-0012-*.md`.
