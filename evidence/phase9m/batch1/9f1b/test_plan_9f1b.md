<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Fase 9F langkah S1b: hash berjalan di samping pekerjaan lain (hash latar belakang) - test plan dan aturan adopsi

Ditulis 2026-10-04 sebelum RTL S1b apa pun dan sebelum pengukuran S1b apa pun. Lingkup: ADR 0036 (Accepted, Faza Dzil, langkah S1b rencana Fmax) dan rencana batch chat 2026-10-04 ("s1b (batch 1) baru masuk batch 2": S1b milik Batch 1, S2 + S3 + butir 4 adalah Batch 2). Baseline: K1 (S1, `test_plan_9f1.md`: sampler K0, hash K0, codec dua-byte) di `rtl/mlkem/mlkem_core2.sv`. Label: MEASURED, ESTIMATE, INFERENCE, perhitungan tim. Matematika terkunci (C1): hash yang sama atas byte yang sama dihitung; hanya kapan ia berjalan yang berubah.

## 1. Mengapa (dari profil K1, MEASURED dalam simulasi, `../9f1/profile_k1_verilator.json`)
Unit hash dipakai pengendali satu operasi mikro sekali. Tiga hash tidak bergantung pada pekerjaan di sampingnya:
- KeyGen: `H(ek)` (HST, HFD 148 word, HGT, sekitar 395 siklus pada K0) hanya butuh t_hat dan rho; ia dapat berjalan selama tiga store s_hat (STP 0, 1, 2, 3 x 265 siklus), yang menyentuh word lain dari memori yang sama.
- Encaps: `H(ek)` (sekitar 394 siklus) hanya butuh ek; load t_hat dan pesan (RD32, LDP 7, 8, 9, 11, sekitar 1,070 siklus) tidak membutuhkannya. Hanya `G(m || H(ek))` berikutnya yang membutuhkannya.
- Decaps: `J(z || c)` (sekitar 390 siklus) hanya butuh z dan ciphertext; ia dapat berjalan selama load pertama dan run dekripsi (RUN 2, 3,111 siklus). Hasilnya pertama kali dipakai oleh perbandingan akhir.
`G(d || k)` KeyGen dan `G(m' || h)` Decaps berada di rantai ketergantungan dan tetap di latar depan.

## 2. Desain (teks baru hanya di `rtl/mlkem/mlkem_core2.sv`, ROM baru, dan model golden; file Fase 9 / 9M / S1 menjaga perilakunya)
1. Sequencer sidecar: state machine kecil kedua (B_IDLE, B_FETCH, B_DISP, B_HFD, B_HGT) dengan program counter dan register instruksi sendiri menjalankan sebuah job hash: word HST, HFD..., HGT, END yang disimpan di memori program setelah program utama. Ia punya salinan sendiri counter feeder dan digest. Pengendali utama mendapat dua operasi mikro: `BGS pc` (mulai job di word `pc`; pengendali utama lanjut seketika) dan `JN` (tunggu sampai job selesai, termasuk tulis digest). Operasi mikro utama tidak berubah.
2. Satu unit hash: selama job berjalan ia dimiliki sidecar; pengendali utama tidak boleh memulai hash saat itu (dijamin oleh program dan diperiksa secara statis di model, oleh pemeriksaan perangkat keras di bawah, dan oleh properti formal). Masukan dan keluaran `mlkem_hash` dimultipleks menurut pemilik.
3. Bus baca (satu port baca per memori, data valid siklus setelah alamat): permintaan pengendali utama selalu menang; sidecar mengeluarkan permintaan hanya pada siklus ketika pengendali utama tidak mengeluarkan; pemilih region memori mengikuti permintaan yang diberikan pada siklus sebelumnya. Pengendali utama tidak pernah ditunda sidecar (jumlah siklusnya tidak bergantung pada job).
4. Bus tulis (satu port tulis): word digest sidecar masuk ke register file hanya pada siklus ketika pengendali utama tidak menulis (`out_ready` hash rendah selain itu).
5. Keselamatan di perangkat keras: `END` program utama menunggu sampai sidecar idle (register hasil lengkap saat `done_o` naik); `HST` utama diabaikan saat job berjalan hanya bila ROM salah (ditandai oleh properti formal, tidak dikoreksi).
6. ROM dan model: `tb/golden/mlkem_ctl_model2.py` membangun program baru dari model Fase 9 (primitives golden sama; op BGS dan JN, word job setelah END); `scripts/build/gen_mlkem_ctl_rom2.py` membangkitkan `rtl/mlkem/mlkem_ctl_rom2.sv` (`--check`). Program baru: KeyGen: `... STP 3, 4, 5; WR32 rho; BGS(H(ek)); STP 0, 1, 2; JN; WR32 H(ek); WR32 z`. Encaps: `BGS(H(ek)); RD32 rho; LDP 7, 8, 9, 11; JN; G; SDL; RUN; STP ...`. Decaps: `BGS(J); LDP 3, 4, 5, 10, 0, 1, 2; RUN 2; STP 10; JN; G; RD32 rho; enkripsi ulang; CMP; END` (J selesai jauh sebelum akhir run dekripsi 3,111 siklus, jadi JN tidak menunggu; ia berdiri sebelum `G` karena `G` butuh unit hash). Secara umum `JN` ditaruh tepat sebelum hash utama pertama atau pemakaian pertama hasil job.
7. Pemeriksaan statis model (`check_static2`): setiap job adalah HST / HFD / HGT / END dengan word HFD mencakup panjang hash; di antara `BGS` dan `JN` program utama tidak mengeluarkan HST, HFD, HGT, tidak membaca atau menulis register tujuan job, dan tidak menulis ke rentang word yang dibaca job; setiap `BGS` punya `JN`-nya sebelum `END`; keluaran golden program baru sama dengan program Fase 9.
Word program: program terbesar tetap di bawah ruang alamat 64-word (pc 6 bit).

