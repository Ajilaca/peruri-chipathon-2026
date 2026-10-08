# ADR 0037: Hasil Fase 9M-3: sponge hash K0 (HASH_C5 = 0) diadopsi aturannya sebagai opsi yang lebih kecil

- Status: Accepted
- Tanggal: 2026-10-04
- Diputuskan oleh: Jo (Team J5), 2026-10-05

## Konteks
ADR 0034 (Accepted, Faza Dzil) menjadikan butir 3 Fase 9M pilihan sponge untuk instans hash (G, H, J): C5 (dua ronde per
siklus, ADR 0027, bawaan Fase 9) atau K0 (satu ronde per siklus, Fase 7). Parameter `HASH_C5` sudah ada; butir 3 tidak
mengubah RTL. Diukur terhadap inti 9M-1 di bawah rencana dan aturannya sendiri
(`evidence/phase9m/batch1/9m3/test_plan_9m3.md`, `result_9m3.md`). Aturan diterapkan pada file dan terpenuhi. Sampler di
dalam mesin K-PKE mempertahankan sponge C5 pada kedua opsi.

## Opsi yang dipertimbangkan
1. Mempertahankan `HASH_C5 = 1` (C5, ADR 0027): 8.327 / 10.159 / 15.515 siklus (masukan profil, `CODEC_W2 = 1`), median
   ALM 17.654,0.
2. Memakai `HASH_C5 = 0` (K0): 8.447 / 10.279 / 15.635 siklus (+120 masing-masing, +1,44 % / +1,18 % / +0,77 %), median
   ALM 15.917,5 (-1.736,5), median Fmax 48,935 lawan 48,855 MHz, latensi pada median Fmax +1,28 % / +1,02 % / +0,61 %,
   timing terpenuhi pada 40 ns di 6 dari 6 seed, ACVP 100 % di kedua simulator (MEASURED, simulasi dan Quartus
   kernel-only; `batch1/9m3/selection_worksheet.md`).

## Keputusan
Diterima oleh Jo (Team J5) pada 2026-10-05 atas instruksi tim untuk menyetujui; teks di bawah adalah usulan seperti
tertulis. Aturan rencana menyatakan angka-angka membenarkan K0 (area dihemat dengan latensi sekitar 1 %); tim memilih.
K0 bukan peningkatan kecepatan: ia membebaskan sekitar 1.700 ALM yang dapat dipakai rencana Fmax (ADR 0036). Nilai
bawaan `HASH_C5` tetap 1 sampai penerimaan tercatat.

## Konsekuensi
Bila diterima: konfigurasi langkah berikutnya (S1 dan seterusnya) adalah `CODEC_W2 = 1`, `HASH_C5 = 0`, atau K0
digantikan di sana oleh pekerjaan sampler S1; ADR 0027 tidak diedit (ADR berikutnya menggantikannya bila tim mengganti
C5 di inti). Latensi adalah perhitungan tim dari timing statis kernel-only. Tidak ada klaim papan. Bila ditolak: C5
tetap, file K0 tetap sebagai parameter.

## Bukti
`evidence/phase9m/batch1/9m3/result_9m3.md`, `selection_worksheet.md`, `formal.md`, `sim_verilator.md`,
`sim_icarus.md`, `regression_default.md`, `quartus_MK*.md`; profil `batch1/9m3/profile_k0_w2_verilator.json` dan
`batch1/9m1/profile_w2_verilator.json`.
