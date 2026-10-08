# ADR 0035: Hasil Fase 9M-1: jalur codec dua byte (CODEC_W2) diadopsi aturannya

- Status: Accepted
- Tanggal: 2026-10-04
- Diputuskan oleh: Jo (Team J5), 2026-10-05

## Konteks
ADR 0034 (Accepted, Faza Dzil) menjadikan butir 1 Fase 9M langkah pertama: memuat dan menyimpan polinomial dibatasi
jalur codec satu-byte-per-siklus pada d = 12 dan d = 10 (`evidence/phase9m/profile.md`). Butir 1 dibangun, diverifikasi,
dan diukur di bawah rencana dan aturannya sendiri (`evidence/phase9m/batch1/9m1/test_plan_9m1.md`, `result_9m1.md`).
Aturan diterapkan pada file dan terpenuhi. Nilai bawaan parameter inti `CODEC_W2` masih 0 (perilaku Fase 9).

## Opsi yang dipertimbangkan
1. Mempertahankan `CODEC_W2 = 0` (Fase 9 seperti digabung): tidak ada perubahan; 9.095 / 10.735 / 16.667 siklus
   (masukan profil).
2. Memakai `CODEC_W2 = 1` sebagai konfigurasi butir Fase 9M berikutnya: 8.327 / 10.159 / 15.515 siklus (-8,4 %, -5,4 %,
   -6,9 %), median ALM 17.654,0 lawan 17.620,5 (+33,5), median Fmax 48,855 lawan 49,280 MHz, timing terpenuhi pada 40 ns
   di setiap seed, ACVP 100 % di kedua simulator (MEASURED, simulasi dan Quartus kernel-only;
   `batch1/9m1/selection_worksheet.md`).

## Keputusan
Diterima oleh Jo (Team J5) pada 2026-10-05 atas instruksi tim untuk menyetujui; teks di bawah adalah usulan seperti
tertulis. Aturan rencana mengadopsi opsi 2; tim menerima atau menolaknya. Sampai penerimaan tercatat, nilai bawaan
tetap 0 dan tidak ada di proposal yang bergantung padanya.

## Konsekuensi
Bila diterima: butir 2, 3, dan 4 Fase 9M diukur pada `CODEC_W2 = 1`; angka Fase 9 (`phase09.md`) tetap seperti adanya dan
angka baru membawa path evidence sendiri. Latensi adalah perhitungan tim dari timing statis kernel-only. Tidak ada klaim
papan. Bila ditolak: inti tetap pada konfigurasi Fase 9 dan file tetap sebagai parameter yang tidak dipakai.

## Bukti
`evidence/phase9m/batch1/9m1/result_9m1.md`, `selection_worksheet.md`, `formal.md`, `sim_verilator.md`,
`sim_icarus.md`, `regression_default.md`, `quartus_MW*.md`; profil `evidence/phase9m/profile_verilator.json` dan
`batch1/9m1/profile_w2_verilator.json`.
