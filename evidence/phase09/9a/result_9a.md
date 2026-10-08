<!-- claim-lint: skip-file (internal block report, not proposal text) -->
# Laporan blok Fase 9a: codec koefisien <-> byte (`mlkem_pack`, `mlkem_unpack`)

- Status: SELESAI (STOP setelah blok, ADR 0032). Ini checkpoint blok, bukan hasil fase: `docs/results/phase09.md` datang di akhir Fase 9 dan kotak Approval-nya milik tim.
- Tanggal (UTC): 2026-10-03. Pekerjaan ada di working tree dan belum di-commit (chat 2026-10-03: commit dibuat saat pekerjaan selesai).
- Rencana dan aturan: `test_plan_9a.md` (ditulis sebelum RTL; Amandemen A1 mencatat temuan di bawah). Rencana blok: `../phase9_plan.md`. Hasil simulasi hanya simulasi; tidak ada di sini yang hasil papan.

## 1. Hasil
Dua blok streaming kecil, keduanya tepat terhadap `primitives` golden yang tidak diubah (`compress`, `decompress`, `byte_encode`, `byte_decode`): `rtl/mlkem/mlkem_pack.sv` (256 koefisien -> Compress_d -> ByteEncode_d, `32 d` byte) dan `rtl/mlkem/mlkem_unpack.sv` (`32 d` byte -> ByteDecode_d -> Decompress_d, 256 koefisien), d dalam {1, 4, 10, 12}, ditambah pembungkus `rtl/mlkem/mlkem_codec_top.sv`. Compress dan Decompress tidak berisi pembagian dan tidak ada kendali yang bergantung data (konstanta dibuktikan pada seluruh domain masukan 3,329 nilai).

## 2. Verifikasi (MEASURED, simulasi dan formal; `verify.md`, `formal.md`)
| Test | Hasil |
|---|---|
| V1 lint: Verilator `-Wall` dan slang pada pack, unpack, dan pembungkus | 0 peringatan, 0 error |
| V2 model codec golden lawan primitives golden yang tidak diubah (semua x untuk compress, semua y untuk decompress, semua 4,096 nilai 12-bit) | 7 lulus |
| V3-V7 cocotb, Icarus dan Verilator: polinomial acak dan khusus, 9 pasangan mode back-pressure / jeda, compress menyeluruh (setiap x, d = 1, 4, 10), decompress menyeluruh (setiap y) dan setiap nilai 12-bit, round trip, start / dsel saat sibuk diabaikan, reset di tengah run, siklus konstan | 13/13 di setiap simulator |
| V8 kontrol negatif (NC-RND, NC-ORD, NC-MOD, NC-CNT) | masing-masing gagal pada test yang dinamai untuknya, di kedua simulator (4/4 masing-masing) |
| V9 formal (SymbiYosys, yosys-slang): P1-P5 untuk packer, U1-U6 untuk unpacker | keduanya PASS (basecase dan induksi); kontrol NC-P2 dan NC-U6 FAIL; NC-P1 dan NC-U1 memberi UNKNOWN pada bukti (pelanggaran melewati kedalaman 40) dan FAIL pada BMC kedalaman 300 |
| V11 siklus per polinomial, sink selalu siap, tanpa jeda (identik untuk setiap nilai data satu d) | pack 261 / 261 / 325 / 389 dan unpack 259 / 259 / 323 / 387 untuk d = 1 / 4 / 10 / 12 |

## 3. Quartus (MEASURED, kernel-only, virtual pin, 25.1std Lite, `selection_worksheet.md`, `quartus_CD*.md`)
- Seed 1-6 pada 40.000 ns: ALM 298-299 (median 299.0), register 192-193, DSP 2, memori blok 0 bit, timing terpenuhi di setiap seed (setup terburuk 30.046 ns, hold terburuk 0.166 ns); Fmax slow corner terendah median 105.630 MHz (100.46-110.38).
- Informasi: CD-20 (20.000 ns, seed 1): timing terpenuhi (setup terburuk 10.952 ns), Fmax 110.52 MHz.
- Peringatan: Critical Warning 15725 (port clock diberi makan virtual pin) di setiap kompilasi, seperti semua kompilasi kernel-only sebelumnya; tidak ada yang diabaikan.

## 4. Temuan dan penyimpangan (semuanya di Amandemen A1 test plan)
1. Kontrol batal (NC-CNT) akibat driver yang tidak pernah menawarkan lebih dari jumlah tepat: diperbaiki di driver sebelum run akhir; run awal bukan evidence.
2. Nilai X dari register data yang tidak di-reset dan dibaca driver: ditangani di driver (nilai terselesaikan diwajibkan setiap kali valid). RTL tidak berubah.
3. Draf formal berisi placeholder tautologi di P4; diganti persamaan keseimbangan bit yang tepat sebelum run bukti pertama. Run bukti packer pertama gagal induksinya sampai invarian "counter DUT sama dengan counter black-box" ditambahkan; bukti akhir memakan 17 s (packer) dan 12 s (unpacker).
4. ESTIMATE meleset: siklus pack dan unpack untuk d = 1 dan 4 (diperkirakan sekitar 36 / 132 dan 256 / 128, terukur 261 / 261 dan 259 / 259): d kecil dibatasi masukan satu koefisien per siklus. d = 10 dan 12 cocok (dibatasi aliran byte).
5. Harapan dua kontrol formal diubah dari "FAIL" menjadi "UNKNOWN pada bukti, FAIL pada BMC kedalaman 300" setelah run pertama menunjukkan UNKNOWN, dengan kontrol NC-B Fase 3 sebagai preseden; properti tidak dilemahkan.

## 5. Yang tidak ditunjukkan ini
Bukan hasil papan. Codec belum punya antarmuka memori (9c). Nilai di luar [0, q-1] pada masukan packer berada di luar domainnya dan tidak diuji. Invarian siklus ditunjukkan dalam simulasi, bukan di perangkat keras. Tidak ada klaim tentang side channel.

## 6. Biaya untuk anggaran 9c
Port tb memindahkan satu koefisien per siklus (256 per polinomial); packer butuh 389 siklus per polinomial d = 12. ESTIMATE (perhitungan tim) waktu encoding dalam KeyGen: 6 polinomial t_hat dan s_hat pada d = 12 sekitar 6 x 389 = 2,334 siklus bila tidak tumpang tindih, dibanding 6,344 siklus aritmetika K-PKE KeyGen (8d, MEASURED): itu biaya yang diputuskan di 9c (tumpang tindih dengan aritmetika, keluaran lebih lebar) dan bukan hasil.

## 7. Keputusan untuk tim
Tidak ada yang terbuka dari blok ini. Blok berikutnya adalah 9b (bagian hash dan FO); dimulai saat tim berkata begitu (ADR 0032).
