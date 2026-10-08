# ADR 0042: Hasil Fase 9F S2b: alamat issue NTT terregistrasi (K3) tidak diadopsi aturannya seperti tertulis, median Fmax +3,4 MHz dengan ekor seed rendah

- Status: Accepted
- Tanggal: 2026-10-05
- Diputuskan oleh: Jo (Team J5), 2026-10-05

## Konteks
ADR 0041 (ketika itu Proposed) melaporkan S2 (register setelah reducer Barrett, K2) netral dan menyebut jalur alamat
penghitung layer sebagai dinding berikutnya. S2b meregistrasi alamat tahap issue inti NTT (parameter `AREG` /
`NTT_AR`, bawaan 0), dihitung satu siklus lebih awal dari nilai state berikutnya; diverifikasi dan diukur di bawah
rencana dan aturannya sendiri (`evidence/phase9m/batch2/9s2b/test_plan_9s2b.md`, `result_9s2b.md`; amandemen A1:
gerbang 40 ns tetap; amandemen A2: tiga seed 15 ns tambahan, dipilih setelah enam yang pertama). Aturan rencana
ditetapkan sebelum mengukur dan diperketat setelah S2: kenaikan di dalam derau seed tidak diadopsi. ADR 0039 (Accepted,
Faza Dzil) menetapkan 15 ns sebagai batas pelaporan.

## Opsi yang dipertimbangkan
1. Mempertahankan K2 (ADR 0041, `NTT_AR = 0`): median Fmax 74,125 MHz pada 15 ns (enam seed, 72,65-76,03), latensi
   pada 15 ns 113,5 / 138,3 / 210,7 us.
2. Memakai K3 (`NTT_AR = 1`): siklus sama (8.416 / 10.250 / 15.619); median Fmax 77,555 MHz pada enam seed
   (73,02-79,37; +3,43 MHz), latensi 108,5 / 132,2 / 201,4 us (-4,4 %); pada sembilan seed median 77,320 MHz
   (72,80-79,37), enam dari sembilan seed di atas seed tertinggi K2; timing terpenuhi di 6 dari 6 seed pada 15 ns dan 6
   dari 6 pada 40 ns; median ALM 14.115,5 pada 40 ns (-97,5), 14.293,0 pada 15 ns (-56,5), register sekitar +40
   sampai +135 (MEASURED, `batch2/9s2b/selection_worksheet.md`). Seed bersifat bimodal: enam pada 77,0 sampai 79,4 MHz
   dan tiga pada 72,8 sampai 75,5 MHz. Analisis jalur K4 (logika S2b yang sama) menemukan sebab ujung bawah: suku
   `start_go` S2b menaruh counter sequencer, lewat enable tulis host, ke dalam kerucut alamat terregistrasi (INFERENCE
   untuk seed K3, MEASURED di K4-15-s6).

## Keputusan
Diterima oleh Jo (Team J5) pada 2026-10-05 atas instruksi tim untuk menyetujui; teks di bawah adalah usulan seperti
tertulis. Menurut aturan seperti tertulis K3 tidak diadopsi; tim menerimanya juga (keputusan tim di atas aturan,
seperti ADR 0020). Menurut aturan seperti tertulis K3 tidak diadopsi (butir 5: kenaikan median, +3,43 MHz, lebih kecil
dari sebaran seed K3, 6,35 MHz, dan seed K3 terendah di bawah seed K2 tertinggi). Butir 1-4 dan 6 terpenuhi. Bukti
menunjuk kenaikan nyata sekitar 3 MHz dengan ekor seed rendah; tidak disembunyikan di sini bahwa aturan berkata tidak.
Tim memutuskan apakah menerima K3 (ia basis pengukuran K4 di ADR 0043), atau menolaknya.

## Konsekuensi
Bila diterima: basisnya adalah `mlkem_core3` / `mlkem_core4` dengan `NTT_P6 = 1`, `NTT_AR = 1`; S2 (ADR 0041)
menjadi bagiannya. Bila ditolak: K2 atau K1b tetap (parameter pada nilai bawaan; hasil butir 4 ADR 0043 relatif
terhadap K3 dan harus diukur ulang pada basis lain). Latensi adalah perhitungan tim dari timing statis kernel-only;
derau seed sekitar 3 MHz dan lebih besar untuk K3. Tidak ada klaim papan. ADR 0041 tidak diedit.

## Bukti
`evidence/phase9m/batch2/9s2b/result_9s2b.md`, `selection_worksheet.md`, `sim.md`, `formal.md`,
`critical_paths_K3-15.md`, `quartus_K3*.md`; `evidence/phase9m/batch2/9i4/critical_paths_K4-15.md`;
`docs/decisions/adr/ADR-0041-phase-9f-s2-result-register-after-the-barrett-reducer-k2-ado.md`,
`ADR-0039-phase-9f-15-ns-is-the-fmax-reporting-limit-14-ns-is-kept-for.md`.
