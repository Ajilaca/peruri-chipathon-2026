# ADR 0019: Jalur minimal ke inti ML-KEM-768 penuh sebelum Kamis 2026-10-08 (menggantikan lingkup ADR 0018)

- Status: Accepted
- Tanggal: 2026-10-02
- Diputuskan oleh: Jevan, Team J5 (chat 2026-10-02: Fase 8 dan 9 harus ada; opsi "Jalur minimal ke ML-KEM penuh"; 6-8 jam per hari)

## Konteks
- ADR 0018 (Accepted 2026-10-02) merencanakan: menyelesaikan Fase 5M S6-S8, lalu Keccak K0, Bagian 3 proposal; Fase 8
  dan 9 tidak dicoba.
- Tim lalu menyatakan Fase 8 dan 9 harus dikerjakan, dan memilih opsi "jalur minimal ke ML-KEM penuh", dengan perhatian
  tim 6-8 jam per hari.
- Batas waktu: Kamis 2026-10-08 (dari Jumat 2026-10-02; jam tidak disebutkan; pembekuan evidence direncanakan Rabu malam).
- Estimasi (ESTIMATE, keyakinan rendah; dasar: langkah S6 memakan sekitar 6 jam waktu jam dinding): Keccak K0 8-14 jam;
  sampler baseline 8-12 jam; pengendali ML-KEM penuh minimal dan integrasi 35-60 jam; Bagian 3 proposal 6-10 jam. Total
  sekitar 57-96 jam untuk enam hari. Keberhasilan tidak dijamin; tingkat di bawah menjaga hasil parsial tetap dapat dilaporkan.
- Risiko yang diketahui: (1) penyimpanan polinomial seluruh KEM tidak muat sebagai memori flip-flop seperti inti NTT
  (anggaran ADR 0009 hanya untuk inti NTT; desain penuh harus muat di 41.910 ALM, penyebut fitter), jadi penyimpanan
  polinomial lain kemungkinan memerlukan M10K; (2) roadmap mensyaratkan ADR tentang apakah pemeriksaan masukan FIPS 203
  berjalan di perangkat keras atau di HPS sebelum Fase 9 mulai; (3) Decaps memerlukan bukti siklus konstan untuk
  ciphertext valid dan ditolak.

## Opsi yang dipertimbangkan
(a) Jalur minimal: hentikan Fase 5M setelah S6; lewati Fase 6; lewati optimasi Fase 8 (8a dua ronde per siklus, 8c
    matriks on-the-fly, 8d tumpang-tindih) dan pakai sampler baseline; integrasikan ML-KEM-768 penuh dengan pengendali
    paling sederhana; optimasi tetap pekerjaan yang direncanakan.
(b) Paralel per blok dengan anggota tim lain di branch terpisah (lingkup sama dengan (a)). Tidak dipilih dalam jawaban,
    tetapi kompatibel dengan (a) bila anggota bergabung; integrasi dan verifikasi tetap di bawah aturan yang sama.
(c) Pertahankan ADR 0018 (tanpa Fase 8-9 sebelum batas waktu).

## Keputusan
Opsi (a), dipilih oleh Jevan, Team J5. ADR 0018 digantikan oleh catatan ini (header statusnya diperbarui; teksnya tidak
berubah).
1. Fase 5M mencakup S6, S7, S8, dan S9 (diedit 2026-10-03 atas permintaan tim, lihat catatan amandemen 3; teks aslinya
   berbunyi "Fase 5M berhenti setelah S6; S7, S8, dan S9 tidak dikerjakan sebelum batas waktu"). ADR 0017 tetap
   Accepted. Laporan Fase 5M ditulis setelah S8 dan vonisnya milik tim.
2. Fase 6 dilewati sebelum batas waktu (urutan operasi tetap yang sepele dipakai di pengendali), dicatat sebagai
   penyimpangan dari "persetujuan fase N sebelum N+1" di roadmap.
3. Urutan kerja (tiap blok: model acuan dulu, lint Verilator -Wall + slang, kedua simulator, uji bit-exact, bukti
   siklus konstan bila berlaku): Fase 7 Keccak K0 (SHA3-256/512, SHAKE128/256) -> sampler baseline (SampleNTT,
   SamplePolyCBD; tanpa optimasi streaming, dari aliran K0) -> encode/decode dan compress/decompress (tanpa
   pembagian) -> K-PKE KeyGen / Encrypt / Decrypt -> ML-KEM Encaps / Decaps dengan transformasi FO, pembandingan
   waktu konstan, dan implicit rejection -> vektor NIST ACVP terpatok.
4. Tingkat pelaporan (sebuah tingkat hanya diklaim bila evidence-nya ada di `evidence/`): T1 K0 dan sampler bit-exact;
   T2 K-PKE KeyGen / Encrypt / Decrypt bit-exact; T3 ML-KEM Encaps / Decaps penuh terhadap vektor ACVP dengan bukti
   siklus konstan. Tingkat yang tidak tercapai dinyatakan di proposal sebagai tidak selesai.
5. Peringanan proses, tanpa melemahkan pemeriksaan kebenaran apa pun: blok tanpa aturan adopsi memakai satu kompilasi
   Quartus (seed bawaan, diberi label kompilasi tunggal) sebagai ganti sapuan seed; bukti formal hanya di tempat yang
   murah dan sudah berpola; regresi Fase 0-5 penuh dijalankan sekali, pada pohon terintegrasi akhir, sesuai semangat
   Amandemen A1 test plan 5M. Lint, kedua simulator, bit-exact terhadap model acuan, dan pemeriksaan siklus konstan
   tidak dikurangi.
