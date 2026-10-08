# ADR 0012: Aturan untuk pekerjaan timing setelah Fase 5: kenaikan siklus dinilai dari waktu terukur, batas 12.573 ALM dipertahankan

- Status: Accepted
- Tanggal: 2026-10-01
- Diputuskan oleh: Faza Dzil, Team J5 (sesi 2026-10-01)

## Konteks
ADR 0010 mempertahankan 50 MHz sebagai target terbaik-upaya dan memindahkan pekerjaan memori, P, atau jadwal ke fase
atau sub-fase terpisah setelah 5a/5b. Pekerjaan itu mungkin memerlukan pipeline lebih dalam dengan stall (siklus lebih
banyak) dan register lebih banyak (ALM lebih banyak). Tim meminta data sebelum menetapkan batas; datanya ada di
`evidence/phase05/baseline/decision_package.md` dan `stall_cycles.txt`:
- MEASURED: C3-P6 NTT 119 / INTT 375 siklus pada 34,19 MHz (slow corner terendah) → t_NTT 3,481 µs, t_INTT
  10,968 µs (INFERENCE); C3-P6 10.484-10.516 ALM pada seed 1-6, margin ke 12.573 sekitar 2.060 ALM.
- perhitungan tim / ESTIMATE: P = 7 tidak memerlukan stall (+1 siklus); P = 8 memerlukan 1 stall (+3 siklus, 2,5 %
  NTT); P = 12 memerlukan +12 siklus (10,1 %); jumlah stall hanya bergantung pada P, arah, dan jadwal alamat tetap,
  bukan pada data.
- MEASURED biaya tahap Fase 4: −27 / +743 / +66 ALM untuk P0→P2 / P2→P4 / P4→P6; biaya bergantung pada posisinya.

## Opsi yang dipertimbangkan
(a) Kenaikan siklus: batas persentase tetap (misalnya ≤ 5 % atau ≤ 10 %), atau aturan berbasis waktu.
(b) ALM: mempertahankan 12.573 sebagai batas untuk register tambahan, atau meninjaunya.

## Keputusan
1. Kenaikan siklus (a): kenaikan jumlah siklus NTT / INTT dapat diterima hanya bila t_NTT dan t_INTT yang dihitung
   dengan Fmax yang benar-benar terukur (Fmax slow-corner terendah dari kompilasi Quartus di repository ini, aturan
   sama seperti ADR 0007) keduanya lebih baik dari baseline C3-P6 (3,481 µs / 10,968 µs), dan sifat siklus konstan
   tetap berlaku (CRG-7: jumlah siklus identik untuk setiap masukan, kedua simulator). Tidak ada batas persentase
   tetap. Clock hipotetis (40 / 45 / 50 MHz) tidak pernah dipakai untuk pemeriksaan ini.
2. ALM (b): register tambahan boleh memakai ruang yang tersedia, tetapi total inti NTT tetap ≤ 12.573 ALM
   ("ALMs needed" fitter, ADR 0009) sebagai batas keras. Bila perubahan timing memerlukan lebih, tidak diubah
   diam-diam: dibawa ke tim sebagai keputusan baru.
3. Nama dan posisi fase yang mengerjakan ini tetap terbuka (PENDING #19).

## Konsekuensi
- Jumlah siklus baru apa pun (menggantikan 119 / 375) dicatat di ADR fase itu bersama waktu terukurnya.
- ALM yang dihemat 5a / 5b dihitung sebagai ruang untuk register tambahan di dalam batas 12.573 yang sama.
- Angka 12.573 tetap anggaran desain inti NTT, bukan anggaran sistem; Keccak, sampler, pengendali, encode/compress,
  penyimpanan, jembatan, dan SignalTap BELUM DIUKUR.

## Bukti
- `evidence/phase05/baseline/decision_package.md`, `stall_cycles.txt`
- `evidence/phase04/quartus_C3-P6.md`, `seed_sweep.md`
- `docs/decisions/adr/ADR-0007-*.md`, `ADR-0009-*.md`, `ADR-0010-*.md`
