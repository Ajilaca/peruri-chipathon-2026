<!-- claim-lint: skip-file (internal block report, not proposal text) -->
# Laporan Fase 9F langkah S1b: hash berjalan di samping pekerjaan lain (konfigurasi K1b)

- Status: SELESAI (STOP setelah langkah, ADR 0036; menutup Batch 1). Branch `phase9m-optimisation`. RTL: modul baru `rtl/mlkem/mlkem_core3.sv` dan `rtl/mlkem/mlkem_ctl_rom2.sv` (dibangkitkan dari model golden baru `tb/golden/mlkem_ctl_model2.py`; amandemen A1 rencana). Rencana dan aturan: `test_plan_9f1b.md` (ditulis sebelum RTL). Timing statis kernel-only dengan virtual pin; bukan sistem di papan. Dua belas kompilasi Quartus, semuanya `rc=0` (K1b-15-s5 dikompilasi dua kali: percobaan pertama dimatikan oleh restart sesi dan tidak dipakai).

## 1. Hasil
K1b diadopsi oleh aturannya dan memulihkan biaya siklus K1. K1b = K1 dengan tiga hash independen (KeyGen H(ek), Encaps H(ek), Decaps J) berjalan di sidecar latar belakang saat pengendali utama memuat atau menyimpan: siklus turun 391 / 391 / 386 terhadap K1 (8,404 / 10,236 / 15,597), dengan +274 ALM (40 ns). Timing terpenuhi pada 40 ns di 6 dari 6 seed dan pada 15 ns di 6 dari 6 seed; latensi pada 15 ns 5.5 / 4.7 / 3.5 % di bawah K1 dan, terhadap inti 9M-1 (MW) pada 15 ns (S0, dua seed), sama dalam +0.2 % (113.8 / 138.6 / 211.2 us lawan 113.6 / 138.5 / 211.6 us), dengan 3,500 ALM (-20 %) lebih sedikit. K1b tidak menaikkan Fmax: penghalang pada 15 ns masih inti NTT / memori (bagian 4).

## 2. Parameter yang diukur (MEASURED; `selection_worksheet.md`, ekstrak `quartus_K1b*.md`)
| Parameter | K1 (S1) | K1b (S1b) | Selisih |
|---|---|---|---|
| Median ALM, 40 ns, seed 1-6 (min-maks) | 14,061.0 (14,002-14,108) | 14,335.0 (14,329-14,376) | +274.0 (+1.9 %) |
| Median ALM, 15 ns, seed 1-6 | 14,211.5 (14,173-14,273) | 14,435.0 (14,390-14,459) | +223.5 |
| ALM dalam % dari 41,910 fitter | 34 % | 34 % | |
| Register, 40 ns | 8,348-8,452 | 8,211-8,258 | sekitar 150 lebih sedikit |
| Blok RAM / DSP | 54 (53 pada 15 ns) / 28 | 54 (53 pada 15 ns) / 28 | 0 |
| Timing terpenuhi pada 40.000 ns | 6 dari 6 | 6 dari 6 | |
| Slack setup terburuk atas seed, 40 ns | +19.063 ns | +18.043 ns | |
| Fmax slow corner terendah, 40 ns, median (min-maks) | 51.765 MHz (47.76-53.40) | 51.730 MHz (45.54-52.28) | sama |
| Timing terpenuhi pada 15.000 ns | 6 dari 6 | 6 dari 6 | |
| Slack setup terburuk atas seed, 15 ns | +1.114 ns | +1.007 ns | |
| Fmax slow corner terendah pada 15 ns, median (min-maks) | 73.070 MHz (72.01-74.10) | 73.855 MHz (71.46-74.40) | +0.8 MHz, di dalam sebaran |
| Siklus KeyGen / Encaps / Decaps (masukan profil; simulasi) | 8,795 / 10,627 / 15,983 | 8,404 / 10,236 / 15,597 | -391 / -391 / -386 (-4.4 %, -3.7 %, -2.4 %) |
| Latensi pada 15 ns, median Fmax (perhitungan tim) | 120.4 / 145.4 / 218.7 us | 113.8 / 138.6 / 211.2 us | -5.5 %, -4.7 %, -3.5 % |
| Latensi inti 9M-1 pada 15 ns (S0, Fmax lebih rendah dari 2 seed) | 113.6 / 138.5 / 211.6 us | | K1b +0.2 %, +0.0 %, -0.2 % |
| Peringatan kritis per kompilasi | 1 | 1 | |
Per state (profil, `profile_k1b_verilator.json` lawan `../9f1/profile_k1_verilator.json`): hanya state hash yang berubah (HFD 364 -> 7 dan HGT 67 -> 35 di KeyGen; HFD 367 -> 10, HGT 67 -> 35 di Encaps; HFD 360 -> 10, HGT 67 -> 35 di Decaps) dan dua siklus fetch / dispatch lebih sedikit; hitungan LDP, STP, RUN, SDL, WR32, RD32, dan CMP sama dengan K1: sidecar tidak pernah menunda pengendali utama.
Perbandingan dengan MW memakai Fmax yang lebih rendah dari dua seed untuk MW dan median enam untuk K1b: indikatif, bukan setara.

