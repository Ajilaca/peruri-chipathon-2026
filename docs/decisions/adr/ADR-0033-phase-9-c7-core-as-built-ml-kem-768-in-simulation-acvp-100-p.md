# ADR 0033: Fase 9: C7-core seperti dibangun (ML-KEM-768 di simulasi, ACVP 100 persen) dan inti sponge hash

- Status: Proposed
- Tanggal: 2026-10-04
- Diputuskan oleh: menunggu keputusan tim

## Konteks
- Fase 9 membangun inti ML-KEM-768 dalam tiga blok (ADR 0032): 9a codec, 9b pembungkus hash dan pembanding FO, 9c
  pengendali `mlkem_core` (`docs/results/phase09.md`, `evidence/phase09/`). Setiap vektor ACVP terpatok ML-KEM-768
  lolos di kedua simulator (keyGen 25, encapsulation 25, decapsulation 10 termasuk ciphertext yang diubah). Pemeriksaan
  masukan FIPS 203 ada di HPS (ADR 0031). Tidak ada di sini yang merupakan hasil papan.
- Tidak ada aturan adopsi di Fase 9 (tidak ada yang dipilih di antara alternatif terukur), jadi hasilnya dicatat
  sebagai konfigurasi untuk diterima tim; satu-satunya pilihan desain yang terbuka adalah inti sponge instans hash
  (sampler di dalam mesin memakai C5 menurut ADR 0027).
- MEASURED (Quartus kernel-only, seed 1-6; siklus simulasi): `mlkem_core` median 17.620,5 ALM (42 % dari 41.910), 54
  blok RAM, 28 DSP, median Fmax 49,280 MHz, timing terpenuhi pada 40,000 ns di setiap seed; KeyGen 9.035-9.076,
  Encaps 10.691, Decaps 16.623 siklus. Instans hash dengan sponge C5 (pembungkus dan pembanding) adalah 6.734,5 ALM;
  dengan sponge K0 adalah 4.221 ALM (seed 1, informasi, 9b).

## Opsi yang dipertimbangkan
(a) Menerima konfigurasi seperti dibangun: instans hash di sponge C5 (bawaan ADR 0027), encode dan decode serial,
    pemeriksaan masukan di HPS.
(b) Menerimanya dengan sponge K0 di instans hash (`HASH_C5 = 0`): sekitar 2.500 ALM lebih sedikit di blok 9b (seed 1;
    belum dikompilasi untuk seluruh inti), 26 siklus per permutasi sebagai ganti 14: sekitar 100 siklus lebih banyak per
    hash kunci 1.184 byte (MEASURED 389 lawan 282 untuk H(ek) di 9b), kecil dibanding 9.000-16.600 siklus satu operasi.
(c) Meminta optimasi sebelum pembekuan (misalnya menumpangkan encode atau decode polinomial dengan mesin, atau codec
    lebih lebar): belum dimulai; biayanya waktu tim, keuntungannya jumlah siklus lebih kecil (pack dan unpack
    polinomial sekitar 2.300-2.400 siklus dari KeyGen atau Decaps, INFERENCE).
(d) Membuka kembali ADR 0031 dan menaruh pemeriksaan masukan FIPS 203 ke RTL.

## Keputusan
Menunggu keputusan tim (PENDING #33). Rekomendasi asisten, bukan keputusan: (a) atau (b); (c) dan (d) hanya bila
waktu tersisa dan ada papan atau alasan.

## Konsekuensi
- Menerima (a) atau (b) menetapkan arsitektur untuk Bagian 3 proposal dan untuk Fase 10 (integrasi HPS, terhambat
  papan, PENDING #8). Menerima tidak mengizinkan klaim apa pun tentang papan, percepatan terhadap perangkat lunak,
  daya, atau ketahanan side-channel: waktu-konstan berarti jumlah siklus yang tidak bergantung pada rahasia
  (ditunjukkan di simulasi untuk satu kunci enkapsulasi tetap; panjang sampling matriks bergantung pada rho publik).
- (b) memerlukan satu kompilasi lagi untuk seluruh inti (seed 1-6, sekitar satu jam) dan menjalankan ulang uji vektor
  dengan `HASH_C5 = 0`.

## Bukti
`docs/results/phase09.md`, `evidence/phase09/9a/result_9a.md`, `9b/result_9b.md`, `9c/result_9c.md`,
`9c/selection_worksheet.md`, `9b/selection_worksheet.md`, `9c/sim_verilator.md`, `9c/sim_icarus.md`; ADR 0027, 0031,
0032.
