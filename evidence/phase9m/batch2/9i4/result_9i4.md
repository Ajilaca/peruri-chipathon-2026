<!-- claim-lint: skip-file (internal block report, not proposal text) -->
# Laporan Fase 9I butir 4: load polinomial di belakang mesin K-PKE (konfigurasi K4 = `mlkem_core4`)

- Status: SELESAI (STOP setelah langkah). Branch `phase9m-optimisation`, belum di-commit saat penulisan. Hanya file baru (file Fase 6-8 dan `mlkem_core3` tidak diedit): `rtl/mlkem/mlkem_core4.sv`, `rtl/mlkem/mlkem_ldpoly2o.sv`, `rtl/mlkem/mlkem_ctl_rom3.sv` (dibangkitkan oleh `scripts/build/gen_mlkem_ctl_rom3.py` dari `tb/golden/mlkem_ctl_model3.py`), `rtl/sched/kpke_sched_smp4.sv`, `rtl/sched/kpke_smp_top_s10o.sv`. Rencana dan aturan: `test_plan_9i4.md` (keterbukaan proses: RTL dan simulasi inti pertama ditulis sebelum rencana; aturan bagian 5 ditulis sebelum kompilasi Quartus apa pun dan sebelum run kontrol, dan tidak disetel ke hasil). Timing statis kernel-only dengan virtual pin; bukan sistem di papan. Dua belas kompilasi Quartus, semuanya `rc=0`, satu per satu.

## 1. Hasil
Aturan rencana mengadopsi K4. Load polinomial kini berjalan saat mesin K-PKE menghitung; pengendali memulai program mesin, memuat polinomial lain di belakangnya (interlock per slot menahan operasi mesin yang butuh slot yang belum dimuat) dan melakukan join. Siklus (masukan profil, simulasi): KeyGen 8,416 (tidak berubah), Encaps 9,611 (-639, -6.2 %), Decaps 12,989 (-2,630, -16.8 %) terhadap K3 (10,250 dan 15,619). Median Fmax pada 15 ns 76.665 MHz lawan 77.555 MHz milik K3 (-0.89 MHz, di dalam sebaran seed). Latensi pada 15 ns (siklus / median Fmax, perhitungan tim): 109.8 / 125.4 / 169.4 us lawan 108.5 / 132.2 / 201.4 us milik K3 (+1.2 %, -5.1 %, -15.9 %). Median ALM +106.5 (40 ns) dan +187.0 (15 ns); register, blok RAM, dan DSP: lihat bagian 2. ACVP 100 % di kedua simulator. Batas evidence: bukti formal terbatas P1 dan kontrol negatif NC-E1-4 timeout; keduanya tidak punya hasil formal (bagian 3).

## 2. Parameter yang diukur (MEASURED; `selection_worksheet.md`, ekstrak `quartus_K4*.md`, K3 dari `../9s2b/`)
| Parameter | K3 | K4 | Selisih |
|---|---|---|---|
| Modul / parameter | `mlkem_core3`, `NTT_P6 = 1`, `NTT_AR = 1` | `mlkem_core4`, sama, `CODEC_W2 = 1` diperlukan | |
| Median ALM, 40 ns, seed 1-6 (min-maks) | 14,115.5 (14,081-14,153) | 14,222.0 (14,189-14,251) | +106.5 |
| Median ALM pada 15 ns | 14,293.0 (14,139-14,359) | 14,480.0 (14,450-14,519) | +187.0 |
| Register, 40 ns / 15 ns | 8,462-8,508 / 8,400-8,472 | 8,472-8,510 / 8,471-8,570 | sekitar +0 sampai +100 |
| Blok RAM / DSP | 54 / 28 (53 pada 15 ns) | 54 / 28 (53 pada 15 ns) | 0 |
| Timing terpenuhi pada 40.000 ns | 6 dari 6 | 6 dari 6 | |
| Slack setup terburuk, 40 ns / 15 ns (semua corner) | +20.302 ns / +1.305 ns | +16.690 ns / +0.596 ns | lebih tipis pada 15 ns |
| Fmax slow corner terendah pada 15 ns, median (min-maks) | 77.555 MHz (73.02-79.37) | 76.665 MHz (69.43-80.99) | -0.890 MHz, di dalam sebaran |
| Siklus per transformasi (NTT, INTT) | 119 | 119 | 0 |
| Siklus KeyGen / Encaps / Decaps (masukan profil; simulasi) | 8,416 / 10,250 / 15,619 | 8,416 / 9,611 / 12,989 | 0 / -639 / -2,630 |
| Siklus masukan test (Encaps / Decaps) | 10,194 / 15,563 | 9,555 / 12,933 | -639 / -2,630 |
| Latensi pada 15 ns (median Fmax; perhitungan tim) | 108.5 / 132.2 / 201.4 us | 109.8 / 125.4 / 169.4 us | +1.16 % / -5.15 % / -15.87 % |
| Latensi pada 15 ns (Fmax terendah dari 6) | 115.3 / 140.4 / 213.9 us | 121.2 / 138.4 / 187.1 us | |
| Peringatan kritis per kompilasi | 1 | 1 | peringatan clock virtual pin di setiap kompilasi kernel-only |
Denominator fitter: 41,910 ALM, 553 blok RAM, 112 DSP: K4 memakai sekitar 34.5 % ALM, 53-54 blok RAM (sekitar 10 %), 28 DSP (25 %).

