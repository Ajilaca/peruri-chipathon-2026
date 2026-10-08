<!-- claim-lint: skip-file (internal decision aid, not proposal text) -->
# Paket keputusan untuk pekerjaan 50 MHz (masukan tindak lanjut ADR 0010; tidak ada di sini yang diputuskan)

Label: MEASURED (laporan Quartus atau log simulasi di repository ini), INFERENCE (aritmetika pada nilai terukur),
ESTIMATE (proyeksi; metode dinyatakan). Dua pertanyaan untuk tim: (a) berapa kenaikan siklus yang dapat diterima bila
stall diperlukan; (b) apakah batas 12,573 ALM tetap untuk register tambahan.

## (a) Kenaikan siklus - yang penting adalah waktu per transformasi, t = siklus / Fmax
Titik awal (MEASURED, C3-P6 seed bawaan): NTT 119 siklus, INTT 375 siklus, Fmax slow corner terendah 34.19 MHz →
t_NTT = 3.481 µs, t_INTT = 10.968 µs (INFERENCE).

Titik impas (INFERENCE): pada clock F, sebuah konfigurasi lebih cepat dari C3-P6 saat ini hanya bila jumlah siklusnya tetap di bawah
3.481 µs × F (NTT) dan 10.968 µs × F (INTT):

| Clock | NTT boleh memakan sampai | INTT boleh memakan sampai |
|---|---:|---:|
| 40 MHz | 139 cycles | 438 cycles |
| 45 MHz | 156 cycles | 493 cycles |
| 50 MHz | 174 cycles | 548 cycles |

Siklus stall per kedalaman pipeline P (`stall_cycles.txt`, `scripts/test/phase5_stall_cycles.py`; stall minimum per
batas ditemukan dengan pencarian atas jadwal alamat L = 8 nyata, lalu diperiksa ulang untuk semua 256 alamat):

| P | Stall NTT (per batas) | Stall INTT (per batas + skala) | Siklus NTT / INTT | Kenaikan lawan C3-P6 | t_NTT pada 40 / 45 / 50 MHz (µs, ESTIMATE) |
|---|---|---|---|---|---|
| 6 (saat ini) | tidak ada | tidak ada | 119 / 375 (MEASURED) | - | 2.975 / 2.644 / 2.380 |
| 7 | tidak ada | tidak ada | 120 / 376 | +1 (0.8 %), +1 (0.3 %) | 3.000 / 2.667 / 2.400 |
| 8 | 1 pada batas 4 | 1 pada batas 3 | 122 / 378 | +3 (2.5 %), +3 (0.8 %) | 3.050 / 2.711 / 2.440 |
| 9 | 2 | 2 | 124 / 380 | +5 (4.2 %), +5 (1.3 %) | 3.100 / 2.756 / 2.480 |
| 10 | 3 | 3 | 126 / 382 | +7 (5.9 %), +7 (1.9 %) | 3.150 / 2.800 / 2.520 |
| 12 | 5 + 1 | 1 + 5 | 131 / 387 | +12 (10.1 %), +12 (3.2 %) | 3.275 / 2.911 / 2.620 |

- Jumlah siklus untuk P ≥ 7 adalah ESTIMATE: relasi terukur Fase 4 (NTT = 113 + P, INTT = 369 + P, 0 stall untuk
  P ≤ 6) ditambah stall yang ditemukan di sini; harus dikonfirmasi dalam simulasi. Pass skala tidak butuh stall sampai
  P = 15 (slack 15).
- Pemeriksaan konsistensi: kontrol negatif Fase 4 (kedalaman 8 tanpa stall) menghasilkan hasil salah
  (`evidence/phase04/cocotb_regression.txt`); tabel ini menyatakan P = 8 butuh tepat satu stall
  per transformasi.
- Siklus konstan: jumlah stall hanya bergantung pada P, arah, dan jadwal alamat tetap - tidak pernah pada
  data polinomial - jadi setiap masukan memberi hitungan yang sama (aturan CRG-7 tidak berubah; hanya nilai 119 / 375 yang
  akan berubah, lewat ADR).
- Waktu pada 40 / 45 / 50 MHz adalah clock hipotetis, bukan Fmax terukur. P yang lebih dalam hanya layak bila Fmax naik
  lebih dari kenaikan siklus: misalnya P = 8 butuh Fmax > 34.19 × 122 / 119 = 35.05 MHz hanya untuk impas dengan hari ini
  (INFERENCE).

Bacaan sederhana: bila stall menambah 3 siklus (2.5 %), NTT memakan 2.440 µs pada 50 MHz lawan 3.481 µs hari ini; bahkan +12
siklus (10 %) memberi 2.620 µs pada 50 MHz. Kenaikan siklus di tabel ini kecil dibanding yang akan diberikan clock lebih tinggi
- tetapi hanya bila clock benar-benar naik, yang hanya dapat ditunjukkan oleh kompilasi.

## (b) Batas ALM untuk register tambahan
Titik awal MEASURED: C3-P6 10,484–10,516 ALM atas seed 1–6 → margin ke 12,573: 2,057–2,089 ALM (INFERENCE).
Sebaran antar seed 32 ALM (P = 6) dan 64 ALM (P = 4). Di bawah setelan global GHRD inti yang sama butuh 11,053 ALM
(+548; +993 untuk C3-P4), margin 1,520 ALM (INFERENCE) - setelan kompilasi relevan bagi anggaran.

Biaya satu stage pipeline di Fase 4 (total MEASURED dan nilai per entitas dari `quartus/phase04_pipeline_c3/
output_files_P{2,4,6}/C3-P*.fit.rpt`; selisih INFERENCE):

