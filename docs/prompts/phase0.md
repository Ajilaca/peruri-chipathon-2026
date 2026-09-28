<!-- claim-lint: skip-file (prompt pack; illustrative numbers) -->
# Prompt pack — Fase 0 (Foundations): golden model ML-KEM-768 + KAT resmi

Fase 0 dari `docs/ROADMAP.md`. Hasil akhirnya: `docs/results/result_phase0.md`.
Sumber uji resmi dan versi yang sudah diverifikasi: `.claude/skills/mlkem-guard/reference/kat_sources.md`.

## Cara memakai
1. Dari root repo: `git switch -c phase0-golden-model` lalu buka `claude`. `CLAUDE.md` dimuat otomatis; prompt di
   bawah tidak mengulang aturannya.
2. Jalankan prompt **berurutan, satu per satu**. Setelah masing-masing: baca ringkasannya, `git diff`, jalankan
   perintah verifikasi yang disebutnya sendiri. Baru lanjut. Bila konteks sudah panjang, mulai sesi baru: semua
   status ada di file, bukan di ingatan sesi.
3. Jangan `git push` dari sesi ini. Jangan centang kotak Approval di result artifact: itu tugas anggota tim.
4. Bila Claude Code berhenti dan bertanya, itu disengaja. Jawab; jangan suruh ia menebak.

Aturan yang berlaku di semua prompt: tidak mengubah parameter matematika; tidak melemahkan tes, toleransi,
atau perbandingan agar hasil hijau; tidak mengarang vektor, angka, atau isi dokumen NIST; bila sesuatu tidak bisa
diambil (jaringan, izin, file), berhenti dan laporkan URL persisnya.

---

## Prompt 0 — Orientasi (hanya membaca)
```
Baca CLAUDE.md, docs/PROJECT_BRIEF.md, docs/ROADMAP.md (Fase 0), docs/decisions/PENDING.md, dan
.claude/skills/mlkem-guard/SKILL.md beserta reference/kat_sources.md.

Jalankan /phase-gate untuk Fase 0 (status saat ini) tanpa menulis kode apa pun.

Laporkan dalam bahasa Indonesia, ringkas:
1. Kriteria selesai Fase 0 dan status tiap kriteria saat ini (semua seharusnya MISSING).
2. Keputusan di PENDING.md yang memblokir Fase 0 (jawab jujur; saya perkirakan hanya #9 errata FIPS 203).
3. Rencana langkah Fase 0 menurut prompt pack ini, dan risikonya.
4. Apa yang tidak bisa Anda verifikasi dari dalam sesi ini.
Berhenti setelah laporan. Jangan membuat file.
```

## Prompt 1 — Spesifikasi FIPS 203 dan errata
```
Tujuan: memastikan kita mengimplementasikan versi standar yang benar, dan mengetahui isu yang diakui NIST.

1. Ambil FIPS 203 final dari https://csrc.nist.gov/pubs/fips/203/final (DOI 10.6028/NIST.FIPS.203). Catat sha256
   PDF dan tanggal akses. Jangan commit PDF-nya.
2. Di halaman itu ada catatan perencanaan (17 Nov 2025) tentang isu yang akan dikoreksi, dengan tautan
   "Errata (potential updates)" di bagian Documentation. Ambil dan baca spreadsheet itu.
3. Tulis docs/evidence/golden/fips203_errata_<tanggal-UTC>.md berisi: setiap butir errata (nomor/ID, bagian standar,
   teks asli dikutip singkat), dan untuk tiap butir: "memengaruhi model golden kita? ya / tidak / belum jelas" beserta
   alasannya dari teks standar. Jangan menafsirkan lebih jauh dari teks.
4. Buat ADR dengan status Proposed lewat /decision-record: "FIPS 203 errata findings and golden-model handling".
   Jangan mengimplementasikan penyimpangan dari standar atas dasar errata tanpa keputusan tim.
5. Konfirmasi dari teks FIPS 203 (Tabel parameter ML-KEM-768) nilai k, eta1, eta2, du, dv. Catat hasilnya di file
   errata di atas (bagian "konfirmasi parameter"). Bila ada yang berbeda dari tb/golden yang direncanakan
   (k=3, eta1=2, eta2=2, du=10, dv=4), berhenti dan laporkan.

Bila spreadsheet atau PDF tidak bisa diunduh: berhenti, berikan URL dan minta saya mengunduhnya manual.
Berhenti setelah selesai dan ringkas temuannya (jumlah butir errata, mana yang memengaruhi).
```

