# ADR 0030: Fase 8d: sampling noise ditumpangkan dengan transformasi (OVERLAP) diadopsi aturan atas STREAM; hasil

- Status: Accepted
- Tanggal: 2026-10-03
- Diputuskan oleh: Jo, Team J5, chat 2026-10-03: "ya terima" (balasan atas usulan menerima C5, W2, STREAM, dan OVERLAP karena semuanya diadopsi aturannya dan terukur) (header sebelumnya "Proposed / menunggu keputusan tim")

## Konteks
- ADR 0026 (Accepted) mengirim langkah bagian 8d lebih dulu: tumpang-tindih sampler dengan aritmetika. Chat 2026-10-03
  (tanpa nama): kerjakan 8b, 8c, 8d tanpa berhenti.
- Test plan dan aturan: `evidence/phase08/8d/test_plan_8d.md` (ditulis sebelum jalur RTL dijalankan dan sebelum
  pengukuran 8d apa pun; Amandemen A1 mencatat temuan). Baseline: STREAM (ADR 0029, ketika itu Proposed). Perubahannya:
  satu polinomial noise disampel tanpa memblokir selagi transformasi menghitung, beat-nya ditulis saat port tulis
  penyimpanan bebas, dan sequencer punya prioritas di port itu (`OVERLAP` = 1, himpunan program OVERLAP).
- Matriks tetap dialirkan (`PWMS` memerlukan sampler), jadi sampling matriks dan noise berurutan: satu sampler.

## Opsi yang dipertimbangkan
(a) STREAM seperti adanya: kendali lebih sederhana; sampler menganggur saat inti NTT berjalan.
(b) OVERLAP: lima dari enam (KeyGen) dan enam dari tujuh (Encrypt) polinomial noise tersembunyi di balik transformasi.
(c) Sampler kedua (untuk menyembunyikan matriks juga): tidak dibangun; biaya tidak diestimasi.

## Keputusan
Tidak diambil tim. Aturan yang ditetapkan sebelum mengukur memberi: OVERLAP diadopsi (keempat syarat terpenuhi). Tim
menerima atau menolaknya.

## Konsekuensi
- Bit-exact terhadap model dan K-PKE acuan yang tidak diubah di kedua simulator, pada program OVERLAP dan pada
  program STRESS khusus uji (sampel noise bertabrakan dengan lintasan ADD; 763 siklus beat sampler ditahan oleh
  penulisan sequencer pada run akhir, jadi arbitrasi teruji; kontrol NC-ARB gagal sesuai syarat).
- MEASURED (simulasi, rata-rata atas masukan yang sama): KeyGen 6.344,1 siklus (STREAM 7.089,1), Encrypt 7.654,6
  (STREAM 8.548,6): 10,5 % dan 10,5 % lebih sedikit ((7.089,1 - 6.344,1) / 7.089,1 dan (8.548,6 - 7.654,6) / 8.548,6),
  terhadap ESTIMATE sekitar 11 %; Decrypt tidak berubah (3.109). MEASURED (Quartus, median atas seed 1-6): OVERLAP
  10.992,5 ALM (STREAM 10.995,5), 3.368-3.414 register, 44 M10K (sama), 26 DSP, Fmax 43,755 MHz (STREAM 43,355),
  timing terpenuhi pada 40 ns di setiap seed. t = siklus / Fmax: KeyGen 145,0 us lawan 163,5 us, Encrypt 174,9 lawan
  197,2 (INFERENCE / perhitungan tim).
- Perbandingan program utuh dengan Fase 6 (hanya aritmetika, masukan diberikan): KeyGen 5.475 -> 6.344 siklus dengan
  semua sampling matriks dan noise termasuk; Encrypt 6.789 -> 7.655; Decrypt 3.109 tidak berubah.
- Informasi pada 20 ns (seed 1): OVERLAP terpenuhi (setup +1,535 ns, 54,16 MHz); kernel-only.
- Temuan langkah ini: start sampler pada siklus yang sama dengan pulsa `done` sampel sebelumnya menghapus penanda
  PWMS (program macet), hanya ditemukan oleh program STRESS; diperbaiki (cabang done kini mendahului cabang start).
- Batas: operasi WAIT adalah properti keselamatan jadwal (transformasi yang ditumpangkan lebih panjang dari sampel
  noise, jadi mengabaikannya tidak mengubah hasil); pemeriksa hazard statis model acuan menjaganya. Hanya satu
  sampler. Tidak ada di perangkat keras.

## Bukti
- `evidence/phase08/8d/selection_worksheet.md`, `quartus_SMP2*.md`, `formal.md`, `cycles_v2.json`,
  `cycles_v3_stress.json`, `evidence/phase08/8c/verify.md` (satu run yang mencakup 8c dan 8d), `test_plan_8d.md`.
