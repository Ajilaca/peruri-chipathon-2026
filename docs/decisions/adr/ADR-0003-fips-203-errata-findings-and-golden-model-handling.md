# ADR 0003: Temuan errata FIPS 203 dan penanganan model acuan

- Status: Accepted
- Tanggal: 2026-09-29
- Diputuskan oleh: Faza Dzil (Team J5), 2026-09-29, lewat instruksi sesi "accept adr3"

## Konteks

Butir #9 di `docs/decisions/PENDING.md` menghambat Fase 0: isi "planning note" FIPS 203 dari NIST
(bertanggal 2025-11-17, terlihat di halaman publikasi) tentang masalah yang akan dikoreksi belum dibaca.
Fase 0 mengharuskan penguncian `tb/golden/params.py` dan vektor KAT resmi sebelum pekerjaan RTL, dan proses
verifikasi mengharuskan errata dibaca sebelum vektor dikunci. ADR ini mencatat temuannya agar tim dapat
mengonfirmasi bahwa model acuan boleh jalan sesuai rencana.

## Opsi yang dipertimbangkan

1. Mengimplementasikan FIPS 203 persis seperti yang diterbitkan (13 Agustus 2024), dan memperlakukan dua item
   errata sebagai non-normatif. Biaya: tidak ada bila errata memang tidak mengubah apa pun yang bisa diuji; risikonya
   adalah pembaruan errata NIST di masa depan (belum terbit) menambah perubahan normatif yang perlu dicek ulang.
2. Menunggu NIST menerbitkan pembaruan atau revisi errata resmi sebelum menulis model acuan. Biaya: menghambat
   Fase 0 tanpa batas karena NIST tidak mengumumkan jadwal.
3. Menerapkan lebih dulu dua koreksi potensial seolah sudah final. Biaya: tidak perlu, karena NIST menyatakan
   keduanya bukan perubahan resmi dan tidak menambah persyaratan teknis; hanya menambah beban proses tanpa
   perbedaan perilaku.

Bukti: `evidence/phase00/fips203_errata.md` (kutipan lengkap, URL sumber, SHA-256 PDF dan spreadsheet errata yang
diambil, dan pemeriksaan silang parameter Tabel 2 untuk ML-KEM-768).

## Keputusan

Opsi 1: implementasi FIPS 203 persis seperti diterbitkan, tanpa penyimpangan akibat errata saat ini. Temuan:

- Spreadsheet "Potential Updates (Errata)" (diakses 2026-09-28 UTC) memuat 2 item, keduanya diberi label NIST
  sebagai klarifikasi atau koreksi salah ketik yang "DO NOT introduce new technical requirements" dan "ARE NOT
  official changes":
  1. Appendix A - menjelaskan mengapa tabel zeta memuat entri i=0 (nilai 1), yang dipakai Algoritma 9/10
     (NTT/NTT⁻¹) hanya untuk i=1..127. Tidak ada langkah algoritma yang berubah.
  2. Bagian 5.3, Algoritma 15, baris 7 - teks komentar menyebut "polynomial v" padahal seharusnya "polynomial w";
     badan algoritma sudah memakai `w` dengan benar. Perbaikan hanya pada komentar.
- Tidak satu pun item mengubah langkah algoritma, parameter, atau vektor uji. Tidak ada yang memengaruhi model
  acuan seperti direncanakan: NTT akan menghitung nilai zeta dari rumus BitRev_7 (bukan menyalin baris tabel
  Appendix A satu per satu), sehingga sudah sesuai dengan klarifikasi Appendix A untuk i=0 tanpa perubahan kode;
  K-PKE.Decrypt mengikuti badan algoritma (`w`), bukan komentar yang keliru.
- Nilai parameter ML-KEM-768 di Tabel 2 (Bagian 8) dibaca langsung dari PDF dan dicocokkan dengan nilai rencana
  `tb/golden/params.py`: k=3, η1=2, η2=2, du=10, dv=4 - cocok persis, tidak ada selisih. n=256 dan q=3329
  dikonfirmasi sebagai konstanta tetap. Ukuran di Tabel 3 (ek 1184 B, dk 2400 B, ct 1088 B, ss 32 B) juga cocok.

Diterima 2026-09-29 oleh Faza Dzil (Team J5). Pekerjaan model acuan Fase 0 (`tb/golden/params.py` dan model
acuan NTT/K-PKE, yang sudah ditulis berdasarkan teks FIPS 203 apa adanya tanpa menunggu NIST) dinyatakan sah
oleh keputusan ini.

## Konsekuensi

- Butir #9 di `docs/decisions/PENDING.md` ditutup oleh penerimaan ini.
- Tidak ada teks proposal, klaim, atau item roadmap yang perlu berubah: tidak ada parameter atau algoritma yang
  menyimpang dari FIPS 203 seperti diterbitkan.
- Bila NIST kelak menerbitkan pembaruan atau revisi errata resmi (di luar daftar "potential updates" ini),
  ADR ini harus ditinjau ulang dan, bila ada yang normatif berubah, digantikan oleh ADR baru.
- Pemicu cek ulang: baca ulang halaman publikasi FIPS 203 NIST sebelum mengunci kumpulan vektor KAT, kalau-kalau
  daftarnya bertambah sejak 2026-09-28.

## Bukti

- `evidence/phase00/fips203_errata.md` - MEASURED: URL sumber, tanggal akses, SHA-256 PDF FIPS 203 dan
  spreadsheet errata yang diambil, kutipan lengkap item errata dengan analisis dampak per item, dan pemeriksaan
  silang parameter Tabel 2 / Tabel 3.
