# ADR 0040: Hasil Fase 9F S1b: hash di latar belakang (K1b) diadopsi aturannya, memulihkan biaya siklus K1

- Status: Accepted
- Tanggal: 2026-10-04
- Diputuskan oleh: Jo (Team J5), 2026-10-05

## Konteks
ADR 0036 (Accepted, Faza Dzil) mendaftar S1b setelah S1: biarkan hash yang tidak bergantung pada pekerjaan di
sebelahnya (KeyGen `H(ek)`, Encaps `H(ek)`, Decaps `J`) berjalan di sidecar latar belakang. S1b dibangun di modul baru
`rtl/mlkem/mlkem_core3.sv` dengan program `rtl/mlkem/mlkem_ctl_rom2.sv` (dibangkitkan dari
`tb/golden/mlkem_ctl_model2.py`), diverifikasi dan diukur di bawah rencana dan aturannya sendiri
(`evidence/phase9m/batch1/9f1b/test_plan_9f1b.md`, `result_9f1b.md`). Aturan diterapkan pada file dan terpenuhi. ADR
0039 (Accepted, Faza Dzil) menetapkan 15 ns sebagai batas pelaporan.

## Opsi yang dipertimbangkan
1. Mempertahankan K1 (ADR 0038, `mlkem_core2`): 8.795 / 10.627 / 15.983 siklus, median ALM 14.061,0 (40 ns), median
   Fmax 73,070 MHz pada 15 ns, latensi pada 15 ns 120,4 / 145,4 / 218,7 us.
2. Memakai K1b (`mlkem_core3`): 8.404 / 10.236 / 15.597 siklus (-391 / -391 / -386), median ALM 14.335,0 (+274,0),
   median Fmax 73,855 MHz pada 15 ns (6 dari 6 seed terpenuhi; 40 ns terpenuhi di 6 dari 6), latensi pada 15 ns
   113,8 / 138,6 / 211,2 us (-5,5 %, -4,7 %, -3,5 % terhadap K1; +0,2 %, +0,0 %, -0,2 % terhadap inti 9M-1 pada 15 ns,
   dua seed S0); ACVP 100 % di kedua simulator; kontrol negatif sesuai syarat termasuk sidecar yang di-throttle yang
   harus lolos dan satu tanpa proteksi yang harus gagal (MEASURED, simulasi, formal, dan Quartus kernel-only;
   `batch1/9f1b/selection_worksheet.md`).

## Keputusan
Diterima oleh Jo (Team J5) pada 2026-10-05 atas instruksi tim untuk menyetujui; teks di bawah adalah usulan seperti
tertulis. Aturan rencana mengadopsi opsi 2. Kontrol formal NC-B7 tidak ditunjukkan oleh run formal (habis waktu;
percobaan ulang tanpa hasil pada saat laporan); ia ditunjukkan oleh simulasi (NC-WR). Tim menerima atau menolaknya.

## Konsekuensi
Bila diterima: basis untuk Batch 2 (S2, S3, butir 4) adalah `mlkem_core3` dengan `SMP_C5 = 0`, `HASH_C5 = 0`,
`CODEC_W2 = 1`; dinding pada 15 ns adalah inti NTT / memori (298 dari 300 jalur terburuk), jadi S2 menyasar kelas itu.
ADR 0027 tidak diedit. Latensi adalah perhitungan tim dari timing statis kernel-only. Tidak ada klaim papan. Bila
ditolak: K1 (ADR 0038) atau inti 9M-1 tetap basis; `mlkem_core3.sv` tetap.

## Bukti
`evidence/phase9m/batch1/9f1b/result_9f1b.md`, `selection_worksheet.md`, `sim.md`, `formal.md`,
`critical_paths_K1b-15.md`, `quartus_K1b*.md`; `evidence/phase9m/batch1/9f1/result_9f1.md`;
`docs/decisions/adr/ADR-0038-phase-9f-s1-result-k0-sampler-and-k0-hash-k1-adopted-by-its-.md`,
`ADR-0039-phase-9f-15-ns-is-the-fmax-reporting-limit-14-ns-is-kept-for.md`.
