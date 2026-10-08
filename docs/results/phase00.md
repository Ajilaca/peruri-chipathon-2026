<!-- claim-lint: skip-file (result artifact: internal status page, not proposal text) -->
# Hasil - Fase 0: Fondasi

- Status: DONE
- Tanggal (UTC): 2026-09-29 01:16
- Git commit (HEAD saat diverifikasi): bac5637
- Lingkungan: Ubuntu 24.04.4 LTS, Python 3.12.3 (`.venv`, pytest 9.1.1); pembanding independen dijalankan
  dengan venv sementara terpisah (`~/.cache/chip2026-oracle/venv`, kyber-py 1.2.0)

## 1. Kriteria selesai (disalin dari docs/ROADMAP.md, tidak diubah)
| # | Kriteria | Evidence (`path` di bawah evidence/ atau tes, atau `cmd: ...`) | Status |
|---|---|---|---|
| 1 | `check_params.py` lulus (parameter terkunci), dan k/eta/du/dv dikonfirmasi terhadap tabel parameter FIPS 203 | `cmd: python3 .claude/skills/mlkem-guard/scripts/check_params.py` dan `evidence/phase00/fips203_errata.md` | PASS |
| 2 | Model acuan (golden model) mereproduksi vektor resmi ML-KEM-768 (NIST ACVP, commit dipatok di kat_sources.md; set sampel NIST; keluaran mentah di evidence/phase00/) | `evidence/phase00/kat_mlkem768.txt` | PASS |
| 3 | Temuan errata tercatat (file evidence + ADR) | `evidence/phase00/fips203_errata.md` dan `docs/decisions/adr/ADR-0003-fips-203-errata-findings-and-golden-model-handling.md` | PASS |
| 4 | Log pemeriksaan silang independen pada masukan acak di evidence/phase00/ (pembanding: kyber-py di venv sementara) | `evidence/phase00/crosscheck_kyberpy.txt` | PASS |
| 5 | `docs/results/phase00.md` lulus `check_result.py`, dan manusia telah menyetujuinya | `cmd: python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase00.md` (file ini; bagian persetujuan manusia dari kriteria ini dilacak terpisah oleh kotak centang yang belum dicentang di bagian 10, bukan oleh baris ini) | PASS |

Status adalah PASS, FAIL, atau MISSING. PASS memerlukan setidaknya satu item evidence berformat backtick yang ada.
Belum ada RTL pada fase ini; tidak ada hasil di sini yang membedakan hanya-simulasi dari terukur-di-papan (pembedaan itu
dimulai pada Fase 1).

## 2. Yang dihasilkan
| Path | Fungsi |
|---|---|
| `tb/golden/params.py` | Konstanta ML-KEM-768 yang terkunci (Q N ZETA K ETA1 ETA2 DU DV EK_BYTES DK_BYTES CT_BYTES SS_BYTES) |
| `tb/golden/primitives.py` | Algoritma pendukung FIPS 203: NTT/NTT⁻¹, MultiplyNTTs, BaseCaseMultiply, SampleNTT, SamplePolyCBD, ByteEncode/Decode, Compress/Decompress, pembungkus hash/XOF |
| `tb/golden/kpke.py` | K-PKE.KeyGen/Encrypt/Decrypt (Algoritma 13-15) |
| `tb/golden/mlkem.py` | Algoritma internal ML-KEM (16-18), pemeriksaan masukan (§7.2, §7.3), pembungkus acak (19-21) |
| `tb/golden/conftest.py` | Pengaturan sys.path pytest agar tes dapat `import params`/`import primitives` |
| `tb/golden/tests/test_primitives.py` | 19 tes properti (NTT bolak-balik, NTT lawan schoolbook, struktur layer, encode/decode, compress/decompress, rentang CBD) |
| `tb/golden/tests/test_mlkem.py` | 4 tes: bolak-balik 500 percobaan, implicit rejection pada pembalikan bit, pemeriksaan panjang, jalankan ulang check_params.py |
| `tb/golden/fetch_acvp_vectors.py` | Mengunduh dan memverifikasi sha256 dua file vektor ACVP yang dipatok |
| `tb/golden/run_kat.py` | Membandingkan model dengan grup ACVP ML-KEM-768 |
| `tb/golden/crosscheck_kyberpy.py` | Pemeriksaan silang deterministik N=2000 terhadap kyber-py (pembanding eksternal) |
| `evidence/phase00/fips203_errata.md` | Hash sumber FIPS 203, butir errata yang dikutip beserta analisis dampak, pemeriksaan silang parameter Tabel 2/3 |
| `evidence/phase00/kat_mlkem768.txt` | Log mentah perbandingan KAT ACVP (80/80 lulus) |
| `evidence/phase00/crosscheck_kyberpy.txt` | Log mentah pemeriksaan silang kyber-py (2000/2000 cocok) |
| `docs/decisions/adr/ADR-0003-fips-203-errata-findings-and-golden-model-handling.md` | ADR (Status: Accepted, 2026-09-29, Faza Dzil / Tim J5) tentang penanganan errata |
| `.claude/skills/mlkem-guard/reference/kat_sources.md` | Commit ACVP yang dipatok, sha256, tata letak vektor, catatan pembanding (diberikan, bukan ditulis oleh sesi ini) |

