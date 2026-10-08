<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Fase 9a: codec koefisien <-> byte (Compress / ByteEncode, ByteDecode / Decompress) - test plan dan aturan lulus

Ditulis 2026-10-03, sebelum RTL 9a apa pun dan sebelum pengukuran 9a apa pun. Lingkup: `evidence/phase09/phase9_plan.md` blok 9a; `docs/ROADMAP.md` Fase 9; FIPS 203 Algoritma 5 dan 6, Bagian 4.2.1 (Compress, Decompress). Golden: `tb/golden/primitives.py` (`compress`, `decompress`, `byte_encode`, `byte_decode`, tidak diubah, diperiksa terhadap vektor resmi di Fase 0). Label: MEASURED, INFERENCE, ESTIMATE, NOT MEASURED, perhitungan tim. Matematika terkunci (C1): RTL mengimplementasikan fungsi yang sama; hanya aritmetikanya ditulis tanpa pembagian.

## 1. Apa yang dibangun
- `rtl/mlkem/mlkem_pack.sv`: masukan aliran 256 koefisien (12 bit, nilai di [0, q-1]), keluaran `32 * d` byte: untuk d dalam {1, 4, 10} setiap koefisien dikompresi dengan Compress_d, untuk d = 12 ia diteruskan tidak berubah (ByteEncode_12); bit dikemas LSB dulu (ByteEncode_d). d dipilih per run oleh `dsel_i` (0: 1, 1: 4, 2: 10, 3: 12) dan dikunci saat `start_i`.
- `rtl/mlkem/mlkem_unpack.sv`: masukan `32 * d` byte, keluaran 256 koefisien: ByteDecode_d, lalu Decompress_d untuk d dalam {1, 4, 10}; untuk d = 12 nilai 12-bit direduksi mod q (ByteDecode_12 standar: `m = q`; satu pengurangan q bila nilai >= q, tidak pernah lebih karena 4,095 < 2q).
- Nilai yang dipakai: d = 1 (pesan), 4 (v), 10 (u), 12 (t_hat, s_hat). d lain tidak dibangun.
- Aritmetika bebas pembagian (alasan konstanta: tanpa pembagian pada data rahasia, KyberSlash): `Compress_d(x) = (((x << d) + 1664) * M_d >> S_d) mod 2^d` dengan (M, S) = (315, 20) untuk d = 1 dan 4, (161,271, 29) untuk d = 10; `Decompress_d(y) = (3329 * y + 2^(d-1)) >> d`. Konstanta ditemukan dengan pencarian dan diperiksa pada semua 3,329 masukan terhadap `compress` golden serta pada semua `2^d` masukan untuk `decompress` (`tb/golden/tests/test_codec_model.py`); ia valid untuk x dalam [0, q-1], satu-satunya nilai yang diambil koefisien.
- Antarmuka (aliran valid / ready; `done_o` satu pulsa setelah keluaran terakhir diterima; `busy_o` tinggi dari `start_i` sampai `done_o`; `start_i` diterima hanya saat idle):
  - pack: `coef_valid_i`, `coef_ready_o`, `coef_data_i[11:0]` masuk; `byte_valid_o`, `byte_ready_i`, `byte_data_o[7:0]`, `byte_last_o` keluar. Ia menerima tepat 256 koefisien per run dan mengeluarkan tepat `32 * d` byte; `byte_last_o` pada yang terakhir.
  - unpack: `byte_valid_i`, `byte_ready_o`, `byte_data_i[7:0]` masuk; `coef_valid_o`, `coef_ready_i`, `coef_data_o[11:0]`, `coef_last_o` keluar. Ia menerima tepat `32 * d` byte dan mengeluarkan tepat 256 koefisien; `coef_last_o` pada yang terakhir.
- Kendali tidak pernah melihat data: counter, isi bit buffer, dan stall bergantung pada `d` dan handshake saja (argumen waktu-konstan).
- Reset: asinkron active low pada state kendali; register datapath tidak di-reset; bit buffer dihapus saat `start_i`.

## 2. Model golden lebih dulu
`tb/golden/codec_model.py` (baru, independen dari RTL): `compress_hw` dan `decompress_hw` bebas pembagian, `pack_poly(d, coeffs)` dan `unpack_poly(d, data)` ditulis dengan rumus perangkat keras dan urutan bit buffer. `tb/golden/tests/test_codec_model.py`: `compress_hw` sama dengan `primitives.compress` untuk setiap x dalam [0, q-1] dan d dalam {1, 4, 10}; `decompress_hw` sama dengan `primitives.decompress` untuk setiap y dan d; `pack_poly` sama dengan `byte_encode(d, compress(d, .))` dan `unpack_poly` sama dengan `decompress(d, byte_decode(d, .))` pada polinomial acak dan khusus; untuk d = 12 `unpack_poly` sama dengan `byte_decode(12, .)`, termasuk setiap nilai 12-bit 0..4095.

