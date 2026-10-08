<!-- claim-lint: skip-file (internal block report, not proposal text) -->
# Laporan Fase 9M butir 3 (9M-3): sponge K0 untuk instans hash (`HASH_C5 = 0`)

- Status: SELESAI (STOP setelah butir, ADR 0034). Branch `phase9m-optimisation`, belum di-commit. Tidak ada perubahan RTL di butir ini: parameter `HASH_C5` sudah ada di Fase 9; hanya skrip test yang berubah (`run_core_tests.py` membaca `CORE_K0`, `profile_core.py` ditambahkan). Rencana dan aturan: `test_plan_9m3.md` (ditulis sebelum pengukuran). Timing statis kernel-only dengan virtual pin; bukan sistem di papan.

## 1. Hasil
Aturan terpenuhi (keempat butir): K0 diadopsi oleh aturan sebagai sponge hash yang lebih kecil. Median ALM 15,917.5 lawan 17,654.0 (-1,736.5), dengan biaya +120 siklus per operasi (+1.0 % sampai +1.4 % siklus; +0.6 % sampai +1.3 % latensi pada median Fmax tiap tabel). Timing pada 40 ns terpenuhi di 6 dari 6 seed; ACVP 100 % di kedua simulator. Adopsi K0 lawan bawaan C5 (ADR 0027) tetap pada tim (ADR 0037 Proposed).

## 2. Parameter yang diukur (MEASURED; `selection_worksheet.md`, ekstrak `quartus_MK*.md`, `../9m1/quartus_MW*.md`)
| Parameter | MW (hash C5, `CODEC_W2 = 1`) | MK (hash K0, `CODEC_W2 = 1`) | Selisih |
|---|---|---|---|
| ALM, median (min-maks), seed 1-6 pada 40 ns | 17,654.0 (17,641-17,683) | 15,917.5 (15,899-15,940) | -1,736.5 (-9.8 %) |
| ALM dalam % dari 41,910 fitter | 42 % | 38 % | |
| Register | 8,189-8,376 | 8,230-8,382 | hampir sama (K0 punya register sponge lebih sedikit, tetapi register bagian lain berbeda menurut seed) |
| RAM blocks / DSP | 54 / 28 | 54 / 28 | 0 |
| Timing terpenuhi pada 40.000 ns | 6 dari 6 | 6 dari 6 | |
| Slack setup terburuk atas seed / hold | +18.655 ns / +0.077 ns | +18.934 ns / +0.080 ns | |
| Fmax, slow corner terendah, median (min-maks) | 48.855 MHz (46.85-52.15) | 48.935 MHz (47.47-49.39) | +0.080 MHz, di dalam sebaran seed |
| Siklus, masukan profil (KeyGen / Encaps / Decaps; simulasi) | 8,327 / 10,159 / 15,515 | 8,447 / 10,279 / 15,635 | +120 masing-masing (+1.44 %, +1.18 %, +0.77 %) |
| Latensi pada median Fmax tabel 40 ns (perhitungan tim) | 170.4 / 207.9 / 317.6 us | 172.6 / 210.1 / 319.5 us | +1.28 %, +1.02 %, +0.61 % |
| Informasi, seed 1 pada 20.000 ns (MW-20, MK-20) | ALM 17,808; setup +4.355 ns; Fmax 63.92 MHz | ALM 16,007; setup +4.003 ns; Fmax 62.51 MHz | hanya satu seed, bukan pernyataan |
| Peringatan kritis per kompilasi | 1 | 1 | peringatan clock virtual pin di setiap kompilasi kernel-only |
Per operasi mikro (profil, `profile_k0_w2_verilator.json` lawan `../9m1/profile_w2_verilator.json`): hanya HFD dan HGT yang berubah, sebesar +96 dan +24 siklus di setiap operasi; setiap hitungan state lain dan setiap hitungan operasi mikro lain sama. Contoh KeyGen: `HFD 0 144 148` 263 -> 359, `HGT 3 4` 25 -> 37.