## 3. Angka (masing-masing berlabel MEASURED, ESTIMATE, atau kutipan [n])
| Besaran | Nilai | Label | Evidence |
|---|---|---|---|
| Hasil `check_params.py` | 12/12 konstanta terkunci sesuai | MEASURED | `cmd: python3 .claude/skills/mlkem-guard/scripts/check_params.py` |
| Hasil `pytest tb/golden` | 23/23 lulus | MEASURED | `cmd: python3 -m pytest tb/golden/tests/ -q` |
| Kasus KAT ACVP ML-KEM-768 | 80/80 lulus (keyGen 25, encapsulation 25, decapsulation 10, decapsulationKeyCheck 10, encapsulationKeyCheck 10) | MEASURED | `evidence/phase00/kat_mlkem768.txt` |
| Percobaan pemeriksaan silang kyber-py | 2000/2000 cocok (keygen_internal, encaps_internal, decaps_internal valid, decaps_internal ciphertext termodifikasi) | MEASURED | `evidence/phase00/crosscheck_kyberpy.txt` |
| Butir errata FIPS 203 yang ditemukan | 2, keduanya non-normatif (klarifikasi / salah ketik komentar) | MEASURED | `evidence/phase00/fips203_errata.md` |

## 4. Standar dan sumber yang dipatok
- FIPS 203 (Module-Lattice-Based Key-Encapsulation Mechanism Standard), terbit 2024-08-13,
  DOI 10.6028/NIST.FIPS.203. PDF diunduh 2026-09-28 UTC dari
  `https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf`,
  sha256 `fe1f12f32a7e44ec9fdebbf400cda843a40b506dee676725234dc6f7923b6cac`.
- Keadaan errata yang dibaca: spreadsheet "Potential Updates (Errata)" NIST, diunduh 2026-09-28 UTC
  dari `https://csrc.nist.gov/files/pubs/fips/203/final/docs/fips-203-potential-updates.xlsx`,
  sha256 `edf899c89762449f43d7713883caeefc2e4ae9ae98d5a76b339547db22cb3ac7`. Berisi 2 butir pada
  tanggal akses tersebut (2025-03-31 klarifikasi tabel zeta di Lampiran A; 2025-10-17 salah ketik
  komentar di Bagian 5.3), keduanya non-normatif. Kutipan lengkap dan analisis dampak ada di
  `evidence/phase00/fips203_errata.md`. Penanganannya tercatat di ADR 0003
  (Status: Accepted, 2026-09-29, diputuskan oleh Faza Dzil / Tim J5 -- lihat Bagian 7 di bawah).
- Vektor uji NIST ACVP-Server: repositori `https://github.com/usnistgov/ACVP-Server`,
  commit dipatok `975de31eb83d87039ec88934fdc47d8c312b892d`. File yang dipakai:
  `gen-val/json-files/ML-KEM-keyGen-FIPS203/internalProjection.json`
  (sha256 `d7a62a2c3476957f56dd8d24f9004ea6776ccfe995ffe71a65bb9506dc9c7b1b`, tingkat atas
  `isSample: false` sebagaimana diunduh -- berbeda dari asumsi `kat_sources.md` yaitu
  `isSample: true`, lihat catatan di bawah) dan
  `gen-val/json-files/ML-KEM-encapDecap-FIPS203/internalProjection.json`
  (sha256 `a556952ce869bb89c3a3196a701dad89647c193a34c86eafb61a9d710d5b810f`, tingkat atas
  `isSample: true`). Kedua hash diverifikasi sebelum dipakai; lihat
  `evidence/phase00/kat_mlkem768.txt`.
- Pembanding independen: kyber-py 1.2.0 (`https://github.com/GiacomoPope/kyber-py`), lisensi
  MIT OR Apache-2.0, Hak Cipta Giacomo Pope. Dipasang hanya di virtualenv sementara di luar
  repositori ini; tidak ditambahkan ke `scripts/requirements-dev.txt`, tidak disalin ke repo.

## 5. Cakupan dan batas
- Hanya set vektor sampel/bawaan NIST. Cakupan KAT ACVP berjumlah 80 kasus ML-KEM-768 (25
  keyGen AFT, 25 encapsulation AFT, 10 decapsulation VAL, 10 decapsulationKeyCheck VAL, 10
  encapsulationKeyCheck VAL) dari satu commit yang dipatok -- bukan cakupan menyeluruh atas setiap
  masukan yang mungkin, jalur kegagalan dekapsulasi, atau konstruksi kunci tidak valid.
- ML-KEM-512 dan ML-KEM-1024 sama sekali tidak diuji. Dari kedua file ACVP hanya grup ML-KEM-768
  yang dipakai, dan `tb/golden/params.py` hanya mendefinisikan konstanta ML-KEM-768 (disengaja, lihat
  SKILL.md mlkem-guard).
