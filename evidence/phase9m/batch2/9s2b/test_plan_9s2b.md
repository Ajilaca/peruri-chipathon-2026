<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Fase 9F langkah S2b: alamat issue terregister di inti NTT/INTT (alamat dihitung satu siklus lebih awal) - test plan dan aturan adopsi

Ditulis 2026-10-04 sebelum RTL S2b apa pun dan sebelum pengukuran S2b apa pun. Lingkup: S2b adalah tindak lanjut yang disebut di `../9s2/result_9s2.md` bagian 6 (Batch 2, Jevan, sesi yang sama; commit di branch `phase9m-optimisation`, belum dibuat). Baseline: K2 (`../9s2/`, `mlkem_core3` dengan `NTT_P6 = 1`). Label: MEASURED, ESTIMATE, INFERENCE. Timing statis kernel-only dengan virtual pin; bukan hasil papan.

## 1. Mengapa (MEASURED: jalur terburuk K2-15-s5, slack +1.404 ns pada 100 C; `../9s2/critical_paths_K2-15.md`; pembacaan tingkat-elemen laporan yang sama, 2026-10-04)
55 dari 300 jalur terburuk K2 berjalan dari `layer_q` ke port alamat dan tulis bank M10K, sisanya dalam 144 pertama berada di +2.354 ns dan lebih. Jalur terburuk adalah satu siklus clock dan punya dua separuh yang kira-kira sama panjang:
1. Aritmetika alamat (sekitar 5 ns, `layer_q` ke keluaran penjumlah): dekode `log2len` dari `layer_q` dan `mode_q` (0.6 ns), shift `p >> log2len` dan `block << (log2len+1)` (1 ns), penjumlah untuk `j` dan `j + len` (sekitar 3 ns).
2. Dekode bank dan multiplekser alamat (sekitar 6 ns, keluaran penjumlah ke pin alamat RAM): nomor bank setiap port (`bank_r`, fanout 65), lalu untuk setiap bank multiplekser yang memilih alamat port yang mengalamatinya (dua level LUT dengan routing 1.6 ns dan 1.7 ns), lalu port RAM.
Hanya separuh pertama yang bergantung pada counter jadwal. Jika alamat siklus berikutnya dihitung di siklus sebelumnya dan diregister, jalur terbelah di keluaran penjumlah: kedua separuh muat dalam satu siklus dengan margin (separuh pertama lalu mulai di `t_q` / `layer_q` dan berakhir di register, sekitar 5 ns ditambah logika next-state counter, sekitar 1.5 ns; separuh kedua mulai di register, sekitar 6.5 ns). Itu potongan di tengah jalur, tanpa siklus tambahan karena alamat terregister adalah nilai yang sama yang dipakai di siklus yang sama hari ini.
Kelas di belakangnya pada seed K2, MEASURED: `mode_q` ke reducer Barrett (+2.354 ns, 144 jalur), delay operand-samping ke M10K (+2.102 ns, 45), delay posisi-baca ke reducer (+2.587 ns, 24), reducer ke M10K (+2.349 ns, 18). Jadi kasus terbaik untuk S2b adalah penghalang sekitar +2.1 sampai +2.4 ns, sekitar 0.7 sampai 1.0 ns lebih baik daripada seed K2 yang dianalisis (INFERENCE).

## 2. Desain (sebuah parameter, seperti S2)
1. Parameter `AREG` (bawaan 0, desain K2 / K1b) pada `rtl/ntt/ntt_core_s10.sv`: bila 1, alamat stage issue `j_lane` dan `jlen_lane` transformasi (`state_q == S_RUN`) berasal dari register `j_q` dan `jlen_q` yang dimuat setiap siklus dengan nilai yang akan dihasilkan aritmetika kombinasional pada siklus berikutnya: fungsi yang sama dievaluasi pada `layer_d`, `t_d`, dan mode siklus berikutnya (`mode_i` pada siklus yang memulai run, `mode_q` selain itu). Jalur host (akses alamat tunggal lajur 0 di luar run, `host_addr_i`) tetap kombinasional, jadi latensi baca host (2) dan sequencer tidak tersentuh. Tidak ada hal lain yang berubah: enable, kendali tulis, jalur zeta, memori dan delay tulisnya.
2. Penerusan parameter seperti S2: parameter gaya-`P6` `AREG` pembungkus `ntt_core_s10_p5`, `NTT_AR` pada `kpke_smp_top_s10` dan `mlkem_core3` (semua bawaan 0), dan parameter tambahan yang sama pada stub formal mesin (`formal/phase09-integration/9c/stubs_9c.sv`; pelajaran S2: alur formal `mlkem_core3` gagal dielaborasi tanpanya).
3. Argumen ekuivalensi (INFERENCE, diperiksa dengan test): dengan `AREG = 1` alamat yang disajikan ke memori di setiap siklus run sama dengan alamat `AREG = 0` di siklus itu, jadi setiap permintaan, waktu tulis, jumlah siklus, dan hasil tidak berubah. Jumlah siklus per transformasi tetap 119 (pada P = 6). Selisih apa pun adalah bug.
4. Biaya (ESTIMATE): 8 lajur x dua register alamat 8-bit = 128 register; tanpa perubahan ALM selain routing.

