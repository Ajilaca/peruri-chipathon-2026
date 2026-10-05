# Keputusan terbuka

Daftar pilihan yang belum diputuskan tim. Tiap kali ada yang diputuskan, pindahkan ke ADR dan catat di bagian "Sudah diputuskan" di bawah.

## Masih terbuka

| No | Pertanyaan | Kenapa penting | Menghambat |
|---|---|---|---|
| 1 | Sisi target: akselerator untuk kartu (secure element) atau untuk reader? | Sumber menyebut bottleneck ada di chip kartu (RAM 8-12 KB), sedangkan HPS di DE10-Nano jauh lebih kuat dari chip kartu. Mengubah kata-kata Bagian 1-3 dan demo. | Fase 4; Bagian 3 proposal |
| 3 | Mekanisme transfer: DMA atau akses memori biasa | Satu polinomial hanya 3.072 bit, jadi setup DMA bisa lebih mahal dari penghematannya | Fase 3 (diputuskan lewat pengukuran) |
| 4 | Sumber keacakan untuk prototipe: HPS atau TRNG di FPGA | TRNG perlu validasi statistik sendiri; saat ini di luar lingkup | Fase 3 |
| 5 | Mode hibrida (ECDH klasik + ML-KEM di HPS): dimasukkan atau tidak? | BSI mewajibkan hibrida untuk produksi; menambah lingkup | Fase 6 |
| 6 | Baseline perangkat lunak kedua (misalnya soft core di fabric pada clock rendah) | Baseline Cortex-A9 bisa menunjukkan percepatan kecil atau negatif | Fase 5 |
| 7 | Alur pesan atau protokol yang diemulasi ("PQ-PACE" belum standar; ICAO masih menyusun) | Perlu untuk mendefinisikan latensi di tingkat protokol | Fase 4 |
| 8 | Ketersediaan papan: apakah DE10-Nano disediakan atau dimiliki? (`jtagconfig` tidak menemukan papan pada 2026-09-24; papan Cyclone III lama bukan target: tanpa HPS, hanya Quartus II 13.1) | Tanpa papan hanya ada bukti simulasi dan Quartus | Fase 3-5; Fase 10-12 |
| 10 | Perluasan penelusuran karya terdahulu (IEEE Xplore, IACR ePrint, Google Patents) | Perlu sebelum menulis klaim kebaruan di luar klaim terbatas yang ada | Sebelum pengumpulan |
| 12 | Apakah lampiran dihitung dalam batas 6 halaman? | Menentukan tempat gambar | Tata letak Bagian 3 |
| 13 | Mengaktifkan hook `rtl-agent-team` lewat `/rtl-agent-team:rat-init-project` (membuat `.rat/`)? Hambatan awal ("ide belum dipilih") sudah selesai lewat ADR 0001 | Gerbang Stop-nya mencegah sesi berakhir setelah edit RTL yang belum diverifikasi, jadi aturan verifikasi-dulu ditegakkan mesin; tetapi menambah struktur di repo | Sebelum Fase 1 |
| 33 | ADR 0033 (Fase 9, inti C7 apa adanya): terima inti ML-KEM-768 Fase 9 (semua vektor ACVP lolos di simulasi; 17.620,5 ALM, 54 blok RAM, 28 DSP, median 49,280 MHz, timing 40 ns terpenuhi di semua seed; KeyGen 9.035-9.076, Encaps 10.691, Decaps 16.623 siklus) dengan instans hash di sponge C5, atau di sponge K0 (sekitar 2.500 ALM lebih sedikit, 26 siklus per permutasi), dan putuskan apakah optimasi (encode / decode tumpang-tindih) diinginkan | Menentukan arsitektur untuk Bagian 3 proposal dan Fase 10 | Bagian 3, Fase 10 |

## Sudah diputuskan

Urut menurut tanggal. Isi lengkap tiap keputusan ada di file ADR-nya di `adr/`.

### 2026-09-29

| No | Keputusan | ADR | Oleh |
|---|---|---|---|
| 9 | Errata FIPS 203 diterima apa adanya | 0003 | Faza Dzil |
| 14 | Kriteria pemilihan jumlah lajur L: utama minimum siklus dalam anggaran 25 % ALM (10.478 ALM); sekunder cek ulang AT bila timing sudah valid | 0004 | Faza Dzil |

### 2026-09-30

| No | Keputusan | ADR | Oleh |
|---|---|---|---|
| 15 | Konfigurasi tambahan C2-K2-K1 dipakai untuk memilih L; L = 8 terpilih (9.754 ALM, dalam anggaran 10.478 ALM). Fase 4 mulai dari C2-K2-K1 pada L = 8 | 0005 | Faza Dzil |
| 16 | Target clock Fase 4 dua tingkat: 40,000 ns (25 MHz) sebagai target eksperimen, bukan syarat perangkat keras atau sistem; tujuan akhir 20,000 ns (50 MHz) setelah Fase 5, bukan gerbang Fase 4. Satu batasan yang sama untuk semua revisi Fase 4, termasuk P = 0 yang dikompilasi ulang | 0006 | Faza Dzil |
| 17 | Kedalaman pipeline P dan aturan seleksi: P dalam {0, 2, 4, 6}; register boleh di jalur akses memori dan pembagi; fungsi bit-exact; kandidat harus bit-exact, siklus konstan, ALM <= 10.478, dan memenuhi 40,000 ns. Pilih t_NTT = siklus_NTT / Fmax terkecil (Fmax slow corner terendah), P lebih kecil bila dalam 5 % dari minimum global. Tidak ada pemilihan otomatis bila tidak ada kandidat | 0007 | Faza Dzil |

