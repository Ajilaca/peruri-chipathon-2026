<!-- claim-lint: skip-file (internal block report, not proposal text) -->
# Laporan Fase 9F langkah S0: inti 9M-1 di bawah batasan 16, 15, dan 14 ns

- Status: SELESAI (STOP setelah langkah, ADR 0036). Branch `phase9m-optimisation`, belum di-commit. Tidak ada perubahan RTL: sumbernya adalah inti 9M-1 (`quartus/phase09m1_core/MW.qsf`). Rencana: `test_plan_9f0.md` (ditulis sebelum kompilasi). Timing statis kernel-only dengan virtual pin; bukan sistem di papan. Delapan kompilasi pada sapuan pertama, dua lagi di amandemen A2 (bagian 8), semuanya `rc=0`.

## 1. Hasil
Timing terpenuhi pada 16, 15, dan 14 ns di kedua seed dengan bawaan Quartus; sapuan tidak menemukan batas desain (ia berakhir pada batasan paling ketatnya, yang terpenuhi). Pada 14 ns Fmax slow corner terendah adalah 75.31 MHz (seed 1) dan 77.29 MHz (seed 2); pada 15 ns 73.94 dan 73.33 MHz. Upaya high performance tidak membantu pada 14 ns (slack terburuk lebih rendah, 970-1,000 ALM dan sekitar 2,200 register lebih banyak). Hanya dua seed: ini sapuan untuk mencari batas, bukan pernyataan enam seed yang diminta ADR 0036 pada batasan pelaporan akhir (itu datang bersama S1).

## 2. Parameter yang diukur (MEASURED, `selection_worksheet.md`, ekstrak `quartus_F*.md`, `quartus_H14-*.md`)
| Revisi | Batasan | ALM | Register | Blok RAM / DSP | Setup / hold terburuk (ns) | Fmax slow corner terendah (MHz) |
|---|---|---|---|---|---|---|
| F16-s1 / s2 | 16 ns | 17,980 / 17,888 | 8,635 / 8,575 | 53 / 28 | +1.992 / +2.075; +0.118 / +0.108 | 71.39 / 71.81 |
| F15-s1 / s2 | 15 ns | 17,971 / 17,926 | 8,719 / 8,700 | 53 / 28 | +1.475 / +1.363; +0.102 / +0.071 | 73.94 / 73.33 |
| F14-s1 / s2 | 14 ns | 17,907 / 17,889 | 8,770 / 8,669 | 53 / 28 | +0.721 / +1.062; +0.109 / +0.108 | 75.31 / 77.29 |
| H14-s1 / s2 (upaya high performance) | 14 ns | 18,876 / 18,897 | 10,966 / 10,935 | 49 / 28 | +0.826 / +0.423; +0.090 / +0.107 | 75.91 / 73.65 |
Acuan, inti sama pada batasan lain (butir sebelumnya): median Fmax 40 ns 48.855 MHz, ALM 17,654.0 (`../9m1/selection_worksheet.md`); median 20 ns 63.990 MHz, ALM 17,779.5 (`../9m2/selection_worksheet.md`). Peringatan kritis: 1 per kompilasi (peringatan clock virtual pin).
Latensi pada Fmax yang lebih rendah dari dua seed (perhitungan tim; siklus masukan profil inti 9M-1 8,327 / 10,159 / 15,515): 16 ns 116.6 / 142.3 / 217.3 us; 15 ns 113.6 / 138.5 / 211.6 us; 14 ns 110.6 / 134.9 / 206.0 us. Terhadap tabel 20 ns 9M-2 (130.1 / 158.8 / 242.5 us) ini 15 % lebih rendah pada 14 ns. Ini angka timing statis, bukan pengukuran papan.

## 3. Klasifikasi jalur kritis (MEASURED, `critical_paths_F14_H14.md`)
Pada 14 ns, bawaan: jalur terburuk di permutasi Keccak C5 instans hash (+0.721 ns, 133 dari 300 jalur), lalu inti NTT / memori / PWM (+1.055 ns, 84), lalu permutasi sponge sampler (+1.266 ns, 83). Dengan upaya high performance kedua permutasi memimpin (+0.423 dan +0.453 ns). Dalam 0.55 ns tiga blok berbagi batas: tidak ada blok tunggal yang mendominasi.