## 3. Test (MEASURED, simulasi dan formal)
| # | Hasil | Evidence |
|---|---|---|
| V1 lint | `verilator --lint-only -Wall -GHASH_C5=0 -GCODEC_W2=1 --top-module mlkem_core` (daftar file `MK.qsf`): rc 0, tanpa baris peringatan; `slang --top mlkem_core -G HASH_C5=0 -G CODEC_W2=1`: 0 error, 0 peringatan (dijalankan 2026-10-04 saat laporan ini; keluaran tidak disimpan sebagai file) | laporan ini |
| V2 ACVP inti, `CORE_K0=1 CORE_W2=1` | keyGen 25, enkapsulasi 25, dekapsulasi 10 sama; cross-check acak, rantai, protokol, siklus konstan lulus; Verilator dan Icarus 6/6 | `sim_verilator.md`, `sim_icarus.md` |
| V3 profil | hanya HFD / HGT yang berubah (bagian 2) | `profile_k0_w2_verilator.json` |
| V4 kontrol `nclen` | `test_acvp_encaps` gagal seperti disyaratkan, kedua simulator (TOTAL 7/7 sesuai harapan) | kedua file sim |
| V5 pembungkus hash formal H1-H5, `CORE_R2 = 0`, stub protokol | bukti PASS, keterjangkauan PASS, dua kontrol negatif FAIL seperti disyaratkan; INFERENCE: bahwa sponge K0 nyata mengikuti protokol stub bertumpu pada bukti Fase 7 dan simulasi V2 | `formal.md` |
| V6 regresi bawaan | `run_core_tests.py verilator core` 6/6 lulus pada nilai bawaan; profil bawaan sama dengan profil Fase 9 (9,095 / 10,735 / 16,667) | `regression_default.md` |
| V7 Quartus | MK seed 1-6 pada 40 ns dan MK-20 semuanya `rc=0`, timing terpenuhi di keenam seed | `quartus_MK*.md` |
Siklus konstan: Encaps 10,235 dan Decaps 15,591 identik di semua masukan yang diuji di V2 (angka rentang ACVP, bukan masukan profil); KeyGen atas seed ACVP 8,387-8,428 (sebaran KeyGen berasal dari rejection sampling publik A, seperti di Fase 9).

## 4. Aturan rencana (bagian 5), diterapkan pada file
1. V1-V6 lulus: terpenuhi (V6: lihat bagian 3).
2. Timing pada 40 ns di setiap seed: terpenuhi (6 dari 6).
3. Median ALM paling sedikit 1,500 di bawah MW: terpenuhi (-1,736.5).
4. Latensi tiap operasi paling banyak 2 % di atas MW (siklus / median Fmax): terpenuhi (+1.28 %, +1.02 %, +0.61 %).

## 5. Estimasi lawan pengukuran (ditulis di rencana sebelum pengukuran)
- Siklus +120: terukur tepat +120 di ketiga operasi.
- ALM 2,000-2,800 lebih sedikit: terukur 1,736.5 lebih sedikit: di luar estimasi (terlalu tinggi; selisih 9b instans hash, sekitar 2,500 ALM, hanya antara pembungkus; di dalam inti penuh fitter berbagi dan memangkas secara berbeda: INFERENCE, tidak diperiksa).
- Register 300-700 lebih sedikit: tidak terpenuhi (rentang 8,230-8,382 lawan 8,189-8,376: hampir sama).
- Median Fmax 47-53 MHz: terukur 48.935 MHz: di dalam. Timing pada 40 ns di semua seed: terpenuhi.
- Blok RAM / DSP tidak berubah: terpenuhi.

## 6. Temuan dan batas
1. Biaya K0: +120 siklus dari 8,327-15,515 (sekitar 1 %) untuk 1,736.5 ALM (sekitar 10 % inti): ia opsi yang lebih murah dalam area per siklus. Ia bukan peningkatan kecepatan; ia membebaskan area. Di bawah rencana Fmax (ADR 0036) area itu dapat dipakai untuk S1/S2.
2. Pada 20 ns (hanya seed 1) MK punya 62.51 MHz lawan 63.92 MHz milik MW: informasi; jalur kritis berada di dalam sponge sampler C5 dan permutasi hash C5 (`../../critical_paths_MW.md`), jadi menghapus hash C5 menyisakan sampler C5 sebagai penghalang (INFERENCE; S1 menggantinya).
3. Inti bawaan Fase 9 dengan K0 (`CODEC_W2 = 0`, `HASH_C5 = 0`) tidak diukur (rencana bagian 1); efek kedua parameter diasumsikan aditif (INFERENCE).
4. Sampler di dalam mesin K-PKE menjaga sponge C5-nya sendiri; `HASH_C5` tidak menyentuhnya.

## 7. Yang tidak ditunjukkan ini
Tidak ada hasil papan; tidak ada klaim kecepatan terhadap perangkat lunak; timing statis kernel-only dengan virtual pin; waktu-konstan berarti invarian jumlah siklus saja; ACVP adalah simulasi.

## 8. File
`test_plan_9m3.md`, `selection_worksheet.md`, `sim_verilator.md`, `sim_icarus.md`, `formal.md`, `regression_default.md`, `cycles_*_core_k0.json`, `profile_k0_w2_verilator.json`, tujuh ekstrak Quartus `quartus_MK*.md`, `quartus/phase09m3_core/` (tujuh revisi, `run_mk.sh`), `scripts/quartus/select_9m3.py`, `formal/run/run_formal_phase9m3.py`, `formal/phase09m-optimisation/9m3/`.
