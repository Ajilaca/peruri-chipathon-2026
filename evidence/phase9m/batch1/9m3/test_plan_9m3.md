<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Fase 9M butir 3 (9M-3): sponge K0 untuk instans hash - test plan dan aturan adopsi

Ditulis 2026-10-04 sebelum pengukuran 9M-3 apa pun. Lingkup: ADR 0034 (Accepted, Faza Dzil), butir 3 ("lanjut", chat 2026-10-04). Label: MEASURED, ESTIMATE, INFERENCE, perhitungan tim. Matematika terkunci (C1): K0 dan C5 menghitung Keccak-f[1600] dan sponge yang sama; hanya ronde per siklus yang berbeda.

## 1. Apa butir ini
Instans hash inti (`mlkem_hash`, G, H, J) dapat memakai sponge C5 (dua ronde per siklus, 12 siklus sibuk, ADR 0027) atau sponge K0 (satu ronde per siklus, 24 siklus sibuk, Fase 7). Inti sudah punya parameter `HASH_C5` (bawaan 1) dan `mlkem_hash` punya parameter `CORE_R2`; file K0 sudah ada di setiap daftar file. Tidak ada file RTL yang berubah di butir ini. Butir ini mengukur `HASH_C5 = 0`, yang dibiarkan terbuka oleh Fase 9 untuk tim (ADR 0033, 9b: instans hash K0 4,221 ALM lawan 6,712-6,745 ALM untuk pembungkus C5). Sampler di dalam mesin K-PKE menjaga sponge C5-nya sendiri; parameter ini tidak menyentuhnya.
Basis pengukuran: inti 9M-1 (`CODEC_W2 = 1`), revisi MK = MW dengan `HASH_C5 = 0`. Pilihan dinyatakan di sini: perbandingan yang menentukan adalah MK lawan MW (identik kecuali sponge); inti bawaan Fase 9 dengan K0 (`CODEC_W2 = 0`, `HASH_C5 = 0`) tidak diukur (INFERENCE: efek kedua parameter bersifat aditif, tidak diuji).

## 2. Estimasi yang ditulis sebelum mengukur (ESTIMATE, dari 9b: siklus per hash, G33 30 -> 42, G64 33 -> 45, H1184 282 -> 390, J1120 274 -> 382; mesin sampler tidak berubah)
| Besaran | MW (`CODEC_W2 = 1`, C5) MEASURED | MK ESTIMATE |
|---|---|---|
| Siklus KeyGen (G33 + H(ek)) | 8,327 | sekitar 8,447 (+120) |
| Siklus Encaps (H(ek) + G64) | 10,159 | sekitar 10,279 (+120) |
| Siklus Decaps (G64 + J) | 15,515 | sekitar 15,635 (+120) |
| Median ALM, seed 1-6 | 17,654.0 | 2,000 sampai 2,800 lebih sedikit (selisih 9b instans hash sekitar 2,500) |
| Register | 8,189-8,376 | sekitar 300 sampai 700 lebih sedikit |
| RAM blocks / DSP | 54 / 28 | 54 / 28 |
| Fmax slow corner terendah, median | 48.855 MHz | 47-53 MHz (jalur kritis ada di tempat lain: INFERENCE) |
| Timing pada 40.000 ns | terpenuhi di setiap seed | terpenuhi di setiap seed |

## 3. Test (kedua simulator; RTL repository tidak pernah dimutasi)
| # | Test | Syarat lulus |
|---|---|---|
| V1 | lint Verilator `-Wall` dan slang inti dengan `HASH_C5 = 0`, `CODEC_W2 = 1` | 0 peringatan, 0 error |
| V2 | inti dengan `HASH_C5 = 0`, `CODEC_W2 = 1`: seluruh target `core` Fase 9c (ACVP keyGen 25, enkapsulasi 25, dekapsulasi 10; cross-check acak; rantai; protokol; siklus konstan), env `CORE_K0=1 CORE_W2=1` | 100 % sama, kedua simulator |
| V3 | profil dengan `HASH_C5 = 0`, `CODEC_W2 = 1` (masukan sama seperti `../../profile.md`) | dicatat; state HFD / HGT memakan siklus tambahan; setiap hitungan state lain sama dengan MW |
| V4 | kontrol bahwa jalur K0 benar-benar dipakai dan diuji: `nclen` (setiap hash kurang satu byte) dengan `CORE_K0=1 CORE_W2=1` | `test_acvp_encaps` gagal, kedua simulator |
| V5 | formal: bukti pembungkus hash 9b (H1-H5) untuk `CORE_R2 = 0` dengan stub protokol `keccak_sponge` (stub 9b dengan nama K0, port sama); bukti pengendali 9c tidak bergantung pada parameter hash (hash adalah stub di sana) | PASS, seperti 9b; INFERENCE dinyatakan: bahwa sponge K0 nyata mengikuti protokol stub ditunjukkan oleh simulasi V2 dan bukti Fase 7 |
| V6 | regresi: inti bawaan tidak berubah (tidak ada file RTL berubah); `tb/mlkem/run_core_tests.py verilator core` pada nilai bawaan | 6/6 dan profil bawaan sama dengan profil Fase 9 |
| V7 | Quartus: revisi MK seed 1-6 pada 40.000 ns dan MK-20 (seed 1, 20.000 ns, informasi), satu per satu, kernel-only | ekstrak; timing terpenuhi atau kegagalan didokumentasikan |

## 4. Parameter yang dilaporkan
ALM (median, min-maks, % dari denominator fitter), register, blok RAM, bit memori blok, DSP, slack setup dan hold terburuk, timing terpenuhi per seed, Fmax slow corner terendah (median, min-maks); siklus per operasi (masukan profil dan rentang ACVP) dan per operasi mikro; latensi t = siklus / median Fmax (perhitungan tim); jumlah ACVP; hasil siklus konstan; hasil formal; peringatan kritis.

## 5. Aturan adopsi (ditetapkan sebelum mengukur; tidak diubah sesudahnya)
K0 diadopsi sebagai sponge hash inti (sebagai opsi yang lebih kecil) hanya bila semua berikut berlaku:
1. V1-V6 lulus seperti dinyatakan (ketidakcocokan ACVP apa pun menolaknya).
2. Timing terpenuhi pada 40.000 ns di setiap seed 1-6.
3. Median ALM MK paling sedikit 1,500 di bawah MW (17,654.0).
4. Untuk masing-masing KeyGen, Encaps, dan Decaps (masukan profil), t = siklus / median Fmax MK paling banyak 2 % di atas MW (siklus profil MW / 48.855 MHz).
Bila tidak, C5 tetap. Hasilnya dicatat sebagai ADR Proposed; pilihan antara K0 yang lebih kecil dan bawaan C5 (ADR 0027) tetap pada tim (ADR 0033 mendaftarkannya). Aturan ini hanya memutuskan apakah angka membenarkan K0; ia tidak mengubah ADR 0027.

## 6. Bukan bagian butir ini
Tanpa perubahan RTL; tanpa hasil papan; tanpa klaim kecepatan terhadap perangkat lunak; waktu-konstan berarti invarian jumlah siklus saja.
