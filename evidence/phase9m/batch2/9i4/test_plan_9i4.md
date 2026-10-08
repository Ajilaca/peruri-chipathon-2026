<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Fase 9I butir 4: load di belakang mesin K-PKE (K4) - test plan dan aturan adopsi

Urutan pekerjaan, dinyatakan apa adanya: instruksi Jevan (chat 2026-10-04 sekitar 23:15) adalah menjalankan butir 4 tanpa pengawasan sampai pagi. RTL (`kpke_sched_smp4`, `kpke_smp_top_s10o`, `mlkem_ldpoly2o`, `mlkem_core4`, `mlkem_ctl_rom3`) dan simulasi pertama seluruh inti (ACVP, Verilator, satu run) ditulis dan dijalankan sebelum dokumen ini ditulis; dokumen ini ditulis saat run kontrol dan proyek Quartus disiapkan. Estimasi di bagian 3 adalah yang diberikan di chat sebelum run pertama `mlkem_core4` (Encaps sekitar -660 dan Decaps sekitar -2,600 siklus, KeyGen tidak berubah; diturunkan dari profil dan pemakaian slot program mesin). Aturan bagian 5 ditulis sebelum kompilasi Quartus apa pun dan sebelum run kontrol butir 4; ia tidak disetel ke suatu hasil. Lingkup: ADR 0034 butir 4 ("varian baru dari file beku Fase 6-8"), Batch 2. Baseline: K3 (`../9s2b/`: `mlkem_core3` dengan `NTT_P6 = 1`, `NTT_AR = 1`). Label: MEASURED, ESTIMATE, INFERENCE. Timing statis kernel-only dengan virtual pin; bukan hasil papan.

## 1. Mengapa (MEASURED: profil K2, `../9s2/profile_k2_verilator.json`)
Per operasi pengendali menghabiskan (siklus, K2): KeyGen RUN 6,740 dan STP 1,578; Encaps RUN 8,060, LDP 1,044, STP 1,052; Decaps RUN 11,177, LDP 2,871, STP 1,315. Satu load polinomial memakan sekitar 263 siklus untuk setiap `d` (satu koefisien per siklus). Port host mesin hanya bekerja saat mesin idle, sehingga setiap load dan store berurutan dengan mesin.
Dari program mesin (`tb/golden/kpke_smp_model.py`, varian OVERLAP, nomor slot perangkat keras): pada program encrypt t_hat (slot 7, 8, 9) pertama dipakai oleh operasi 31 dari 37 dan polinomial pesan (slot 11) oleh operasi terakhir; pada program decrypt hanya slot 3 (polinomial ciphertext pertama) dibutuhkan operasi pertama (NTT), slot 4 dan 5 oleh NTT kedua dan ketiga, slot rahasia 0, 1, 2 oleh perkalian, slot 10 oleh pengurangan terakhir. Jadi semua load kecuali yang pertama dapat berjalan saat mesin sudah menghitung.