## Prompt 2 — Konstanta dan primitif (NTT, sampling, encode, compress)
```
Tujuan: tb/golden/ berisi model acuan Python murni (stdlib saja; hashlib untuk SHA3/SHAKE) yang mentranskripsikan
FIPS 203 apa adanya. Baca algoritmanya dari PDF; tulis nomor algoritma dan bagian standar di komentar tiap fungsi.

Berkas:
- tb/golden/params.py: persis nama Q N ZETA K ETA1 ETA2 DU DV EK_BYTES DK_BYTES CT_BYTES SS_BYTES (ML-KEM-768 saja;
  jangan menambah 512/1024). Jalankan .claude/skills/mlkem-guard/scripts/check_params.py sampai lulus.
- tb/golden/primitives.py: ntt, intt (7 lapis, "tidak lengkap": len 128 turun ke 2), multiply_ntts,
  base_case_multiply, sample_ntt, sample_poly_cbd, byte_encode, byte_decode, compress, decompress, serta pembungkus
  hash/XOF (G, H, J, PRF, XOF) di atas hashlib. Tabel zeta HITUNG dari ZETA=17 dengan urutan bit-reversal seperti
  standar, jangan menempel konstanta dari ingatan.
  Setiap fungsi berdiri sendiri dan bisa dipanggil terpisah: fase RTL nanti membandingkan blok satu per satu.
- tb/golden/tests/test_primitives.py (pytest) dengan uji SIFAT yang tidak bergantung pada KAT:
  a. intt(ntt(f)) == f untuk banyak f acak.
  b. hasil kali di domain NTT == perkalian sekolah negacyclic modulo (X^256+1, q) untuk banyak pasangan acak.
  c. instrumentasi: NTT memakai tepat 7 lapis dengan panjang blok 128,64,32,16,8,4,2 (dokumentasi "incomplete NTT").
  d. byte_decode(byte_encode(f)) == f untuk setiap d yang dipakai standar.
  e. compress/decompress: galat maksimum sesuai batas yang dinyatakan teks FIPS 203 (kutip bagiannya).
  f. sample_poly_cbd: semua koefisien dalam [-eta, eta] (mod q) dan panjang masukan sesuai standar.

Jalankan pytest. Jangan lanjut bila ada yang gagal; perbaiki modelnya, bukan tesnya. Berhenti setelah semua lulus dan
laporkan: berapa tes, apa saja yang tercakup, dan apa yang belum.
```

## Prompt 3 — K-PKE dan ML-KEM tingkat atas
```
Tujuan: tb/golden/kpke.py dan tb/golden/mlkem.py.

Implementasikan dari standar: K-PKE.KeyGen/Encrypt/Decrypt; ML-KEM.KeyGen_internal(d, z), Encaps_internal(ek, m),
Decaps_internal(dk, c) yang deterministik; pembungkus KeyGen/Encaps/Decaps yang mengambil keacakan dari os.urandom;
serta pemeriksaan masukan yang diwajibkan standar (untuk ek dan dk; sebut bagian standarnya di komentar).
Penolakan implisit pada Decaps ikuti standar (perbandingan ciphertext lalu pemilihan K atau K-bar).

Tes (tb/golden/tests/test_mlkem.py):
- Untuk 500 seed acak: Decaps(dk, Encaps(ek)) == K.
- Ciphertext yang diubah satu bit menghasilkan K-bar deterministik yang berbeda dari K.
- Panjang ek, dk, ciphertext, kunci bersama sama dengan EK_BYTES, DK_BYTES, CT_BYTES, SS_BYTES.
- check_params.py masih lulus.
Model Python ini bukan implementasi waktu-konstan dan tidak perlu begitu; jangan mengklaim apa pun soal itu.
Jalankan pytest; berhenti bila gagal. Laporkan hasilnya jujur, termasuk yang belum diuji.
```

## Prompt 4 — Vektor uji resmi NIST (ACVP)
```
Tujuan: bukti bit-exact terhadap vektor resmi. Baca dulu .claude/skills/mlkem-guard/reference/kat_sources.md.

1. Tulis tb/golden/fetch_acvp_vectors.py: mengunduh dua berkas internalProjection.json dari commit terpatok
   975de31eb83d87039ec88934fdc47d8c312b892d ke tb/vectors/acvp/ dan MEMVERIFIKASI sha256-nya terhadap nilai di
   reference/kat_sources.md. Bila beda: berhenti dan laporkan. Berkas JSON tidak di-commit (sudah di .gitignore).
2. Tulis tb/golden/run_kat.py yang memakai HANYA grup ML-KEM-768 dan membandingkan model kita:
   keyGen (d,z -> ek,dk), encapsulation (ek,m -> c,k), decapsulation (dk,c -> k; termasuk kasus "modified
   ciphertext"), encapsulationKeyCheck dan decapsulationKeyCheck (hasil boolean vs testPassed). Bandingkan hex tanpa
   membedakan huruf besar/kecil.
3. Keluaran mentah ke docs/evidence/golden/kat_mlkem768_<tanggal-UTC>.txt: URL sumber, commit, sha256, dan per grup
   jumlah kasus / lulus / gagal, daftar tcId yang gagal, serta kalimat: "Vektor ini adalah set sampel NIST
   (isSample: true), 25 kasus per grup, bukan cakupan menyeluruh."
Jangan mengubah vektor, perbandingan, atau menambah toleransi. Bila ada yang gagal, debug modelnya dan laporkan
tcId-nya; bila Anda curiga penyebabnya errata, kutip butir errata dari berkas Prompt 1.
Berhenti setelah log tersimpan dan laporkan angkanya apa adanya.
```

