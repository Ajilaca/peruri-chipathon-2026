# ADR 0027: Fase 8a: dua ronde Keccak per siklus (C5) - hasil aturan

- Status: Accepted
- Tanggal: 2026-10-03
- Diputuskan oleh: Jo, Team J5, chat 2026-10-03: "ya terima" (balasan atas usulan menerima C5, W2, STREAM, dan OVERLAP karena semuanya diadopsi aturannya dan terukur) (header sebelumnya "Proposed / menunggu keputusan tim")

## Konteks
- ADR 0026 (Accepted, Jose): langkah bagian 8a, 8b, 8c, 8d semuanya dikerjakan. 8a menggantikan inti permutasi K0
  (Fase 7) dengan inti yang menghitung dua ronde per siklus (konfigurasi C5). Test plan dan aturan adopsi ditulis dan
  di-commit sebelum RTL 8a apa pun dan sebelum pengukuran 8a apa pun (`evidence/phase08/8a/test_plan_8a.md`, commit
  9bdbad6).
- Hanya file baru: `rtl/keccak/keccak_f1600_r2.sv`, `keccak_sponge_r2.sv`; RTL K0 tidak diedit. File test K0
  mendapat parameter lingkungan yang nilai bawaannya mereproduksi K0; verifikasi K0 dijalankan ulang sebagai regresi
  dan lolos.

## Opsi yang dipertimbangkan
(a) Mengadopsi C5 sebagai inti permutasi Keccak untuk 8b-8d dan Fase 9. (b) Mempertahankan K0 (satu ronde per siklus).
(c) Lainnya.

## Keputusan
Hasil aturan yang ditetapkan lebih dulu (`scripts/quartus/select_8a.py`, tanpa toleransi): C5 diadopsi oleh aturan
(semua syarat PASS). Penerimaan sebagai konfigurasi milik tim (C5): catatan ini sebelumnya Proposed.

## Konsekuensi
- MEASURED (Quartus, seed 1-6, 40,000 ns; `evidence/phase08/8a/selection_worksheet.md`): ALM 6.152-6.169 (median
  6.167,0; K0 3.558-3.572, median 3.566,5), register 1.652 (K0 1.653), 0 M10K, 0 DSP; timing terpenuhi di setiap seed;
  median Fmax slow-corner terendah 50,655 MHz (rentang 47,38-51,67) lawan K0 67,675 MHz (56,99-70,39).
- Sebuah permutasi adalah 14 siklus di sponge sebagai ganti 26 (12 sibuk sebagai ganti 24); t per permutasi pada
  median Fmax adalah 14 / 50,655 = 0,2764 us lawan 26 / 67,675 = 0,3842 us (-28 %, perhitungan tim). Satu panggilan
  utuh menyusut lebih sedikit (H(ek) 1184 B: 281 siklus lawan 389).
- Siklus Keccak untuk satu operasi ML-KEM-768 (perhitungan tim dari rumus terukur): sekitar 1.510 / 1.550 / 1.542
  (KeyGen / Encaps / Decaps, median atas 200 rho) lawan sekitar 2.026 / 2.078 / 2.070 dengan K0, tanpa tumpang-tindih.
- Biaya: +73 % ALM (sekitar +2.600 ALM); Fmax inti permutasi turun 25 %, jadi sistem yang jalur kritisnya inti Keccak
  akan kehilangan Fmax sebesar itu; saat ini inti NTT (S10: median 44,320 MHz pada 40 ns) lebih lambat dari median C5,
  jadi seluruh desain tidak dibatasi C5 (INFERENCE; belum ada kompilasi sistem).
- Informasi (seed 1, 20,000 ns, bukan bagian aturan): C5-20 6.178 ALM, setup terburuk +4,591 ns (terpenuhi), Fmax
  64,90 MHz; K0-20 3.573 ALM, +6,893 ns, 76,30 MHz.
- Koreksi dicatat untuk Fase 7: angka K0 56,99 MHz di `phase07.md` adalah seed 1 dan terendah dari enam; median atas
  seed 1-6 adalah 67,675 MHz (seed K0 2-6 dikompilasi untuk aturan ini).
- Verifikasi: kedua simulator, semua 24 ronde dibandingkan (state per siklus dan keluaran ronde pertama), 12 siklus
  sibuk untuk setiap state, 306 titik siklus sama dengan rumus dengan p = 14, tiga kontrol negatif gagal, formal K1-K5
  PASS dengan NC-K1 dan NC-K4 gagal. Hanya Critical Warning 15725 (clock virtual pin) pada setiap kompilasi; tidak ada
  yang diabaikan.
- Tidak tercakup: perangkat keras, kompilasi tingkat sistem dengan inti Keccak dan inti NTT bersama, batasan lain.

## Bukti
- `evidence/phase08/8a/` (test plan, verify, formal, cycles, worksheet seleksi, `quartus_C5[-s2..s6].md`,
  `quartus_C5-20.md`), `evidence/phase07/quartus_K0[-s2..s6].md` (baseline), `scripts/quartus/select_8a.py`.
