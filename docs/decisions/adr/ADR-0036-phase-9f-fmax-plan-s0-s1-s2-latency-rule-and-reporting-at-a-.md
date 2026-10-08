# ADR 0036: Rencana Fmax Fase 9F S0-S1-S2: aturan latensi dan pelaporan pada batasan 15 ns di samping 40 ns

- Status: Accepted
- Tanggal: 2026-10-04
- Diputuskan oleh: Faza Dzil (Team J5), chat 2026-10-04

## Konteks
Faza Dzil meminta rencana untuk menaikkan Fmax dengan anggaran ALM 20.000 (chat 2026-10-04). Jalur kritis inti 9M-1
diukur (`evidence/phase9m/critical_paths_MW.md`, MEASURED): pada 20 ns semua 300 jalur setup terburuk ada di dalam dua
permutasi Keccak-f[1600] C5 (195 di instans hash, 105 di sponge sampler mesin; slack terburuk +4,355 ns); di luar
keduanya desain mengizinkan sekitar 69 MHz (INFERENCE). ADR 0010 menyebut pembacaan memori sebagai jalur kritis Fase 5;
itu tidak lagi menjadi batas inti penuh. K0 (satu ronde per siklus) lebih cepat sebagai blok (median 67,7 MHz pada
40 ns, 76,3 MHz pada 20 ns, MEASURED Fase 7 dan 8a) tetapi menambah siklus. Fmax yang dilaporkan bergantung pada
batasan (48,9 MHz pada 40 ns, 64,0 MHz pada 20 ns, desain sama).

## Opsi yang dipertimbangkan
Rencana yang diusulkan di chat 2026-10-04 (semua penghematan dan nilai Fmax adalah ESTIMATE): S0 sapuan batasan (18,
16, 15 ns; seed 1-2) dan upaya kinerja-tinggi Quartus pada inti 9M-1, tanpa perubahan RTL; S1 sponge K0 di kedua
tempat (instans hash dan sampler mesin), sekitar 13.200-13.800 ALM, Fmax sekitar 65-72 MHz pada batasan 15 ns, siklus
sekitar +450 per operasi; S2 menyerang batas berikutnya yang ditemukan setelah S1 (keluaran hash ke register file, atau
pembacaan memori NTT), +100 sampai +800 ALM; S3 (opsional, setelah pembekuan) sampler K0 kedua (butir 5). Opsi yang
tidak diambil: melaporkan Fmax hanya pada 40 ns (menyembunyikan batas sebenarnya); menilai dari Fmax saja (K0 menambah
siklus, jadi Fmax lebih tinggi belum tentu memberi latensi lebih rendah).

## Keputusan
Faza Dzil, chat 2026-10-04 (menjawab tiga pertanyaan): "saya setuju semua".
1. Urutan S0 -> S1 (-> S2 bersyarat pada apa yang ditunjukkan S1) disetujui; S3 tetap ide untuk pekerjaan mendatang.
2. Aturan adopsi langkah Fmax berdasarkan latensi, t = siklus / Fmax, untuk KeyGen, Encaps, dan Decaps, bukan Fmax saja.
3. Fmax dilaporkan pada batasan 15 ns di samping gerbang 40 ns (seed 1-6, timing statis kernel-only, diberi label
   demikian). Ini perubahan kebijakan pelaporan: hasil 40 ns tetap menjadi gerbang Fase 5-9 (ADR 0011 D1, ADR 0017);
   angka 15 ns adalah informasi (seperti angka 20 ns, ADR 0010) dan tidak pernah disajikan sebagai clock papan.

## Konsekuensi
Setiap langkah punya test plan dan aturan sendiri yang ditulis sebelum RTL atau kompilasinya, verifikasi yang sama
seperti butir 1-3 (ACVP 100 % di kedua simulator, siklus konstan, formal, Quartus seed 1-6), dan ADR Proposed untuk
adopsinya; tim menerima. Anggaran ALM 20.000 adalah batas rencana (inti 9M-1 memakai 17.654 ALM, median). Sebelum
pembekuan (2026-10-07) sasarannya S0 dan S1; S2 hanya bila S1 menunjukkan batas sederhana. Tidak ada klaim clock papan:
inti yang memenuhi 15 ns pada timing statis kernel-only tidak otomatis di-clock lebih cepat, dan clock sistem DE10-Nano
memerlukan keputusan PLL di Fase 10 (bukan bagian rencana ini). Butir 4 dan 5 ADR 0034 tetap pekerjaan mendatang.

## Bukti
`evidence/phase9m/critical_paths_MW.md`, `evidence/phase9m/batch1/9m2/result_9m2.md` (20 ns, seed 1-6),
`evidence/phase08/8a/` dan `evidence/phase07/` (blok K0 dan C5), `docs/decisions/adr/ADR-0010-*` dan `ADR-0034-*`.
