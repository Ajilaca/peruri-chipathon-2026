# ADR 0014: Fase 5c: masukan butterfly INTT malas, kontrak operand D6 diubah, aturan adopsi

- Status: Accepted
- Tanggal: 2026-10-01
- Diputuskan oleh: Faza Dzil, Team J5 (sesi 2026-10-01: opsi lingkup (b); aturan adopsi seperti diinstruksikan untuk 5c)

## Konteks
- 5c (opsional, `docs/ROADMAP.md`): reduksi malas, hanya dengan batas nilai yang terbukti. ADR 0011 D3 menunda
  keputusan untuk mencobanya sampai setelah 5a/5b; tim memintanya pada 2026-10-01 dengan tujuan mengeluarkan
  `sub_mod` dari segmen kritis.
- Pemeriksaan awal (`evidence/phase05/5c/precheck_critical_path.md`, MEASURED pada C4b-B seed 1): jalur terburuk
  adalah pembacaan memori (21,03 ns) → `sub_mod(b, a)` (4,22 ns) → DSP (3,59 ns), slack +11,044 ns; kelas jalur
  berikutnya adalah pembacaan memori → `add_mod(a, b)` (3,96 ns) → delay line sisi, slack +12,102 ns. Menghapus hanya
  `sub_mod` akan menyisakan batas Fmax sekitar 35,8 MHz (INFERENCE, satu seed).
- ADR 0011 D6 (kontrak operand): setiap reducer harus sama dengan (a·b) mod q untuk a, b di [0, q).
- Konfigurasi dasar: C4b-B (Barrett, ADR 0013 ketika itu Proposed; tim melanjutkan di atasnya).

## Opsi yang dipertimbangkan
(a) hanya masukan pengali malas (`b + q − a`); (b) kedua masukan butterfly INTT malas. Lihat pemeriksaan awal untuk
biayanya.

## Keputusan
1. Lingkup (b). Pada mode INTT butterfly memberi pengali `u = b + q − a` (eksak, di [1, 2q), 13 bit) sebagai ganti
   `sub_mod(b, a)`, dan membawa operand sisi `s = a + b` (eksak, di [0, 2q), 13 bit) sebagai ganti `add_mod(a, b)`;
   `s` direduksi sekali di keluaran butterfly (satu pengurangan bersyarat, di segmen tulis). Mode NTT tidak berubah.
   Memori, jadwal, L, P = 6, dan posisi register C4b-B tetap.
2. Kontrak operand D6, diubah hanya untuk pengali lajur C4c: reducer Barrett yang dipakai di sana harus sama dengan
   (z·u) mod q untuk setiap z di [0, q) dan setiap u di [0, 2q) (menyeluruh, 22.164.482 pasangan). Pengali skala dan
   semua pemakaian lain mempertahankan kontrak D6 [0, q) x [0, q). Hasil tetap bit-exact dengan FIPS 203 (`tb/golden`).
3. Batas nilai dibuktikan formal (SymbiYosys) pada logika masukan / keluaran malas: u < 2q, s < 2q, (u mod q) =
   (b − a) mod q, keluaran butterfly < q dan sama dengan persamaan acuan, tidak ada sinyal yang lebih lebar dari
   deklarasinya; dengan kontrol negatif.
4. Aturan adopsi (ditetapkan sebelum mengukur). C4c (malas, revisi `C4c`, seed 1-6, 40,000 ns, bawaan Quartus)
   diadopsi sebagai konfigurasi C4 hanya bila semuanya terpenuhi:
   - benar (test plan V1-V8 termasuk butir 5c, kedua simulator) dan bukti batas formal PASS dengan kontrol negatifnya
     gagal;
   - siklus NTT / INTT konstan dan persis 119 / 375;
   - ALM ≤ 12.573 di setiap seed;
   - timing terpenuhi pada 40,000 ns di setiap seed;
   - median atas seed 1-6 dari Fmax slow-corner terendah di atas 34,84 MHz (puncak rentang seed 5b Barrett,
     `evidence/phase05/5b/selection_worksheet.md`);
   - ADR 0012: t_NTT dan t_INTT pada median Fmax itu lebih baik dari Barrett 5b pada median Fmax-nya (34,515 MHz):
     t_NTT < 3,448 µs dan t_INTT < 10,865 µs (119 / 34,515 dan 375 / 34,515, perhitungan tim).
   Bila ada syarat yang gagal, C4c dilaporkan seperti terukur dan tidak diadopsi; C4b-B tetap konfigurasi C4.

## Konsekuensi
- Hanya file baru (`rtl/arith/` varian Barrett dengan operand malas 13 bit, butterfly malas, logika I/O untuk bukti
  formal; parameter `ntt_core_c4` yang bawaannya perilaku saat ini; pembungkus `ntt_core_c4c.sv`); C4a / C4b-B /
  C4b-M tetap harus lolos tanpa perubahan setelah perubahan inti.
- Delay line sisi melebar dari 12 menjadi 13 bit per lajur (register / bit M10K bisa naik; diukur).
- Enam kompilasi Quartus (seed 1-6), satu per satu.

## Bukti
- `evidence/phase05/5c/precheck_critical_path.md`
- `evidence/phase05/5b/selection_worksheet.md`
- `docs/decisions/adr/ADR-0011-*.md` (D3, D6), `ADR-0012-*.md`, `ADR-0013-*.md`

## Hasil (ditambahkan 2026-10-01 setelah sapuan; keputusan di atas tidak berubah)
- Aturan adopsi diterapkan tanpa perubahan pada seed 1-6 (`evidence/phase05/5c/selection_worksheet.md`).
  Median Fmax 33,100 MHz (aturan: di atas 34,84 MHz); t_NTT 3,595 us dan t_INTT 11,329 us (aturan: di bawah
  3,448 / 10,865 us). Kebenaran, siklus 119 / 375, ALM, dan timing pada 40 ns lolos. C4c tidak diadopsi; C4b-B tetap
  konfigurasi C4.
- Perubahan D6 (operand kedua [0, 2q)) hanya berlaku untuk eksperimen C4c (`modmul_barrett_lazy.sv`,
  `ntt_core_c4c.sv`). Konfigurasi C4 mempertahankan kontrak D6 [0, q) x [0, q).
- Pemeriksaan jalur baseline sebelum RTL yang disyaratkan instruksi 5c dicatat di
  `evidence/phase05/5c/precheck_critical_path.md` (diukur sebelum RTL 5c apa pun ditulis).
- Tidak ada seed yang ditambah dan aturan tidak diubah setelah mengukur.
