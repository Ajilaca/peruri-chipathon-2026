<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Fase 9F langkah S2: register setelah reducer Barrett di inti NTT/INTT (P = 5 -> 6) - test plan dan aturan adopsi

Ditulis 2026-10-04 sebelum RTL S2 apa pun dan sebelum pengukuran S2 apa pun. Lingkup: ADR 0036 (Accepted: S2 menyerang batas yang diungkap S1) dan rencana batch chat 2026-10-04 (S2 milik Batch 2, diambil alih Jevan pada sesi yang sama; commit di branch `phase9m-optimisation`). Baseline: K1b (`../../batch1/9f1b/`, `mlkem_core3`: sampler K0, hash K0, codec dua-byte, hash latar belakang). Label: MEASURED, ESTIMATE, INFERENCE. Timing statis kernel-only dengan virtual pin; bukan hasil papan.

## 1. Mengapa (MEASURED: jalur terburuk K1b pada 15 ns, seed 1, `critical_paths_K1b-15.md`; rincian tingkat-field dihitung ulang 2026-10-04 dari database yang diarsipkan, laporan mentah tidak disimpan)
298 dari 300 jalur terburuk berada di kelas inti NTT / memori (2 sisanya sequencer mesin ke sponge sampler pada +2.420 ns). Yang terburuk tunggal (slack +1.170 ns, 182 dari 300 jalur berbagi bentuknya) berjalan dalam satu siklus clock dari register terakhir reducer Barrett (`g_cut[2]`, potongan setelah pengurangan kedua) lewat empat blok logika ke data tulis bank M10K:
1. langkah Barrett terakhir (`d3 = r - q`, pilih `p3`): rantai pengurang 13-bit ditambah pemilihan, sekitar 3.1 ns (6.5 sampai 9.6 ns pada jalur);
2. add / subtract butterfly (`add_mod`, `sub_mod`: rantai penjumlah 12-bit ditambah perbandingan dengan q dan pemilihan keluaran): sekitar 4.3 ns (9.6 sampai 13.9 ns);
3. multiplekser data tulis bank (`g_bank[4].wd[*]`, dua level logika dengan routing panjang): sekitar 4.0 ns (13.9 sampai 17.9 ns);
4. routing ke port tulis RAM dan setup-nya: sekitar 1.4 ns.
Kelas lain di kompilasi yang sama, MEASURED: register mode ke butterfly (+2.212 ns, 72 jalur), pemilih baca memori ke butterfly (+2.288 ns, 24 jalur), counter layer ke memori (+1.910 ns, 20 jalur). Jadi potongan antara blok 1 dan blok 2 menggeser penghalang sekitar 1.2 sampai 1.5 ns paling banyak (kelas berikutnya di +1.9 ns), tidak lebih; penghalang berikutnya setelahnya berbeda (INFERENCE).
Modul Barrett sudah mendukung potongan keempat: `REG_AFTER[3]` meregister `p3`, keluaran koreksi akhir. Potongan yang dipakai adalah bit 0, 1, 2 (P = 5: latensi baca 2 ditambah tiga potongan pengali). Mengatur bit 3 memberi P = 6. Tanpa aritmetika baru, tanpa struktur perangkat keras baru: sebuah parameter.

## 2. Desain (perubahan terkecil yang aman, parameter lebih dulu)
1. Pembungkus baru `rtl/ntt/ntt_core_s10_p6.sv`: `ntt_core_s10` pada `NUM_LANES = 8`, `RD_LAT = 2`, bit `MUL_REG` 0, 1, 2, 3 (P = 6). Inti sudah menurunkan `WrDly`, `Pipe`, counter drain, delay tulis memori (`WR_DELAY`), operand samping tertunda (`u_side`, `Lat`), dan penyelarasan tulis-host tertunda dari `MUL_REG`; tanpa edit `ntt_core_s10.sv`, `butterfly_m6.sv`, `modmul_barrett.sv`, `poly_mem_m10k.sv`.
2. Parameter `NTT_P6` (bawaan 0) pada `kpke_smp_top_s10` (sebuah generate memilih `ntt_core_s10_p5` atau `ntt_core_s10_p6`) dan pada `mlkem_core3` (diteruskan ke mesin). Pada bawaan 0 desain terelaborasi adalah desain K1b (V8 memeriksa siklus dan masukan netlist yang relevan bagi Quartus). `mlkem_core.sv` dan `mlkem_core2.sv` tidak diedit.
3. Sequencer (`kpke_sched_smp`) bergantung pada inti NTT hanya lewat latensi baca host (`CORE_RDLAT = 2`, tidak berubah) dan `busy`/`done`; ia tidak bergantung pada `Pipe` (diperiksa dengan membaca file, V6 memeriksa dengan simulasi).
4. Bebas stall (INFERENCE, `../../ntt_pipeline_depth_analysis.md`): P terbesar tanpa stall pada batas layer adalah 7 untuk L = 8; P = 6 tidak stall di mana pun, jadi satu transformasi memakan 113 + 6 = 119 siklus (118 pada P = 5). Properti formal A, B, C (V5) dan test bit-exact membuktikan atau mengukur ini; tidak ada yang diasumsikan di RTL.