6. Bagian 3 proposal ditulis paralel hanya dari evidence repository, di bawah aturan klaim; tidak ada yang diklaim di
   luar tingkat yang tercapai; pembekuan evidence Rabu malam 2026-10-07.

## Konsekuensi
- Dua butir harus diputuskan tim sebelum pekerjaan pengendali mencapainya: PENDING #25 (pemeriksaan masukan FIPS 203
  di perangkat keras atau di HPS) dan PENDING #26 (protokol checkpoint: lebih sedikit STOP, lihat di bawah).
- Proposal menyatakan hasil terukur untuk NTT/INTT dan tingkat yang tercapai; optimasi (Fase 6, 8a, 8c, 8d) muncul
  hanya sebagai pekerjaan yang direncanakan; S6-S9 selesai dan muncul dengan hasil terukurnya (diedit 2026-10-03; teks
  aslinya mendaftar S7-S9 sebagai pekerjaan yang direncanakan).
- Bila kelebihan sumber daya muncul saat integrasi, itu menjadi keputusan tim (ADR), bukan perubahan diam-diam;
  anggaran 12.573 ALM tetap anggaran inti NTT (ADR 0009, 0012).

## Bukti
- `docs/decisions/adr/ADR-0017-*.md`, `ADR-0018-*.md`, `docs/ROADMAP.md` Fase 6-9, chat 2026-10-02.

## Catatan amandemen (2026-10-02, Jevan, Team J5; keputusan di atas tidak berubah)
(Digantikan catatan amandemen 2 dan 3: S7 dan S8 direncanakan lalu dikerjakan; kata-kata asli menyusul.) S7 dan S8 ADR
0017 disimpan sebagai pekerjaan cadangan, tidak dijadwalkan: tim boleh membukanya kembali hanya bila waktu tersisa
setelah tingkat T2 (K-PKE KeyGen / Encrypt / Decrypt bit-exact) tercapai, dan hanya lewat instruksi eksplisit baru.
Keduanya akan mulai dari C4b-B di branch `phase5m-memory-schedule` dan mengikuti pola S6 (test plan dan aturan adopsi
dulu, ADR 0012). Karena mengubah file memori dan inti, menggabungkannya setelah pekerjaan integrasi dimulai memerlukan
regresi Fase 0-5 penuh (Amandemen A1 test plan 5M) dan menjalankan ulang uji terintegrasi; selain itu keduanya tetap
tidak digabung sebagai pekerjaan mendatang. Tuas Fmax tanpa perubahan RTL (setelan kinerja Quartus, evidence Fase 4
`ghrd_plus_c3p6_integration.md`) diizinkan untuk kompilasi akhir sebagai hasil informasi, diberi label setelannya.

## Catatan amandemen 2 (2026-10-02, Jevan, Team J5; menggantikan kata "cadangan" di catatan amandemen 1, keputusan selebihnya tidak berubah)
Tim menyatakan S7 dan S8 akan dikerjakan di basis M6 (ADR 0020) sebelum pindah ke fase berikutnya. S7 dan S8 karena itu
direncanakan, bukan cadangan, dan datang sebelum Fase 7 (Keccak K0); S9 tetap dilepas (digantikan catatan 3: S9
dikerjakan). Dampak jadwal (ESTIMATE): sekitar 9-10 jam lagi sebelum Fase 7 mulai. Risiko batas waktu yang ditambahkan
ini milik tim; batas waktu usulan ada di test plan S7. Tingkat-tingkat catatan ini tercapai lebih lambat, atau tidak
sama sekali, sesuai itu.

## Catatan amandemen 3 (2026-10-03, Jevan, Team J5, chat: "s9 sekalian dikerjain" dan "tolong hapus/edit adr atau .md yang menyatakan s7-s9 tidak di implementasikan"; keputusan selebihnya tidak berubah)
S7, S8, dan S9 ADR 0017 semuanya dikerjakan (S9 sebagai studi hanya-dokumentasi yang didefinisikan ADR). Pernyataan di
catatan ini, di ADR 0020, dan di dokumen repository yang menyebut S7-S9 tidak dikerjakan, tidak dijadwalkan, atau
dilepas diedit di tempat atas permintaan tim, masing-masing dengan jejak berkurung tentang apa yang tertulis
sebelumnya. Hasil: S7 diadopsi aturan (ADR 0021, Proposed), S8 tidak diadopsi aturan (ADR 0023, Proposed), studi S9
(ADR 0022, Proposed). ADR 0018 (Superseded) dibiarkan: teksnya mencatat opsi yang ditolak dan bersifat historis.
Dampak jadwal yang ditulis di catatan 2 menjadi nyata; waktu yang dihabiskan ada di laporan Fase 5M.

## Catatan amandemen 4 (2026-10-03, Jevan, Team J5, chat: "fase 6 dulu aja"; menggantikan butir 2 saja: "Fase 6 dilewati")
Fase 6 dikerjakan berikutnya, sebelum Fase 7 (Keccak), dan S10 (ADR 0022 opsi A) di dalam Fase 6 sesudahnya. Dicatat di
ADR 0024 (Accepted). Sisa catatan ini tidak berubah.

## Catatan amandemen 5 (2026-10-03, Jose, Team J5, chat: "8a 8b 8c 8d dikerjakan , adr tolong diganti"; menggantikan pelewatan 8a, 8c, dan 8d di butir 2)
Langkah bagian 8a, 8b, 8c, dan 8d Fase 8 semuanya dikerjakan, berurutan menurut ROADMAP, masing-masing diukur dan
ditinjau sendiri. Dicatat di ADR 0026 (Accepted). Sisa catatan ini tidak berubah.