### 2026-10-01

| No | Keputusan | ADR | Oleh |
|---|---|---|---|
| - | Pilihan akhir Fase 4 (ADR 0008 mengusulkan P = 4 pada anggaran 25 %, tidak pernah diterima): L = 8, P = 6 (C3-P6). Anggaran desain inti NTT 30 % = 12.573 ALM, menggantikan 25 % untuk inti NTT mulai Fase 4 (bukan batas tingkat sistem). Target ADR 0006 tidak berubah | 0009 | Faza Dzil |
| 18 | Target timing Fase 5: 50 MHz tetap target terbaik-upaya, bukan gerbang Fase 5. Ekspektasi ADR 0006 dikoreksi: jalur kritis C3-P6 ada di pembacaan memori (MEASURED). Pekerjaan memori / P / jadwal dipisah ke fase atau sub-fase sesudah 5a dan 5b (nama dan posisi: #19) | 0010 | Faza Dzil |
| 22 | Keputusan rencana Fase 5 D1 sampai D8 dan aturan seleksi 5b: 40 ns untuk revisi C4 dan kompilasi informasi 20 ns untuk C4 akhir dan C3-P6; anggaran 12.573 ALM, bawaan Quartus, DSP dilaporkan; 5c dan 5d setelah 5b; pembacaan (ii) untuk 5a; tidak ada pemindahan register di Fase 5; kontrak operand [0, q); seed 1 sampai 6 untuk 5b | 0011 | Faza Dzil |
| 20, 21 | Kenaikan siklus yang boleh dan batas ALM untuk register tambahan: siklus lebih banyak hanya bila t_NTT dan t_INTT pada Fmax terukur lebih baik dari C3-P6 dan siklus tetap konstan. Inti NTT <= 12.573 ALM tetap batas; melewatinya perlu keputusan tim baru | 0012 | Faza Dzil |

### 2026-10-02

| No | Keputusan | ADR | Oleh |
|---|---|---|---|
| 11 | Lisensi repositori: MIT (file `LICENSE`) | 0016 | Faza Dzil |
| 19 | Fase memori / jadwal: fase terpisah antara Fase 5 dan Fase 6 dengan nama kerja "Fase 5M", langkah S6 sampai S9; branch `phase5m-memory-schedule` | 0017 | Jevan |
| 23 | Fase 5b: Barrett menjadi reducer C4 (DSP naik 9 ke 18, dicatat) | 0013 | Jevan |
| 24 | Fase 5d tidak dicoba di Fase 5 dan pindah ke Fase 6 | 0015 | Jevan |

### 2026-10-03

| No | Keputusan | ADR | Oleh |
|---|---|---|---|
| 28 | S10 (16 bank 1R1W, P = 5, 118 siklus) menjadi inti NTT/INTT untuk fase berikutnya; top Fase 6 memakai S10. Kutipan chat: "kan udah di adaptasi dan kita menggambil s10" | 0025 | Jevan |
| 27 | Konfigurasi Fase 5M tidak lagi relevan setelah ADR 0025: ADR 0021 (S7), 0022 (studi S9), dan 0023 (S8) ditandai digantikan 0025 | 0021, 0022, 0023 | Jevan |
| - | Lingkup Fase 8: 8a, 8b, 8c, dan 8d semuanya dikerjakan (menggantikan penundaan 8a, 8c, 8d di ADR 0019 butir 2) | 0026 | Jose |
| 29 | C5 (Keccak dua ronde per siklus) diterima | 0027 | Jo |
| 30 | Sampler W2 diterima | 0028 | Jo |
| 31 | STREAM (matriks A dialirkan, tidak disimpan) diterima | 0029 | Jo |
| 32 | OVERLAP (sampling tumpang-tindih dengan transformasi) diterima | 0030 | Jo |
| 25 | Pemeriksaan masukan FIPS 203 dikerjakan HPS, bukan RTL, dan belum diuji di papan. Kutipan chat: "HPS untuk sekarang karena papan tidak ada aksesnya" | 0031 | Jo |
| 26 | Protokol checkpoint: satu STOP per blok; commit dibuat di akhir pekerjaan. Kutipan chat: "b" | 0032 | Jo |

Keputusan #29 sampai #32 diterima dengan chat "ya terima"; masing-masing lolos aturan adopsinya dan terukur (`docs/results/phase08.md`).

### 2026-10-05

| No | Keputusan | ADR | Oleh |
|---|---|---|---|
| 34 sampai 40 | Hasil Fase 9M diterima. Konfigurasi akhir K4 (`mlkem_core4`). ADR 0042 (K3) tidak diadopsi aturannya seperti tertulis, tetapi tim menerimanya | 0035, 0037, 0038, 0040, 0041, 0042, 0043 | Jo |
| 2 | Subtema yang dipilih: 02 Hardware Cryptography Accelerator (tertulis di README). Belum dicatat sebagai ADR | - | Jo |
