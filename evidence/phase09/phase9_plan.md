<!-- claim-lint: skip-file (internal plan, not proposal text) -->
# Fase 9: ML-KEM-768 lengkap di RTL (simulasi) - rencana blok

Ditulis 2026-10-03, sebelum RTL Fase 9 apa pun dan sebelum pengukuran Fase 9 apa pun. Lingkup: `docs/ROADMAP.md` Fase 9; ADR 0019 (jalur dan tier), ADR 0027-0030 (Accepted: sponge C5, sampler W2, STREAM, OVERLAP), ADR 0031 (Accepted: pemeriksaan masukan FIPS 203 di HPS, bukan di RTL), ADR 0032 (Accepted: satu STOP per blok). Label: MEASURED, INFERENCE, ESTIMATE, NOT MEASURED, perhitungan tim. Matematika terkunci (C1).

## 1. Apa yang ada dan apa yang kurang
Ada (semuanya bit-exact, simulasi dan Quartus MEASURED di Fase 6-8): inti NTT/INTT S10, sequencer operasi K-PKE `kpke_sched_smp` (VAR = 2, OVERLAP) dengan slot store, unit PWM dan sampler streaming, dan sponge (C5). Sequencer menerima seed `rho` dan `sd` lewat port seed dan memindahkan koefisien lewat port host (`tb_we_i`, `tb_slot_i`, `tb_addr_i`, `tb_wdata_i`, `tb_rdata_o`, satu koefisien 12-bit per siklus, saat sequencer idle). Masukan sebuah program ditulis ke slot dan hasilnya dibaca dari slot lewat port itu; hashing kunci dan encoding byte tidak ada di perangkat keras (header Fase 8).
Yang kurang untuk ML-KEM (FIPS 203 Algoritma 16-18): (1) ByteEncode / ByteDecode dan Compress / Decompress antara byte dan koefisien; (2) hash G (SHA3-512), H (SHA3-256), J (SHAKE256) pada pesan yang dirakit; (3) bagian FO Decaps: enkripsi ulang, perbandingan waktu-konstan, pemilihan K atau kunci implicit-rejection; (4) pengendali yang mengurutkan semuanya, dengan buffer byte untuk ek, dk, c.
Tidak ada di RTL menurut ADR 0031: pemeriksaan masukan FIPS 203 (Bagian 7.2 dan 7.3). Inti mengasumsikan masukan yang sudah diperiksa.

## 2. Blok (satu STOP setelah masing-masing, ADR 0032; pembagiannya usulan asisten)
| Blok | Isi | Selesai bila |
|---|---|---|
| 9a | `mlkem_pack` (koefisien -> Compress_d -> byte ByteEncode_d) dan `mlkem_unpack` (byte -> ByteDecode_d -> koefisien Decompress_d) untuk d dalam {1, 4, 10, 12}; Compress bebas pembagian (konstanta dibuktikan pada semua 3,329 masukan) | bit-exact terhadap `primitives` untuk setiap d, menyeluruh untuk aritmetika, kedua simulator, kontrol gagal, formal, Quartus kernel-only |
| 9b | Bagian hash dan FO: feeder pesan untuk G, H, dan J di atas sponge (word dari buffer byte, word prefiks konstan), `mlkem_fo_cmp` (perbandingan 1,088 byte waktu-konstan dan pemilihan mask K / K_bar) | masing-masing bit-exact terhadap `hashlib` / golden, siklus tetap, kedua simulator, kontrol gagal, formal, Quartus |
| 9c | Pengendali `mlkem_core`: KeyGen_internal, Encaps_internal, Decaps_internal pada buffer byte, mesin K-PKE sebagai kotak hitam; semua grup ACVP yang dipin; evidence siklus-konstan untuk Decaps; Quartus inti penuh | ACVP keyGen (25), enkapsulasi (25), dekapsulasi (10) 100% di kedua simulator; siklus konstan; Quartus; grup key-check tidak dijalankan terhadap RTL (ADR 0031) |