## 3. Kasus sudut
- Setiap x dalam [0, q-1] melalui RTL untuk d = 1, 4, 10 (seluruh domain masukan, termasuk x = 0, x = q-1 di mana Compress_10 memberi 0 lewat wrap-around, dan tie pembulatan); setiap masukan 12-bit unpack d = 12 (0..4095, nilai >= q direduksi); setiap y dalam [0, 2^d - 1] unpack untuk d = 1, 4, 10.
- Polinomial acak; semua-nol, semua q-1, bergantian 0 / q-1, ramp.
- Back pressure: `byte_ready_i` / `coef_ready_i` selalu tinggi, acak (p = 0.5), run rendah panjang; jeda valid masukan (acak, panjang); keluaran ditahan (valid dan data stabil) selama tidak diterima.
- `start_i` saat sibuk diabaikan; `dsel_i` yang berubah saat sibuk diabaikan (dikunci); reset di tengah run, lalu run bersih; dua run beruntun dengan d berbeda.
- Hitungan tepat: 256 koefisien masuk / keluar dan 32 d byte keluar / masuk per run; `byte_last_o` / `coef_last_o` hanya pada yang terakhir.
- Siklus konstan: dengan sink selalu siap dan tanpa jeda masukan, jumlah siklus sebuah run identik untuk setiap nilai data d yang sama (polinomial acak dan khusus tetap, masing-masing 100).

## 4. Test
| ID | Pemeriksaan | Alat | Disyaratkan |
|---|---|---|---|
| V1 | Lint kedua modul (CRG-1, CRG-2) | Verilator `-Wall`, slang | 0 peringatan, 0 error |
| V2 | Test model golden (bagian 2) | pytest | semua lulus |
| V3 | pack: polinomial acak dan khusus, keempat d, semua mode back-pressure, byte sama dengan `byte_encode(d, compress(d, .))` golden yang tidak diubah | cocotb, kedua simulator | semua sama |
| V4 | unpack: sama, koefisien sama dengan `decompress(d, byte_decode(d, .))`; d = 12 dengan setiap nilai 12-bit | cocotb, kedua simulator | semua sama |
| V5 | Menyeluruh: setiap x untuk compress (d = 1, 4, 10) dan setiap masukan decompress, melalui RTL; round trip pack lalu unpack polinomial utuh sama dengan round trip golden | cocotb, kedua simulator | semua sama |
| V6 | Handshake dan hitungan: keluaran ditahan sampai diterima; hitungan tepat; start-saat-sibuk dan dsel-saat-sibuk diabaikan; reset di tengah run | cocotb | semua lulus |
| V7 | Siklus konstan (bagian 3) | cocotb | identik per d |
| V8 | Kontrol negatif (salinan khusus test): NC-RND compress tanpa suku pembulatan (1664 -> 0); NC-ORD urutan bit packer dibalik; NC-MOD unpack d = 12 tanpa reduksi; NC-CNT pack menerima koefisien ke-257 | cocotb | pemeriksaan yang dinamai untuk masing-masing GAGAL |
| V9 | Formal: hitungan dan rentang kedua modul dengan handshake bebas dan data bebas: paling banyak 256 koefisien dan `32 d` byte per run, `*_last` tepat pada yang terakhir, keluaran yang belum diterima ditahan, tidak ada keluaran saat idle, isi bit-buffer tetap dalam rentang | SymbiYosys (yosys-slang) | PASS |
| V10 | Quartus kernel-only (kedua modul dalam satu pembungkus `mlkem_codec_top`, virtual pin), 40.000 ns, seed 1-6, satu per satu; informasi: seed 1 pada 20.000 ns | `quartus_sh`, `/quartus-report` | evidence diekstrak |
| V11 | Siklus per polinomial dan d dengan sink selalu siap (tabel untuk anggaran pengendali) | cocotb | tabel ditulis |

## 5. Aturan lulus (ditetapkan sebelum mengukur; tanpa toleransi)
9a PASS hanya bila: 1. V1-V9 lulus di kedua simulator dan setiap kontrol V8 gagal seperti disyaratkan; 2. V10: fit berhasil dan timing terpenuhi pada 40.000 ns di setiap seed; 3. jumlah sumber daya dan Fmax (median Fmax slow corner terendah atas seed 1-6) dilaporkan sebagai MEASURED. Tidak ada aturan adopsi (tidak ada yang dipilih di antara alternatif); angka-angkanya memberi makan anggaran 9c. Pemakaian DSP dilaporkan dan tidak dibatasi di sini (112 blok DSP tersedia menurut datasheet; mesin 8d memakai 26).

