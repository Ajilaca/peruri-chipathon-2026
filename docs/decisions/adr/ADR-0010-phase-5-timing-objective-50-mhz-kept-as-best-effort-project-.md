# ADR 0010: Tujuan timing Fase 5: 50 MHz tetap sebagai target proyek terbaik-upaya; ekspektasi ADR 0006 dikoreksi

- Status: Accepted
- Tanggal: 2026-10-01
- Diputuskan oleh: Faza Dzil, Team J5 (arah dinyatakan dan dikonfirmasi pada sesi 2026-10-01)

## Konteks
- ADR 0006 (Accepted) menetapkan 40,000 ns sebagai milestone Fase 4 dan 20,000 ns (50 MHz) sebagai tujuan akhir
  "setelah Fase 5", dan mengharapkan pencapaian 50 MHz memerlukan kerja aritmetika Fase 5 selain pipelining.
  Ekspektasi itu berasal dari rincian jalur P = 0, di mana pembagi (`%` di `modmul_reduce`) sekitar 44 ns
  (`evidence/phase04/k1_l8_worst_path_breakdown.md`).
- Fase 5 (`docs/ROADMAP.md`) menjaga jadwal, memori, L, dan P tetap; hanya unit `rtl/arith/` yang berubah.
- Bukti baru pada C3-P6 terpilih (`evidence/phase05/baseline/c3p6_critical_path.md`):
  - MEASURED: 300 jalur setup terburuk (Slow 1100mV 100C, seed bawaan, 40,000 ns) semuanya mulai dari register
    arbitrasi slot memori; yang terburuk (slack +10,753 ns) adalah decode baca memori + read mux sekitar 21,3 ns,
    lalu masukan butterfly `sub_mod(b, a)` sekitar 4,3 ns, lalu pengali DSP sekitar 3,7 ns. Tidak ada jalur di dalam
    reducer di antara 300 itu; segmen reducer punya slack +23,6 sampai +24,5 ns.
  - INFERENCE: bagian pembacaan memori saja lebih panjang dari 20 ns, jadi dengan memori, jadwal, L, dan P tetap,
    perubahan aritmetika Fase 5 tidak bisa mencapai 20,000 ns. Menghapus `sub_mod` seluruhnya akan menyisakan segmen
    itu sekitar 25 ns (ESTIMATE), sekitar 40 MHz.

## Opsi yang dipertimbangkan
1. Mempertahankan 50 MHz sebagai target proyek, terbaik-upaya, bukan gerbang Fase 5; koreksi ekspektasi ADR 0006;
   kerjakan pekerjaan yang menyentuh memori / P / jadwal sebagai fase atau sub-fase terpisah setelah 5a/5b, dengan
   ADR dan test plan sendiri.
2. Meninggalkan 50 MHz dan menetapkan clock proyek di 40,000 ns yang terpenuhi (25 MHz, target eksperimen menurut
   ADR 0006).
3. Memperluas lingkup Fase 5 untuk mencakup perubahan memori / P / jadwal sekarang. Bertentangan dengan roadmap
   "jadwal, memori, L, dan P tetap" dan mencampur efek aritmetika dan memori dalam satu himpunan pengukuran.

## Keputusan
1. 50 MHz (20,000 ns) tetap menjadi target timing proyek, secara terbaik-upaya. Bukan jaminan dan bukan gerbang
   Fase 5.
2. Ekspektasi ADR 0006 dikoreksi: mencapai 50 MHz tidak diharapkan dari aritmetika Fase 5 saja, karena jalur kritis
   C3-P6 ada di jalur pembacaan memori (MEASURED, Konteks). Teks ADR 0006 tidak diubah; ADR ini mencatat koreksinya.
3. Pekerjaan yang mengubah memori, P, atau jadwal (misalnya register di dalam read mux, P > 7 dengan stall, register
   jalur tulis, memori baca-sinkron) dikerjakan sebagai fase atau sub-fase terpisah setelah 5a/5b, dengan ADR dan
   test plan sendiri (aturan seleksi ditulis sebelum mengukur), verifikasi ulang bit-exact / siklus konstan / hazard
   (kontrol negatif di luar slack tetap harus gagal) dan kompilasi pada 20,000 ns dengan slack dilaporkan per segmen.
   Nama dan posisinya di roadmap masih terbuka dan akan diputuskan tim.
4. Fase 5 (5a-5d) berjalan seperti di roadmap: aritmetika benar dan terukur; Fmax, slack, dan ALM dilaporkan
   terhadap C3-P6. Fase 5 lolos atau gagal pada kriteria PASS roadmap, bukan pada 50 MHz.

## Konsekuensi
- "50 MHz setelah Fase 5" tidak lagi menjadi ekspektasi yang dinyatakan di mana pun muncul (konsekuensi ADR 0006,
  catatan serah terima, file hasil, laporan); teks baru harus mengutip ADR ini.
- Keputusan lanjutan diperlukan untuk fase memori / P / jadwal (nama, posisi, tuas, kenaikan siklus yang boleh,
  batas ALM untuk register tambahan). Data yang disiapkan untuknya:
  `evidence/phase05/baseline/stall_cycles.txt` (siklus stall per P, perhitungan tim) dan
  `evidence/phase05/baseline/decision_package.md`.
- Aturan siklus konstan tidak berubah; perubahan P kelak dapat mengubah jumlah siklus (119 / 375), yang akan dicatat
  di ADR-nya sendiri.
- Tidak boleh ada klaim 50 MHz sampai kompilasi Quartus pada 20,000 ns memenuhi timing.

## Bukti
- `evidence/phase05/baseline/c3p6_critical_path.md`, `c3p6_top300_path_classes_slow100.txt`
- `evidence/phase04/quartus_C3-P6.md`, `seed_sweep.md`
- `evidence/phase04/k1_l8_worst_path_breakdown.md`
- `docs/decisions/adr/ADR-0006-phase-4-target-clock.md`, `docs/decisions/adr/ADR-0009-phase-4-final-decision-l-8-p-6-c3-p6-and-a-30-alm-design-bud.md`