## 3. Estimasi yang ditulis sebelum mengukur (ESTIMATE; angka K2 MEASURED)
| Besaran | K2 (MEASURED) | S2b ESTIMATE |
|---|---|---|
| Siklus per transformasi (NTT, INTT) | 119 | 119 (tidak berubah) |
| Siklus KeyGen / Encaps / Decaps | 8,416 / 10,250 / 15,619 | sama |
| Median ALM pada 40 ns | 14,213.0 | dalam +-150 |
| Register (40 ns) | 8,327-8,375 | +100 sampai +200 |
| Blok RAM / DSP | 54 / 28 | 54 / 28 |
| Fmax slow corner terendah pada 15 ns, median 6 seed | 74.125 MHz | 75 sampai 79 MHz. Keyakinan rendah: rencana S2 memperkirakan 76 sampai 80 MHz dan mengukur 74.1 karena kelas berikutnya hanya 0.2 ns di belakang; di sini kelas di belakang yang terburuk berada 0.7 sampai 1.0 ns di belakang (INFERENCE), hanya 300 jalur satu seed yang diketahui, dan derau seed sekitar 3 MHz |
| Latensi pada 15 ns, KeyGen / Encaps / Decaps (siklus / median Fmax) | 113.5 / 138.3 / 210.7 us | 107 sampai 112 / 130 sampai 137 / 198 sampai 208 us |
Hasil di luar rentang dinyatakan demikian di laporan.

## 4. Test (kedua simulator; RTL repository tidak pernah dimutasi, kontrol pada salinan)
| # | Test | Syarat lulus |
|---|---|---|
| V1 | lint: Verilator `-Wall` dan slang `ntt_core_s10_p5` (`AREG` 0 dan 1), `kpke_smp_top_s10`, `mlkem_core3` pada K2 dengan `NTT_AR` 0 dan 1 | 0 peringatan, 0 error |
| V2 | unit test inti NTT pada P = 6 dengan `AREG = 1` (target baru `s10p6a` dari `tb/s10/run_s10_tests.py`) | NTT dan INTT bit-exact, siklus tepat 119 / 119, 0 stall, Verilator dan Icarus |
| V3 | kontrol NC-A1: salinan di mana alamat terregister diambil satu siklus terlalu terlambat (register dimuat dari nilai siklus saat ini) | NTT dan INTT bit-exact harus FAIL |
| V4 | formal: bukti kendali S10 pada P = 6 dengan `AREG = 1` (properti H, O, R, A, B, C; salinan top formal S2), dan kontrol negatifnya NC-O, NC-A | bukti PASS, kontrol FAIL seperti disyaratkan |
| V5 | test sequencer K-PKE dengan `NTT_P6 = 1`, `NTT_AR = 1` (`KP_VAR = 2`, sampler K0) | 3/3 lulus, kedua simulator |
| V6 | inti `mlkem_core3` pada `NTT_P6 = 1`, `NTT_AR = 1`: seluruh target `core` dan profil | 100 % sama; siklus identik dengan K2 (8,416 / 10,250 / 15,619); Encaps dan Decaps identik di semua masukan; Verilator dan Icarus |
| V7 | regresi pada nilai bawaan: profil `AREG = 0` sama dengan profil K2 dan K1b (8,416 / 10,250 / 15,619 pada `NTT_P6 = 1`, 8,404 / 10,236 / 15,597 pada 0); target `run_s10_tests.py` bawaan (118) dan `s10p6` (119) lulus; formal `mlkem_core3` (bukti 9f1b) masih dielaborasi dan lulus dengan perubahan stub | PASS |
| V8 | Quartus K3 (K2 + `NTT_AR = 1`) seed 1-6 pada 40.000 ns (gerbang) dan K3-15 seed 1-6 pada 15.000 ns, satu kompilasi sekali (batas RAM mesin: paling sedikit 2 GB bebas), tanpa batasan di bawah 15 ns (ADR 0039) | ekstrak; timing terpenuhi pada 40 ns di setiap seed; pada 15 ns jumlah seed yang terpenuhi dan Fmax tiap seed |
| V9 | jalur kritis seed slack terkecil pada 15 ns, diklasifikasi seperti di S2, ditambah pembacaan tingkat-elemen jalur terburuk | dicatat: blok mana penghalang berikutnya |

