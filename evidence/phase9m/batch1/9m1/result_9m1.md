<!-- claim-lint: skip-file (internal block report, not proposal text) -->
# Laporan Fase 9M butir 1 (9M-1): dua byte per siklus pada jalur codec (`CODEC_W2`)

- Status: SELESAI (STOP setelah butir, ADR 0034). Pekerjaan ada di branch `phase9m-optimisation` dan belum di-commit (chat 2026-10-04: pekerjaan dilaporkan dulu). Aturan adopsi rencana terpenuhi; penerimaan adalah milik tim (ADR 0035, Proposed).
- Tanggal (UTC): 2026-10-04. Rencana dan aturan: `test_plan_9m1.md` (ditulis sebelum RTL; Amandemen A1 mencatat apa yang ditemukan atau ditambahkan). Hanya simulasi, formal, dan timing statis; tidak ada di sini yang hasil papan.

## 1. Apa yang diubah
File baru di `rtl/mlkem/`: `mlkem_pack2.sv`, `mlkem_unpack2.sv`, `mlkem_wordbytes2.sv`, `mlkem_bytedst2.sv`, `mlkem_ldpoly2.sv`, `mlkem_stpoly2.sv`, `mlkem_codec2_top.sv` (dua byte per beat, buffer 32-bit, aritmetika Compress / Decompress sama). `mlkem_core.sv` mendapat parameter `CODEC_W2` (bawaan 0 = task Fase 9, perilaku tidak berubah); pada 1 ia memakai task baru. Mikro-program (ROM), mesin, dan semua file Fase 6-8 tidak berubah (0 file berbeda dari main).

## 2. Parameter yang diukur dan hasilnya
| Parameter | Fase 9 (baseline) | 9M-1 (`CODEC_W2 = 1`) | Sumber |
|---|---|---|---|
| Load / store satu polinomial, d = 12 (siklus) | 391 / 393 | 263 / 265 | `profile_w2_verilator.json`, `../../profile_verilator.json` |
| Load / store, d = 10 | 326-327 / 329 | 262-263 / 265 | sama |
| Load / store, d = 1 atau 4 | 263 / 265 | 263 / 265 (tidak berubah, dibatasi port mesin) | sama |
| Codec saja: siklus pack / unpack per polinomial, d = 1, 4, 10, 12 | 261 / 261 / 325 / 389 dan 259 / 259 / 323 / 387 | 261 / 261 / 261 / 261 dan 259 / 259 / 259 / 259 | `cycles_*_pack2.json`, `cycles_*_unpack2.json` |
| Siklus KeyGen, Encaps, Decaps (masukan profil) | 9,095 / 10,735 / 16,667 | 8,327 / 10,159 / 15,515 (-8.4 %, -5.4 %, -6.9 %) | profil |
| Siklus atas vektor ACVP: KeyGen (25 seed) | 9,035-9,076 | 8,267-8,308 | `cycles_*_core_w2.json`, `9c/cycles_*_core.json` |
| Siklus atas vektor ACVP: Encaps (25 ek) / Decaps (10 dk) | 10,664-10,727 / 16,601-16,663 | 10,088-10,151 / 15,449-15,511 | sama |
| Encaps / Decaps dengan ek tetap (konstan) | 10,691 / 16,623 | 10,115 / 15,471 | sama |
| ALM, median (min-maks), seed 1-6 | 17,620.5 (17,608-17,636) | 17,654.0 (17,641-17,683), +33.5 | `selection_worksheet.md` |
| ALM dalam % dari 41,910 fitter | 42 % | 42 % | sama |
| Register | 8,210-8,365 | 8,189-8,376 | sama |
| Blok RAM / bit memori blok / DSP | 54 / 120,350 / 28 | 54 / 120,350 / 28 | sama |
| Timing pada 40.000 ns | terpenuhi di setiap seed (setup terburuk 19.010 ns, hold terburuk 0.075 ns) | terpenuhi di setiap seed (setup terburuk 18.655 ns, hold terburuk 0.077 ns) | sama |
| Fmax, slow corner terendah, median (min-maks) | 49.280 MHz (47.64-51.74) | 48.855 MHz (46.85-52.15), -0.425 | sama |
| Informasi pada 20.000 ns (seed 1) | terpenuhi, +4.419 ns, 64.18 MHz, 17,650 ALM | terpenuhi, +4.355 ns, 63.92 MHz, 17,808 ALM | `quartus_MW-20.md`, `9c/quartus_MC-20.md` |
| Latensi pada median Fmax (perhitungan tim; timing statis kernel-only, bukan pengukuran papan), KeyGen / Encaps / Decaps | 184.6 / 217.8 / 338.2 us | 170.4 / 207.9 / 317.6 us | worksheet |
| Peringatan kritis per kompilasi | 1 (clock virtual pin, seperti semua kompilasi kernel-only sebelumnya) | 1 | ekstrak |

