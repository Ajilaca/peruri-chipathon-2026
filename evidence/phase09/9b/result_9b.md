<!-- claim-lint: skip-file (internal block report, not proposal text) -->
# Laporan blok Fase 9b: pembungkus hash (G, H, J) dan perbandingan FO / pemilihan kunci

- Status: SELESAI (STOP setelah blok, ADR 0032). Checkpoint blok, bukan hasil fase; `docs/results/phase09.md` datang di akhir Fase 9 dan kotak Approval-nya milik tim.
- Tanggal (UTC): 2026-10-03. Pekerjaan ada di working tree dan belum di-commit (chat 2026-10-03: commit dibuat saat pekerjaan selesai).
- Rencana dan aturan: `test_plan_9b.md` (ditulis sebelum RTL; Amandemen A1 mencatat temuan di bawah), `../phase9_plan.md` (Amandemen A1: antarmuka word, tanpa byte feeder). Hasil simulasi dan formal bukan hasil papan.

## 1. Hasil
`rtl/mlkem/mlkem_hash.sv` (H = SHA3-256, G = SHA3-512, J = SHAKE256 dengan 32 byte, pada aliran word 64-bit; squeeze SHAKE dihentikan setelah 4 word; parameter `CORE_R2` memilih sponge C5 atau sponge K0), `rtl/mlkem/mlkem_fo_cmp.sv` (pembandingan waktu-konstan dua ciphertext 136-word dan pemilihan mask K' atau K_bar; tanpa keluar dini, tanpa cabang pada data) dan pembungkus `rtl/mlkem/mlkem_hash_fo_top.sv`. Digest sama dengan `primitives.H/G/J` golden yang tidak diubah (hashlib); perbandingan sama dengan model bentuk-perangkat-keras `tb/golden/fo_model.py`, yang sama dengan `ml_kem_decaps_internal` golden yang tidak diubah dari ujung ke ujung.

## 2. Verifikasi (MEASURED; `verify.md`, `formal.md`, `formal_vacuity_check.md`)
| Test | Hasil |
|---|---|
| V1 lint: Verilator `-Wall` (kedua inti sponge) dan slang | 0 peringatan, 0 error |
| V2 model FO golden lawan `ml_kem_decaps_internal` (setiap dari 8,704 perubahan satu bit untuk pilihan; 40 perubahan acak dari ujung ke ujung) | 3 lulus |
| V3, V4 hash, kedua inti sponge: empat panjang Algoritma 16-18, 16 panjang batas pada rate semua mode dan panjang acak, 9 pasangan mode back-pressure / jeda, start / sel / len saat sibuk diabaikan, reset di tengah run, J lalu H lalu G beruntun | 6/6 per inti di setiap simulator |
| V5 compare: pasangan sama dan acak, setiap dari 8,704 selisih satu bit, beat pertama / terakhir / semua, kunci khusus, start saat sibuk, reset, hasil ditahan setelah done | 5/5 di setiap simulator |
| V6 siklus konstan (hash per operasi; compare untuk masukan sama, bit-pertama, bit-terakhir, acak, dan semua-berbeda) | identik |
| V7 kontrol negatif (NC-STOP, NC-LAST, NC-SEL, NC-MASK, NC-SWAP, NC-EARLY) | masing-masing gagal pada test yang dinamai untuknya, di kedua simulator |
| V8 formal: pembungkus hash H1-H5 (dengan stub protokol sponge) dan compare F1-F4; run cover; kontrol | kedua bukti PASS; kedua run cover mencapai setiap state yang dicakup; NC-H1, NC-H5, NC-F1, NC-F3, NC-F4 FAIL seperti disyaratkan |
| V10 siklus, sink selalu siap, tanpa jeda | G 33 byte 30, G 64 byte 33, H 1,184 byte 282, J 1,120 byte 274 (C5); 42, 45, 390, 382 (K0); compare 137 |

## 3. Quartus (MEASURED, kernel-only, virtual pin, 25.1std Lite; `selection_worksheet.md`, `quartus_HF*.md`)
- Seed 1-6 pada 40.000 ns, sponge C5: ALM 6,712-6,745 (median 6,734.5), register 1,976, DSP 0, memori blok 0 bit, timing terpenuhi di setiap seed (setup terburuk 19.095 ns, hold terburuk 0.161 ns); Fmax slow corner terendah median 50.625 MHz (47.84-52.07).
- Informasi: HF-20 (20.000 ns): timing terpenuhi (setup terburuk 3.843 ns), Fmax 61.89 MHz. HF-K0 (sponge K0, 40.000 ns, seed 1): 4,221 ALM, 1,977 register, timing terpenuhi (setup terburuk 25.719 ns), Fmax 70.02 MHz.
- Critical Warning 15725 (port clock diberi makan virtual pin) di setiap kompilasi, seperti semua kompilasi kernel-only sebelumnya; tidak ada yang diabaikan.

## 4. Temuan dan penyimpangan (semuanya di Amandemen A1 test plan)
1. Bukti vakum, ditemukan oleh pemeriksaan cover dan dibuang. Stub sponge pertama untuk bukti formal punya sinyal bebas yang diperlakukan alat sebagai konstanta, sehingga bukti memberi PASS tanpa pernah mencapai squeeze. Stub dikoreksi, pernyataan cover dan run mode cover ditambahkan ke runner, dan bukti serta kontrol dijalankan ulang. Stub formal lain di repository yang memakai sinyal bebas diperiksa: sinyal bebas stub sampler 8c memang bebas (cover tercapai; state PWMS sendiri tidak tercapai pada kedalaman 140 atau 20, efek kedalaman, jadi properti PWMS 8c bertumpu pada induksi, bukan pada jejak), dan stub Fase 3 dikonfirmasi bebas oleh kontrolnya sendiri (`formal_vacuity_check.md`). Tidak ada hasil Fase 6-8 yang berubah karenanya.
2. Pembungkus hash dibuktikan dengan stub protokol sponge karena sponge nyata membuat induksi terlalu lambat (dihentikan setelah 30 menit pada langkah 20); kontrol sponge sendiri dicakup formal Fase 8a dan digest-nya oleh simulasi terhadap hashlib. Modul perbandingan dibuktikan apa adanya.
3. Teks kontrol (NC-EARLY) tidak dikompilasi di Icarus (dipakai sebelum dideklarasikan): diperbaiki; setiap run yang dilaporkan dibuat setelah perbaikan.
4. Pemeriksaan ESTIMATE: siklus hash dan compare cocok dengan ESTIMATE dalam beberapa siklus; pembungkus ditambah perbandingan menambah sekitar 570 ALM pada sponge C5 (INFERENCE).

## 5. Yang tidak ditunjukkan ini
Bukan hasil papan. Blok belum punya buffer dan perakitan pesan (9c). Kendali sponge di dalam bukti pembungkus di-stub (butir 2). Pemeriksaan masukan tidak ada di RTL (ADR 0031). Nilai di luar panjang yang dinyatakan (pesan di atas 65,535 byte) tidak dicakup. Invarian siklus ditunjukkan hanya dalam simulasi.

## 6. Biaya untuk anggaran 9c (ESTIMATE, perhitungan tim, dari siklus MEASURED di atas)
Hash KeyGen: G(d || 3) sekitar 30 + H(ek) sekitar 282 = sekitar 312 siklus; Encaps: H(ek) sekitar 282 + G sekitar 33 = sekitar 315; Decaps: G sekitar 33 + J sekitar 274 + compare 137 = sekitar 444 siklus (ditambah enkripsi ulang mesin K-PKE); semuanya dengan buffer word yang mengirim satu word per siklus. Ini biaya yang akan ditempatkan di jadwal 9c dan bukan hasil.

## 7. Keputusan untuk tim
Opsional, tidak memblokir: instans hash dapat memakai sponge C5 (bawaan, ADR 0027: 6,745 ALM dan median 50.6 MHz di sini) atau sponge K0 (4,221 ALM dan 70.0 MHz pada seed 1, 26 siklus per permutasi bukan 14). Waktu hashing adalah bagian kecil dari operasi pada kedua pilihan (angka di bagian 3 dan 6); penghematan pilihan K0 sekitar 2,500 ALM. Tidak diputuskan di sini; beri tahu bila ingin dijadikan butir PENDING.
Blok berikutnya adalah 9c (pengendali dan semua grup ACVP); dimulai saat tim berkata begitu (ADR 0032).