## 6. ESTIMATE yang ditulis sebelum mengukur (bukan pengukuran)
- Throughput (perhitungan tim): packer mengeluarkan satu byte per siklus, jadi satu polinomial memakan sekitar `32 d` siklus ditambah latensi pipeline compress (sekitar 4): sekitar 388 (d = 12), 324 (d = 10), 132 (d = 4), 36 (d = 1). Unpacker menerima masukan satu byte per siklus: sekitar `32 d` siklus untuk d = 12, 10, 4 dan sekitar 256 untuk d = 1 (satu koefisien per siklus adalah batasnya).
- Sumber daya: dua FSM kecil dengan bit buffer 24-bit masing-masing, satu pengali sekitar 22 x 18 bit di packer (dapat dipetakan ke blok DSP atau ALM: tidak diprediksi), perkalian konstan dengan 3329 (empat suku tergeser) di unpacker: ALM di ratusan rendah masing-masing (INFERENCE; tidak ada angka yang diklaim). Fmax: tidak diprediksi; pengali compress dipipeline menjadi dua stage karena alasan itu.

## 7. Tidak dicakup
Antarmuka memori dan pengendali (9c); hashing (9b); pemeriksaan masukan (ADR 0031); papan; side channel. Codec diperiksa invarian siklusnya hanya dalam simulasi.

## 8. Amandemen A1 (2026-10-03, ditulis setelah run pertama; aturan lulus bagian 5 tidak berubah)
1. Kontrol batal ditemukan dan diperbaiki (driver test, RTL tidak berubah): versi pertama driver menawarkan tepat 256 koefisien (atau `32 d` byte) dan tidak lebih, sehingga NC-CNT (packer menerima koefisien ke-257) lulus semua test: kontrolnya batal. Driver kini terus menawarkan data setelah hitungan tepat; pemeriksaan hitungan tepat (`accepted == 256`, `accepted == 32 d`) lalu gagal untuk NC-CNT. Run pertama V8 tidak dipakai sebagai evidence.
2. Register data yang tidak di-reset: driver pertama mengonversi nilai keluaran tak terselesaikan (X) menjadi integer saat keluaran tidak valid; driver kini membaca nilai yang bukan 0/1 sebagai -1 dan mensyaratkan nilai terselesaikan setiap kali `*_valid_o` bernilai 1. Tanpa perubahan RTL.
3. Lint: lint pertama `mlkem_pack.sv` melaporkan bit tak terpakai register hasil kali 40-bit; register dipersempit menjadi 14 bit yang dipakai (`q10_q`, `q4_q`). Fungsi sama; setiap test dijalankan pada file akhir.
4. Formal (V9): (a) langkah induksi butuh invarian pendukung "counter DUT sendiri sama dengan counter black-box" (`cin_q == nin`, `bout_q == nout`, `bin_q == nbin`, `cout_q == ntake`); run induksi pertama packer gagal pada P1 tanpanya; (b) sebuah placeholder (`|| 1'b1`, tautologi) telah diketik di P4 draf pertama top formal dan diganti dengan persamaan keseimbangan bit yang tepat sebelum run bukti pertama; tidak ada hasil yang diambil dari draf; (c) kontrol NC-P1 dan NC-U1 (pelanggaran hitungan yang butuh 257 koefisien atau 33 byte) tidak dapat dicapai di dalam kedalaman induksi 40: bukti mengembalikan UNKNOWN (base case lulus, langkah induksi gagal), bukan PASS, yang menunjukkan properti tidak vakum; seperti NC-B `formal/run/run_formal_slang.py` keduanya dilengkapi dengan run BMC kedalaman 300 yang harus FAIL. Nilai yang diharapkan runner ditulis sesuai (UNKNOWN untuk bukti, FAIL untuk run BMC); properti tidak dilemahkan.
5. Pemeriksaan ESTIMATE (bagian 6): siklus pack MEASURED 261 (d = 1), 261 (d = 4), 325 (d = 10), 389 (d = 12) terhadap ESTIMATE sekitar 36, 132, 324, 388: estimasi benar untuk d = 10 dan 12 (dibatasi keluaran, satu byte per siklus) dan salah untuk d = 1 dan 4, yang dibatasi masukan (satu koefisien per siklus: 256 + 5). Unpack MEASURED 259, 259, 323, 387 terhadap sekitar 256 (d = 1), 128 (d = 4), 320, 384: salah untuk d = 4 karena alasan yang sama (satu koefisien per siklus). Sumber daya tidak diestimasi dalam angka (bagian 6); nilai MEASURED ada di worksheet.