## 3. Verifikasi (semuanya MEASURED)
| Test (rencana bagian 4) | Hasil | Evidence |
|---|---|---|
| V1 lint (Verilator -Wall, slang), inti pada kedua nilai parameter, top codec2 | 0 peringatan, 0 error | run 2026-10-04 (diulang setelah perbaikan `generate`) |
| V2 codec2: test pack dan unpack 9a dengan dua byte per beat | pack 6/6 dan unpack 7/7, bit-exact terhadap primitives golden, Verilator dan Icarus | file `cycles_*`; log `tb/mlkem/run_codec2_tests.py` |
| V3 inti dengan `CODEC_W2 = 1`: ACVP keyGen 25, enkapsulasi 25, dekapsulasi 10, cross-check acak (20 kasus), rantai, protokol, siklus konstan | 6/6 dan 100 % sama, kedua simulator | `sim_verilator.md`, `sim_icarus.md` |
| V4 profil dengan `CODEC_W2 = 1` | bagian 2 | `profile_w2_verilator.json` |
| V5 kontrol negatif NC-W-ORD, NC-W-CNT (codec2) dan NC-W-CORE (inti) | masing-masing gagal pada test yang dinamai untuknya, kedua simulator | `sim_*.md` dan log runner codec2 |
| V6 formal: pack2 dan unpack2 (P1-P5, U1-U6) dengan kontrol; bukti pengendali 9c dengan `CODEC_W2 = 1` | semua sesuai harapan (NC-P1 dan NC-U1 UNKNOWN pada bukti dan FAIL pada BMC kedalaman 300, seperti di 9a); bukti pengendali PASS | `formal.md`; `mlkem_core_w2_safety.sby` (PASS dengan k-induksi, run 2026-10-04) |
| V7 regresi pada parameter bawaan | `phase9c_verify.sh` OVERALL PASS (ACVP 11/11 per simulator, 9a 17/17, 9b 23/23 dengan formal, blok beku 0 file berbeda); formal 9c SEMUA SESUAI HARAPAN; profil pada nilai bawaan sama persis dengan profil Fase 9 | `regression_default.md` |
| V8 Quartus MW seed 1-6 dan MW-20 | bagian 2 | `quartus_MW*.md`, `selection_worksheet.md` |

## 4. Aturan adopsi (test plan bagian 6; ditetapkan sebelum mengukur)
| Butir | Hasil |
|---|---|
| 1 kebenaran (V1-V3, V5-V7) | terpenuhi |
| 2 timing terpenuhi pada 40.000 ns di setiap seed | terpenuhi |
| 3 t = siklus / median Fmax lebih rendah dari Fase 9 untuk KeyGen, Encaps, dan Decaps | terpenuhi (170.4 < 184.6, 207.9 < 217.8, 317.6 < 338.2 us) |
| 4 median ALM paling banyak 1,000 di atas 17,620.5 | terpenuhi (+33.5) |
9M-1 diadopsi oleh aturannya. Bawaan `CODEC_W2` tetap 0 sampai tim menerimanya (ADR 0035, Proposed).

## 5. Estimasi lawan pengukuran (estimasi ditulis di rencana sebelum mengukur)
- Siklus load / store: diperkirakan sekitar 263 / 265 untuk d = 10 dan 12; terukur 263 / 265 (d = 10: 262-263): di dalam.
- KeyGen, Encaps, Decaps: diperkirakan sekitar 8,330 / 10,160 / 15,520; terukur 8,327 / 10,159 / 15,515: di dalam.
- ALM: diperkirakan +100 sampai +500; terukur +33.5: terlalu tinggi (modul dua-byte hampir sekecil modul satu-byte).
- Fmax: diperkirakan 47-51 MHz; terukur median 48.855: di dalam. Penurunan 0.425 MHz terhadap Fase 9 berada dalam sebaran antar seed (46.85-52.15); bahwa codec tidak berada di jalur kritis adalah INFERENCE dan jalur kritis tidak diperiksa di sini.

## 6. Temuan dan penyimpangan (semuanya di Amandemen A1 rencana)
1. Kompilasi Quartus pertama gagal dalam hitungan detik (Quartus 25.1 butuh `generate` / `endgenerate` di sekitar `if` generate); keluarannya tidak dipakai; ketujuh revisi dan simulasi inti dijalankan ulang pada file akhir (kesalahan saya, bukan masalah desain).
2. Bukti formal inti dengan `CODEC_W2 = 1` ditambahkan setelah rencana; tidak ada run cover untuk pack2 dan unpack2 (modul 9a juga tidak punya).
3. Run Icarus seluruh set inti memakan sekitar satu jam; kontrol memakai set vektor yang dikurangi, seperti di 9c.

## 7. Yang tidak ditunjukkan ini
Tidak ada hasil papan dan tidak ada perbandingan dengan perangkat lunak. Penghematan terbatas pada load dan store polinomial (sekitar 6-8 % siklus); mesin (65-72 % siklus) tidak berubah. Latensi dalam mikrodetik adalah timing statis kernel-only dibagi siklus hasil simulasi. Waktu-konstan berarti invarian jumlah siklus saja; siklus bergantung pada ek atau rho publik lewat sampling matriks.

## 8. Keputusan untuk tim
ADR 0035 (Proposed): terima `CODEC_W2 = 1` sebagai konfigurasi untuk butir Fase 9M berikutnya (butir 2: seed 20 ns; butir 3: hash K0; butir 4: tumpang tindih dengan mesin). Tidak ada yang diputuskan di sini.
