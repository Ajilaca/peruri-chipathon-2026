# ADR 0018: Lingkup dan urutan sampai batas Kamis 2026-10-08: selesaikan 5M, lalu baseline Keccak, tunda Fase 6, tulis Bagian 3 proposal

- Status: Superseded by 0019
- Tanggal: 2026-10-02
- Diputuskan oleh: Jevan, Team J5 (chat 2026-10-02: jawaban batas waktu dan opsi strategi "Selesaikan Fase 5M lalu Keccak baseline")

## Konteks
- Tim punya waktu sampai Kamis 2026-10-08 (dihitung dari Jumat 2026-10-02; jam tidak disebutkan, jadi pembekuan Rabu
  malam direncanakan agar aman). Hasil yang disebut di chat adalah proposal lengkap, termasuk Bagian 3 (halaman 4-6),
  yang sebelumnya belum ditulis (aturan C4: "jangan ditulis sampai diminta"; tim kini memintanya dengan menyebutnya
  sebagai hasil batas waktu).
- Pekerjaan roadmap yang tersisa, ESTIMATE (keyakinan rendah, dasar: langkah S6 memakan sekitar 6 jam waktu jam
  dinding): Fase 5M S6-S9 sekitar 12-13 jam dari malam 2026-10-02; Fase 6 12-20 jam; Fase 7 8-14 jam; Fase 8 30-50 jam;
  Fase 9 45-80 jam. Fase 6-9 bersama (95-165 jam) tidak muat dalam enam hari; Fase 10 terhambat papan yang tidak ada
  (PENDING #8).
- Terukur sejauh ini: inti NTT/INTT C4b-B, evidence Quartus kernel-only dan simulasi (`docs/results/phase05.md`); S6
  terukur, vonisnya menunggu (lihat ADR 0019 begitu ditulis).

## Opsi yang dipertimbangkan
(a) Menyelesaikan Fase 5M (S6-S8, S9 sebagai dokumen bila waktu ada), lalu baseline Keccak Fase 7 (K0); menulis
    Bagian 3 paralel. Dua blok terukur (NTT/INTT dan Keccak) pada batas waktu. Biaya: Fase 6, 8, 9 tidak selesai;
    Fase 7 mulai tanpa Fase 6.
(b) Menghentikan Fase 5M setelah S6, langsung ke Keccak. Dua blok yang sama, Keccak mulai lebih awal, lebih longgar
    untuk proposal; S7-S8 (kerja Fmax) dilepas.
(c) Tanpa RTL baru; seluruh waktu untuk proposal dan ringkasan evidence. Risiko terendah untuk dokumen; tidak ada blok
    terukur baru.

## Keputusan
Opsi (a) dipilih oleh Jevan, Team J5, dengan Bagian 3 proposal ditulis. Konsekuensi yang diterima tim dengan memilihnya:
1. Fase 5M berlanjut berurutan S6, S7, S8, dengan S9 hanya sebagai dokumen dan hanya bila waktu ada; tiap langkah tetap
   berhenti untuk tim.
2. Fase 6 ditunda (tidak selesai sebelum batas waktu). Fase 7 (Keccak K0, `docs/ROADMAP.md`) mulai setelah S8 tanpa
   persetujuan Fase 6. Ini menyimpang dari "persetujuan fase N sebelum N+1" di roadmap dan dicatat di sini; Fase 6 tetap
   di roadmap sebagai pekerjaan mendatang.
3. Fase 8, 9, 10, dan 11 tidak dicoba sebelum batas waktu dan di proposal digambarkan hanya sebagai pekerjaan yang
   direncanakan, tanpa hasil yang diklaim.
4. Bagian 3 proposal (halaman 4-6) ditulis hanya dari evidence repository, di bawah aturan klaim (C2, C3, C8,
   `/proposal-claims`); angka dilacak di `docs/proposal/CLAIMS_REGISTER.md`. Tidak ada yang diklaim untuk ML-KEM penuh,
   percepatan terhadap perangkat lunak, daya, atau validasi perangkat keras.
5. Pembekuan: tidak ada pengukuran baru ditambahkan ke proposal setelah Rabu malam 2026-10-07; hasil sesudahnya hanya
   masuk repository.

## Konsekuensi
- Rencana (ESTIMATE, bisa meleset; aturan adopsi ADR 0012 dan aturan satu-perubahan-per-langkah tidak berubah):
  Jumat 10-02 malam laporan S6; Sabtu S7; Minggu-Senin S8 (dengan satu regresi penuh, Amandemen A1 test plan 5M);
  Senin-Selasa Fase 7 (K0); Selasa-Rabu Bagian 3 proposal dan pemeriksaan klaim; Kamis tinjauan akhir dan pengumpulan.
  Bila S8 tidak diadopsi atau terlambat, Fase 7 tetap dimulai dan hasil S8 dilaporkan seperti terukur.
- Bila Fase 7 tidak selesai, K0 dilaporkan "tidak selesai" dan proposal menyatakannya; Keccak parsial tidak disajikan
  sebagai hasil.
- Klaim apa pun di proposal tentang Keccak hanya boleh setelah K0 punya log uji lolos dan laporan Quartus di `evidence/`.

## Bukti
- `docs/ROADMAP.md` (Fase 6-10), `docs/decisions/adr/ADR-0017-*.md`, `docs/results/phase05.md`, chat 2026-10-02.
