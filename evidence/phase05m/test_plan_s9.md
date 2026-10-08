<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Fase 5M, langkah S9: studi M10K / baca sinkron (hanya dokumentasi, tanpa RTL) - rencana

Ditulis 2026-10-03, sebelum skrip analisis ditulis atau dijalankan. Lingkup: ADR 0017 (S9 = "studi M10K / baca sinkron: hanya dokumentasi, tanpa RTL; kebutuhan port lawan M10K, opsi (lebih banyak bank 1R1W, dua
koefisien per word, double-pumping, perubahan jadwal), syarat evidence bebas konflik, ESTIMATE ALM / M10K berlabel; tim memilih; tanpa aturan adopsi"). ADR 0019 telah menghapus S9 demi
tenggat; ia dikerjakan sekarang karena tim memintanya di chat pada 2026-10-03 ("s9 sekalian dikerjain"); catatan amandemen 3 ADR 0019 mencatat hal itu. Label: MEASURED, INFERENCE, ESTIMATE, NOT MEASURED.

## 1. Pertanyaan yang dijawab studi
Q1. Apa yang dituntut jadwal NTT/INTT pada L = 8 dari setiap bank memori per siklus (baca, tulis, keduanya), dengan peta 8 bank saat ini dan dengan P dari S7?
Q2. Apakah itu muat dalam satu blok M10K (true dual port: dua operasi port per siklus; simple dual port: satu baca dan satu tulis)? Apa yang dibutuhkan bank 1R1W dari peta alamat?
Q3. Adakah peta bank dengan akses bebas konflik untuk setiap layer, kedua arah, dan setiap siklus (satu baca dan satu tulis per bank per siklus)? Diperiksa dengan enumerasi menyeluruh jadwal alamat nyata, bukan dengan argumen.
Q4. Untuk setiap opsi ADR 0017 (lebih banyak bank 1R1W, dua koefisien per word, double-pumping, perubahan jadwal): apa yang dibutuhkan, berapa biayanya (ESTIMATE dengan metode), apa yang harus dibuktikan sebelum RTL?

## 2. Metode (ditetapkan sebelum dijalankan)
- `scripts/test/phase5m_s9_port_analysis.py`: Python murni pada model yang ada `tb/mem/bank_model.py` (`addr_pair`, `lane_p`, `bank_of`, `build_maps`), tanpa RTL, tanpa Quartus; keluaran deterministik disimpan sebagai
  `evidence/phase05m/s9/port_analysis.txt`. Model timeline: layer k mengeluarkan satu butterfly per lajur per siklus selama 16 siklus; 16 alamat satu siklus dibaca pada siklus itu dan
  ditulis P siklus kemudian (P = 7, nilai S7, sebagai acuan tanpa stall); layer berurutan beruntun; kedua arah; semua 256 alamat.
- Pemeriksaan: (1) peta saat ini: baca, tulis, dan baca + tulis terburuk per bank per siklus; (2) peta 16 bank kandidat `bank = (a7^a3^a2^a1, a6, a5, a4)`, `offset = a[3:0]` (diturunkan dengan tangan dari struktur
  `addr_pair`, untuk dikonfirmasi atau dibantah oleh skrip): bijektif, seimbang (16 word per bank), paling banyak satu baca dan satu tulis per bank per siklus sepanjang timeline; (3) kontrol negatif yang harus
  konflik: `bank = a[7:4]` (tanpa XOR), `bank = a[3:0]`, dan peta 8 bank saat ini dipakai dengan 16 port pada satu akses per bank; (4) hitungan menyeluruh kegagalan bebas konflik untuk masing-masing.
- Angka sumber daya: hanya nilai MEASURED yang sudah ada di repository (file evidence Quartus) dan ESTIMATE yang metodenya ditulis di sebelahnya. Tidak ada run Quartus untuk S9 (tanpa RTL). Fakta perangkat Intel (kapasitas M10K,
  mode port, perilaku read-during-write, frekuensi maksimum) diambil dari sumber yang dikutip repository atau ditandai NOT VERIFIED di sini; tidak ada yang dikarang.

## 3. Keluaran dan aturan keputusan
`evidence/phase05m/s9/study_m10k.md` (opsi, syarat evidence, estimasi) dan sebuah ADR (Proposed) yang mendaftar opsi untuk tim. Tanpa aturan adopsi: tim memilih
(C5). S9 tidak mengubah RTL, jadi tidak perlu regresi. Bila analisis membantah peta turunan tangan, hal itu dilaporkan sebagai hasilnya.

## Amandemen A1 (2026-10-03, ditulis setelah run pertama skrip)
Run pertama membantah peta turunan tangan di bagian 2 (`bank = (a7^a3^a2^a1, a6, a5, a4)`): 384 sel (siklus, bank) dengan dua baca dan 384 dengan dua tulis di setiap arah, jumlah yang sama dengan kontrol
negatif `bank = a[7:4]`. Penyebab: turunan saya menaruh bit lajur butterfly (bit p 4..6) pada bit alamat 4..6 untuk setiap layer; bit itu jatuh pada bit k hanya bila k < log2len, selain itu pada bit k + 1. Turunan
yang dikoreksi (kandidat 2, `bank = (a1^a2^a3^a4, a7, a6, a5)`, `offset = a[3:0]`) diuji oleh skrip yang sama dalam bentuk yang sama; kedua hasil tetap ada di file evidence. Skrip juga mendapat pemeriksaan
opsi "dua koefisien per word" (bagian 4 keluarannya). Tidak ada kriteria atau ambang yang berubah.