## 2. Desain (varian baru; file Fase 6-8 dan `mlkem_core3` tidak diedit)
1. Loader dengan backpressure `rtl/mlkem/mlkem_ldpoly2o.sv`: `mlkem_ldpoly2` ditambah masukan `tb_wready_i`; sebuah koefisien ditulis dan diambil dari unpacker hanya pada siklus dengan `tb_wready_i = 1` (unpacker sudah punya `coef_ready_i`). Diikat ke 1 ia adalah `mlkem_ldpoly2`.
2. Varian sequencer mesin `rtl/sched/kpke_sched_smp4.sv` (salinan `kpke_sched_smp.sv`, parameter `HOSTOV`): (a) tulis host saat program berjalan diberikan hanya pada siklus ketika baik sequencer maupun beat sampler tidak menulis store (`tb_wready_o`); host punya prioritas terendah; (b) interlock: sebuah operasi tidak dimulai (sequencer menunggu di FETCH) selama slot yang dipakainya ditandai di `ov_pend_i` (NTT, INTT, SMPN, SMPA: d; PWM, ADD, SUB: d, a, b; PWMS: d, b). Baca host saat berjalan tidak mungkin (store tetap berurutan). Top `rtl/sched/kpke_smp_top_s10o.sv` meneruskan dua port baru.
3. Pengendali `rtl/mlkem/mlkem_core4.sv` (salinan `mlkem_core3.sv`) dengan dua operasi mikro: `RUNS prog mask` (mulai program mesin dan lanjut; `mask` = slot yang dimuat di belakangnya, ditulis ke register interlock `pend_q`) dan `RUNJ` (tunggu sampai mesin selesai; selesainya diingat, jadi tidak terlewat saat load berjalan). Load yang selesai menghapus bitnya di `pend_q`. `RUN` yang ada tetap (KeyGen). Membutuhkan `CODEC_W2 = 1`. ROM `rtl/mlkem/mlkem_ctl_rom3.sv`, dibangkitkan oleh `scripts/build/gen_mlkem_ctl_rom3.py` dari `tb/golden/mlkem_ctl_model3.py` (pemeriksaan statis `check_static3`).
4. Program baru: KeyGen tidak berubah. Encaps: `BGS; RD32 rho; LDP 7; JN; G; SDL; RUNS(encrypt, {8, 9, 11}); LDP 8, 9, 11; RUNJ; STP ...` (H(ek) di latar belakang di belakang RD32 dan satu load; ia tetap harus lengkap sebelum G, jadi sekitar 390 siklus tetap terlihat). Decaps: `BGS; LDP 3; RUNS(decrypt, {4, 5, 0, 1, 2, 10}); LDP 4, 5, 0, 1, 2, 10; RUNJ; STP 10; JN; G; RD32; SDL; RUNS(encrypt, {7, 8, 9, 11}); LDP 7, 8, 9, 11; RUNJ; STP ...; CMP`. Urutan load adalah urutan mesin memakainya.
5. Mengapa waktu-konstan: setiap tunggu adalah pada sinyal yang bergantung pada loader (panjang tetap) dan mesin (panjang tetap kecuali rejection sampling publik A); tidak ada kendali yang bergantung pada rahasia.
6. Pemeriksaan statis (`check_static3`): pemeriksaan model2 pada program baru; di antara `RUNS` dan `RUNJ` hanya `LDP`; mask tepat himpunan slot yang dimuat; setiap slot yang dimuat dipakai oleh program mesin; tidak ada STP, SDL, RUN, hash, WR32, RD32, CMP, atau END di antaranya; program paling banyak 64 word.

## 3. Estimasi (ESTIMATE; angka K3 MEASURED di `../9s2b/`, profil K2 di `../9s2/`)
| Besaran | K3 (siklus sama dengan K2) | K4 ESTIMATE (diberikan di chat sebelum run pertama) |
|---|---|---|
| Siklus KeyGen / Encaps / Decaps | 8,416 / 10,250 / 15,619 | 8,416 / sekitar 9,590 (-660) / sekitar 12,990 (-2,630) |
| ALM (median 15 ns) | median K3 di worksheet S2b | +50 sampai +300 (handshake loader, interlock, register pending, dua operasi mikro lagi) |
| Fmax | median K3 77.555 MHz pada 15 ns | dalam derau seed K3; jalur baru adalah grant tulis host ke store (tidak diketahui) |
| Latensi pada Fmax K3 | 108.5 / 132.2 / 201.4 us | 108.5 / sekitar 123.6 / sekitar 167.5 us |

