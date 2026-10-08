<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Fase 8b: sampler streaming (SampleNTT dari aliran XOF, CBD dari aliran PRF), lebar keluaran W1 lalu W2 - test plan, gerbang penerimaan, dan aturan pemilihan

Ditulis 2026-10-03, sebelum RTL 8b apa pun dan sebelum pengukuran 8b apa pun (CRG-4). Lingkup: `docs/ROADMAP.md` Fase 8b; ADR 0026 (Accepted: 8a-8d lanjut; setiap sub-langkah punya rencana sendiri dan aturan atau pernyataan "tanpa aturan" yang ditulis sebelum mengukur);
ADR 0019 butir 3 (sampler). Basis: sponge Keccak 8a (`keccak_sponge_r2.sv`, C5) dan Fase 7 (`keccak_sponge.sv`, K0), keduanya tidak diedit. Label: MEASURED, INFERENCE, ESTIMATE, NOT MEASURED, perhitungan tim.
Matematika terkunci (C1): FIPS 203 Algoritma 7 (SampleNTT) dan Algoritma 8 (SamplePolyCBD_eta) dengan q = 3329, n = 256, eta = 2 (ETA1 = ETA2 = 2 untuk ML-KEM-768); hanya cara byte dikonsumsi yang baru.
PENDING #29 (terima C5 atau pertahankan K0) terbuka: pembungkus menerima sponge mana pun lewat parameter, jadi 8b tidak menunggunya.

## 0. Keputusan tim tentang urutan kerja dan kedua lebar
Chat 2026-10-03 (orang yang mengetik tidak menyebut nama; tidak ada pengambil keputusan disebut di sini): "8b melakukan keduanya saja jadi pertama kita test 1 siklus dan setelah itu 2 siklus setelah itu selesai baru kita mulai 8c".
- Tahap W1: satu koefisien per siklus di keluaran (`OUTW` = 1). Dibangun, diverifikasi, dan diukur lebih dulu (revisi Quartus sendiri); evidence-nya diambil pada commit git yang dicatat sebelum kode W2 ada.
- Tahap W2: dua koefisien per siklus (`OUTW` = 2): file yang sama dengan logika packing ditambahkan; diverifikasi dan diukur kedua; aturan pemilihan bagian 5 menentukan lebar mana yang menjadi sampler 8b.
- 8b selesai bila kedua tahap terukur dan aturan diterapkan; lalu STOP (ADR 0026), lalu 8c. W1 dan W2 bukan sub-langkah terpisah dan tidak ada STOP di antara keduanya kecuali sebuah tahap gagal.

## 1. Apa arti "streaming" di sini (tanpa store di antara sponge dan koefisien)
- Word keluaran sponge (64 bit, valid/ready, seperti hari ini) masuk langsung ke jendela byte paling banyak 11 byte dan dari sana ke sampler. Keluaran XOF/PRF tidak pernah ditulis ke memori: angka yang diperiksa adalah M10K = 0 dan DSP = 0.
  (ADR 0019 butir 3 menyebut sampler pertama "non-streaming-optimised"; tidak ada sampler berbuffer yang dibangun di sini, jadi aturan bagian 4 adalah gerbang, dan bagian 5 memilih antara W1 dan W2 saja.)
