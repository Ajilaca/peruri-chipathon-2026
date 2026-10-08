# ADR 0041: Hasil Fase 9F S2: register setelah reducer Barrett (K2) diadopsi aturannya, tanpa kenaikan Fmax terukur

- Status: Accepted
- Tanggal: 2026-10-04
- Diputuskan oleh: Jo (Team J5), 2026-10-05

## Konteks
ADR 0036 (Accepted, Faza Dzil) mendaftar S2 sebagai langkah yang menyerang batas yang diungkap S1; ADR 0040 (ketika
itu Proposed) menyebut inti NTT / memori sebagai dinding K1b pada 15 ns. S2 menambah potongan pengali keempat (register
setelah koreksi Barrett akhir, P = 5 -> 6) lewat parameter `NTT_P6` (bawaan 0), diverifikasi dan diukur di bawah
rencana dan aturannya sendiri (`evidence/phase9m/batch2/9s2/test_plan_9s2.md`, `result_9s2.md`). Aturan diterapkan pada
file dan terpenuhi. ADR 0039 (Accepted, Faza Dzil) menetapkan 15 ns sebagai batas pelaporan.

## Opsi yang dipertimbangkan
1. Mempertahankan K1b (ADR 0040, `NTT_P6 = 0`): 8.404 / 10.236 / 15.597 siklus, median ALM 14.335,0 (40 ns), median
   Fmax 73,855 MHz pada 15 ns, latensi pada 15 ns 113,8 / 138,6 / 211,2 us.
2. Memakai K2 (`NTT_P6 = 1`): 8.416 / 10.250 / 15.619 siklus (+12 / +14 / +22), median ALM 14.213,0 (-122,0), register
   sekitar +120, median Fmax 74,125 MHz pada 15 ns (+0,270 MHz, di dalam sebaran seed 3,38 / 2,94 MHz), latensi pada
   15 ns 113,5 / 138,3 / 210,7 us (-0,2 %, di bawah derau seed); timing terpenuhi di 6 dari 6 seed pada 40 ns dan pada
   15 ns; ACVP 100 % di kedua simulator; bukti kontrol formal pada P = 6 PASS (MEASURED, simulasi, formal, dan Quartus
   kernel-only; `batch2/9s2/selection_worksheet.md`). Jalur reducer ke memori bergeser dari +1,170 ke +2,349 ns, tetapi
   jalur alamat penghitung layer (+1,910 ns di K1b) kini membatasi pada +1,404 ns di seed yang dianalisis.

## Keputusan
Diterima oleh Jo (Team J5) pada 2026-10-05 atas instruksi tim untuk menyetujui; teks di bawah adalah usulan seperti
tertulis. Aturan rencana mengadopsi opsi 2; bukti menunjukkan S2 netral untuk Fmax dan latensi (ESTIMATE rencana 76
sampai 80 MHz tidak tercapai). Tim menerima atau menolaknya; S2 bernilai terutama sebagai separuh pertama langkah S2b
(meregistrasi aritmetika alamat per layer), yang belum direncanakan atau dibangun.

## Konsekuensi
Bila diterima: basis untuk langkah berikutnya adalah `mlkem_core3` dengan `SMP_C5 = 0`, `HASH_C5 = 0`, `CODEC_W2 = 1`,
`NTT_P6 = 1`; siklus NTT per transformasi 119; dinding pada 15 ns adalah jalur alamat tahap issue (`layer_q` ke port
memori), kandidat untuk S2b. Bila ditolak: K1b tetap (nilai parameter bawaan, tidak ada kode yang dihapus). Latensi
adalah perhitungan tim dari timing statis kernel-only; derau seed sekitar 3 MHz. Tidak ada klaim papan. ADR 0040 tidak
diedit.

## Bukti
`evidence/phase9m/batch2/9s2/result_9s2.md`, `selection_worksheet.md`, `sim.md`, `formal.md`,
`critical_paths_K2-15.md`, `quartus_K2*.md`; `evidence/phase9m/batch1/9f1b/` (acuan K1b);
`docs/decisions/adr/ADR-0036-phase-9f-fmax-plan-s0-s1-s2-latency-rule-and-reporting-at-a-.md`,
`ADR-0039-phase-9f-15-ns-is-the-fmax-reporting-limit-14-ns-is-kept-for.md`,
`ADR-0040-phase-9f-s1b-result-background-hash-k1b-adopted-by-its-rule-.md`.