## 4. Estimasi lawan pengukuran (ditulis di rencana sebelum kompilasi)
- 16 ns terpenuhi di kedua seed: terpenuhi. 15 ns terpenuhi di satu atau kedua seed: terpenuhi di keduanya.
- 14 ns tidak terpenuhi pada upaya bawaan: salah (terpenuhi di kedua seed, slack +0.721 dan +1.062 ns).
- Upaya high performance mendapat 0.3-1 ns pada 14 ns: tidak teramati (slack +0.826 / +0.423 ns lawan +0.721 / +1.062 untuk bawaan; upaya itu memakan area dan register).
- ALM dalam +/- 3 % dari 17,654: bawaan di dalam (+1.3 % sampai +1.8 %); upaya high performance di luar (+6.9 % sampai +7.0 %). Register dalam +/- 3 %: di luar (bawaan +2.4 % sampai +4.7 % terhadap maks 8,376; upaya +30 %: replikasi dan retiming fitter di bawah batasan ketat: INFERENCE).
- Blok RAM 54 dan DSP 28 tidak berubah: DSP tidak berubah; blok RAM 53 (bawaan) dan 49 (upaya): fitter mengepak memori secara berbeda di bawah batasan (INFERENCE, tidak diperiksa).
- INFERENCE 20 ns sebelumnya "di luar Keccak sekitar 69 MHz": konsisten dengan hasil 14 ns hanya dalam hal kelas NTT (jalur sekitar 12.9 ns di sini) dekat di belakang Keccak; angka 69 MHz sendiri adalah batas bawah dari kompilasi yang longgar, bukan batas.

## 5. Temuan dan batas
1. Batas inti C5 bukan 50-64 MHz seperti disarankan kompilasi 20 ns; pada batasan lebih ketat fitter mencapai 73-77 MHz (slow corner terendah) pada ALM yang kira-kira sama. Kompilasi 20 ns adalah batasan longgar, bukan batas.
2. Batas berada di bawah 14 ns. Untuk menemukannya sapuan butuh 13, 12, 11 ns (keputusan untuk Faza Dzil: enam kompilasi lagi pada dua seed, ESTIMATE sekitar 3 jam waktu mesin dengan kompilasi lain berjalan); ini tidak dilakukan.
3. Konsekuensi S1 (INFERENCE): K0 sebagai pengganti C5 menghapus kelas permutasi; jalur NTT / memori berada dalam sekitar 0.33 ns dari permutasi hash pada 14 ns, jadi S1 mungkin hanya mendapat sedikit Fmax dan terutama menghemat area. S1 mengukurnya.
4. File SDC langkah ini (`C-16.sdc`, `C-15.sdc`, `C-14.sdc`) tidak punya `set_false_path -from [get_ports {rst_ni}]`, sedangkan `C.sdc` dan `C-20.sdc` Fase 9 punya (kelalaian saya, tidak disengaja; rencana berkata "bentuk sama seperti C-20.sdc"). Masukan `rst_ni` tidak punya input delay di kedua file, jadi jalurnya tidak dibatasi pada kedua kasus (INFERENCE, tidak diuji dengan kompilasi memakai baris itu). Kompilasi S1 pada 15 ns (K1-15) memakai bentuk SDC yang sama dengan langkah ini agar tetap sebanding.
5. Dua seed per batasan; angka Fmax-lebih-rendah-dari-dua bukan median.

## 6. Yang tidak ditunjukkan ini
Tidak ada hasil papan; tidak ada klaim kecepatan terhadap perangkat lunak; timing statis kernel-only dengan virtual pin; pohon clock DE10-Nano, PLL, dan HPS tidak ada di kompilasi ini (keputusan PLL milik Fase 10); waktu-konstan berarti invarian jumlah siklus saja.