## 3. Test (MEASURED)
| # | Hasil | Evidence |
|---|---|---|
| V1 lint | `verilator --lint-only -Wall` `mlkem_core3` pada parameter K1 dan nilai bawaan: rc 0, tanpa peringatan; `slang`: 0 error, 0 peringatan (dijalankan saat build; keluaran tidak disimpan) | laporan ini |
| V2 model | `check_static2` lulus; program baru memberi keluaran keygen / encaps / decaps yang sama dengan program Fase 9 untuk 2 kasus acak (ciphertext valid dan dimodifikasi; rencana meminta 200: tidak dilakukan, ACVP dan 20 kasus acak V3 pada RTL mencakupnya); `gen_mlkem_ctl_rom2.py --check` lulus (program 22 / 22 / 33 word) | run saat build; ACVP V3 adalah bukti akhir |
| V3 inti K1b ACVP: keyGen 25, enkapsulasi 25, dekapsulasi 10, cross-check acak (20), rantai, protokol, siklus konstan | 6/6 lulus di Verilator dan Icarus (file akhir) | `sim.md`, `cycles_*_core_k1b_*.json` |
| V4 profil | lihat bagian 2 | `profile_k1b_verilator.json` |
| V5 siklus konstan | Encaps 10,180 dan Decaps 15,541 identik di semua masukan yang diuji (angka rentang ACVP); KeyGen 8,332-8,385 atas seed ACVP (sampling publik A, seperti sebelumnya) | `sim.md` |
| V6 kontrol negatif (salinan; RTL repository tidak dimutasi) | `nclen`, `ncoff`, `ncrom` (Verilator), `nclen` (Icarus) gagal seperti disyaratkan; NC-PRIO (baca sidecar menang) gagal di Encaps dan Decaps (run pertama mengharapkan `test_acvp_keygen`, test yang salah, KeyGen tidak membaca saat jobnya berjalan; dikoreksi ke `test_acvp_encaps` dan dijalankan ulang: gagal seperti disyaratkan); NC-WR gagal di KeyGen; NC-ROM (offset job +1) gagal; sidecar yang di-throttle lulus seluruh target inti (join menunggu job lambat) dan salinan ter-throttle tanpa perlindungan apa pun gagal (join efektif, bukan hanya tidak pernah dibutuhkan) | `sim.md` |
| V7 formal (dua salinan, stub protokol): E1, S1-S7, B1-B7 | PASS (basecase dan induksi, setelah satu invarian pendukung: sidecar berjalan hanya saat pengendali utama tidak idle); cover: tulis digest sidecar (langkah 155) dan baca sidecar (langkah 9) tercapai; kontrol NC-B3 dan NC-E1 FAIL seperti disyaratkan; NC-B7 timeout pada 1,800 s (tidak ada pelanggaran ditemukan sampai langkah 94), percobaan ulang 3 jam belum punya hasil saat laporan ini: kontrol B7 ditunjukkan oleh simulasi (NC-WR), bukan oleh run formal | `formal.md` |
| V8 regresi | nilai bawaan `mlkem_core` dan `mlkem_core2` sama dengan profil Fase 9 (S1 V7, `../9f1/regression_default.md`); `mlkem_core3` pada parameter bawaannya sendiri (C5) tidak dijalankan (hanya parameter K1) | |
| V9 Quartus | K1b seed 1-6 pada 40 ns dan K1b-15 seed 1-6 pada 15 ns, semuanya terpenuhi; jalur kritis pada 15 ns (K1b-15-s1): 298 dari 300 di kelas inti NTT / memori / PWM (+1.170 ns), 2 di sequencer mesin ke sponge sampler (+2.420 ns) | `quartus_K1b*.md`, `critical_paths_K1b-15.md` |