- File baru (kernel aritmetika dan semua file Keccak tidak dimodifikasi):
  - `rtl/sample/sample_ntt_core.sv`: aliran word masuk; beat koefisien keluar (`coef_data_o` adalah `OUTW` x 12 bit, `coef_valid_o`, `coef_ready_i`, `coef_last_o` pada beat yang memuat koefisien ke-256); `bytes_o` = byte aliran yang dikonsumsi (3 per triple, menghitung triple yang melengkapi
    polinomial bahkan bila kandidat keduanya tidak dipakai: definisi `tb/golden/sampler_model.py`); `done_o`. Per triple (b0, b1, b2): d1 = b0 + 256 (b1 mod 16), d2 = b1 div 16 + 16 b2; sebuah kandidat diterima bila `d < 3329` (perbandingan dengan
    konstanta, tanpa modulo, tanpa pembagian). Sebuah triple memberi 0, 1, atau 2 koefisien; yang kedua dibuang setelah polinomial penuh.
    Sebuah beat selalu memuat `OUTW` koefisien berurutan (indeks OUTW x m ... OUTW x m + OUTW - 1), jadi setiap beat penuh (256 adalah kelipatan kedua lebar).
    W1: triple ditahan sampai koefisien yang diterimanya telah dikeluarkan (sebuah triple memakan max(1, diterima) siklus).
    W2: satu triple diambil per siklus; koefisien yang diterima dan satu koefisien bawaan (0 atau 1 ditahan) membentuk pool 0 sampai 3; sebuah beat dikeluarkan setiap pool mencapai 2, sisanya (paling banyak 1) dibawa.
  - `rtl/sample/cbd2_core.sv`: aliran word masuk, beat keluar; byte k dari 128 byte memberi koefisien 2k (nibble rendah) dan 2k + 1 (nibble tinggi); x = bit0 + bit1, y = bit2 + bit3, f = x - y mod 3329 (lima nilai 3327, 3328, 0, 1, 2; tanpa
    pembagian, tanpa jalur yang bergantung data). W1 mengeluarkan satu koefisien per siklus (256 siklus), W2 satu byte, yaitu dua koefisien, per siklus (128 siklus). Tepat 16 word diambil (word ke-17 blok SHAKE256 136-byte tidak pernah diambil).
  - `rtl/sample/keccak_sampler.sv` (top revisi Quartus): `parameter CORE_R2` memilih `keccak_sponge_r2` (1) atau `keccak_sponge` (0), `parameter OUTW` memilih 1 atau 2; `kind_i` 0 = SampleNTT pada SHAKE128 (`mode_i` 2), 1 = CBD2 pada SHAKE256 (`mode_i` 3); word pesan
    (rho || j || i = 34 byte, atau sigma || N = 33 byte; `len_i` apa pun diizinkan) diteruskan ke sponge; bila polinomial lengkap pembungkus mengeluarkan `stop_i` ke sponge (yang menghapus state-nya) dan menaikkan `done_o`; `abort_i` melakukan hal yang sama kapan saja.
- Jendela byte, register triple, koefisien bawaan, dan state sponge dihapus pada `done_o`, pada `abort_i`, dan pada reset (jendela memuat byte rahasia pada kasus CBD). Reset: asinkron, active low (seperti sponge). Satu domain clock, `clk_i`.
- Lantai, dinyatakan sebagai batas yang diketahui dan bukan hasil: W1 butuh paling sedikit 256 siklus per polinomial; W2 paling sedikit 128 (CBD) dan sekitar satu siklus per triple (SampleNTT, rata-rata 157.8 triple).

## 2. Kasus sudut (ditulis sebelum test; setiap kasus dijalankan untuk `OUTW` = 1 dan untuk `OUTW` = 2)
SampleNTT (tingkat inti, dengan aliran buatan, dan tingkat top dengan aliran XOF nyata):
- kandidat tepat q - 1 = 3328 diterima, tepat q = 3329 ditolak (d1 dan d2 terpisah), 4095 ditolak; d = 0 diterima.
- sebuah triple dengan kedua kandidat ditolak (0 koefisien), tepat satu diterima (hanya d1, hanya d2), keduanya diterima.
- koefisien ke-256 adalah d1 sebuah triple (kandidat kedua tidak dipakai: `bytes_o` tetap menghitung triple itu), dan ke-256 adalah d2 sebuah triple.
- packing W2: bawaan ada dan triple menambah 0, 1, 2; bawaan tidak ada dan triple menambah 0, 1, 2 (keenam ukuran pool 0-3); bawaan tertunda saat koefisien ke-256 tiba (pool 3 pada hitungan 255 dengan kandidat kedua dibuang); run panjang tanpa kandidat diterima saat bawaan ditahan.
- aliran di mana setiap triple diterima dua kali (128 triple, `bytes_o` = 384) dan run panjang triple ditolak (lebih dari 100 beruntun) diikuti yang diterima: tanpa hang, tanpa `done_o` dini.
- ketiga keselarasan sebuah triple terhadap word 8-byte (8 mod 3 = 2): triple sepenuhnya di dalam word, melintasi dua word dengan 1 byte lalu 2 byte, dan dengan 2 lalu 1; setiap dari 56 triple satu blok (168 byte = 21 word).
- polinomial yang butuh tepat 3 dan tepat 4 blok XOF. Satu atau dua blok tidak pernah cukup (2 blok = 112 triple = 224 kandidat < 256), jadi setiap polinomial melintasi paling sedikit dua batas blok (T = 56 dan 112 triple). Dalam 3,000 aliran XOF golden (seed PRNG tetap, diperiksa 2026-10-03) 2,970 butuh 3 blok
  dan 30 butuh 4 (1 %), dengan rata-rata 157.8 triple dan 261.6 siklus keluaran (model W1); nilai rho untuk kasus 4-blok ditemukan dengan pencarian memakai seed PRNG tetap dan didaftar di evidence. Blok ke-5 hanya dapat dicapai dengan aliran buatan di tingkat inti.
