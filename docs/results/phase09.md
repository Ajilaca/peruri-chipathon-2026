<!-- claim-lint: skip-file (result artifact: internal status page, not proposal text) -->
# Hasil - Fase 9: ML-KEM-768 penuh dalam RTL, simulasi (blok 9a, 9b, 9c; konfigurasi C7-core)

- Status: DONE (ketiga blok dibangun, diverifikasi, dan diukur; penerimaan ADR 0033 dan kotak Persetujuan adalah hak tim)
- Catatan status: ADR 0031 (Accepted, Jo 2026-10-03): pemeriksaan masukan FIPS 203 dijalankan di HPS, bukan di RTL, sehingga grup ACVP pemeriksaan kunci tidak dijalankan terhadap RTL. ADR 0032 (Accepted): satu STOP per blok. Chat 2026-10-03 (Jo): tidak ada commit selama bekerja, minimal 20 commit di akhir sesuai urutan kerja sebenarnya. Setiap blok punya rencana tes yang ditulis sebelum RTL-nya, dan aturan lulus tidak diubah setelah pengukuran (Amandemen A1 dari 9a, 9b, dan 9c, A2 dari 9c mencatat apa yang ditemukan atau ditambahkan kemudian). Pekerjaan ada di working tree; commit dibuat setelah hasil ini.
- Tanggal (UTC): 2026-10-03 / 2026-10-04
- Git commit (HEAD saat diverifikasi): lihat `git log main..phase9-mlkem-core` (cabang dibuat saat commit dibuat; sampai saat itu seluruh Fase 9 belum di-commit di working tree di atas main 497482f)
- Hasil: `rtl/mlkem/mlkem_core.sv` menjalankan KeyGen_internal, Encaps_internal, dan Decaps_internal FIPS 203 (Algoritma 16-18) pada buffer byte, dengan mesin K-PKE Fase 8d tidak berubah, codec koefisien/byte (9a), pembungkus hash G / H / J dan pembandingan waktu-konstan dengan pemilihan mask (9b), dan pengendali micro-program lurus (9c). Setiap vektor ACVP ML-KEM-768 yang dipatok lulus di kedua simulator: keyGen 25, encapsulation 25, decapsulation 10 (kasus ciphertext termodifikasi termasuk). Siklus konstan: Decaps 16,623 untuk ciphertext valid dan ditolak serta untuk kunci rahasia berbeda dengan ek yang sama; Encaps 10,691; KeyGen 9,035-9,076. Quartus kernel-only (seed 1-6, 40 ns): 17,608-17,636 ALM (42 % dari 41,910), 54 blok RAM, 28 DSP, timing terpenuhi di setiap seed, Fmax median 49.280 MHz. Bukti formal kontrol 9a, 9b, dan 9c dengan kontrol negatif. Hanya simulasi, tanpa papan (PENDING #8).
- Lingkungan: Ubuntu 24.04.4 LTS, OSS CAD Suite 2026-09-23 (Verilator 5.053, Icarus 14.0 devel, slang, SymbiYosys dengan boolector), cocotb 2.1.0, Quartus Prime Lite 25.1std.0 Build 1129.
- Constraint: 40.000 ns (constraint bergaya `C.sdc` pada proyek Quartus baru, identik dengan Fase 5-8); kompilasi informasi pada 20.000 ns.

## 1. Kriteria selesai (Common RTL Gate, docs/ROADMAP.md), Fase 9
| # | Kriteria | Evidence | Status |
|---|---|---|---|
| CRG-1 | Lint bersih | `evidence/phase09/9a/verify.md`, `evidence/phase09/9b/verify.md`, `evidence/phase09/9c/verify.md` (Verilator -Wall: 0 peringatan; dua peringatan nama-tersembunyi pada lint 9c pertama diperbaiki dengan mengganti nama) | PASS |
| CRG-2 | Elaborasi bersih (slang) | `evidence/phase09/9a/verify.md`, `evidence/phase09/9b/verify.md`, `evidence/phase09/9c/verify.md` (slang: 0 error, 0 peringatan) | PASS |
| CRG-3 | Bit-exact terhadap model acuan, kedua simulator | 9a: pack dan unpack terhadap primitif acuan untuk d = 1, 4, 10, 12 dan konstanta Compress pada semua 3,329 masukan; 9b: G, H, J terhadap hashlib dan pembandingan serta pemilihan mask terhadap model FO acuan; 9c: setiap vektor ACVP yang dipatok (keyGen 25, encapsulation 25, decapsulation 10) dan pemeriksaan silang acak: `evidence/phase09/9a/verify.md`, `evidence/phase09/9b/verify.md`, `evidence/phase09/9c/sim_verilator.md`, `evidence/phase09/9c/sim_icarus.md` | PASS |
| CRG-4 | Kasus sudut sebelum tes | `evidence/phase09/9a/test_plan_9a.md`, `evidence/phase09/9b/test_plan_9b.md`, `evidence/phase09/9c/test_plan_9c.md`, `evidence/phase09/phase9_plan.md` (ditulis sebelum RTL setiap blok; amandemen mencatat perubahan setelah jalankan pertama) | PASS |
| CRG-5 | Regresi: fase sebelumnya masih lulus | `evidence/phase09/9c/verify.md` (menjalankan ulang 9a dan 9b di kedua simulator dan formal; 0 file blok Fase 6-8 yang dibekukan berbeda dari main), `evidence/phase09/9c/regression_phase8.md` (tes mesin Fase 8 dijalankan ulang) | PASS |
| CRG-6 | Parameter terkunci | `.claude/skills/mlkem-guard/scripts/check_params.py` (dijalankan pada fase ini, keluarannya di bawah pada verifikasi hasil ini); tidak ada konstanta FIPS 203 yang berubah; Compress, Decompress, dan ByteEncode mengikuti FIPS 203 Algoritma 5, 6, dan 4.7 dan tepat terhadap model acuan yang tidak dimodifikasi pada semua masukan | PASS |
| CRG-7 | Evidence jumlah siklus konstan | `evidence/phase09/9c/cycles_verilator_core.json`, `evidence/phase09/9c/cycles_icarus_core.json`, `evidence/phase09/9c/sim_verilator.md`: Decaps identik untuk ciphertext valid dan ditolak serta untuk kunci rahasia berbeda dengan ek yang sama; Encaps identik untuk m berbeda; tabel siklus 9a dan 9b di `evidence/phase09/9a/cycles_verilator_pack.json` dan `evidence/phase09/9b/cycles_verilator_fo.json` | PASS |
| CRG-8 | Properti formal | `evidence/phase09/9a/formal.md`, `evidence/phase09/9b/formal.md`, `evidence/phase09/9b/formal_vacuity_check.md`, `evidence/phase09/9c/formal.md` (setiap bukti sesuai harapan, setiap kontrol negatif gagal sebagaimana disyaratkan; pengendali dibuktikan dengan stub protokol) | PASS |
| CRG-9 | Evidence Quartus; tidak ada slack negatif atau kegagalan didokumentasikan | `evidence/phase09/9a/selection_worksheet.md`, `evidence/phase09/9b/selection_worksheet.md`, `evidence/phase09/9c/selection_worksheet.md` dan ekstrak Quartus di sampingnya (misalnya `evidence/phase09/9c/quartus_MC.md`): seed 1-6 pada 40 ns timing terpenuhi untuk CD, HF, dan MC, ditambah kompilasi informasi 20 ns | PASS |
| CRG-10 | Artefak hasil + pemeriksa klaim | `cmd: python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase09.md` dan `cmd: python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal` | PASS |

## 1b. Kriteria PASS Fase 9 (docs/ROADMAP.md Fase 9, butir 5) dan blok
| # | Kriteria | Evidence | Status |
|---|---|---|---|
| P9-1 | 100 % vektor yang berlaku lulus di kedua simulator (keyGen 25, encapsulation 25, decapsulation 10; grup pemeriksaan kunci ada di HPS menurut ADR 0031) | `evidence/phase09/9c/sim_verilator.md`, `evidence/phase09/9c/sim_icarus.md`, `docs/decisions/adr/ADR-0031-phase-9-fips-203-input-checks-are-done-by-the-hps-not-in-the.md` | PASS |
| P9-2 | Evidence siklus konstan untuk Decaps (ciphertext valid dan ditolak, kunci rahasia berbeda, masukan publik tetap) | `evidence/phase09/9c/cycles_verilator_core.json`, `evidence/phase09/9c/cycles_icarus_core.json` | PASS |
| P9-3 | Evidence Quartus untuk inti penuh | `evidence/phase09/9c/selection_worksheet.md`, `evidence/phase09/9c/quartus_MC.md` | PASS |
| P9-4 | Baris C7-core ROADMAP terisi | `docs/ROADMAP.md` (baris C7a, C7b, C7-core), `docs/decisions/adr/ADR-0033-phase-9-c7-core-as-built-ml-kem-768-in-simulation-acvp-100-p.md` | PASS |
| 9a | Codec (pack dan unpack), tepat, formal, Quartus | `evidence/phase09/9a/result_9a.md` | PASS |
| 9b | Pembungkus hash dan pembandingan FO, tepat, formal, Quartus | `evidence/phase09/9b/result_9b.md` | PASS |
| 9c | Pengendali inti ML-KEM, ACVP 100 %, formal, Quartus | `evidence/phase09/9c/result_9c.md` | PASS |

## 2. Yang dihasilkan
| Path | Fungsi |
|---|---|
| `rtl/mlkem/mlkem_pack.sv`, `mlkem_unpack.sv`, `mlkem_codec_top.sv` | 9a: Compress_d + ByteEncode_d dan ByteDecode_d + Decompress_d, d dalam {1, 4, 10, 12}, tanpa pembagian |
| `rtl/mlkem/mlkem_hash.sv`, `mlkem_fo_cmp.sv`, `mlkem_hash_fo_top.sv` | 9b: G, H, J pada sponge (C5 bawaan, `CORE_R2`), pembandingan 1,088 byte waktu-konstan dan pemilihan mask K / K_bar |
| `rtl/mlkem/mlkem_core.sv`, `mlkem_ctl_rom.sv` (dibangkitkan), `mlkem_ram.sv`, `mlkem_fifo4.sv`, `mlkem_wordbytes.sv`, `mlkem_bytedst.sv`, `mlkem_ldpoly.sv`, `mlkem_stpoly.sv` | 9c: pengendali dengan micro-program 40-bit, buffer kunci, konverter byte / word, tugas muat dan simpan polinomial; mesin 8d di-instansiasi tanpa perubahan |
| `tb/golden/codec_model.py`, `fo_model.py`, `mlkem_ctl_model.py` dan tesnya | model acuan lebih dahulu (codec, pembandingan, program pengendali dengan pemeriksa statis) |
| `tb/mlkem/` | tes cocotb dan runner di kedua simulator dengan kontrol negatif (pack, unpack, hash, pembandingan FO, inti) |
| `formal/phase09-integration/9a`, `9b`, `9c`, `formal/run/run_formal_phase9a.py`, `9b.py`, `9c.py` | bukti SymbiYosys, cover, dan kontrol negatif |
| `quartus/phase09a_codec/`, `phase09b_hashfo/`, `phase09c_core/` | revisi Quartus (kernel-only, pin virtual), seed 1-6 dan 20 ns |
| `scripts/test/phase9a_verify.sh`, `phase9b_verify.sh`, `phase9c_verify.sh`, `select_9a.py`, `select_9b.py`, `select_9c.py`, `gen_mlkem_ctl_rom.py`, `build_phase9_report.py` | verifikasi, aturan dari file, pembangkitan ROM, laporan PDF |
| `evidence/phase09/` | rencana fase, rencana tes, verifikasi, log simulasi dan formal, tabel siklus, ekstrak Quartus, worksheet, laporan blok |
| `docs/decisions/0031` sampai `0033` | pemeriksaan masukan di HPS (Accepted), protokol checkpoint (Accepted), C7-core sebagaimana dibangun (Proposed) |
| `docs/reports/CHIPATON_Phase9_Report.pdf` | laporan (Bahasa Indonesia) |

## 3. Angka (MEASURED: laporan Quartus dan simulasi; latensi dalam mikrodetik adalah INFERENSI / perhitungan tim)
### 3a. 9a, codec (kernel-only)
| Besaran | Nilai | ESTIMATE yang ditulis sebelum pengukuran |
|---|---|---|
| ALM, median (min-maks), seed 1-6 | 299.0 (298-299) | tidak dinyatakan sebagai rentang |
| Register / M10K / DSP | 192-193 / 0 / 2 | - |
| Timing pada 40.000 ns | terpenuhi di setiap seed | - |
| Fmax slow corner terendah, median (min-maks) MHz | 105.630 (100.46-110.38) | - |
| Siklus per polinomial, pack d = 1 / 4 / 10 / 12 | 261 / 261 / 325 / 389 | d = 1 dan 4: estimasi meleset (unit terikat masukan pada 256 koefisien) |
| Siklus per polinomial, unpack d = 1 / 4 / 10 / 12 | 259 / 259 / 323 / 387 | sama |
Informasi pada 20.000 ns (seed 1): terpenuhi, setup +10.952 ns. Sumber: `evidence/phase09/9a/selection_worksheet.md`, `cycles_*.json`.

### 3b. 9b, pembungkus hash dan pembandingan (kernel-only, sponge C5)
| Besaran | Nilai | Catatan |
|---|---|---|
| ALM, median (min-maks), seed 1-6 | 6,734.5 (6,712-6,745) | sponge C5 menyumbang 6,167 di antaranya (Fase 8a) |
| Register / M10K / DSP | 1,976 / 0 / 0 | - |
| Timing pada 40.000 ns | terpenuhi di setiap seed | - |
| Fmax slow corner terendah, median (min-maks) MHz | 50.625 (47.84-52.07) | - |
| Siklus, C5: G (33 B) / G (64 B) / H (1,184 B) / J (1,120 B) / bandingkan 1,088 B | 30 / 33 / 282 / 274 / 137 | - |
| Siklus, sponge K0 (informasi): G 33 / G 64 / H / J | 42 / 45 / 390 / 382 | instance K0: 4,221 ALM, 70.02 MHz (seed 1, `HF-K0`) |
Informasi pada 20.000 ns (seed 1): terpenuhi, setup +3.843 ns. Sumber: `evidence/phase09/9b/selection_worksheet.md`, `cycles_*.json`.

### 3c. 9c, inti ML-KEM-768 (kernel-only, hash `HF` dengan sponge C5, mesin 8d OVERLAP tidak berubah)
| Besaran | Nilai | ESTIMATE yang ditulis sebelum pengukuran |
|---|---|---|
| ALM, median (min-maks), seed 1-6 | 17,620.5 (17,608-17,636), 42 % dari 41,910 milik fitter | sekitar 20,000: terlalu tinggi (jumlah bagian-bagian terukur) |
| Register | 8,210-8,365 | - |
| Blok RAM / bit memori blok / DSP | 54 / 120,350 / 28 | - |
| Timing pada 40.000 ns | terpenuhi di setiap seed (worst setup 19.010 ns, worst hold 0.075 ns) | - |
| Fmax slow corner terendah, median (min-maks) MHz | 49.280 (47.64-51.74) | - |
| Siklus: Encaps (ek tetap) | 10,691 (rentang ek ACVP 10,664-10,727) | sekitar 11,500: meleset |
| Siklus: Decaps (ek tetap) | 16,623 (rentang dk ACVP 16,601-16,663) | - |
| Siklus: KeyGen atas 25 seed ACVP | 9,035-9,076 | - |
| Latensi pada Fmax median (perhitungan tim; static timing kernel-only, bukan pengukuran papan) | KeyGen sekitar 184 us, Encaps sekitar 217 us, Decaps sekitar 337 us | - |
Informasi pada 20.000 ns (seed 1, MC-20): timing terpenuhi (worst setup +4.419 ns), 64.18 MHz, 17,650 ALM; static timing kernel-only, bukan sistem pada 50 MHz.
ACVP: keyGen 25 (ek dan dk), encapsulation 25 (c dan k), decapsulation 10: 100 % di Icarus dan Verilator. Simulasi: target `core` 6/6 dan lima kontrol negatif (NC-CMP, NC-SEL, NC-LEN, NC-OFF, NC-ROM) masing-masing menggagalkan tes yang dinamai untuknya: 11/11 per simulator.
Sumber: `evidence/phase09/9c/selection_worksheet.md`, `quartus_MC*.md`, `sim_*.md`, `cycles_*_core.json`.

### 3d. Formal (MEASURED, properti kontrol dan rentang; nilai dicakup oleh simulasi)
| Blok | Bukti | Kontrol | Cover |
|---|---|---|---|
| 9a | P1-P5 (hitungan, byte tertahan, idle, keseimbangan bit) PASS (kasus dasar dan induksi) | NC-P2, NC-U6 gagal; NC-P1 dan NC-U1 memberi UNKNOWN pada bukti dan FAIL pada BMC kedalaman 300, sebagaimana disyaratkan (bagian 6) | tercapai |
| 9b | H1-H5 pembungkus hash (sponge diganti stub protokol), F1-F4 pembandingan PASS | NC-H1, NC-H5, NC-F1, NC-F3, NC-F4 gagal sebagaimana disyaratkan | tercapai; bukti stub semula vakum dan dikoreksi (bagian 6) |
| 9c | E1 non-interferensi pengendali, S1-S7 PASS (kasus dasar dan induksi) | NC-E1, NC-S3, NC-S4 gagal sebagaimana disyaratkan | KeyGen selesai, Encaps selesai, word digest ditulis tercapai pada kedalaman 260; Decaps selesai dan S_CMPK tercapai pada jalankan dalam (kedalaman 480, `9c/formal_deep_cover.md`) |
Sumber: `9a/formal.md`, `9b/formal.md`, `9b/formal_vacuity_check.md`, `9c/formal.md`, `9c/formal_deep_cover.md` di bawah `evidence/phase09/`.

## 4. Standar dan sumber yang dipatok
FIPS 203 (ML-KEM) Algoritma 4-6 (ByteEncode, ByteDecode, Compress, Decompress) dan Algoritma 16-18 (ML-KEM.KeyGen_internal, Encaps_internal, Decaps_internal); FIPS 202 seperti di Fase 7; vektor ACVP ML-KEM-768 NIST yang dipatok di `reference/kat_sources.md` (set sampel NIST dari server ACVP, bukan validasi CAVP penuh). Tidak ada parameter atau aritmetika FIPS 203 yang berubah (C1). Pemeriksaan masukan FIPS 203 (Bagian 7.2 dan 7.3) tidak ada di RTL (ADR 0031).

## 5. Cakupan dan batas
- Hanya simulasi, formal, dan static timing. Tidak ada papan; Fmax bersifat kernel-only dengan pin virtual. "Timing terpenuhi pada 20 ns" adalah static timing alur ini, bukan sistem pada 50 MHz. Tidak ada klaim tentang kecepatan terhadap perangkat lunak, daya, atau side channel (C3). Tidak ada yang di sini merupakan validasi perangkat keras (C8).
- Waktu-konstan di sini berarti jumlah siklus tidak bergantung pada nilai rahasia, ditunjukkan dalam simulasi untuk masukan publik tetap. Jumlah siklus bergantung pada ek atau rho publik melalui rejection sampling matriks A (Encaps 10,664-10,727 dan Decaps 16,601-16,663 atas kunci ACVP). Ini bukan hasil side-channel.
- Formal mencakup properti kontrol dan rentang dengan sub-blok diganti stub protokol (mesin K-PKE, sponge, pembungkus hash, loader), bukan nilai; nilai dicakup oleh simulasi terhadap model acuan, hashlib, dan ACVP. Cover dalam (Decaps selesai, S_CMPK, kedalaman 480) adalah jalankan terpisah, evidence di bagian 6.
- Vektor ACVP adalah set sampel yang dipatok; dua grup pemeriksaan kunci tidak dijalankan terhadap RTL (ADR 0031, HPS yang melakukan pemeriksaan, tidak diuji di papan).
- Keacakan masuk lewat port (`d`, `z`, `m`); tidak ada sumber acak di RTL. Materi kunci rahasia tetap di register dan memori yang tidak dihapus setelah operasi (tidak ada klaim tentang ini).
- Jalankan Icarus seluruh set ACVP memakan waktu sekitar satu jam, sehingga kontrol negatif memakai set vektor yang dikurangi; target `core` menjalankan set penuh.
- Codec dan pemuatan bersifat serial dan tidak ditumpangtindihkan dengan mesin (sekitar 2,300 siklus pada KeyGen, sekitar 2,400 pada Decaps): biaya terukur jadwal dan kemungkinan optimasi kemudian, bukan hasil.

## 6. Penyimpangan, kegagalan, dan masalah terbuka
- Bukti formal vakum ditemukan dan dibuang (9b): bukti pertama pembungkus hash dengan stub protokol lulus karena sinyal stub yang dideklarasikan sebagai `(* anyseq *) logic` dan hanya dibaca di kode prosedural diperlakukan sebagai konstanta. Jalankan cover menunjukkannya; stub diubah menjadi `(* anyseq *) wire`, bukti dijalankan ulang, dan hasil yang dibuang didokumentasikan di `evidence/phase09/9b/formal_vacuity_check.md`. Stub anyseq lain dari fase sebelumnya diperiksa kemudian (stub 8c bebas; `modmul_reduce_uf` Fase 3 bebas, ditunjukkan oleh kontrolnya sendiri); tidak ada hasil Fase 3-8 yang berubah.
- Bukti pembungkus 9b dengan sponge asli terlalu lambat (dihentikan setelah 30 menit lewat id prosesnya); pembungkus dibuktikan dengan stub protokol sponge dan sponge sendiri punya buktinya sendiri (Fase 7 dan 8a). Nilai digest dicakup oleh simulasi terhadap hashlib.
- Bukti formal inti tidak direncanakan dan ditambahkan (Amandemen A2 rencana tes 9c) setelah jalankan verifikasi karena CRG-8 memintanya; aturan rencana tidak diubah.
- Kontrol formal 9a (NC-P1 dan NC-U1) memberi UNKNOWN pada jalankan bukti (pelanggaran berada di luar kedalaman induksi) dan FAIL pada BMC kedalaman 300, seperti NC-B Fase 3; didokumentasikan di Amandemen A1 rencana 9a.
- Cover dalam (kedalaman 480) mencapai setiap state yang di-cover, termasuk Decaps selesai (langkah 272) dan S_CMPK (langkah 266); ini jalankan panjang terpisah (28 menit, setara `formal/run/run_formal_phase9c.py deep`, `formal/phase09-integration/9c/mlkem_core_cover_deep.sby`), evidence `evidence/phase09/9c/formal_deep_cover.md`. Pada kedalaman 260 hanya KeyGen selesai, Encaps selesai, dan sebuah word digest yang tercapai.
- ESTIMATE meleset: siklus pack dan unpack untuk d = 1 dan 4 (terikat masukan); siklus Encaps diperkirakan sekitar 11,500, terukur 10,691; ALM inti diperkirakan sekitar 20,000, terukur 17,620.5.
- Kesalahan proses (milik saya, bukan cacat RTL): import yang hilang pada tes protokol 9c; path file yang salah pada `.qsf` Quartus pertama 9c (jalankan pertama gagal dalam 45 detik dan tidak ada keluarannya yang dipakai; ketujuh revisi dijalankan ulang); driver 9a pertama tidak pernah menawarkan koefisien ke-257, sehingga satu kontrol batal sampai driver diperbaiki.
- Parameter lokal yang diganti nama di `mlkem_fo_cmp.sv` (nama tersembunyi pada lint) diikuti dengan jalankan ulang simulasi dan bukti 9b; ekstrak Quartus 9b tidak dikompilasi ulang untuknya (INFERENSI: penggantian nama tidak dapat mengubah logika).
- Critical Warning 15725 (port clock diberi pin virtual) di setiap kompilasi kernel-only, seperti fase sebelumnya; tidak ada yang di-waive.
- Terbuka: PENDING #8 (tanpa papan); repositori memuat sekitar 855 MB salinan Quartus paralel yang tidak dilacak di `quartus/par_a` sampai `par_d` yang tidak pernah di-commit (dipindahkan tim ke penyimpanan cloud).

## 7. Keputusan yang diperlukan
- ADR 0033 (C7-core sebagaimana dibangun; juga: inti sponge hash pembungkus, C5 bawaan pada 6,734.5 ALM lawan K0 pada 4,221 ALM per instance hash, dan apakah akan mengoptimasi codec serial): Proposed; PENDING #33. Tim menerima atau menolaknya.
- PENDING #8 (papan): Fase 10 dan 11 membutuhkan DE10-Nano.
- Bagian 3 proposal (halaman 4-6) belum ditulis (C4); hanya ditulis bila tim memintanya.

## 8. Klaim yang dibuat pada fase ini
Tidak ada yang ditulis untuk juri atau teks proposal. Baris ROADMAP C7a, C7b, dan C7-core diisi dari evidence di atas. Klaim apa pun kemudian harus membawa label hanya simulasi.

## 9. Persetujuan
- [x] Penyetuju manusia (Faza Dzil, 2026-10-05; dicentang oleh asisten atas instruksi Jo, Tim J5):
      Fase berikutnya dimulai hanya setelah anggota tim mencentang kotak ini. Claude tidak pernah mencentangnya.