## 3. Keputusan arsitektur di dalam rencana (INFERENCE dari antarmuka yang ada, akan ditunjukkan oleh test)
- Mesin K-PKE dan port tb-nya tidak disentuh (file beku Fase 6-8). Pengendali memindahkan koefisien antara codec dan slot lewat port host saat mesin idle; pada satu koefisien per siklus ini memakan 256 siklus per polinomial (ESTIMATE, dari lebar port), kecil dibanding ribuan siklus mesin. Tanpa perubahan pada mesin.
- Setiap loop codec dan pengendali punya panjang tetap: 256 koefisien dan 32 * d byte per polinomial, panjang pesan dan ciphertext tetap. Tidak ada cabang, alamat, atau hitungan yang bergantung pada rahasia; satu-satunya panjang variabel adalah rejection sampling A (rho / ek publik).
- Sponge untuk G, H, J adalah instans kedua (sampler punya sendiri di dalam `keccak_sampler`). Intinya (C5 atau K0) adalah parameter; C5 bawaan (ADR 0027); K0 lebih kecil dan waktu hashing tidak kritis; area terukur yang menentukan apakah bawaan dipertahankan (dilaporkan, tidak diputuskan di sini).
- Keacakan masuk sebagai port masukan (`d`, `z`, `m`) seperti kata roadmap; tanpa RNG di RTL.

## 4. Biaya (ESTIMATE, perhitungan tim; digantikan angka Quartus bila terukur)
Perangkat punya 41,910 ALM (datasheet) dan mesin 8d terukur 10,993 ALM, 44 M10K, 26 DSP (kernel-only, median seed 1-6). Buffer ek / dk / c butuh 1,184 + 2,400 + 1,088 byte = 4,672 byte = 37,376 bit, sekitar 4 blok M10K 10 Kb paling banter (lebih banyak dengan pembulatan lebar dan port). Codec dan pengendali adalah FSM kecil dan register byte; tidak dibuat estimasi ALM untuk keduanya di sini; keduanya diukur.

## 5. Aturan umum setiap blok (seperti Fase 5-8)
- Test plan dengan aturan adopsi atau lulus ditulis sebelum RTL blok itu; perubahan setelah run pertama dicatat sebagai Amandemen, aturan tidak diubah setelah mengukur.
- Lint Verilator `-Wall` dan slang 0 peringatan; cocotb di Verilator dan Icarus; kontrol negatif pada salinan khusus test; SymbiYosys untuk properti kendali; Quartus 25.1std Lite kernel-only, virtual pin, seed 1-6, satu revisi sekali, timing pada 40.000 ns (20.000 ns informasi).
- Setiap file RTL diawali `` `default_nettype none `` dan diakhiri `` `default_nettype wire ``; strategi reset: asinkron active-low pada state kendali, tanpa reset pada register datapath (seperti Fase 6-8), dinyatakan di setiap file.
- Hasil simulasi diberi label hanya simulasi. Tidak ada klaim tentang papan (tanpa DE10-Nano), tidak ada klaim percepatan terhadap perangkat lunak, tidak ada klaim side-channel: waktu-konstan berarti invarian jumlah siklus saja.

## 6. Amandemen A1 (2026-10-03, ditulis di awal 9b; tidak ada di atas yang diedit)
Rencana 9b di bagian 2 menyebut "feeder pesan (word dari buffer byte, word prefiks konstan)". Membaca antarmuka sponge (`rtl/keccak/keccak_sponge_r2.sv`: word 64-bit, byte k dari word w adalah byte pesan 8w + k, panjang dalam byte diberikan saat start) menunjukkan tidak perlu feeder byte: setiap segmen pesan Algoritma 16-18 adalah kelipatan 8 byte (d, z, m, h, K: 32 byte; ek: 1,184; c: 1,088) dan dimulai pada batas word saat segmen digabung; satu-satunya pengecualian adalah `d || k` (G(d || 3), 33 byte), yang word terakhirnya `0x03` dan disuplai pengendali. Maka 9b membangun `mlkem_hash` (pembungkus sponge dengan tiga mode H, G, J, penghitungan digest, dan penghentian squeeze SHAKE256) dan `mlkem_fo_cmp` (perbandingan waktu-konstan dua ciphertext 136-word dan pemilihan mask K atau kunci implicit-rejection), keduanya dengan antarmuka word 64-bit. Buffer byte, urutan segmen, dan perakitan pesan adalah pekerjaan pengendali di 9c.
