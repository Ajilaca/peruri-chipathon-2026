# ADR 0028: Fase 8b: sampler streaming, lebar keluaran W2 (dua koefisien per siklus) dipilih aturan atas W1; hasil

- Status: Accepted
- Tanggal: 2026-10-03
- Diputuskan oleh: Jo, Team J5, chat 2026-10-03: "ya terima" (balasan atas usulan menerima C5, W2, STREAM, dan OVERLAP karena semuanya diadopsi aturannya dan terukur) (header sebelumnya "Proposed / menunggu keputusan tim")

## Konteks
- ADR 0026 (Accepted) mengirim langkah bagian 8b lebih dulu: sampler yang mengambil aliran Keccak langsung ke SampleNTT
  dan CBD tanpa penyimpanan di antaranya. Chat 2026-10-03 (tanpa nama) meminta dua lebar keluaran, diuji berurutan:
  W1 (satu koefisien per siklus), lalu W2 (dua per siklus), lalu pilihan.
- Test plan dengan gerbang penerimaan (bagian 4) dan aturan W1-lawan-W2 (bagian 5) ditulis dan di-commit sebelum RTL
  dan pengukuran apa pun: `evidence/phase08/8b/test_plan_8b.md` (Amandemen A1 mencatat perubahan setelah run pertama:
  kriteria counter permutasi dan kontrol formal).
- Sponge C5 (ADR 0027, ketika itu Proposed; PENDING #29 terbuka) adalah inti top yang terukur; pembungkus juga
  menerima sponge K0 lewat parameter dan keduanya disimulasikan.

## Opsi yang dipertimbangkan
(a) W1, satu koefisien per siklus: antarmuka paling sederhana; batas bawah 256 siklus per polinomial.
(b) W2, dua koefisien per siklus: kolam hingga tiga kandidat dengan satu koefisien terbawa; 128 siklus per polinomial
    CBD, sekitar satu siklus per triple untuk SampleNTT.
(c) Tidak keduanya (pertahankan sampler berpenyangga): tidak dibangun; gerbang memerlukan M10K = 0, yang tidak bisa
    dipenuhi desain berpenyangga menurut konstruksi.

## Keputusan
Tidak diambil tim. Aturan yang ditetapkan sebelum mengukur memberi: kedua lebar lolos gerbang dan W2 dipilih (lolos
gerbang dan t = siklus / median Fmax lebih rendah dari W1 untuk SampleNTT dan untuk CBD). Tim menerima atau menolak W2
sebagai sampler 8b; sampai itu W2 adalah bawaan untuk 8c dan 8d (rencana 8c menyebutnya).

## Konsekuensi
- 8c dan 8d memakai sampler dengan `OUTW` = 2. W1 tetap di file yang sama (`OUTW` = 1, diverifikasi lagi setelah W2
  ditambahkan).
- Waktu sampling per polinomial MEASURED di simulasi: SampleNTT rata-rata 206,48 siklus (194-231) dan CBD 152 dengan
  sponge C5 (W1: 305,23 dan 280). Dengan W2 siklus SampleNTT sama dengan jumlah triple ditambah 49 (3 blok XOF) atau
  61 (4 blok) pada setiap dari 500 polinomial.
- Counter permutasi sponge bisa satu di atas hitungan acuan ketika jendela byte sampler sudah mengambil word terakhir
  blok akhir sementara keluaran ditahan (terlihat sekali dalam 500 kasus K0, W1): tidak berbahaya (hasilnya tidak
  pernah dibaca, sponge dihentikan dan dihapus); Amandemen A1 rencana.
- Yang tidak ditunjukkan ini: tidak ada di perangkat keras; sampler yang disembunyikan di balik pekerjaan lain adalah
  8d; kedua inti sponge adalah ADR 0027.

## Bukti
- `evidence/phase08/8b/selection_worksheet.md` (gerbang per lebar dan aturan), `quartus_SM1*.md`, `quartus_SM2*.md`
  (MEASURED, kernel-only, seed 1-6 masing-masing; seed 1 juga pada 20 ns dan dengan sponge K0 sebagai informasi),
  `verify_W1.md`, `verify_W2.md`, `formal_W1.md`, `formal_W2.md`, `sampler_cycles_W1.md`, `sampler_cycles_W2.md`.
- MEASURED (Quartus, median atas seed 1-6): W1 5.279 ALM, 1.913 register, M10K 0, DSP 0, Fmax 51,220 MHz
  (50,10-55,79); W2 5.290 ALM, 1.947 register, M10K 0, DSP 0, Fmax 50,220 MHz (48,46-53,42); timing terpenuhi pada
  40 ns di setiap seed keduanya; median S10 yang dipakai gerbang adalah 44,320 MHz (Fase 6).
- Meleset dari ESTIMATE yang ditulis sebelum mengukur (dicatat di rencana): ALM tambahan W2 diperkirakan 100-300 dan
  terukur sekitar +11 (median); top lebih kecil dari sponge 8a saja (6.167 ALM) karena sebab yang tidak diselidiki
  (INFERENCE: bit mode konstan dan resintesis ronde kedua berbeda antar kedua kompilasi); keduanya bukan cacat.