## 3. Test (MEASURED; `sim.md`, `formal.md`)
| # | Hasil | Evidence |
|---|---|---|
| V1 lint | `verilator --lint-only -Wall`: 0 peringatan pada `NTT_AR` 0 dan 1; `slang`: 0 error, 0 peringatan | `sim.md` |
| V2 model | `gen_mlkem_ctl_rom3.py --check`: ROM sama dengan yang dibangkitkan, `check_static3` lulus | sama |
| V3 inti K4 | keyGen 25, enkapsulasi 25, dekapsulasi 10 sama; 20 kasus acak sama; rantai, protokol, siklus konstan lulus; Verilator 6/6, Icarus 6/6 (+ `nclen` seperti disyaratkan) | sama |
| V4 profil | KeyGen 8,416 / Encaps 9,611 / Decaps 12,989; RUNJ 6,245 dan 6,367 | sama, `profile_k4_verilator.json` |
| V5, V6 kontrol | `nclen`, `ncoff`, `ncrom`, `ncprio`, `ncwr`, `ncjob`, `ncilk`, `ncgrant`, `ncjoin` gagal seperti disyaratkan; `ncthr` dan `ncthrld` (port ter-throttle, interlock utuh) lulus seluruh target; dua kontrol awalnya salah dan diperbaiki (catatan run di file sim) | sama |
| V7 regresi | profil K3 `mlkem_core3`, bawaan `mlkem_core`, dan test sequencer tidak berubah | sama, `../9s2b/sim.md` |
| V8 formal | A (E1 non-interferensi dengan `pend_q` dan `eng_dn_q`, S1-S7, B1-B7): PASS (base case dan induksi); cover: PASS; NC-JOIN4: FAIL seperti disyaratkan; P1 (terbatas, kedalaman 160): TIMEOUT; NC-E1-4: TIMEOUT (percobaan ulang 4 jam dihentikan setelah sekitar 2 jam 40 menit atas keputusan tim; P2 dibuang dan tidak terbukti) | `formal.md` |
| V9 Quartus | K4-15 seed 1-6 dan K4 seed 1-6 pada 40 ns: semuanya `rc=0`; terpenuhi pada 40 ns 6 dari 6, pada 15 ns 6 dari 6 | `quartus_K4*.md` |
| V10 jalur kritis K4-15-s6 | terburuk +0.736 ns (slow 100 C): jalur S2b `cnt_q` -> `core_hwe_o` -> `start_go` -> penjumlah alamat -> `jlen_r`; butir 4 (grant, interlock, `pend_q`) tidak termasuk 300 terburuk | `critical_paths_K4-15.md` |

## 4. Aturan rencana (bagian 5), diterapkan pada file
1. V1-V7 lulus: terpenuhi (dua kontrol yang salah dikoreksi dan dijalankan ulang, dinyatakan di file sim). V8 bukan bagian aturan; batasnya dinyatakan di atas.
2. Timing pada 40 ns dan 15 ns di setiap seed 1-6: terpenuhi (6 dari 6 dan 6 dari 6).
3. Median ALM paling banyak 20,000: terpenuhi (14,222.0 dan 14,480.0).
4. Latensi Encaps dan Decaps lebih rendah dari K3; KeyGen tidak lebih dari +3 %: terpenuhi (Encaps -5.15 %, Decaps -15.87 %, KeyGen +1.16 %).
5. Seed terpenuhi pada 15 ns: 6 dari 6. Median Fmax 76.665 lawan 77.555 MHz (-0.890); sebaran K4 11.56 MHz, K3 6.35 MHz; penurunan tidak lebih besar dari sebaran, jadi tidak disebut penurunan; seed terendah K4 (69.43 MHz) 3.6 MHz di bawah terendah K3 (73.02 MHz).
Aturan mengadopsi. Tim memutuskan (ADR 0043 Proposed). Basis pengukuran adalah K3 (ADR 0042, Proposed, tidak diadopsi oleh aturannya sebagaimana tertulis).

