# ADR 0016: Lisensi repositori: MIT

- Status: Accepted
- Tanggal: 2026-10-02
- Diputuskan oleh: Faza Dzil, Team J5 (chat 2026-10-02: "isi lisensi dengan MIT")

## Konteks
- PENDING #11: repositori bersifat publik (batasan C7); tanpa lisensi berlaku hak cipta bawaan dan penggunaan ulang
  tidak diizinkan.
- Ketua tim meminta pada 2026-10-02 agar lisensi diisi dengan MIT.

## Opsi yang dipertimbangkan
Hanya MIT yang disebut dalam permintaan; tidak ada lisensi alternatif yang dievaluasi.

## Keputusan
Repositori berlisensi MIT License (`LICENSE`). Baris hak cipta berbunyi "Team J5 (Institut Teknologi Bandung), CHIP 2026
Hackathon" (kata-kata dipilih asisten, dikoreksi tim bila diinginkan nama pemegang lain). Materi pihak ketiga yang
membawa lisensi sendiri (misalnya file GHRD Intel/Terasic bila dibawa, dan vektor uji yang diunduh) tetap memakai
lisensi itu; MIT berlaku untuk file milik tim sendiri.

## Konsekuensi
- Bagian lisensi di `README.md` diperbarui; butir #11 di `docs/decisions/PENDING.md` ditutup.
- Siapa pun boleh memakai ulang kode di bawah ketentuan MIT; tidak ada pemberian paten (MIT tidak punya).
- Teks proposal hanya boleh menyebut lisensi seperti tertulis di `LICENSE`.

## Bukti
- `LICENSE`; chat 2026-10-02 (Faza Dzil): "isi lisensi dengan MIT".