| Langkah | Potongan | Δ ALM total | Δ register | Δ ALM entitas memori | Catatan |
|---|---|---:|---:|---:|---|
| P0 → P2 | + A_13, D_3 | −27 | +720 | (P0 adalah file inti berbeda) | register dikemas ke ALM yang sudah dipakai |
| P2 → P4 | A_13, D_3 → A_7, M, X, D_7 | +743 | +328 | +656.6 (6,964.6 → 7,621.2) | potongan M setelah arbitrasi slot adalah yang mahal |
| P4 → P6 | → A_4, A_11, M, X, D_5, D_11 | +66 | +23 | +39.5 | dua potongan arbitrasi sebagai ganti satu |

Per stage ini −13.5 sampai +371.5 ALM (INFERENCE, Δ/2). Biaya bergantung pada di mana register diletakkan, bukan pada jumlah
bitnya: satu stage setelah arbitrasi slot memakan sekitar 650 ALM; stage di dalam reducer hampir tidak memakan apa pun.

Bit per tuas yang diusulkan (ESTIMATE dari lebar sinyal di `rtl/mem/poly_mem_multiport_pipe.sv` dan
`rtl/ntt/butterfly_shared_pipe.sv`; 8 bank × 32 word, 2 slot baca per bank, 16 port, data 12-bit):

| Tuas (murah → mahal) | Register baru (ESTIMATE) | Perubahan P / siklus | ALM (ESTIMATE, dibatasi oleh rentang terukur di atas) |
|---|---|---|---|
| 1. Pecah mux baca (word di dalam bank, lalu bank/slot) | 8 bank × 2 slot × 12 bit = 192 bit data + pemilih bank/slot per port ≈ 64 bit | P → 7, tanpa stall (+1 siklus) | 0 sampai sekitar 650 |
| 2. Hapus `sub_mod` dari segmen kritis (5c, `b + q − a` malas) | tidak ada (masukan pengali lebih lebar 1 bit) | tidak ada | kecil; reducer harus menerima [0, 2q) |
| 3. Reducer lebih pendek (5a/5b) agar register reducer dapat pindah ke jalur baca/tulis | tidak ada (jumlah tetap 3) | tidak ada | selisih reducer; reducer hari ini berjumlah 1,395.8 ALM (MEASURED, batas atas penghematan apa pun) |
| 4. Register di jalur tulis sebelum `add_mod` / mux tulis | 8 lajur × 24 bit data = 192 + alamat/slot tulis yang ditunda ≈ 16 × 9 = 144 | P + 1 | 0 sampai sekitar 650 |
| 5. P > 7 dengan stall (tabel (a)) | seperti tuas 1/4 per stage tambahan + kendali stall | +1 sampai +12 siklus | per stage seperti di atas |
| 6. Memori M10K baca-sinkron | penyimpanan pindah ke M10K; 2R + 2W per bank per siklus tidak muat satu M10K true-dual-port | perubahan jadwal mungkin | tidak dapat diestimasi tanpa desain |

Bacaan sederhana: tuas 1 dan 4 bersama dapat memakan sampai sekitar 1,300 ALM (ESTIMATE, kasus terburuk rentang
terukur) terhadap margin sekitar 2,060 - muat di atas kertas, tetapi dengan sedikit ruang tersisa dan dengan efek
seed dan setelan sebesar 32–993 ALM. Reducer yang lebih murah dari 5a/5b akan mengembalikan ruang; berapa banyak baru
diketahui setelah 5a/5b dikompilasi.

Pengingat lingkup: angka 12,573 ALM adalah anggaran desain inti NTT ADR 0009, bukan anggaran sistem. Keccak, sampler,
pengendali KEM, encode/compress, penyimpanan, bridge HPS, dan SignalTap NOT MEASURED, sehingga tidak ada di sini
yang menyatakan sistem ML-KEM lengkap muat.

## Saran (hanya saran; tim yang memutuskan)
- (a) Terima kenaikan siklus selama t_NTT dan t_INTT pada Fmax terukur lebih baik dari C3-P6
  (3.481 / 10.968 µs) dan pemeriksaan siklus-konstan lulus; tanpa persentase tetap.
- (b) Pertahankan 12,573 ALM sebagai gerbang; bila tuas yang dibutuhkan melampauinya, bawa ke tim sebagai keputusan alih-alih
  mengubah batas diam-diam; ALM yang dihemat 5a/5b dihitung sebagai ruang untuk register tambahan.

## Koreksi (2026-10-01, lebih lambat pada hari yang sama; tidak ada di atas yang dihapus)
Tabel stall di (a) memakai model perencanaan Fase 4 (`scripts/test/pipeline_hazard_slack.py`), di mana butterfly
membaca pada siklus ia diterbitkan, sehingga kondisi stall bergantung pada seluruh kedalaman P. Kontrol negatif inti
Fase 5 pertama menunjukkan ini konservatif: dengan RdLat 1 + WrDly 7 (P = 8) hasil tetap benar di kedua
simulator (`../5a/negctl_first_attempt_rd1_wr7.txt`), karena memori membaca RdLat siklus setelah
permintaan. Berdasarkan evidence ini (INFERENCE, satu konfigurasi) kondisi stall bergantung pada WrDly = P − RdLat:
register yang ditambahkan sebelum baca (misalnya tuas 1, memecah mux baca) tidak butuh stall (siklus tetap naik karena
drain, +1 per stage), dan jumlah stall di tabel berlaku untuk register yang ditambahkan setelah baca. Tabel jumlah siklus karenanya adalah batas atas; fase memori
/ P harus mengonfirmasi model fisik dalam simulasi. Aturan ADR 0012 (nilai menurut waktu terukur) tidak terpengaruh.