## 5. Estimasi lawan pengukuran (ditulis di rencana sebelum pengukuran)
- Siklus Encaps sekitar -660 dan Decaps sekitar -2,630, KeyGen tidak berubah: terpenuhi (-639, -2,630, 0).
- ALM +50 sampai +300: terpenuhi (+106.5 pada 40 ns, +187.0 pada 15 ns).
- Fmax dalam derau seed K3: terpenuhi (-0.89 MHz, di dalam sebaran keduanya).
- Latensi pada Fmax K3 108.5 / sekitar 123.6 / sekitar 167.5 us: pada median Fmax K4 nilai terukur adalah 109.8 / 125.4 / 169.4 us (estimasi mengasumsikan Fmax K3; selisihnya adalah 0.89 MHz).

## 6. Temuan
1. Tumpang tindih bekerja sesuai desain dan terverifikasi: bit-exact terhadap model golden pada 60 vektor ACVP dan 20 kasus acak di dua simulator; setiap tunggu bergantung pada blok panjang-tetap (loader, mesin) atau rejection sampling publik A, tidak pernah pada rahasia (jumlah siklus Encaps dan Decaps identik di semua masukan yang diuji).
2. Penghematan ada di Encaps dan Decaps (load di belakang mesin); KeyGen tidak punya load untuk disembunyikan dan tidak berubah. Decaps mendapat lebih banyak karena memuat lebih banyak polinomial (decrypt lalu enkripsi ulang).
3. Seed Fmax rendah K4 bukan jalur butir 4. Jalur terburuk seed slack terkecil (69.43 MHz) milik alamat issue terregister S2b (`start_go` bergantung pada counter sequencer lewat enable tulis host). Butir 4 tidak membuat jalur kritis baru di 300 jalur terburuk seed itu.
4. Evidence formal tidak lengkap untuk P1 dan NC-E1-4. P1 (mesin tidak sibuk di STP dan SDL) bertumpu pada simulasi (ACVP, siklus konstan, kontrol `ncjoin` dan `ncgrant`) dan pada kontrol negatif NC-JOIN4 yang gagal di run formal.
5. Biaya: sekitar 190 ALM (+1.3 %) dan beberapa puluh register; tanpa blok RAM atau DSP.

## 7. Yang tidak ditunjukkan ini
Tidak ada hasil papan; tidak ada klaim kecepatan terhadap perangkat lunak; timing statis kernel-only dengan virtual pin; derau seed 3 sampai 11 MHz membatasi pernyataan Fmax di bawah ukuran itu; waktu-konstan berarti invarian jumlah siklus saja; ACVP dan kontrol adalah simulasi; model formal memakai stub protokol, dan P1 serta NC-E1-4 tidak punya hasil formal; store masih berurutan dengan mesin dan KeyGen tidak berubah (langkah berikutnya yang mungkin); satu seed (K4-15-s6) dianalisis untuk jalurnya.

## 8. File
`test_plan_9i4.md`, `selection_worksheet.md`, `sim.md`, `formal.md`, `critical_paths_K4-15.md`, `profile_k4_verilator.json`, `cycles_*_core_k4.json`, dua belas ekstrak `quartus_K4*.md`, `quartus/phase09i4_core/` (dua belas revisi, `run_k4.sh`), `scripts/quartus/select_9i4.py`, `scripts/build/gen_mlkem_ctl_rom3.py`, `tb/golden/mlkem_ctl_model3.py`, `formal/run/run_formal_phase9i4.py`, `formal/phase09m-optimisation/9i4/`, runner yang berubah `tb/mlkem/run_core_tests.py`, `tb/mlkem/test_profile_core.py`, `scripts/quartus/archive_quartus_outputs.py`.
