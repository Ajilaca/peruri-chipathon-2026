<!-- claim-lint: skip-file (internal block report, not proposal text) -->
# Laporan blok Fase 9c: inti ML-KEM-768 (`mlkem_core`)

- Status: SELESAI (STOP setelah blok, ADR 0032). Checkpoint blok; hasil fase adalah `docs/results/phase09.md`, yang kotak Approval-nya milik tim.
- Tanggal (UTC): 2026-10-03 / 2026-10-04. Pekerjaan ada di working tree dan belum di-commit (chat 2026-10-03: commit dibuat saat pekerjaan selesai).
- Rencana dan aturan: `test_plan_9c.md` (ditulis sebelum RTL; Amandemen A1 mencatat temuan di bawah), `../phase9_plan.md`. Hasil simulasi bukan hasil papan.

## 1. Hasil
`rtl/mlkem/mlkem_core.sv` menjalankan KeyGen_internal, Encaps_internal, dan Decaps_internal FIPS 203 (Algoritma 16-18) dari mikro-program garis-lurus (`mlkem_ctl_rom.sv`, dibangkitkan dari model golden `tb/golden/mlkem_ctl_model.py`) pada buffer byte, register file, mesin K-PKE 8d (tidak berubah), codec 9a, serta pembungkus hash dan perbandingan 9b. Setiap vektor ACVP ML-KEM-768 yang dipin lulus di kedua simulator: keyGen 25 (ek dan dk), enkapsulasi 25 (c dan k), dekapsulasi 10 (k, termasuk ciphertext yang dimodifikasi untuk menguji implicit rejection). Dua grup key-check tidak dijalankan terhadap RTL (ADR 0031: pemeriksaan masukan ada di HPS).

## 2. Verifikasi (MEASURED, simulasi; `verify.md`, `sim_verilator.md`, `sim_icarus.md`)
| Test | Hasil |
|---|---|
| V1 lint seluruh desain (Verilator `-Wall`, slang) | 0 peringatan, 0 error |
| V2 ROM sama dengan ROM yang dibangkitkan; pemeriksaan statis ROM; model kendali golden terhadap ACVP (25 + 25 + 10) dan golden yang tidak diubah | 4 lulus |
| V3 ACVP: keyGen 25, enkapsulasi 25, dekapsulasi 10 | 100 % sama, Icarus dan Verilator |
| V4 cross-check acak (20 kasus KeyGen, Encaps, Decaps dengan ciphertext valid dan berubah satu bit) dan rantai KeyGen -> Encaps -> Decaps | semua sama di kedua simulator |
| V5 protokol: start, op, dan tulis host saat sibuk diabaikan, reset di tengah Decaps lalu KeyGen bersih, beruntun dengan kunci lain, shared secret ditahan setelah done | lulus di kedua simulator |
| V6 siklus konstan (Decaps: ciphertext valid dan ditolak serta kunci rahasia berbeda dengan ek sama; Encaps: m berbeda dengan ek sama) | identik di kedua simulator |
| V7 kontrol negatif (NC-CMP, NC-SEL, NC-LEN, NC-OFF, NC-ROM) | masing-masing gagal pada test yang dinamai untuknya, kedua simulator |
| V10 regresi: skrip 9a dan 9b; tidak ada file blok beku yang berbeda dari main | PASS |

## 2b. Formal (MEASURED, SymbiYosys dengan boolector; `formal.md`, test plan Amandemen A2)
| Run | Hasil |
|---|---|
| A keselamatan: E1 non-interferensi kendali (dua salinan, data berbeda, handshake sama), S1 rentang, S2 busy / done, S3 tidak ada tulis host saat sibuk, S4 strobe, S5 port mesin, S6 alamat, S7 counter | PASS (base case dan induksi) |
| B kontrol NC-E1, NC-S3, NC-S4 pada salinan yang dirusak | masing-masing GAGAL di base case, seperti disyaratkan |
| C cover, kedalaman 260: KeyGen selesai, Encaps selesai, sebuah word digest ditulis | tercapai (bukti tidak vakum) |
Decaps selesai dan state S_CMPK butuh lebih dari 260 langkah (umpan hash memakan 136-148 word); run dalam terpisah (kedalaman 480, 28 menit) mencapai keduanya (S_CMPK pada langkah 266, Decaps selesai pada langkah 272): `formal_deep_cover.md`.