## 3. Estimasi yang ditulis sebelum mengukur (ESTIMATE; angka K1b MEASURED)
| Besaran | K1b (MEASURED) | S2 ESTIMATE |
|---|---|---|
| Siklus NTT / INTT per transformasi | 118 | 119 (+1) |
| Siklus KeyGen / Encaps / Decaps (masukan profil; 6 / 7 / 11 transformasi) | 8,404 / 10,236 / 15,597 | 8,410 / 10,243 / 15,608 (+6 / +7 / +11) |
| Median ALM pada 40 ns | 14,335.0 | +0 sampai +250 |
| Register (40 ns) | 8,211-8,258 (`../../batch1/9f1b/selection_worksheet.md`) | +250 sampai +450 (8 lajur x dua stage 12-bit: keluaran reducer dan operand samping, sekitar 190; rantai delay tulis kendali memori untuk 16 port, sekitar 150) |
| Blok RAM / DSP | 54 / 28 | 54 / 28 |
| Fmax slow corner terendah pada 15 ns, median 6 seed | 73.855 MHz | 76 sampai 80 MHz (kelas berikutnya berada 0.7 sampai 1.1 ns di belakang jalur terburuk K1b; skew dan penempatan bervariasi menurut seed) |
| Latensi KeyGen / Encaps / Decaps pada 15 ns (siklus / median Fmax) | 113.8 / 138.6 / 211.2 us | 104 sampai 111 / 127 sampai 135 / 194 sampai 206 us |
Hasil di luar rentang dinyatakan demikian di laporan.

## 4. Test (kedua simulator; RTL repository tidak pernah dimutasi, kontrol berjalan pada salinan)
| # | Test | Syarat lulus |
|---|---|---|
| V1 | lint: Verilator `-Wall` dan slang `ntt_core_s10_p6`, `kpke_smp_top_s10` pada `NTT_P6` 0 dan 1, `mlkem_core3` pada K1b dan pada `NTT_P6 = 1` | 0 peringatan, 0 error |
| V2 | unit test inti NTT (`tb/s10/run_s10_tests.py`, target baru `s10p6`: test inti S10 dengan `C3_WRDLY = 4`) | NTT dan INTT bit-exact terhadap model golden, siklus tepat 119 / 119, Verilator dan Icarus |
| V3 | unit test memori pada `WR_DELAY = 4` (target baru `mem6`) | lulus, kedua simulator |
| V4 | kontrol negatif pada salinan untuk P = 6: NC-M (peta bank tanpa bit XOR) dan NC-W (kendali tulis kurang satu siklus) | NTT dan INTT bit-exact harus FAIL |
| V5 | formal: bukti kendali S10 (properti H, O, R, A, B, C) dengan P = 6 (salinan top formal dengan `P = 6`, kedalaman 9), dan kontrol negatifnya (F_SKEW) | bukti PASS, kontrol FAIL seperti disyaratkan |
| V6 | test sequencer K-PKE dengan `NTT_P6 = 1` (`KP_VAR = 2`, sampler K0): tiga program bit-exact, siklus konstan untuk rho tetap, cakupan stall | 3/3 lulus, kedua simulator |
| V7 | inti `mlkem_core3` dengan `NTT_P6 = 1`: seluruh target `core` (ACVP keyGen 25, enkapsulasi 25, dekapsulasi 10, cross-check acak, rantai, protokol, siklus konstan) dan profil | 100 % sama, kedua simulator; siklus seperti bagian 3 (+6 / +7 / +11 terhadap K1b, hanya hitungan RUN dan state terikat-NTT yang berubah); jumlah siklus Encaps dan Decaps identik di semua masukan |
| V8 | regresi pada nilai bawaan: `NTT_P6 = 0` memberi profil K1b (8,404 / 10,236 / 15,597) dan target S10 (`s10`, `ncm`, `ncw`, `mem`, `p6`) lulus dengan 118 / 118; profil bawaan `mlkem_core` tidak berubah (9,095 / 10,735 / 16,667) | PASS |
| V9 | Quartus K2 (K1b + `NTT_P6 = 1`) seed 1-6 pada 40.000 ns (gerbang) dan K2-15 seed 1-6 pada 15.000 ns (ADR 0036 butir 3), satu kompilasi sekali per proyek; tanpa batasan di bawah 15 ns (ADR 0039) | ekstrak; timing terpenuhi pada 40 ns di setiap seed; pada 15 ns jumlah seed yang terpenuhi dan Fmax tiap seed |
| V10 | jalur kritis seed slack terbaik pada 15 ns, diklasifikasi seperti di S1 (`classify_paths_9f.py`) ditambah rincian tingkat-field jalur terburuk | dicatat: blok mana penghalang berikutnya |
Urutan: V1-V8 dulu (gerbang cepat); V9 hanya untuk desain akhir langkah ini.

