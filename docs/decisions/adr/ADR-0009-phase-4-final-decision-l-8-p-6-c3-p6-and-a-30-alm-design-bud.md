# ADR 0009: Keputusan akhir Fase 4: L = 8, P = 6 (C3-P6) dan anggaran desain ALM 30 % untuk inti NTT

- Status: Accepted
- Tanggal: 2026-10-01
- Diputuskan oleh: Faza Dzil, Team J5

## Konteks
- ADR 0004 (Accepted 2026-09-29) menetapkan anggaran ALM 25 % dari device (10.478 ALM) untuk pemilihan jumlah
  lajur. Tinjauan 2026-10-01 menemukan bahwa 25 % adalah anggaran desain yang dipilih sendiri, bukan persyaratan
  terdokumentasi: angka itu masuk sebagai contoh ("misal 25%") dalam pertanyaan yang menghasilkan ADR 0004, dan
  belum ada estimasi isi fabric lainnya saat itu.
- ADR 0007 (Accepted) menetapkan kedalaman kandidat Fase 4, syarat kandidat (dengan "ALM <= 10.478") dan aturan
  seleksi. ADR 0008 (Proposed, tidak pernah diterima) menerapkan aturan itu dengan anggaran 25 % dan mengusulkan
  P = 4.
- Bukti yang dikumpulkan setelah ADR 0008 (semuanya di `evidence/phase04/`, MEASURED kecuali ditandai):
  - sapuan seed, seed 1-6 (`seed_sweep.md`): P = 6 memakai 10.484-10.516 ALM dan melewati 10.478 di setiap seed;
    P = 4 memakai 10.439-10.503 ALM dan dalam 10.478 di 4 dari 6 seed; kedua belas kompilasi memenuhi 40,000 ns;
    Fmax slow-corner terendah P = 4 30,60-33,00 MHz, P = 6 32,60-34,20 MHz;
  - shell GHRD DE10-Nano saja (`ghrd_shell_measured.md`): 1.304-1.309 ALM, 35 M10K, 0 DSP; blok keras HPS memakai
    0 ALM fabric;
  - GHRD + C3-P4 dalam satu kompilasi (`ghrd_plus_c3p4_integration.md`): 12.754 ALM; delta integrasi +18 ALM
    terhadap bagian mandiri yang dikompilasi dengan setelan sama; 40,000 ns terpenuhi; kesulitan packing Rendah;
    interkoneksi puncak 48,2 %. Ini bukti integrasi dengan P = 4 sebagai baseline; P = 6 + GHRD tidak dikompilasi.
  - draf isi fabric (`fabric_estimate_DRAFT.md`, ESTIMATE, keyakinan rendah).

## Opsi yang dipertimbangkan
1. Mempertahankan 25 % dan menerima ADR 0008 (P = 4). P = 4 dalam anggaran hanya di 4 dari 6 seed; pembagian
   P = 4 / P = 6 bertumpu pada beberapa puluh ALM, dalam derau fitter.
2. Menaikkan anggaran desain inti NTT menjadi 30 % (12.573 ALM) dan memilih dengan aturan ADR 0007. Baik P = 4
   maupun P = 6 dalam anggaran di setiap seed yang diukur (margin ≥ 2.057 ALM).
3. Anggaran lebih besar (35-40 %). Tidak ada P tambahan yang menjadi kandidat; hanya ruang untuk fase berikutnya
   yang berubah, dan tidak ada estimasi yang mendukung angka lebih besar tertentu.

## Keputusan
1. Anggaran desain: 30 % ALM device untuk inti NTT = 12.573 ALM (41.910 x 0,30, penyebut fitter), memakai angka
   "Logic utilization (ALMs needed)" fitter seperti di Fase 4. Ini menggantikan nilai 25 % ADR 0004 untuk inti NTT
   mulai Fase 4. Ini anggaran desain untuk inti NTT, bukan batas untuk sistem akhir, dan tidak menyatakan bahwa 70 %
   sisanya cukup untuk bagian ML-KEM lainnya.
2. Konfigurasi terpilih: L = 8 lajur, kedalaman pipeline P = 6, implementasi C3-P6
   (`rtl/ntt/ntt_core_c3_p6.sv`, revisi Quartus `C3-P6`). Fase 5 mulai dari C3-P6.
3. Target timing tidak berubah (ADR 0006): milestone Fase 4 40,000 ns (25 MHz, target eksperimen, dipenuhi oleh
   C3-P6); target Fase 5 20,000 ns (50 MHz, belum dipenuhi).

Pemeriksaan terhadap aturan ADR 0007 dengan anggaran 30 % (perhitungan tim dari `selection_worksheet.md` dan
`seed_sweep.md`): pada seed bawaan kandidatnya {4, 6}; t_NTT(6) = 3,481 µs adalah minimum dan
d(4) = 0,051 > 0,05, jadi aturan memilih P = 6. Dinyatakan terus terang: di seed 1-6 aturan yang sama memilih P = 6
di seed 1, 4, 5 dan P = 4 di seed 2, 3, 6 (keduanya dekat garis seri 5 %). Pilihan tim P = 6 konsisten dengan aturan
pada seed bawaan yang dipakai untuk semua revisi terukur; tidak diklaim bebas dari seed.

## Hubungan dengan ADR sebelumnya (tidak ada yang ditulis ulang)
- ADR 0004: nilai 25 %-nya digantikan untuk inti NTT mulai Fase 4 oleh ADR ini; teks ADR 0004 dan keputusan Fase 3
  yang diambil di bawahnya (ADR 0005, L = 8) tetap seperti tercatat.
- ADR 0007: aturan, himpunan kandidat, dan syarat tidak berubah kecuali syarat 3 kini berbunyi "ALM <= 12.573".
- ADR 0008: Proposed, tidak diterima; digantikan oleh ADR ini. Pengukurannya tetap bukti yang valid.
- ADR 0006: tidak berubah.

## Konsekuensi
- Margin terukur C3-P6 ke 12.573 ALM: 2.057-2.089 ALM (seed 1-6).
- Sumber daya tingkat sistem belum tuntas: P = 6 + GHRD belum dikompilasi; Keccak, sampler, pengendali KEM,
  encode/compress, penyimpanan, jembatan, dan SignalTap belum diukur. Angka integrasi di atas memakai P = 4.
- Setelan kompilasi berpengaruh: setelan global GHRD menaikkan C3-P4 dari 10.439 menjadi 11.432 ALM (MEASURED). Di
  bawah setelan itu C3-P6 belum diukur; build sistem mungkin memerlukan pemeriksaan anggaran sendiri.
- Fase 5 (aritmetika) harus menjaga C3-P6 dalam 12.573 ALM atau mencatat keputusan baru.

## Bukti
- `evidence/phase04/selection_worksheet.md`, `seed_sweep.md`,
  `quartus_C3-P6.md`, `seed_sweep/quartus_C3-P6-s{2..6}.md`
- `evidence/phase04/ghrd_shell_measured.md`, `quartus_GHRD-de10-nano-base.md`,
  `ghrd_plus_c3p4_integration.md`, `fabric_estimate_DRAFT.md`
- `docs/decisions/adr/ADR-0004-*.md`, `ADR-0006-*.md`, `ADR-0007-*.md`, `ADR-0008-*.md`; `docs/results/phase04.md`