- Model Python ini BUKAN implementasi waktu-konstan dan tidak ada klaim semacam itu tentangnya.
  Docstring `tb/golden/mlkem.py` menyatakannya secara eksplisit (ada percabangan pada data rahasia/turunan
  di jalur implicit-rejection dan pemeriksaan masukan). Waktu-konstan adalah sifat tingkat RTL yang akan
  diukur pada fase berikutnya, terpisah dari kebenaran model acuan ini.
- Pemeriksaan silang kyber-py berupa 2000 percobaan pseudo-acak dari satu seed tetap (dapat diulang, tidak
  menyeluruh) -- secara eksplisit berlabel "bukan bukti" di lognya sendiri.
- Belum ada angka FPGA/Quartus -- Fase 0 hanya Python; tidak ada klaim ALM/register/M10K/DSP/Fmax
  atau jumlah siklus yang dibuat atau tersirat oleh fase ini.
- "Key pair check" §7.1 (konsistensi seed + konsistensi berpasangan) tidak diimplementasikan atau
  diuji -- hanya pemeriksaan kunci enkapsulasi §7.2 dan pemeriksaan masukan dekapsulasi §7.3 per panggilan
  yang diimplementasikan (`tb/golden/mlkem.py`), sesuai dengan yang benar-benar diuji grup ACVP
  `encapsulationKeyCheck` / `decapsulationKeyCheck`.
- Jalur penolakan masukan tidak valid untuk `check_encapsulation_key` /
  `check_decapsulation_input` buatan kami hanya diuji lewat 20 kasus pemeriksaan kunci ACVP (10+10);
  tidak ada fuzzing tambahan untuk panjang/hash yang cacat di luar itu.
- ADR 0003 (penanganan errata) berstatus Accepted (2026-09-29, Faza Dzil / Tim J5); lihat Bagian 7.

## 6. Penyimpangan, kegagalan, dan masalah terbuka
Tidak ada. Tidak ada tes yang gagal kapan pun pada fase ini; tidak ada toleransi, assertion, atau perbandingan
yang dilonggarkan agar hasil lulus.

Satu koreksi fakta terhadap asumsi sebelumnya: `.claude/skills/mlkem-guard/reference/kat_sources.md`
menyatakan vektor ACVP adalah "sample sets (isSample: true)" NIST. Sebagaimana benar-benar diunduh dan
diverifikasi sha256 (2026-09-28), JSON file keyGen sendiri menyatakan `"isSample": false` (hanya file
encapDecap yang menyatakan `true`). Hal ini dilaporkan apa adanya, tidak dikoreksi diam-diam di file
acuan tersebut; lihat `evidence/phase00/kat_mlkem768.txt` untuk nilai persisnya.

## 7. Keputusan yang diperlukan
- ADR 0003 (`docs/decisions/adr/ADR-0003-fips-203-errata-findings-and-golden-model-handling.md`) kini
  Accepted (2026-09-29, diputuskan oleh Faza Dzil / Tim J5). Butir #9 di `docs/decisions/PENDING.md`
  ditutup karenanya.
- Tidak ada butir lain di `docs/decisions/PENDING.md` yang menghalangi penutupan Fase 0; butir #1-#8 dan #10-#13 semuanya
  menyasar fase berikutnya (lihat PENDING.md sendiri untuk daftar terbaru).

## 8. Klaim yang dibuat pada fase ini
Tidak ada yang ditulis untuk juri/teks proposal pada fase ini. Satu-satunya artefak proposal yang disentuh adalah
`docs/proposal/CLAIMS_REGISTER.md` baris "Bit-exact match with official KATs", diperbarui pada perubahan yang sama
dari "not started" menjadi pernyataan yang tepat dan berbukti (lihat git log / diff pada Bagian 9);
`claim_lint.py` dijalankan terhadap `docs/results` dan `docs/proposal` sebagaimana disyaratkan (lihat Bagian 9).

## 9. Mereproduksi
```bash
# from repo root
. scripts/env.sh

# 1. Golden model tests
python3 -m pytest tb/golden/tests/ -v

# 2. Locked parameters
python3 .claude/skills/mlkem-guard/scripts/check_params.py

# 3. Official NIST ACVP KAT comparison (downloads + sha256-verifies vectors first)
python3 tb/golden/fetch_acvp_vectors.py
python3 tb/golden/run_kat.py

# 4. Independent oracle cross-check (needs a throwaway venv with kyber-py==1.2.0
#    installed OUTSIDE this repo, e.g. ~/.cache/chip2026-oracle/venv)
~/.cache/chip2026-oracle/venv/bin/python3 tb/golden/crosscheck_kyberpy.py

# 5. Validate this result artifact
python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase00.md
python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal
```

## 10. Persetujuan
- [x] Penyetuju manusia (Faza Dzil, 2026-09-29):
      Fase berikutnya dimulai hanya setelah anggota tim mencentang kotak ini.