- `coef_ready_i` rendah selama run 1, 2, 7, dan 40 siklus pada titik acak, termasuk tepat saat permutasi berjalan dan di batas blok; keluaran ditahan (valid dan data stabil) selama tidak ready; dengan W2 juga saat bawaan ditahan.
- `abort_i` di tengah polinomial, selama absorb, selama permutasi; reset di tengah; `start_i` saat sibuk diabaikan; dua polinomial beruntun dengan rho sama dan berbeda (bawaan satu polinomial tidak boleh bocor ke berikutnya).
CBD:
- setiap nilai nibble 0-15 pada kedua posisi nibble dan di semua 16 word (tabel 16 hasil ditetapkan oleh x - y); aliran semua-nol dan semua-satu; byte one-hot; 128 byte acak dengan seed PRNG tetap.
- word ke-17 tidak diambil (diperiksa dari counter word sponge); keluaran ditahan di bawah back-pressure; abort; reset.
Keduanya: word aliran tiba dengan jeda (`in_valid`/`out_valid` rendah 1-5 siklus pada titik acak, tingkat inti), dan penghapusan jendela setelah `done_o`/`abort_i`/reset.

## 3. Test (dijalankan untuk `OUTW` = 1 di tahap W1 dan lagi, dengan `OUTW` = 2 ditambahkan, di tahap W2)
| ID | Pemeriksaan | Alat | Disyaratkan |
|---|---|---|---|
| V1 | Lint ketiga modul baru (CRG-1, CRG-2), kedua `OUTW` | Verilator `-Wall`, slang | 0 peringatan, 0 error |
| V2 | Model golden `tb/golden/sampler_model.py` sama dengan `primitives.sample_ntt` dan `sample_poly_cbd` yang tidak diubah, termasuk jumlah byte yang dikonsumsi (sudah ditulis; dijalankan ulang) | pytest | semua sama |
| V3 | `sample_ntt_core` terhadap golden pada aliran buatan (setiap kasus bagian 2) dan pada 500 aliran XOF (seed PRNG tetap): 256 koefisien berurutan (beat m memuat koefisien OUTW x m ...), `bytes_o` sama dengan byte yang dikonsumsi golden, `coef_last_o` hanya pada beat terakhir, `done_o` sekali | cocotb, kedua simulator (CRG-3) | semua sama |
| V4 | `cbd2_core` terhadap golden pada setiap kasus nibble dan 500 aliran PRF: 256 koefisien berurutan, 16 word diambil | cocotb, kedua simulator | semua sama |
| V5 | Top `keccak_sampler`, `CORE_R2` = 1 dan 0: SampleNTT untuk rho || j || i dengan 3 x 3 pasangan indeks dan rho acak (500 kasus), CBD2 untuk sigma || N (500 kasus); keluaran sama dengan golden yang diberi `hashlib.shake_128` / `shake_256` pesan yang sama; pola back-pressure bagian 2; `bytes_o` sama; counter permutasi sponge sama dengan jumlah permutasi yang kata golden dibutuhkan (kriteria diperhalus di Amandemen A1, bagian 8) | cocotb, kedua simulator | semua sama |
| V6 | Siklus konstan (CRG-7). CBD: siklus dari `start_i` ke `done_o` identik untuk semua sigma dan N pada satu `len_i` (paling sedikit 3 sigma berbeda per N, 100 titik); SampleNTT: masukan sama dua kali memberi hitungan sama; dengan r = siklus - (W1: jumlah atas triple dari max(1, kandidat diterima); W2: jumlah triple dikonsumsi), keduanya diambil dari golden, r dilaporkan per jumlah blok XOF B (3 atau 4; data publik saja). Diharapkan, tidak disyaratkan: satu nilai r per B dan `CORE_R2` (stall batas blok tetap); bila r bervariasi menurut aliran, variasinya adalah fungsi rho publik dan dilaporkan apa adanya. Jumlah siklus diukur dengan `coef_ready_i` selalu tinggi | cocotb | CBD identik di setiap titik; SampleNTT dapat diulang; tabel r ditulis ke evidence |
| V7 | Penghapusan: setelah `done_o`, `abort_i`, dan reset jendela byte, register triple, dan bawaan terbaca nol (probe khusus test) | cocotb | nol di setiap kasus |
| V8 | Kontrol negatif (salinan khusus test, agar unit test gagal sebagaimana mestinya): NC-LT `d <= q` (menerima 3329); NC-2ND kandidat kedua diterima saat polinomial penuh (atau `bytes_o` tidak menghitung triple itu); NC-ORD urutan byte sebuah word dibalik; NC-CBD f = y - x; NC-17 CBD mengambil word ke-17; NC-STOP pembungkus tidak pernah mengeluarkan `stop_i`; hanya W2: NC-CARRY koefisien bawaan dibuang saat pool 3 terjadi, dan NC-LEAK bawaan tidak dihapus di antara polinomial | cocotb | pemeriksaan GAGAL (setiap kontrol punya pemeriksaan bernama sendiri) |
| V9 | Formal (file baru; SymbiYosys, yosys-slang): S1 `coef_data_o` < 3329 di setiap lajur setiap kali valid; S2 paling banyak 256 koefisien diterima per run dan `coef_last_o` hanya pada beat terakhir; S3 keluaran stabil selama valid dan tidak ready; S4 `bytes_o` tidak pernah menurun dan tidak pernah melebihi word diambil x 8; S5 legalitas FSM dan, setelah `done_o`, tidak ada keluaran valid; S6 (W2) bawaan memuat paling banyak satu koefisien; aliran masukan bebas (byte apa pun, jeda apa pun); kedalaman induksi 30 seperti Fase 7; kontrol NC-S1 (`<=`) dan NC-S2 (koefisien ke-257) harus FAIL | SymbiYosys | PASS; kontrol FAIL |
| V10 | Regresi (CRG-5, CRG-6): `scripts/test/phase7_verify.sh`, `scripts/test/phase8a_verify.sh`, `formal/run/run_formal_phase7.py`, dan `formal/run/run_formal_phase8a.py` hasil tidak berubah; `check_params.py`; di tahap W2 juga seluruh set test W1 dijalankan ulang dengan `OUTW` = 1 (perilaku W1 harus tidak berubah) | skrip | PASS |
| V11 | Quartus (kernel-only, virtual pin): `keccak_sampler`, `CORE_R2` = 1, pada 40.000 ns, seed 1-6 per lebar, satu per satu (revisi berbagi satu .qpf): W1 di tahap W1, W2 di tahap W2; informasi: `CORE_R2` = 0 seed 1 per lebar dan top C5 pada 20.000 ns seed 1 per lebar | `quartus_sh`, `/quartus-report` | evidence diekstrak |

