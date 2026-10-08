# ADR 0034: Lingkup optimasi Fase 9M: jalur byte codec lebih lebar, seed 20 ns, inti hash K0, tumpang-tindih host-mesin; sampler kedua disimpan sebagai ide

- Status: Accepted
- Tanggal: 2026-10-04
- Diputuskan oleh: Faza Dzil (Team J5), chat 2026-10-04

## Konteks
Fase 9 (C7-core, `docs/results/phase09.md`, digabung di PR #9) menjalankan KeyGen, Encaps, dan Decaps ML-KEM-768 di RTL;
semua vektor ACVP terpatok lolos di simulasi. Jo menutup Fase 9; Faza Dzil mengambil alih optimasi dan perapihan
repository (chat 2026-10-04). Jo sempat menyatakan proposal berhenti di Fase 9; Fase 10-12 tetap tertunda (tanpa papan,
PENDING #8).
Profil siklus inti (`evidence/phase9m/profile.md`, MEASURED di simulasi) menunjukkan ke mana siklus pergi: mesin K-PKE
65-72 %, memuat polinomial ke mesin 0-23 %, menyimpannya 9-26 %, hash dan pembandingan sekitar 3 %. Memuat dan menyimpan
polinomial dengan d = 12 atau d = 10 dibatasi jalur satu-byte-per-siklus codec, bukan port satu-koefisien-per-siklus mesin.

## Opsi yang dipertimbangkan
Didaftar ke Faza Dzil di chat 2026-10-04 (penghematan ESTIMATE dari profil):
1. Jalur byte codec lebih lebar (dua byte per siklus): sekitar 9 % KeyGen, 6 % Encaps, 7 % Decaps; hanya file Fase 9
   yang berubah; sekitar satu hari kerja.
2. Inti pada batasan 20 ns: sudah terpenuhi di seed 1 (MC-20); seed 1-6 menjadikannya pengukuran penuh; tanpa perubahan RTL.
3. Sponge K0 untuk instans hash: sekitar 2.500 ALM lebih sedikit dengan sekitar 120 siklus lebih banyak per operasi;
   sebuah parameter (`HASH_C5`).
4. Tumpang-tindih muat dan simpan polinomial dengan mesin: hingga 25-32 % secara teori; memerlukan port host mesin
   bekerja saat mesin berjalan, yaitu varian baru dari file Fase 6-8 yang dibekukan; sekitar 2-4 hari kerja, risiko tinggi.
5. Sampler kedua untuk matriks A: sekitar 900 siklus; varian mesin baru dan sekitar 5.300 ALM lebih banyak; sekitar
   2-3 hari kerja, risiko tinggi.

## Keputusan
Faza Dzil, chat 2026-10-04: "kita kerjakan no 1 2 3 4 saja 5 kita simpan sebagai ide/solusi yang mungkin digunakan";
lalu "kerjakan 1 dulu kemudian stop dan lapor ke saya, parameter apa yang diukur, penggunaan resource dan seterusnya,
lakukan untuk semuanya; kita bikin branch baru fase 9m optimasi".
- Butir 1, 2, 3, dan 4 dikerjakan di Fase 9M (branch `phase9m-optimisation`), satu per satu, dimulai dari butir 1;
  setelah tiap butir ada laporan (parameter yang diukur, sumber daya, timing, siklus) dan STOP (seperti ADR 0032).
- Butir 5 (sampler kedua) disimpan sebagai ide untuk pekerjaan mendatang dan tidak diimplementasikan.
- Tiap butir punya test plan dan aturan adopsi sendiri yang ditulis sebelum RTL atau pengukurannya; adopsi sebuah hasil
  dicatat sebagai ADR Proposed untuk tim.

## Konsekuensi
- File Fase 9 hanya boleh berubah sebagai varian baru atau di balik parameter yang nilai bawaannya mempertahankan
  perilaku Fase 9; uji Fase 9 dijalankan ulang pada nilai bawaan (regresi). File Fase 6-8 yang dibekukan tidak diedit
  (butir 4 membuat varian baru).
- Pembekuan evidence adalah Rabu malam 2026-10-07; butir 4 (ESTIMATE 2-4 hari) mungkin tidak selesai pada saat itu.
  Yang belum selesai dan terverifikasi dilaporkan tidak selesai, tidak diklaim.
- Kotak Approval `docs/results/phase09.md` masih kosong (2026-10-04); tim yang mencentangnya.

## Bukti
`evidence/phase9m/profile.md`, `docs/results/phase09.md`,
`docs/decisions/adr/ADR-0033-phase-9-c7-core-as-built-ml-kem-768-in-simulation-acvp-100-p.md`.
