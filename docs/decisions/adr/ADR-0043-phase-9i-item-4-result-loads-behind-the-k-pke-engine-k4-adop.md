# ADR 0043: Hasil Fase 9I butir 4: pemuatan di belakang mesin K-PKE (K4) diadopsi aturannya, Encaps -639 dan Decaps -2.630 siklus

- Status: Accepted
- Tanggal: 2026-10-05
- Diputuskan oleh: Jo (Team J5), 2026-10-05

## Konteks
ADR 0034 mendaftar butir 4 (tumpang-tindih muat polinomial dengan mesin) sebagai penghematan siklus terbesar yang
tersisa ("memerlukan port host mesin bekerja saat mesin berjalan, yaitu varian baru dari file Fase 6-8 yang
dibekukan; risiko tinggi"). Butir ini dibangun sebagai varian baru (`mlkem_core4`, `kpke_sched_smp4`,
`kpke_smp_top_s10o`, `mlkem_ldpoly2o`, `mlkem_ctl_rom3`; file Fase 6-8 dan `mlkem_core3` tidak diedit) dan
diverifikasi serta diukur di bawah rencana dan aturannya sendiri (`evidence/phase9m/batch2/9i4/test_plan_9i4.md`,
`result_9i4.md`). Basis pengukuran adalah K3 (ADR 0042, ketika itu Proposed); parameter K3 (`NTT_P6 = 1`,
`NTT_AR = 1`) adalah parameter K4.

## Opsi yang dipertimbangkan
1. Mempertahankan K3 (`mlkem_core3`): 8.416 / 10.250 / 15.619 siklus; median Fmax 77,555 MHz pada 15 ns; latensi
   108,5 / 132,2 / 201,4 us; median ALM 14.115,5 (40 ns) dan 14.293,0 (15 ns).
2. Memakai K4 (`mlkem_core4`): 8.416 / 9.611 / 12.989 siklus (KeyGen sama, Encaps -639, Decaps -2.630); median Fmax
   76,665 MHz pada 15 ns (enam seed 69,43-80,99; -0,89 MHz, di dalam sebaran); latensi pada 15 ns 109,8 / 125,4 /
   169,4 us (+1,2 %, -5,1 %, -15,9 % terhadap K3); median ALM 14.222,0 (40 ns, +106,5) dan 14.480,0 (15 ns, +187,0);
   timing terpenuhi di 6 dari 6 seed pada 40 ns dan pada 15 ns (MEASURED, `batch2/9i4/selection_worksheet.md`). ACVP
   100 % di kedua simulator; kontrol negatif sesuai syarat, termasuk port host yang di-throttle yang harus lolos
   dengan interlock dan gagal tanpanya; formal: keselamatan (E1, S1-S7, B1-B7) PASS dan cover PASS, NC-JOIN4 FAIL
   sesuai syarat, tetapi P1 (terbatas) dan NC-E1-4 habis waktu dan tidak punya hasil formal (`formal.md`).

## Keputusan
Diterima oleh Jo (Team J5) pada 2026-10-05 atas instruksi tim untuk menyetujui; teks di bawah adalah usulan seperti
tertulis. Aturan rencana mengadopsi opsi 2. Tim menerima atau menolaknya. Jalur terburuk pada seed K4 dengan slack
terkecil adalah jalur S2b (ADR 0042), bukan butir 4; seed rendah (69,43 MHz) milik jalur itu. Bila K3 (ADR 0042)
ditolak, K4 harus diukur ulang pada basis lain: penghematan siklus tidak bergantung pada parameter NTT, Fmax bergantung.

## Konsekuensi
Bila diterima: basisnya adalah `mlkem_core4` dengan parameter K3; pengendali punya micro-operation RUNS dan RUNJ,
varian mesin memberi port tulis host selagi berjalan dan memulai operasi hanya setelah setiap slot yang dipakainya
termuat penuh; KeyGen tidak berubah (penyimpanannya tetap berderet); penyimpanan tidak ditumpangkan (langkah
mendatang yang mungkin). `mlkem_core4` memerlukan `CODEC_W2 = 1`. Bila ditolak: `mlkem_core3` tetap; `mlkem_core4`
dan filenya tetap tidak dipakai. Latensi adalah perhitungan tim dari timing statis kernel-only. Tidak ada klaim papan;
waktu-konstan berarti invarian jumlah siklus saja.

## Bukti
`evidence/phase9m/batch2/9i4/result_9i4.md`, `selection_worksheet.md`, `sim.md`, `formal.md`,
`critical_paths_K4-15.md`, `profile_k4_verilator.json`, `quartus_K4*.md`;
`docs/decisions/adr/ADR-0042-phase-9f-s2b-result-registered-ntt-issue-address-k3-not-adop.md`, `ADR-0034-*.md`,
`ADR-0039-*.md`.