## 4. Test (kedua simulator; RTL repository tidak pernah dimutasi, kontrol berjalan pada salinan)
| # | Test | Syarat lulus |
|---|---|---|
| V1 | lint: Verilator `-Wall` dan slang `mlkem_core4` (dan `mlkem_ldpoly2o`, `kpke_sched_smp4`, `kpke_smp_top_s10o`) pada K4 dan nilai bawaan | 0 peringatan, 0 error |
| V2 | model: `check_static3`; `mlkem_ctl_model3` sama dengan `mlkem_ctl_model2` (keygen, encaps, decaps, ciphertext valid dan dimodifikasi); `gen_mlkem_ctl_rom3.py --check` | lulus |
| V3 | inti K4 (`CORE_TOP=mlkem_core4 CORE_SMP0=1 CORE_K0=1 CORE_W2=1 CORE_P6=1 CORE_AR=1`): seluruh target `core` (ACVP keyGen 25, enkapsulasi 25, dekapsulasi 10, cross-check acak, rantai, protokol, siklus konstan) | 100 % sama, Verilator dan Icarus; jumlah siklus Encaps dan Decaps identik di semua masukan |
| V4 | profil pada K4 | dicatat; hitungan LDP / STP pengendali utama; hitungan RUN |
| V5 | kontrol langkah sebelumnya pada `mlkem_core4`: `nclen`, `ncoff`, `ncrom`, `ncprio`, `ncwr`, `ncjob`, `ncthr` (harus lulus), `ncthrnj` tidak dijalankan (ia memutasi baris yang dibagi core4; dinyatakan bila dilewati) | seperti disyaratkan |
| V6 | kontrol butir 4: `ncthrld` (port host diberikan satu siklus dari delapan, interlock utuh: load selesai terlambat dan mesin menunggu) harus LULUS seluruh target; `ncilk` (port ter-throttle yang sama TANPA interlock) harus GAGAL; `ncgrant` (tulis host ditulis walau sequencer menulis) harus GAGAL; `ncjoin` (`RUNJ` tidak menunggu) harus GAGAL | seperti disyaratkan |
| V7 | regresi: `mlkem_core3` pada K3 memberi 8,416 / 10,250 / 15,619 (file-nya sendiri tidak berubah); bawaan `mlkem_core` memberi 9,095 / 10,735 / 16,667; test sequencer mesin K-PKE (`run_smp_tests.py`) dengan file yang tidak berubah | PASS |
| V8 | formal, bila waktu mengizinkan: bukti stub-protokol 9f1b diadaptasi ke `mlkem_core4` (E1 non-interferensi, S1-S7, B1-B7) dengan stub `kpke_smp_top_s10o`; bila tidak dikerjakan dilaporkan tidak dikerjakan | dinyatakan |
| V9 | Quartus K4 (parameter K3, `mlkem_core4`) seed 1-6 pada 15.000 ns dan seed 1-6 pada 40.000 ns, satu kompilasi sekali; tanpa batasan di bawah 15 ns (ADR 0039) | ekstrak; timing terpenuhi; Fmax tiap seed |
| V10 | jalur kritis seed slack terkecil pada 15 ns | dicatat |

## 5. Aturan adopsi (ditetapkan sebelum kompilasi Quartus apa pun dan sebelum kontrol)
K4 diadopsi di atas K3 hanya bila semua berikut berlaku:
1. V1-V7 lulus seperti dinyatakan (ketidakcocokan ACVP apa pun menolaknya; kontrol yang tidak gagal seperti disyaratkan membatalkan klaim).
2. Timing terpenuhi pada 40.000 ns di setiap seed 1-6 (gerbang) dan pada 15.000 ns di setiap seed 1-6.
3. Median ALM paling banyak 20,000 (15 ns dan 40 ns).
4. Untuk Encaps dan Decaps, t = siklus / median Fmax pada 15 ns K4 lebih rendah dari K3; untuk KeyGen (siklus sama) t tidak lebih dari 3 % di atas K3 (selisih hanya derau Fmax).
5. Jumlah seed yang terpenuhi pada 15 ns dilaporkan; median Fmax dan sebaran K4 lawan K3 (77.555 MHz, enam seed S2b, K3-15-s1..s6) dinyatakan, dan penurunan Fmax lebih besar dari sebaran seed disebut penurunan.
Bila tidak, K4 dilaporkan tidak diadopsi. Hasilnya adalah ADR Proposed. V8 tidak dikerjakan tidak menolak K4 tetapi dinyatakan di samping adopsi sebagai batas evidence.

## 6. Bukan bagian langkah ini
Tanpa baca lewat port host saat mesin berjalan (store tetap berurutan), tanpa tumpang tindih store dengan mesin, tanpa perubahan program mesin atau aritmetika, tanpa sampler kedua, tanpa batasan di bawah 15 ns, tanpa hasil papan. Waktu-konstan berarti invarian jumlah siklus saja.