## 4. Gerbang penerimaan (ditetapkan sebelum mengukur; tanpa toleransi; diterapkan pada setiap lebar secara terpisah)
Sebuah lebar sampler streaming pada sponge C5 lolos gerbang hanya bila semua berikut berlaku:
1. V1-V10 PASS dan setiap kontrol gagal seperti disyaratkan, di kedua simulator.
2. Keluaran SampleNTT dan CBD serta `bytes_o` sama dengan golden di setiap titik test; siklus CBD identik di setiap titik; setiap run SampleNTT yang dicatat dapat diulang.
3. M10K = 0 dan DSP = 0 di setiap seed (tanpa buffer antara sponge dan sampler).
4. ALM <= 12,573 di setiap seed (batas kerja ADR 0009, diasumsikan untuk seluruh top dan terbuka bagi tim) dan timing terpenuhi pada 40.000 ns di setiap seed 1-6.
5. Median atas seed 1-6 dari Fmax slow corner terendah pada 40 ns adalah >= 44.320 MHz, median S10, inti NTT/INTT (`docs/decisions/0025-*.md`, MEASURED di Fase 6): sampler tidak boleh membuat sisi Keccak lebih lambat dari inti NTT. (Sponge C5 sendirian 50.655 MHz, MEASURED di 8a.)
Sebuah lebar yang gagal gerbang dicatat sebagai terukur dan tidak diterima, dengan butir yang gagal; tidak ada sampler lain sebagai cadangan, jadi apakah tetap dipertahankan adalah keputusan tim (C5).

