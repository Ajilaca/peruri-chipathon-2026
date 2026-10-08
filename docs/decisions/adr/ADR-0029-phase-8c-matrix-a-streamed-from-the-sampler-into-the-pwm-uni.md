# ADR 0029: Fase 8c: matriks A dialirkan dari sampler ke unit PWM (STREAM) diadopsi aturan atas penyimpanannya (STORE); hasil

- Status: Accepted
- Tanggal: 2026-10-03
- Diputuskan oleh: Jo, Team J5, chat 2026-10-03: "ya terima" (balasan atas usulan menerima C5, W2, STREAM, dan OVERLAP karena semuanya diadopsi aturannya dan terukur) (header sebelumnya "Proposed / menunggu keputusan tim")

## Konteks
- ADR 0026 (Accepted) mengirim langkah bagian 8c lebih dulu: matriks A dibangkitkan on the fly, tidak disimpan. Chat
  2026-10-03 (tanpa nama): kerjakan 8b, 8c, 8d tanpa berhenti.
- Test plan dan aturan adopsi ditulis sebelum RTL dan sebelum pengukuran apa pun: `evidence/phase08/8c/test_plan_8c.md`
  (di-commit bersama RTL; Amandemen A1 mendaftar apa yang berubah setelah run pertama). Kedua build memakai
  sequencer yang sama, inti S10 yang sama (ADR 0025, ketika itu Proposed), sampler 8b yang sama (W2, ADR 0028, ketika
  itu Proposed), dan sponge C5 (ADR 0027, ketika itu Proposed).
- STORE adalah baseline: sembilan entri disampel ke slot 0-8 (`SMPA` memblokir) dan lintasan PWM Fase 6 membacanya
  dari penyimpanan (24 slot). STREAM: beat sampler mengisi unit PWM langsung (`PWMS`); slot matriks tidak ada
  (12 slot).

## Opsi yang dipertimbangkan
(a) STORE: jalur perangkat keras baru lebih sedikit; sembilan polinomial disimpan.
(b) STREAM: tidak ada penyimpanan A, lintasan PWM berjalan pada kecepatan sampler.
(c) Mempertahankan antarmuka Fase 6 dengan A ditulis testbench: tidak ada sampler di sistem (bukan desain).

## Keputusan
Tidak diambil tim. Aturan yang ditetapkan sebelum mengukur memberi: STREAM diadopsi (keempat syarat terpenuhi). Tim
menerima atau menolak STREAM; 8d dibangun di atasnya.

## Konsekuensi
- Program K-PKE utuh dengan sampling bit-exact terhadap model acuan dan K-PKE acuan yang tidak diubah (KeyGen,
  Encrypt, Decrypt) di kedua simulator; counter 6/0/9, 3/4/12, 3/1/3 ditambah 6 dan 7 operasi sampling; Decrypt tidak
  berubah (3.109 siklus).
- MEASURED (simulasi, rata-rata atas masukan yang sama): KeyGen 7.089,1 siklus (STORE 8.268,1), Encrypt 8.548,6
  (STORE 9.727,6). MEASURED (Quartus, median atas seed 1-6): STREAM 10.995,5 ALM, 3.377-3.395 register, 44 M10K
  (STORE 10.958 ALM, 3.342-3.378 register, 55 M10K), 26 DSP keduanya, Fmax 43,355 MHz (STORE 42,270), timing terpenuhi
  pada 40 ns di setiap seed keduanya. t = siklus / Fmax: KeyGen 163,5 us lawan 195,6 us, Encrypt 197,2 lawan 230,1
  (INFERENCE / perhitungan tim: siklus simulasi dengan Fmax kompilasi kernel-only).
- Sebelas blok M10K lebih sedikit (penyimpanan memuat 12 slot sebagai ganti 24); ESTIMATE yang ditulis sebelum
  mengukur adalah 10-14 blok lebih sedikit dan sekitar 15 % siklus lebih sedikit: keduanya di dalam: 11 blok lebih
  sedikit, 14,3 % siklus KeyGen lebih sedikit dan 12,1 % siklus Encrypt lebih sedikit
  ((8.268,1 - 7.089,1) / 8.268,1 dan (9.727,6 - 8.548,6) / 9.727,6).
- Informasi pada 20 ns (seed 1): STREAM terpenuhi (setup +1,783 ns, 54,89 MHz), STORE terpenuhi (+0,992 ns,
  52,61 MHz); kernel-only, bukan sistem pada 50 MHz.
- Temuan: tag valid pipeline PWMS tidak punya reset (ditemukan run formal pertama, diperbaiki); konstanta `Q` inti
  sampler diganti nama menjadi `QC` untuk lint (catatan evidence 8b).
- Yang tidak ditunjukkan ini: tidak ada di perangkat keras; hash kunci dan seluruh KEM tidak ada di sistem; seed
  ditulis testbench.

## Bukti
- `evidence/phase08/8c/selection_worksheet.md` (tabel per seed dan aturan), `quartus_SMP0*.md`, `quartus_SMP1*.md`,
  `verify.md`, `formal.md`, `cycles_v0.json`, `cycles_v1.json`, `evidence/phase08/8c/test_plan_8c.md`.