## 3. Estimasi yang ditulis sebelum mengukur (ESTIMATE; biaya hash MEASURED di profil K1: KeyGen 395, Encaps 394, Decaps 390 siklus untuk operasi mikro hash yang pindah ke latar belakang)
| Besaran | K1 (MEASURED) | K1b ESTIMATE |
|---|---|---|
| Siklus KeyGen / Encaps / Decaps (masukan profil) | 8,795 / 10,627 / 15,983 | sekitar 8,410 / 10,240 / 15,600 (sekitar -385 masing-masing: hash yang dipindah dikurangi BGS, JN, dan satu siklus tunggu) |
| Median ALM | akan diukur di S1 (ESTIMATE S1 sekitar 13,400; dua seed pertama 14,066 / 14,106) | S1 + 150 sampai 450 (sequencer kedua, instans ROM kedua, multiplekser) |
| Register | S1 | S1 + 100 sampai 250 |
| Blok RAM / DSP | 54 / 28 | 54 / 28 |
| Fmax | S1 | dalam 2 % dari S1 (multiplekser baru pada alamat baca dan masukan hash; INFERENCE: tidak di jalur kritis S1 pada 15 ns, V9 memeriksa) |
| Siklus LDP dan STP yang dilihat pengendali utama | 263 / 265 | sama (sidecar tidak pernah menundanya) |

## 4. Test (kedua simulator; RTL repository tidak pernah dimutasi)
| # | Test | Syarat lulus |
|---|---|---|
| V1 | lint Verilator `-Wall` dan slang `mlkem_core2` dengan ROM baru pada K1 dan nilai bawaan | 0 peringatan, 0 error |
| V2 | model: `check_static2`; program baru memberi keluaran keygen / encaps / decaps yang sama dengan program Fase 9 untuk vektor ACVP dan 200 kasus acak; `gen_mlkem_ctl_rom2.py --check` | semua lulus |
| V3 | inti K1b: seluruh target `core` 9c (ACVP keyGen 25, enkapsulasi 25, dekapsulasi 10, cross-check acak, rantai, protokol, siklus konstan) | 100 % sama, kedua simulator |
| V4 | profil pada K1b | dicatat; hitungan per state LDP, STP, RUN, SDL, WR32, RD32, CMP sama dengan K1; state hash hilang dari program utama kecuali G (HFD / HGT milik G) |
| V5 | siklus konstan: Encaps identik untuk m berbeda dan tidak bergantung ek; Decaps identik untuk ciphertext valid dan ditolak; KeyGen berselisih hanya dari sampling publik | seperti 9c V6 |
| V6 | kontrol negatif pada salinan: NC-PRIO (baca sidecar menang atas permintaan utama) -> ACVP V3 harus FAIL; NC-WR (tulis digest mengabaikan tulis utama pada siklus yang sama) -> ACVP V3 harus FAIL; NC-ROM (job membaca offset word + 1) -> FAIL; NC-JOIN: salinan ter-throttle (sidecar mengeluarkan satu baca setiap 16 siklus sehingga job melampaui pekerjaan utama) harus LULUS dengan join, dan salinan ter-throttle yang sama dengan `JN` dihapus harus GAGAL (menunjukkan join efektif, bukan hanya tidak pernah dibutuhkan) | masing-masing seperti dinyatakan |
| V7 | formal (sby, stub protokol seperti 9c): properti 9c E1 (dua salinan, data berbeda, kendali sama: non-interferensi) dan S1-S7 untuk `mlkem_core2`; baru: B1 pengendali utama tidak pernah memulai hash saat job berjalan; B2 `done_o` hanya saat sidecar idle; B3 pengendali utama meninggalkan JN hanya saat sidecar idle; B4 sidecar menulis hanya register file, hanya alamat register tujuannya; B5 alamat baca sidecar tetap di dalam memorinya; kontrol (mutan yang menghapus pemeriksaan B1 / B3 harus membuatnya FAIL) | PASS, kontrol FAIL |
| V8 | regresi pada nilai bawaan: profil bawaan `mlkem_core` sama dengan profil Fase 9, dan `mlkem_core2` pada SMP_C5 = 1, HASH_C5 = 1, ROM lama sama dengan `mlkem_core` (siklus) | PASS |
| V9 | Quartus K1b seed 1-6 pada 40.000 ns (gerbang) dan K1b-15 seed 1-6 pada 15.000 ns (informasi, ADR 0036 butir 3), satu per satu; klasifikasi jalur kritis pada 15 ns | ekstrak; timing terpenuhi pada 40 ns di setiap seed; pada 15 ns jumlah seed yang terpenuhi dan Fmax dilaporkan |
Aturan batch (chat): V1-V8 adalah gerbang cepat setelah tiap langkah; V9 (gerbang lambat) dijalankan sekali untuk desain akhir Batch 1.

