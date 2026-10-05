# FIPS 203 — sumber, integritas berkas, dan errata (diakses 2026-09-28 UTC)

## Sumber

| Berkas | URL | Diakses (UTC) | SHA-256 |
|---|---|---|---|
| FIPS 203 final PDF | https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf (DOI 10.6028/NIST.FIPS.203) | 2026-09-28 | `fe1f12f32a7e44ec9fdebbf400cda843a40b506dee676725234dc6f7923b6cac` |
| Errata "Potential updates" (xlsx) | https://csrc.nist.gov/files/pubs/fips/203/final/docs/fips-203-potential-updates.xlsx | 2026-09-28 | `edf899c89762449f43d7713883caeefc2e4ae9ae98d5a76b339547db22cb3ac7` |
| Halaman publikasi | https://csrc.nist.gov/pubs/fips/203/final | 2026-09-28 | — |

Tanggal terbit dokumen (dari halaman & PDF): **13 Agustus 2024**. Catatan perencanaan di
halaman publikasi ("issue that will be corrected in a future update/revision"): tertanggal
**17 November 2025**.

**Kedua berkas TIDAK di-commit ke repo** (sesuai instruksi); hanya hash dan isi yang
diekstrak dicatat di sini. Berkas sumber berada di scratchpad sesi lokal, bukan di repo.

## Isi spreadsheet errata ("Potential Updates")

Spreadsheet berjudul "Potential Updates (Errata)" untuk NIST FIPS 203 (dirilis 13 Agustus
2024) berisi disclaimer berikut (dikutip dari sheet):
> "These errors were overlooked during the NIST review process... Potential corrections
> attempt to remove ambiguity and improve interpretation of the document. Potential
> corrections DO NOT introduce new technical requirements. Potential corrections ARE NOT
> official changes, but may be corrected in a future errata update of the publication."

Per 2026-09-28, spreadsheet berisi **2 butir**:

### Butir 1 — Appendix A, diidentifikasi 2025-03-31

- **Lokasi:** Appendix A.
- **Teks masalah (dikutip):** "Algorithms 9 and 10 use the zeta values for i = 1, …, 127,
  however Appendix A also includes the value 1 (corresponding to i = 0)."
- **Koreksi potensial (dikutip):** "After the first two sentences of Appendix A, a new
  sentence will be added: 'The value 1, corresponding to i = 0, has been included so that
  i-th entry of the array would then equal 𝜁^BitRev_7(i).'"
- **Memengaruhi model golden kita? TIDAK.**
  **Alasan:** Ini adalah klarifikasi tekstual tentang mengapa tabel zeta di Appendix A
  memuat entri i=0 (bernilai 1), padahal Algoritma 9/10 (NTT/NTT⁻¹) hanya memakai i=1..127.
  Tidak ada langkah algoritma yang berubah. Jika golden model kita menghitung nilai zeta
  langsung dari rumus 𝜁^BitRev_7(i) (bukan menyalin tabel Appendix A baris demi baris),
  entri i=0 otomatis bernilai 𝜁^0 = 1 dan konsisten dengan koreksi ini tanpa perubahan kode.

### Butir 2 — Section 5.3, Algorithm 15, diidentifikasi 2025-10-17

- **Lokasi:** Section 5.3, Algorithm 15 (K-PKE.Decrypt), baris 7.
- **Teks masalah (dikutip):** "In Algorithm 15, line 7, the comment reads 'decode
  plaintext m from polynomial v.' However, v is not used in the algorithm."
- **Koreksi potensial (dikutip):** "The comment will be changed to read 'decode plaintext
  m from polynomial w.'"
- **Memengaruhi model golden kita? TIDAK.**
  **Alasan:** Ini adalah koreksi komentar/anotasi pseudokode di Algorithm 15, bukan
  perubahan langkah algoritma itu sendiri. Variabel yang benar-benar dipakai pada baris
  itu (yang didekode menjadi m) sudah bernama `w` di badan algoritma; hanya teks komentar
  yang salah menyebut `v`. Implementasi golden model yang mengikuti badan algoritma (bukan
  komentarnya) sudah benar tanpa perubahan.

**Kesimpulan errata:** 2/2 butir bersifat klarifikasi/typo redaksional, tidak mengubah
langkah algoritma atau parameter. Tidak ada yang memaksa penyimpangan dari implementasi
literal standar. Tidak ditemukan butir yang berpotensi mengubah vektor KAT.

## Konfirmasi parameter (Tabel 2, Section 8, FIPS 203)

Dikutip langsung dari Table 2 "Approved parameter sets for ML-KEM" di PDF (halaman 48):

| Parameter set | n | q | k | η1 | η2 | du | dv | RBG strength (bits) |
|---|---|---|---|---|---|---|---|---|
| ML-KEM-512 | 256 | 3329 | 2 | 3 | 2 | 10 | 4 | 128 |
| **ML-KEM-768** | **256** | **3329** | **3** | **2** | **2** | **10** | **4** | **192** |
| ML-KEM-1024 | 256 | 3329 | 4 | 2 | 2 | 11 | 5 | 256 |

**Hasil perbandingan dengan rencana `tb/golden` (k=3, η1=2, η2=2, du=10, dv=4):
COCOK — tidak ada perbedaan.** Tidak perlu berhenti/lapor sesuai instruksi butir 5.

Ukuran kunci/ciphertext (Table 3, halaman 48) untuk ML-KEM-768: encapsulation key 1184 B,
decapsulation key 2400 B, ciphertext 1088 B, shared secret key 32 B — cocok dengan nilai
`EK_BYTES DK_BYTES CT_BYTES SS_BYTES` yang direncanakan di `CLAUDE.md`/`SKILL.md`.

n=256 dan q=3329 dikonfirmasi sebagai konstanta tetap (bukan per-parameter-set), sesuai
Section 8: "There are also two constants: n = 256 and q = 3329."