## 4. Temuan
1. S1b mengembalikan siklus tanpa biaya area atau Fmax selain +274 ALM. Dengan S1 dan S1b bersama inti punya latensi inti 9M-1 pada 15 ns (dalam +0.2 % terhadap dua seed S0) dan area 20 % lebih kecil (14,335 lawan 17,654 ALM pada 40 ns).
2. Penghalangnya tidak berubah. Pada 15 ns jalur terburuk berada di inti NTT / memori / PWM (298 dari 300): S1 dan S1b tidak menyentuhnya; menaikkan Fmax butuh perubahan di sana (S2, Batch 2).
3. Tidak ada biaya timing dari sidecar: sidecar tidak termasuk 300 jalur terburuk pada 15 ns; median Fmax pada 15 ns 73.855 MHz lawan 73.070 MHz untuk K1 (di dalam sebaran seed).
4. Penghematan hanya dari tiga hash independen (sekitar 390 dari 8,400 / 10,200 / 15,600 siklus, 2.4-4.4 %). Hash pada rantai ketergantungan (`G` KeyGen, `G` Decaps) tetap di latar depan.
5. Waktu konstan: jumlah siklus Encaps dan Decaps identik di semua masukan yang diuji; tidak ada kendali yang bergantung pada rahasia (E1 berlaku dalam bukti formal untuk model dua-salinan dengan sidecar).

## 5. Estimasi lawan pengukuran (ditulis di rencana sebelum RTL)
- Siklus sekitar 8,410 / 10,240 / 15,600: terukur 8,404 / 10,236 / 15,597 (-6, -4, -3): di dalam.
- ALM S1 + 150 sampai 450: terukur +274.0 (40 ns), +223.5 (15 ns): di dalam.
- Register S1 + 100 sampai 250: terukur sekitar 150 lebih sedikit: arah salah (hasil fitter; tidak diperiksa).
- Blok RAM / DSP 54 / 28: terpenuhi.
- Fmax dalam 2 % dari S1: terukur +1.1 % pada median 15 ns: di dalam.
- Siklus LDP dan STP sama dengan S1: terpenuhi (hitungan per state).

## 6. Yang tidak ditunjukkan ini
Tidak ada hasil papan; tidak ada klaim kecepatan terhadap perangkat lunak; timing statis kernel-only dengan virtual pin; pohon clock DE10-Nano, PLL, dan HPS tidak ada di kompilasi ini; waktu-konstan berarti invarian jumlah siklus saja; ACVP adalah simulasi; kontrol formal B7 tidak ditunjukkan oleh run formal.

## 7. File
`test_plan_9f1b.md` (dengan amandemen A1), `selection_worksheet.md`, `sim.md`, `formal.md`, `critical_paths_K1b-15.md`, `profile_k1b_verilator.json`, `cycles_*_core_k1b_*.json`, dua belas ekstrak `quartus_K1b*.md`, `quartus/phase09f1b_core/` (dua belas revisi, `run_k1b.sh`, `run_k1b_rest.sh`), `rtl/mlkem/mlkem_core3.sv`, `rtl/mlkem/mlkem_ctl_rom2.sv`, `tb/golden/mlkem_ctl_model2.py`, `scripts/build/gen_mlkem_ctl_rom2.py`, `scripts/quartus/select_9f1b.py`, `formal/run/run_formal_phase9f1b.py`, `formal/phase09m-optimisation/9f1b/`.