## 5. Aturan pemilihan W1 lawan W2 (ditetapkan sebelum pengukuran apa pun; gaya ADR 0012, tanpa toleransi)
Misalkan F median atas seed 1-6 dari Fmax slow corner terendah pada 40 ns top C5, dan c rata-rata siklus dari `start_i` ke `done_o` dengan `coef_ready_i` selalu tinggi: untuk SampleNTT atas 500 aliran yang sama untuk kedua lebar (himpunan V5), untuk CBD atas himpunan V5 (identik di setiap titik).
- t = c / F untuk SampleNTT dan untuk CBD, per lebar. W2 dipilih atas W1 hanya bila: W2 lolos gerbang bagian 4, dan t_W2 < t_W1 untuk SampleNTT dan untuk CBD.
- Selain itu W1 tetap sampler 8b (bila W1 lolos gerbang); bila W1 gagal gerbang dan W2 lolos, W2 dipilih; bila keduanya gagal, 8b dicatat tidak diterima dan tim memutuskan.
- Hasilnya adalah ADR Proposed (seperti 8a); tim menerimanya (PENDING). ALM dan register dilaporkan, bukan bagian pilihan selain batas gerbang.

## 6. ESTIMATE yang ditulis sebelum mengukur (metode dan asumsi; bukan pengukuran)
- Logika sampler (tanpa sponge), W1: sekitar 200-500 ALM dan 150-350 register (jendela 11-byte, register triple, dua inti kecil, pembanding terhadap 3329); M10K 0; DSP 0. Top dengan C5: sekitar 6,400-6,700 ALM (median C5 6,167 ALM MEASURED, 8a).
  W2 menambah pool dan jalur terima kedua: sekitar 100-300 ALM lebih banyak dari W1 dan sekitar 20-50 register lebih banyak. Keyakinan rendah: estimasi Fase 7 sebelumnya meleset dari rentangnya beberapa persen.
- Fmax: jalur baru pendek (pembanding 12-bit, multiplekser byte; W2 menambah penjumlah kecil untuk hitungan pool); top seharusnya tetap dekat sponge, sekitar 47-51 MHz (C5: 47.38-51.67 atas seed 1-6, MEASURED, 8a); W2 mungkin sedikit lebih rendah dari W1.
- Siklus per polinomial dengan C5 dan `coef_ready_i` tinggi (perhitungan tim dari 157.8 triple model golden dan 261.6 siklus keluaran W1 atas 3,000 aliran, ditambah sponge: absorb 34 byte sekitar 21 siklus, stall 14 siklus di setiap dari 2 batas blok yang dilintasi setiap polinomial, 3 pada 1 % kasus):
  SampleNTT W1 sekitar 310 (K0: sekitar 350), CBD W1 sekitar 280; SampleNTT W2 sekitar 210 (sekitar 22 + 158 + 28), CBD W2 sekitar 150 (sekitar 22 + 128). Per operasi, sampling saja (perhitungan tim, tidak diukur): KeyGen 9 SampleNTT + 6 CBD, Encaps 9 + 7, Decaps mengulang sampling Encaps:
  W1 sekitar 4,500 / 4,800 siklus, W2 sekitar 2,800 / 2,900 siklus. Ini melebihi 1,510-1,550 siklus Keccak tabel 8a, yang hanya menghitung transfer word; aritmetika Fase 6 adalah 5,493 (KeyGen) dan 6,810 (Encrypt) siklus. Tumpang tindih (8d) tidak diklaim di sini.

## 7. Tidak dicakup
Perangkat keras (tanpa papan); koneksi ke memori atau sequencer Fase 6 (8c, 8d); organisasi matriks A (8c); lebar di atas 2; `ETA` selain 2; seed selain 6; jumlah siklus operasi penuh (jumlah angka per blok, perhitungan tim sampai Fase 9 menyambungkan blok-blok itu).
Formal mencakup properti kendali dan rentang, bukan digest (itu dicakup simulasi terhadap hashlib).