## Prompt 5 — Pembanding independen (kyber-py), acak
```
Tujuan: menangkap kesalahan yang lolos dari vektor sampel dengan membandingkan model kita terhadap implementasi
independen pada banyak masukan acak.

1. Buat virtualenv sementara DI LUAR repo (mis. ~/.cache/chip2026-oracle) dan pasang kyber-py==1.2.0 di sana.
   Jangan menambahkannya ke scripts/requirements-dev.txt dan jangan menyalin kodenya ke repo (lisensi MIT sudah
   dicek; tetap hanya dipakai sebagai oracle saat uji).
2. Tulis tb/golden/crosscheck_kyberpy.py yang, bila kyber_py tersedia, membandingkan model kita dengan
   ML_KEM_768._keygen_internal / _encaps_internal / _decaps_internal untuk N=2000 (d,z), m, dan ciphertext
   yang diubah acak, dengan seed RNG tetap agar bisa diulang. Bila kyber_py tidak ada, skrip berhenti dengan pesan
   jelas (bukan lulus diam-diam).
3. Simpan log mentah ke docs/evidence/golden/crosscheck_kyberpy_<tanggal-UTC>.txt: versi kyber-py, N, seed, hasil.
Bila ada selisih: jangan memutuskan siapa yang benar berdasarkan tebakan. Tentukan dari teks standar dan vektor NIST,
laporkan kedua nilai, dan berhenti.
```

## Prompt 6 — Penutup: artifact hasil dan gerbang fase
```
Tujuan: menyelesaikan Fase 0 dengan jujur dan berhenti untuk persetujuan manusia.

1. Jalankan ulang, segar: pytest tb/golden, check_params.py, run_kat.py (tulis log baru bila perlu), crosscheck
   (bila oracle terpasang).
2. Jalankan /phase-gate untuk Fase 0 dan buat docs/results/result_phase0.md dari
   docs/results/TEMPLATE_result_phase.md. Isi HANYA dari bukti yang ada. Kriteria tanpa bukti = MISSING. Status
   keseluruhan DONE hanya bila semua baris PASS; kalau tidak, PARTIAL atau NOT DONE.
   Bagian "Standards and sources pinned": revisi FIPS 203, keadaan errata yang dibaca, commit ACVP + sha256, versi oracle.
   Bagian "Coverage and limits": set sampel NIST saja; model Python tidak waktu-konstan; ML-KEM-512/1024 tidak diuji;
   apa pun lain yang belum tercakup.
3. Validasi: python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/result_phase0.md
   dan python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal
   Perbaiki sampai 0 error. Jangan melonggarkan pemeriksanya.
4. Perbarui HANYA yang terbukti: baris status di docs/ROADMAP.md dan baris "Bit-exact match with official KATs" di
   docs/proposal/CLAIMS_REGISTER.md, dengan kata-kata presisi (mis. "lulus N vektor sampel NIST ACVP dan cocok
   dengan implementasi independen pada N kasus acak"), bukan "terverifikasi penuh".
5. Commit lokal dalam commit-commit kecil bermakna di cabang phase0-golden-model. JANGAN push. JANGAN centang kotak Approval.
6. Laporkan dalam bahasa Indonesia: apa yang PASS/FAIL/MISSING, hal yang harus saya tinjau manual (sebutkan
   berkas dan baris), keputusan tim yang dibutuhkan, dan prasyarat Fase 1. Lalu berhenti.
```

---

## Setelah Prompt 6: yang dikerjakan manusia
- Baca `docs/results/result_phase0.md` sendiri, dan buka minimal dua berkas bukti yang ia rujuk.
- Jalankan ulang `pytest tb/golden` dan `python3 tb/golden/run_kat.py` di mesin Anda.
- Bila puas: centang kotak Approval, commit, lalu push lewat `scripts/setup_github.sh push`.
- Fase 1 baru dimulai setelah itu (prompt pack Fase 1 dibuat menyusul, dari hasil Fase 0).
