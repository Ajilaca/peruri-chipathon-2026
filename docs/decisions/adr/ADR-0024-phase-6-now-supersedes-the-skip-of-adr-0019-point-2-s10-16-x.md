# ADR 0024: Fase 6 sekarang (menggantikan pelewatan ADR 0019 butir 2); S10 (memori M10K 16 x 1R1W) di dalam Fase 6 sesudahnya

- Status: Accepted
- Tanggal: 2026-10-03
- Diputuskan oleh: Jevan, Team J5, chat 2026-10-03: "fase 6 dulu aja" dan "kemudian kerjakan s10 di fase 6 saja"

## Konteks
- ADR 0019 (Accepted) butir 2 melewati Fase 6 sebelum batas waktu (urutan operasi tetap yang sepele di pengendali
  sebagai gantinya). Tim (Jevan) meminta pada 2026-10-03 agar Fase 6 dikerjakan dulu, lalu S10 di dalam Fase 6.
- S10 = opsi A ADR 0022 (Proposed): 16 bank M10K 1R1W dengan peta bebas konflik
  `bank = (a1^a2^a3^a4, a7, a6, a5)`, `offset = a[3:0]`, crossbar, tanpa arbitrasi slot. Menyasar Fmax; Fase 6 sendiri
  tidak (docs/ROADMAP.md Fase 6).
- Lingkup Fase 6 (ROADMAP): penjadwal untuk aritmetika K-PKE pada KeyGen, Encrypt, dan Decrypt; transformasi dihitung
  dan sama dengan acuan yang direproduksi (KeyGen 6 NTT / 0 INTT / 9 perkalian pointwise, Encaps 3 / 4 / 12, Decaps
  6 / 5 / 15, `tb/golden/op_counts.py`); masukan (matriks, noise) disuntikkan testbench; tanpa Keccak atau sampler di
  perangkat keras.

## Opsi yang dipertimbangkan
(a) Mempertahankan urutan ADR 0019 (Keccak K0 berikutnya, Fase 6 dilewati). (b) Fase 6 sekarang, S10 sesudahnya di fase
yang sama (dipilih). (c) S10 dulu.

## Keputusan
Opsi (b), diputuskan Jevan (chat 2026-10-03). Asumsi kerja yang dinyatakan asisten, bukan diputuskan tim (tim boleh
menimpanya): basis inti NTT/INTT untuk Fase 6 = S7 (terukur terbaik, ADR 0021 masih Proposed; penjadwal memakai inti
hanya lewat port host-nya, jadi inti dapat ditukar); lingkup ROADMAP penuh untuk Fase 6. S10 menyusul setelah vonis
Fase 6 dengan test plan sendiri dan aturan ADR 0012 (dibanding S7). Estimasi waktu yang diberikan tim (selesai "pagi
ini") tidak sesuai dengan ESTIMATE asisten sebesar 10-14 jam untuk keduanya (dasar: pekerjaan S6-S8 2026-10-02/03).

## Konsekuensi
- ADR 0019 butir 2 ("Fase 6 dilewati") digantikan oleh catatan ini (ADR 0019 tetap Accepted selebihnya; catatan
  amandemen 4 ditambahkan di sana). Fase 7 (Keccak) dan blok berikutnya pindah setelah Fase 6 dan S10.
- Branch `phase6-scheduling`. Approval Fase 6 (anggota tim) diperlukan sebelum Fase 7 (ROADMAP); Approval Fase 5M
  masih kosong.
- Fmax tidak diharapkan naik di Fase 6 (INFERENCE); efek Fmax S10 BELUM DIUKUR.
- Risiko batas waktu (2026-10-08) untuk Keccak, sampler, dan jalur ML-KEM penuh naik; itu milik tim.

## Bukti
- Chat 2026-10-03; `docs/ROADMAP.md` Fase 6; `docs/decisions/adr/ADR-0019-*.md`; `docs/decisions/adr/ADR-0022-*.md`;
  `tb/golden/op_counts.py` (hitungan direproduksi).
