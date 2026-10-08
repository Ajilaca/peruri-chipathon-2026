# ADR 0031: Fase 9: pemeriksaan masukan FIPS 203 dikerjakan HPS, bukan di RTL (belum ada akses papan)

- Status: Accepted
- Tanggal: 2026-10-03
- Diputuskan oleh: Jo, Team J5, chat 2026-10-03: "HPS untuk sekarang karena papan tidak ada aksesnya" (balasan atas saran: di HPS, dengan catatan tidak diuji di papan)

## Konteks
- `docs/ROADMAP.md` Fase 9 butir 2 memerlukan keputusan sebelum fase dimulai: pemeriksaan masukan FIPS 203
  (pemeriksaan kunci enkapsulasi, pemeriksaan masukan dekapsulasi) berjalan di perangkat keras atau di HPS. PENDING #25
  (saran di daftar pending: di HPS untuk lingkup batas waktu).
- Tidak ada DE10-Nano yang dapat diakses tim (PENDING #8 terbuka; `jtagconfig` tidak menemukan papan pada 2026-09-24;
  chat 2026-10-03: tim tidak punya akses papan). HPS tidak dapat dijalankan, jadi apa pun yang ditaruh di HPS tetap
  tidak diuji di papan.
- Model acuan sudah punya kedua pemeriksaan sebagai fungsi perangkat lunak: `check_encapsulation_key` dan
  `check_decapsulation_input` di `tb/golden/mlkem.py`.
- Batas waktu 2026-10-08 (pembekuan evidence malam 2026-10-07); tingkat ADR 0019: T3 tidak dijamin.

## Opsi yang dipertimbangkan
(a) Pemeriksaan di RTL (perangkat keras): menambah RTL (encode ulang dan bandingkan kunci, hash kunci rahasia,
    pemeriksaan panjang) dan grup key-check ACVP (10 + 10) ke run vektor Fase 9; area lebih besar dan pekerjaan
    verifikasi lebih banyak sebelum batas waktu; dapat diuji di simulasi.
(b) Pemeriksaan di HPS (perangkat lunak): tanpa RTL; akselerator mengasumsikan masukan lolos pemeriksaan; fungsi
    perangkat lunak ada di model acuan; tidak dapat dijalankan di HPS tanpa papan.

## Keputusan
(b). Pemeriksaan masukan FIPS 203 dikerjakan HPS (perangkat lunak), bukan di RTL, untuk sekarang. Chat 2026-10-03 (Jo,
Team J5): "HPS untuk sekarang karena papan tidak ada aksesnya". Kata "untuk sekarang" milik tim: pertanyaan dapat
dibuka kembali bila papan tersedia atau waktu tersisa.

## Konsekuensi
- Fase 9 (C7-core) tidak punya RTL key-check. Run vektor mencakup grup ACVP keyGen, encapsulation, dan decapsulation
  (decapsulation dengan ciphertext yang diubah termasuk); grup key-check (10 + 10) tidak dijalankan terhadap RTL.
  Apakah dijalankan terhadap fungsi perangkat lunak model acuan adalah langkah terpisah dan opsional dan harus diberi
  label hanya perangkat lunak.
- Inti RTL menyatakan asumsi di spesifikasinya: pemanggil (HPS) sudah memeriksa masukan. Proposal tidak boleh
  mengatakan bahwa perangkat keras melakukan pemeriksaan masukan FIPS 203.
- TIDAK diuji di papan: pemeriksaan sisi HPS tetap niat desain sampai Fase 10 (terhambat PENDING #8). Tidak ada klaim
  validasi perangkat keras (C8). Implicit rejection Decaps (FO) tetap di RTL dan menjadi bagian Fase 9.
- Bukti siklus konstan untuk Decaps tidak terpengaruh (ciphertext valid dan diubah, kunci rahasia berbeda).
- Bila papan tidak pernah tersedia, proposal menggambarkan pemeriksaan HPS sebagai langkah perangkat lunak yang
  direncanakan, dengan fungsi model acuan sebagai acuan.

## Bukti
- `docs/ROADMAP.md` Fase 9 butir 2 dan 3; `docs/decisions/PENDING.md` #25 dan #8; `tb/golden/mlkem.py` (kedua fungsi
  pemeriksaan); ADR 0019 (tingkat, batas waktu).
- Tidak ada pengukuran dalam keputusan ini.