## 5. Aturan adopsi (ditetapkan sebelum mengukur; ADR 0036: menurut latensi pada 15 ns)
S2 diadopsi di atas K1b hanya bila semua berikut berlaku:
1. V1-V8 lulus seperti dinyatakan (ketidakcocokan ACVP apa pun menolaknya).
2. Timing terpenuhi pada 40.000 ns di setiap seed 1-6.
3. Median ALM paling banyak 20,000 (anggaran).
4. Untuk masing-masing KeyGen, Encaps, dan Decaps, t = siklus / median Fmax pada batasan 15 ns (slow corner terendah, seed 1-6) K2 lebih rendah dari K1b (113.8 / 138.6 / 211.2 us).
5. Jumlah seed yang memenuhi 15 ns dilaporkan; bila K2 memenuhi lebih sedikit seed dari K1b (6 dari 6) aturan diterapkan pada seed yang memenuhinya di keduanya dan selisihnya dinyatakan.
Apakah kenaikan Fmax lebih besar dari sebaran seed dinyatakan (K1b: kelas sebaran 72.0 sampai 74.1 MHz); kenaikan di dalam sebaran dilaporkan demikian dan tidak disebut kenaikan. Bila tidak, S2 dilaporkan tidak diadopsi dan K1b tetap. Hasilnya adalah ADR Proposed.

## 6. Bukan bagian langkah ini
Tanpa perubahan aritmetika, jadwal, atau peta memori; tanpa sampler kedua (S3); tanpa tumpang tindih dengan mesin (butir 4); tanpa batasan di bawah 15 ns; tanpa hasil papan; waktu-konstan berarti invarian jumlah siklus saja. Bila V10 menunjukkan penghalang berikutnya yang dapat digeser perubahan kecil lain (misalnya register mode terduplikasi per lajur, register pemilih baca), itu diusulkan di laporan sebagai S2b dengan rencana dan aturan sendiri, tidak dikerjakan di bawah rencana ini.

## 7. Amandemen A1 (2026-10-04, ditulis saat membangun; tidak ada di atas yang diedit dan aturan bagian 5 tidak berubah)
1. Tanpa file pembungkus baru. Bagian 2 butir 1 dan 2 menyebut `rtl/ntt/ntt_core_s10_p6.sv` dan sebuah generate di `kpke_smp_top_s10`. Modul baru akan menuntut setiap daftar file yang mengelaborasi mesin (runner simulasi, `.sby` formal, `.qsf` Quartus 9c, 9M, 9F) diedit. Sebagai gantinya pembungkus yang ada `rtl/ntt/ntt_core_s10_p5.sv` mendapat parameter `P6` (bawaan 0 = desain P = 5, tidak berubah), `kpke_smp_top_s10` mendapat `NTT_P6` (bawaan 0) dan meneruskannya, `mlkem_core3` mendapat `NTT_P6` (bawaan 0). Nama modul `ntt_core_s10_p5` tetap pada P = 6 (didokumentasikan di headernya).
2. V1 dijalankan untuk `NTT_P6` 0 dan 1 pada setiap daftar file yang dipakai (Verilator dan slang pada top level test); V8 mengonfirmasi bahwa masukan netlist bawaan dan jumlah siklus adalah milik K1b.
