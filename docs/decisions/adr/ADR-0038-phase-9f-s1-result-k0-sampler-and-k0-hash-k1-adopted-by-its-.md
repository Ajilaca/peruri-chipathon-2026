# ADR 0038: Hasil Fase 9F S1: sampler K0 dan hash K0 (K1) diadopsi aturannya sebagai konfigurasi yang lebih kecil, bukan lebih cepat

- Status: Accepted
- Tanggal: 2026-10-04
- Diputuskan oleh: Jo (Team J5), 2026-10-05

## Konteks
ADR 0036 (Accepted, Faza Dzil) menjadikan S1 langkah setelah S0: sponge Keccak K0 (satu ronde per siklus) di kedua
tempat, instans hash dan sampler mesin K-PKE, untuk menyingkirkan permutasi C5 dari jalur kritis. S1 dibangun di modul
baru `rtl/mlkem/mlkem_core2.sv` (parameter `SMP_C5`), diverifikasi dan diukur di bawah rencana dan aturannya sendiri
(`evidence/phase9m/batch1/9f1/test_plan_9f1.md`, `result_9f1.md`). Aturan diterapkan pada file dan terpenuhi. Langkah S0
(`batch1/9f0/result_9f0.md`), yang diukur kemudian, menunjukkan bahwa inti 9M-1 sudah memenuhi 14 ns (75,3 MHz slow
corner terendah) dan gagal pada 13 ns di kelas inti NTT / memori bersama permutasi C5.

## Opsi yang dipertimbangkan
1. Mempertahankan inti 9M-1 (sampler C5 dan hash C5, `SMP_C5 = 1`, `HASH_C5 = 1`): 8.327 / 10.159 / 15.515 siklus,
   median ALM 17.654,0 (40 ns), Fmax slow corner terendah 73,6 MHz pada 15 ns (S0, dua seed), latensi pada 15 ns
   113,6 / 138,5 / 211,6 us.
2. Memakai K1 (`SMP_C5 = 0`, `HASH_C5 = 0`): 8.795 / 10.627 / 15.983 siklus (+468 masing-masing), median ALM 14.061,0
   (-3.593, -20 %), median Fmax 73,07 MHz pada 15 ns (enam seed, semua terpenuhi), latensi pada 15 ns 120,4 / 145,4 /
   218,7 us (+6,0 %, +5,0 %, +3,4 % terhadap opsi 1 pada batasan yang sama); timing terpenuhi pada 40 ns di 6 dari 6
   seed; ACVP 100 % di kedua simulator (MEASURED, simulasi dan Quartus kernel-only; `batch1/9f1/selection_worksheet.md`).
   Pada 15 ns semua 300 jalur terburuk K1 ada di kelas inti NTT / memori / PWM.

## Keputusan
Diterima oleh Jo (Team J5) pada 2026-10-05 atas instruksi tim untuk menyetujui; teks di bawah adalah usulan seperti
tertulis. Aturan rencana mengadopsi opsi 2 (membandingkan dengan MW pada 20 ns, ditetapkan sebelum S0); terhadap MW
pada batasan yang sama K1 lebih lambat 3-6 %. K1 membebaskan sekitar 3.600 ALM dan tidak menaikkan Fmax. Tim memilih;
hasil S1b (`batch1/9f1b/`) memulihkan sekitar 390 siklus dari 468.

## Konsekuensi
Bila diterima: langkah berikutnya memakai `SMP_C5 = 0`, `HASH_C5 = 0` sebagai basis; ADR 0027 tidak diedit (ADR
berikutnya menggantikannya di tempat tim mengganti C5). S2 menyasar kelas inti NTT / memori. Latensi adalah perhitungan
tim dari timing statis kernel-only. Tidak ada klaim papan. Bila ditolak: inti C5 tetap; `mlkem_core2.sv` tetap dengan
parameternya.

## Bukti
`evidence/phase9m/batch1/9f1/result_9f1.md`, `selection_worksheet.md`, `sim_verilator.md`, `sim_icarus.md`, `formal.md`,
`critical_paths_K1-15.md`, `quartus_K1*.md`; `evidence/phase9m/batch1/9f0/result_9f0.md` (S0).