## 5. Aturan adopsi (ditetapkan sebelum mengukur; ADR 0036: menurut latensi pada 15 ns; diperketat setelah S2: kenaikan di dalam derau seed tidak diadopsi)
S2b diadopsi di atas K2 hanya bila semua berikut berlaku:
1. V1-V7 lulus seperti dinyatakan (ketidakcocokan ACVP apa pun menolaknya).
2. Timing terpenuhi pada 40.000 ns di setiap seed 1-6.
3. Median ALM paling banyak 20,000.
4. Untuk masing-masing KeyGen, Encaps, dan Decaps, t = siklus / median Fmax pada batasan 15 ns (slow corner terendah, seed 1-6) K3 lebih rendah dari K2 (113.5 / 138.3 / 210.7 us).
5. Kenaikan median Fmax atas K2 (74.125 MHz) lebih besar dari sebaran seed yang lebih besar milik K2 (3.38 MHz) dan K3, atau seed terendah K3 di atas seed tertinggi K2 (76.03 MHz); kenaikan di dalam derau dilaporkan netral dan S2b lalu tidak diadopsi (pelajaran S2).
6. Jumlah seed yang terpenuhi pada 15 ns dilaporkan.
Bila tidak, S2b dilaporkan tidak diadopsi dan K2 tetap. Hasilnya adalah ADR Proposed.

## 6. Bukan bagian langkah ini
Tanpa perubahan aritmetika, jadwal, peta memori, atau peta bank; tanpa perubahan jalur host atau sequencer; tanpa sampler kedua (S3); tanpa tumpang tindih dengan mesin (butir 4); tanpa batasan di bawah 15 ns; tanpa hasil papan. Bila V9 menunjukkan penghalang berikutnya yang dapat digeser perubahan kecil lain, itu hanya diusulkan di laporan. Waktu-konstan berarti invarian jumlah siklus saja.

## 7. Amandemen A1 (2026-10-04, sebelum pengukuran S2b apa pun; tidak ada di atas yang diedit)
1. Gerbang 40 ns tetap. Usulan melewati kompilasi 40 ns dibuat dan ditarik pada hari yang sama (Jevan, chat 2026-10-04: "kita test aja di 40ns gapapa"): bagian 4 (V8) dan 5 (butir 2 dan 3) berlaku sebagaimana tertulis, enam kompilasi pada 40.000 ns (`K3`, `K3-s2` .. `K3-s6`) setelah enam pada 15.000 ns.
2. Keputusan untuk batch (Jevan, chat sama): setelah S2b pekerjaan beralih ke butir 4 (tumpang tindih load / store dengan mesin). Jika S2b, seperti S2, tidak memberi efek di luar derau seed, S2 dan S2b akan dihapus (apa tepatnya yang dihapus dikonfirmasi dengan tim sebelum ada yang dihapus; evidence hasil negatif disimpan kecuali tim berkata lain).
3. Catatan run: runner pertama `run_k3.sh` (15 ns dulu, lalu 40 ns) dihentikan setelah K3-15-s1 (rc 0) karena kesalahan operator saat K3-15-s2 berjalan; sisanya berjalan di bawah `run_k3_15.sh` (K3-15-s3 .. s6, K3-15-s2 selesai di sampingnya) lalu `run_k3_40.sh` (enam revisi 40 ns). Kompilasi sama, urutan hasil sama, satu per satu.

## 8. Amandemen A2 (2026-10-04, ditulis SETELAH enam seed 15 ns diukur; aturan bagian 5 tidak diubah)
Enam seed 15 ns memberi median K3 77.555 MHz lawan 74.125 MHz milik K2 (+3.430 MHz), lima dari enam seed K3 (77.32-79.37 MHz) di atas setiap seed K2 (maksimum 76.03 MHz) dan satu seed (seed 4, 73.02 MHz) di bawah; sebaran K3 (6.35 MHz) lebih besar dari kenaikan, jadi butir 5 bagian 5 tidak terpenuhi sebagaimana tertulis. Atas permintaan Jevan (chat 2026-10-04: "setelah 40ns selesai jalankan 3 seed tambahan") tiga seed lagi (7, 8, 9) K3 pada 15.000 ns dikompilasi setelah kompilasi 40 ns (`K3-15-s7` .. `K3-15-s9`, `run_k3_x.sh`). Ini informasi tambahan yang dipilih setelah melihat hasil: hasil formal aturan tetap "tidak terpenuhi sebagaimana tertulis" dengan enam seed; statistik sembilan seed (median, sebaran, berapa seed di atas seed tertinggi K2) dilaporkan di sampingnya, dan tidak ada seed yang dibuang atau diganti. K2 hanya punya enam seed; perbandingan sembilan lawan enam dinyatakan demikian. Adopsi tetap keputusan tim (ADR Proposed).