## 8. Amandemen A1 (2026-10-03, ditulis setelah run penuh pertama V3-V8 dan sebelum run akhir; tidak ada file RTL yang berubah karenanya)
1. Kesalahan test ditemukan pada run smoke pertama (30 kasus), dikoreksi sebelum run tercatat apa pun: V5 membandingkan counter permutasi sponge dengan "jumlah blok yang kata golden dibutuhkan". Versi test pertama mengambil angka itu hanya sebagai ceil(byte dikonsumsi / 168); untuk enam panjang pesan tambahan
   (168, 169, dan 300 byte) sponge juga menyerap floor(len / 168) + 1 permutasi. Test kini memakai floor(len / 168) + 1 + (blok - 1). Kriterianya sama; hitungannya yang salah.
2. Temuan pada run penuh pertama (500 kasus SampleNTT per top, kedua simulator; log verifikasi `evidence/phase08/8b/` run pertama diringkas di sini): dengan sponge K0 (`CORE_R2` = 0), `coef_ready_i` pada mode "runs" (rendah sampai 40 siklus) dan polinomial yang byte terkonsumsinya berakhir 6 byte sebelum akhir blok 3 (498 dari 504), `perm_cnt_o` adalah 4 sementara golden butuh 3. Jendela byte sudah mengambil word terakhir blok 3 (63 word = 504 byte diambil, 498 dikonsumsi), sehingga sponge mulai dan, selama stall 40 siklus, menyelesaikan permutasi berikutnya.
   Verilator dan Icarus menunjukkan satu kasus tunggal yang sama; top C5 tidak punya satu pun dalam 500 kasusnya (INFERENCE, tidak diuji terpisah: permutasinya 14 siklus bukan 26, jadi dibutuhkan stall lebih panjang untuk menyelesaikan permutasi tambahan). Setiap pemeriksaan lain lulus pada run itu (lint, regresi, semua kontrol, formal).
3. Mengapa kriteria berubah dan RTL tidak: permutasi tambahan dihitung mendahului kebutuhan dan hasilnya tidak pernah dibaca; pembungkus lalu menghentikan sponge, yang menghapus state-nya; keluaran, `bytes_o`, word diambil (CBD: 16), dan jumlah siklus tanpa back-pressure tidak terpengaruh. Itu konsekuensi prefetch jendela byte (sampai 11 byte melewati yang dikonsumsi), bukan cacat.
   Kriteria V5 baru: `perm_cnt_o` sama dengan hitungan golden; ia boleh satu lebih banyak hanya bila byte terkonsumsi menjangkau 11 byte terakhir blok akhir; dengan `coef_ready_i` selalu tinggi dan tanpa jeda aliran ia harus sama. Jumlah run dengan satu lebih banyak dicatat di evidence. Ini perubahan nilai yang diharapkan setelah melihat hasil dan dinyatakan demikian (C2, "never fake-pass");
   kriteria asli akan menyatakan desain yang benar sebagai salah, yang baru tetap gagal bila hitungan meleset lebih dari satu atau meleset satu di tempat lain mana pun.
4. Kontrol formal, sebagaimana diwujudkan: NC-S2 V9 diwujudkan dengan memulai hitungan koefisien pada 1: kasus koefisien ke-257 berada melewati kedalaman BMC (256 siklus), jadi relasi hitungan di balik S2 (last pada ke-256) yang dirusak kontrol; NC-S1 pertama kali tertangkap oleh invarian rentang pendukung pada kandidat yang diterima (nilai 3329 ditandai diterima), satu langkah sebelum mencapai pemeriksaan keluaran S1.
5. Batas bukti (dinyatakan, tidak disembunyikan): `bytes_o` adalah 16 bit; run formal mengasumsikan paling banyak 8,000 word aliran (64,000 byte) per polinomial agar tidak dapat wrap. Aliran buatan dengan lebih dari 21,845 triple ditolak beruntun akan membuatnya wrap; aliran SHAKE128 tidak melakukan itu dalam praktik (probabilitas tidak dihitung di sini; NOT MEASURED).