## 7. File
`test_plan_9f0.md`, `selection_worksheet.md`, `critical_paths_F14_H14.md`, delapan ekstrak Quartus, `quartus/phase09f0_core/` (delapan revisi, `run_f0.sh`), `scripts/quartus/select_9f0.py`, `scripts/quartus/classify_paths_9f.py`.

## 8. Hasil Amandemen A2: sapuan diperluas (Faza Dzil, chat 2026-10-04: "check sampai fail; jika pada 10 ns masih pass kita stop di sana")
Aturan dan estimasi ada di `test_plan_9f0.md` bagian 7 (ditulis sebelum run). Dijalankan oleh `quartus/phase09f0_core/run_f0x.sh`: 13 ns, seed 1 dan 2 (bawaan), lalu berhenti karena satu seed gagal (log `quartus/phase09f0_core/f0x_status.log`).
| Revisi | Batasan | ALM | Register | Blok RAM / DSP | Setup / hold terburuk (ns, semua corner) | Timing terpenuhi | Fmax slow corner terendah (MHz) | Peringatan kritis |
|---|---|---|---|---|---|---|---|---|
| F13-s1 | 13 ns | 17,900 | 8,807 | 53 / 28 | +0.227 / +0.112 | ya | 78.29 | 1 |
| F13-s2 | 13 ns | 17,891 | 8,873 | 53 / 28 | -0.213 / +0.100 (setup slow 100 C: -0.185) | TIDAK | 75.68 | 3 |
(Nilai persis: `selection_worksheet.md`, `quartus_F13-s1.md`, `quartus_F13-s2.md`.)
- Hasil: 13 ns terpenuhi di 1 dari 2 seed; batas inti 9M-1 berada antara 13 dan 14 ns (14 ns terpenuhi di kedua seed, 13 ns di satu). Aturan berhenti 10 ns tidak tercapai.
- Jalur kritis pada 13 ns (`critical_paths_F14_H14.md`, bagian tambahan): seed yang gagal gagal di inti NTT / memori / PWM (-0.185 ns, 171 dari 300 jalur), dengan permutasi Keccak instans hash juga negatif (-0.030 ns); pada seed yang lulus permutasi hash memimpin (+0.227 ns) dan kelas NTT menyusul (+0.571 ns). Jadi pada batas, jalur NTT / memori dan permutasi C5 gagal bersama: penghalangnya sekitar 13.2 ns (sekitar 75 MHz), bukan permutasi saja.
- Estimasi lawan pengukuran: 13 ns terpenuhi di kedua seed: salah (satu seed gagal); kegagalan pertama di 12 atau 11 ns: salah (13 ns); pertumbuhan ALM sampai +3 % dan register sampai +10 % yang dinyatakan: ALM +1.3 % sampai +1.4 % di atas 17,654 (17,891-17,900), register 8,807 / 8,873 (+5.1 % / +5.9 % di atas maks 40 ns 8,376): di dalam.
- Konsekuensi untuk S1 (INFERENCE): mengganti permutasi C5 dengan K0 menghapus kelas permutasi tetapi bukan kelas NTT / memori, yang berada di penghalang dalam 0.2 ns dari keduanya; S1 paling banyak dapat memperoleh beberapa persen Fmax pada batas ini. Kompilasi S1 pada 15 ns (bagian 9 `../9f1/result_9f1.md`) menunjukkan bagaimana penghematan area dan Fmax berperilaku.
- Batas pernyataan: dua seed per batasan; satu run per seed; penghalang berbeda menurut seed (seed 2 gagal 0.185 ns, seed 1 lulus 0.227 ns), jadi batasnya punya sebaran sebesar selisih slack antar seed (sekitar 0.4 ns).
- Peringatan kritis (triase, aturan 10 CLAUDE.md): F13-s1 punya satu yang ada di setiap kompilasi kernel-only (15725, port clock diberi makan virtual pin; diterima). F13-s2 punya dua lagi, `332148 Timing requirements not met` (dicetak oleh fitter dan timing analyzer untuk slack setup gagal -0.213 ns): keduanya adalah hasil gagal itu sendiri, bukan masalah alat; kegagalan dilaporkan, tidak diabaikan.