## 5. Aturan adopsi (ditetapkan sebelum mengukur; ADR 0036: menurut latensi)
S1b diadopsi di atas S1 hanya bila semua berikut berlaku:
1. V1-V8 lulus seperti dinyatakan (ketidakcocokan ACVP apa pun menolaknya).
2. Timing terpenuhi pada 40.000 ns di setiap seed 1-6.
3. Median ALM paling banyak 20,000 (anggaran).
4. Untuk masing-masing KeyGen, Encaps, dan Decaps, t = siklus / median Fmax pada batasan 15 ns (slow corner terendah, seed 1-6) K1b lebih rendah dari K1 (dari kampanye S1).
5. Pada 15 ns: jumlah seed yang memenuhinya dilaporkan (pernyataan "terpenuhi di k dari 6 seed"); bila K1b memenuhi lebih sedikit seed dari K1 aturan diterapkan pada seed yang memenuhinya di keduanya dan selisihnya dinyatakan.
Bila tidak, K1b dilaporkan tidak diadopsi dan konfigurasi S1 tetap. Hasilnya adalah ADR Proposed.

## 6. Bukan bagian langkah ini
Tanpa perubahan pada mesin (beku), tanpa tumpang tindih load dan store dengan mesin (butir 4, Batch 2), tanpa sampler kedua (S3), tanpa perubahan S2; tanpa hasil papan; waktu-konstan berarti invarian jumlah siklus saja.

## 7. Amandemen A1 (2026-10-04, ditulis saat membangun; tidak ada di atas yang diedit dan aturan bagian 5 tidak berubah)
1. Modul baru `rtl/mlkem/mlkem_core3.sv` sebagai ganti mengedit `mlkem_core2.sv` (bagian 2 dan header bagian 4 berkata "di mlkem_core2"): kampanye Quartus S1 (`quartus/phase09f1_core`, dua belas revisi) membaca `mlkem_core2.sv` saat berjalan. `mlkem_core3` adalah `mlkem_core2` ditambah sidecar dan `mlkem_ctl_rom2` sebagai ganti `mlkem_ctl_rom`; parameternya milik `mlkem_core2` (SMP_C5, HASH_C5, CODEC_W2). Revisi Quartus K1b memakai `mlkem_core3.sv` dan `mlkem_ctl_rom2.sv`.
2. Pengaman perangkat keras di luar bagian 2 butir 5: sebuah `HST`, `BGS`, atau `JN` utama yang bertemu job yang berjalan menunggu di DISP (program lalu lebih lambat tetapi hash-nya tetap benar); `END` menunggu job. Mereka tidak memakan biaya pada program yang benar. Bahaya register (membaca register tujuan sebuah job sebelum `JN`) tidak dideteksi di perangkat keras; mereka dikecualikan oleh `check_static2` dan oleh simulasi.
3. Detail bus tulis: tulis digest sidecar masuk ke register file hanya saat pengendali utama tidak menulis pada siklus itu (`fw_en`); pada siklus yang sama keluaran hash di-stall (`out_ready` rendah).
4. Runner test: `CORE_TOP=mlkem_core3` memilih modul dan ROM; kontrol `nclen` memutasi `.len_i(hx_len)`.