## 3. Siklus (MEASURED, simulasi, tanpa stall host)
Encaps 10,691 (konstan untuk setiap m dengan ek sama), Decaps 16,623 (konstan untuk ciphertext valid dan ditolak serta untuk kunci rahasia berbeda dengan ek sama), KeyGen 9,035-9,076 atas 25 seed ACVP. Siklus hanya bergantung pada rho publik (rejection sampling matriks A di dalam mesin): atas 25 kunci enkapsulasi ACVP Encaps memakan 10,664-10,727 siklus, atas 10 kunci dekapsulasi ACVP Decaps memakan 16,601-16,663.

## 4. Quartus (MEASURED, kernel-only, virtual pin, 25.1std Lite; `selection_worksheet.md` dan `quartus_MC*.md`)
- Seed 1-6 pada 40.000 ns: ALM 17,608-17,636 (median 17,620.5; 42 % dari 41,910 fitter), register 8,210-8,365, 54 blok RAM, 120,350 bit memori blok, 28 DSP; timing terpenuhi di setiap seed (setup terburuk 19.010 ns, hold terburuk 0.075 ns); Fmax slow corner terendah median 49.280 MHz (47.64-51.74).
- Informasi: MC-20 (20.000 ns, seed 1): timing terpenuhi (setup terburuk 4.419 ns), Fmax 64.18 MHz, 17,650 ALM.
- Critical Warning 15725 (port clock diberi makan virtual pin) di setiap kompilasi, seperti semua kompilasi kernel-only sebelumnya; tidak ada yang diabaikan.

## 5. Temuan dan penyimpangan (semuanya di Amandemen A1 test plan)
1. ESTIMATE meleset: siklus Encaps diperkirakan sekitar 11,500 dan terukur 10,691; ALM diperkirakan sekitar 20,000 dan terukur 17,620.5 (jumlah bagian terukur melebihkan perkiraan glue).
2. Kesalahan setup saya, bukan cacat RTL: import hilang di test protokol; path file salah di `.qsf` Quartus pertama (run pertama gagal dalam 45 detik dan tidak ada keluarannya yang dipakai).
3. Lint: dua nama tersembunyi (diganti nama) dan perbaikan lebar; penggantian nama di modul perbandingan 9b diikuti run ulang simulasi dan bukti 9b (evidence Quartus 9b tidak dikompilasi ulang untuk parameter lokal yang diganti nama, yang tidak bisa mengubah logika: INFERENCE).
4. Kontrol memakai set vektor yang dikurangi untuk membatasi waktu run (target `core` menjalankan set penuh). Run Icarus seluruh set memakan sekitar satu jam.

## 6. Yang tidak ditunjukkan ini
Bukan hasil papan, tanpa integrasi HPS (Fase 10), tanpa perbandingan dengan perangkat lunak, dan tanpa klaim percepatan atau daya. Bukti formal inti hanya mencakup properti kendali dan rentang, dengan sub-blok diganti stub protokol (bagian 2b; nilai dicakup simulasi terhadap ACVP). Pemeriksaan masukan FIPS 203 tidak ada di RTL (ADR 0031). Siklus-konstan ditunjukkan dalam simulasi untuk ek tetap (rho publik menentukan panjang sampling matriks); ini bukan hasil side-channel.

## 7. Catatan biaya (INFERENCE, perhitungan tim)
Encode dan decode polinomial berurutan dan tidak tumpang tindih dengan mesin: satu KeyGen menghabiskan sekitar 2,300 siklus untuk pack t_hat dan s_hat dan satu Decaps sekitar 2,400 siklus untuk load; ini biaya terukur dari jadwal, kemungkinan optimasi nanti, dan bukan bagian hasil ini.

## 8. Keputusan untuk tim
Hasil Fase 9 (`docs/results/phase09.md`) mendaftar butir terbuka: penerimaan konfigurasi inti C7 sebagaimana dibangun (ADR 0033, Proposed), pilihan inti sponge hash (C5 bawaan, K0 lebih kecil), dan pertanyaan papan (PENDING #8). Tidak ada yang diputuskan di sini.
