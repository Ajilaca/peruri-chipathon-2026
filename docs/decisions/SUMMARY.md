# Ringkasan Seluruh Keputusan (ADR 0001 sampai 0043)

Ringkasan ini merangkum semua catatan keputusan di folder [`adr/`](adr/). Sumber kebenaran tetap berkas ADR masing-masing; daftar pilihan yang masih terbuka ada di [`PENDING.md`](PENDING.md). Status dan pengambil keputusan dikutip dari header tiap ADR. ADR yang sudah *Accepted* tidak disunting; perubahan dicatat dengan ADR baru yang menggantikan.

**Hitungan status:** 37 Accepted · 5 Superseded (0008, 0018, 0021, 0022, 0023) · 1 Proposed (0033).

## 1. Fondasi, kebijakan, dan lisensi
| ADR | Keputusan | Status | Diputuskan |
|---|---|---|---|
| [0001](adr/ADR-0001-project-idea-mlkem768-accelerator.md) | Membangun akselerator ML-KEM-768 (HW/SW co-design) di DE10-Nano. HPS: alur protokol, baseline, pengukuran waktu. Fabric: NTT/INTT + pointwise, Keccak, sampler, compress/encode, kontrol. | Accepted | Tim J5, 2026-09-28 |
| [0002](adr/ADR-0002-scope-and-claims.md) | **Matematika dikunci** (q, n, k, η, du, dv, akar satuan, aritmetika FIPS 203); inovasi hanya di arsitektur. Bahasa keamanan: "dirancang mengikuti standar pasca-kuantum", bukan "quantum-proof"; ketahanan side-channel tidak diklaim; klaim inti = konstan-waktu lewat invarian siklus. | Accepted | Tim J5, 2026-09-28 |
| [0003](adr/ADR-0003-fips-203-errata-findings-and-golden-model-handling.md) | Errata FIPS 203 (2 item, keduanya non-normatif): implementasi dan model emas mengikuti standar apa adanya, tanpa penyimpangan akibat errata. | Accepted | Faza Dzil, 2026-09-29 |
| [0016](adr/ADR-0016-repository-licence-mit.md) | Lisensi repositori MIT; pemegang hak cipta "Team J5 (ITB), CHIP 2026 Hackathon"; materi pihak ketiga tetap memakai lisensinya sendiri. | Accepted | Faza Dzil, 2026-10-02 |

## 2. Inti NTT/INTT: lajur, pipeline, aritmetika (Fase 3 sampai 5)
| ADR | Keputusan | Status | Diputuskan |
|---|---|---|---|
| [0004](adr/ADR-0004-phase-3-lane-count-l-selection-criterion.md) | Kriteria pemilihan jumlah lajur L: utama minimalkan siklus dalam anggaran 25 % ALM (10.478); sekunder AT bila ada Fmax yang valid. | Accepted | Faza Dzil, 2026-09-29 |
| [0005](adr/ADR-0005-apply-adr-0004-l-selection-to-the-c2-k2-k1-supplementary-con.md) | Konfigurasi C2-K2-K1 (satu pengali per butterfly) diadopsi dan **L = 8** dipilih (9.754 ALM, NTT 113 / INTT 369 siklus). Penyimpangan dari lingkup tertulis dicatat. | Accepted | Faza Dzil, 2026-09-30 |
| [0006](adr/ADR-0006-phase-4-target-clock.md) | Target clock dua tingkat: 40 ns (25 MHz) sebagai target eksperimen Fase 4; 20 ns (50 MHz) sebagai tujuan akhir setelah Fase 5. | Accepted | Faza Dzil, 2026-09-30 |
| [0007](adr/ADR-0007-phase-4-pipeline-depth-p-and-selection-criterion.md) | Kedalaman pipeline P ∈ {0, 2, 4, 6}; fungsi matematika tidak boleh berubah; kriteria seleksi P berdasarkan t_NTT terukur. | Accepted | Faza Dzil, 2026-09-30 |
| [0008](adr/ADR-0008-apply-adr-0007-to-the-phase-4-pipeline-sweep-proposed-pipeli.md) | Usulan P = 4 pada anggaran 25 %; tidak pernah diterima. | Superseded oleh 0009 | (tidak diputuskan) |
| [0009](adr/ADR-0009-phase-4-final-decision-l-8-p-6-c3-p6-and-a-30-alm-design-bud.md) | **Keputusan akhir Fase 4: L = 8, P = 6 (C3-P6)**; anggaran desain inti NTT 30 % = 12.573 ALM (anggaran inti, bukan batas sistem). | Accepted | Faza Dzil, 2026-10-01 |
| [0010](adr/ADR-0010-phase-5-timing-objective-50-mhz-kept-as-best-effort-project-.md) | 50 MHz tetap target terbaik-upaya (bukan gerbang). Ekspektasi ADR 0006 dikoreksi: jalur kritis ada di pembacaan memori, bukan aritmetika. | Accepted | Faza Dzil, 2026-10-01 |
| [0011](adr/ADR-0011-phase-5-plan-decisions-d1-d8-and-the-5b-selection-rule.md) | Keputusan rencana Fase 5 (D1–D8) dan aturan seleksi 5b: Fmax median tertinggi, pita seri 5 %, lalu ALM. | Accepted | Faza Dzil, 2026-10-01 |
| [0012](adr/ADR-0012-rules-for-timing-work-beyond-phase-5-cycle-increase-judged-b.md) | Kenaikan jumlah siklus diterima hanya bila t_NTT dan t_INTT terukur lebih baik daripada baseline C3-P6 dan sifat siklus-konstan tetap; batas 12.573 ALM dipertahankan. | Accepted | Faza Dzil, 2026-10-01 |
| [0013](adr/ADR-0013-phase-5b-choice-barrett-reducer-selected-by-the-adr-0011-rul.md) | **Reducer Barrett** dipilih menurut aturan 0011; biaya DSP 9 → 18 dicatat eksplisit. | Accepted | Jevan, 2026-10-02 |
| [0014](adr/ADR-0014-phase-5c-lazy-intt-butterfly-inputs-operand-contract-d6-amen.md) | Aturan adopsi 5c (butterfly INTT dengan masukan malas). Hasil pengukuran: tidak diadopsi. | Accepted | Faza Dzil, 2026-10-01 |
| [0015](adr/ADR-0015-phase-5d-karatsuba-style-base-case-not-attempted-in-phase-5-.md) | 5d (basis perkalian ala Karatsuba) tidak dicoba di Fase 5 dan dipindah ke Fase 6. | Accepted | Jevan, 2026-10-02 |

## 3. Memori dan penjadwalan (Fase 5M dan 6)
| ADR | Keputusan | Status | Diputuskan |
|---|---|---|---|
| [0017](adr/ADR-0017-memory-and-schedule-phase-between-phase-5-and-phase-6-pendin.md) | Fase 5M (memori dan jadwal) disisipkan antara Fase 5 dan 6: langkah S6–S9 dengan dasar C4b-B; tiap langkah satu perubahan, satu rencana uji sebelum pengukuran, satu STOP. | Accepted | Jevan, 2026-10-02 |
| [0018](adr/ADR-0018-scope-and-order-until-the-thursday-deadline-finis.md) | Urutan sampai batas 2026-10-08: selesaikan 5M, lalu baseline Keccak, tunda Fase 6. | Superseded oleh 0019 | Jevan, 2026-10-02 |
| [0019](adr/ADR-0019-minimal-path-to-a-full-ml-kem-768-core-before-thursday-2026-.md) | Jalur minimal menuju inti ML-KEM-768 penuh sebelum batas 2026-10-08 (5M S6–S9, lalu Fase 7–9); menggantikan 0018. Poin penundaan Fase 6 dan 8a/8c/8d kemudian digantikan 0024 dan 0026. | Accepted | Jevan, 2026-10-02 |
| [0020](adr/ADR-0020-phase-5m-s6-intt-without-the-scaling-pass-halving-in-every-l.md) | S6: INTT tanpa lintasan skala (pembagian dua di tiap layer). Aturan **tidak** mengadopsi (selisih 0,008 µs), tetapi tim memilih M6 sebagai dasar S7 dan S8. | Accepted | Jevan, 2026-10-02 |
| [0021](adr/ADR-0021-phase-5m-s7-split-memory-read-path-rd-split-p-7-rule-result-.md) | S7 (pembacaan memori terbelah) lolos aturan; sebagai konfigurasi digantikan 0025. | Superseded oleh 0025 | (tidak diputuskan) |
| [0022](adr/ADR-0022-phase-5m-s9-m10k-study-result-options-for-the-memory-team-ch.md) | S9: studi M10K, peta 16 bank 1R1W bebas konflik ada; opsi memori digantikan 0025 (opsi A dibangun sebagai S10). | Superseded oleh 0025 | (tidak diputuskan) |
| [0023](adr/ADR-0023-phase-5m-s8-write-path-register-and-one-bubble-per-direction.md) | S8 (register jalur tulis) **tidak** lolos aturan (kondisi 4: t = 3,211 µs lawan 3,099 µs S7). | Superseded oleh 0025 | (tidak diputuskan) |
| [0024](adr/ADR-0024-phase-6-now-supersedes-the-skip-of-adr-0019-point-2-s10-16-x.md) | Fase 6 dikerjakan sekarang (menggantikan penundaan di 0019); S10 dikerjakan di dalam Fase 6 setelah verdict; dasar sementara inti S7. | Accepted | Jevan, 2026-10-03 |
| [0025](adr/ADR-0025-s10-inside-phase-6-16-x-1r1w-bank-memory-without-slot-arbitr.md) | **S10 (16 × 1R1W tanpa arbitrase slot) lolos aturan dan diterima sebagai inti NTT/INTT.** | Accepted | Jevan, 2026-10-03 |

## 4. Keccak, sampler, dan K-PKE (Fase 8)
| ADR | Keputusan | Status | Diputuskan |
|---|---|---|---|
| [0026](adr/ADR-0026-phase-8-sub-steps-8a-8b-8c-and-8d-all-go-ahead-supersedes-th.md) | Sub-langkah 8a, 8b, 8c, 8d semuanya dikerjakan (menggantikan penundaan 8a/8c/8d di 0019). | Accepted | Jose, 2026-10-03 |
| [0027](adr/ADR-0027-phase-8a-two-keccak-rounds-per-cycle-c5-rule-result.md) | Keccak dua ronde per siklus (C5) lolos aturan dan diterima. | Accepted | Jo, 2026-10-03 |
| [0028](adr/ADR-0028-phase-8b-streaming-samplers-output-width-w2-two-coefficients.md) | Sampler streaming dengan keluaran **W2** (dua koefisien per siklus) dipilih atas W1; diterima. | Accepted | Jo, 2026-10-03 |
| [0029](adr/ADR-0029-phase-8c-matrix-a-streamed-from-the-sampler-into-the-pwm-uni.md) | Matriks A dialirkan dari sampler ke unit PWM (**STREAM**) dan tidak disimpan; diterima. | Accepted | Jo, 2026-10-03 |
| [0030](adr/ADR-0030-phase-8d-noise-sampling-overlapped-with-the-transforms-overl.md) | Pengambilan sampel noise ditumpangkan dengan transformasi (**OVERLAP**); diterima. | Accepted | Jo, 2026-10-03 |

## 5. Integrasi inti penuh dan tata kerja (Fase 9)
| ADR | Keputusan | Status | Diputuskan |
|---|---|---|---|
| [0031](adr/ADR-0031-phase-9-fips-203-input-checks-are-done-by-the-hps-not-in-the.md) | Pemeriksaan masukan FIPS 203 dilakukan HPS (perangkat lunak), bukan RTL, "untuk sekarang" karena tidak ada akses papan. | Accepted | Jo, 2026-10-03 |
| [0032](adr/ADR-0032-checkpoint-protocol-until-one-stop-per-block-phas.md) | Protokol checkpoint sampai 2026-10-08: satu STOP per blok (Fase 9 dan seterusnya); tidak ada commit sebelum pekerjaan selesai. | Accepted | Jo, 2026-10-03 |
| [0033](adr/ADR-0033-phase-9-c7-core-as-built-ml-kem-768-in-simulation-acvp-100-p.md) | Inti C7 apa adanya (ML-KEM-768 dalam simulasi, ACVP 100 %) dan inti sponge hash. **Menunggu keputusan tim** (PENDING #33). | Proposed | (menunggu tim) |

## 6. Optimasi inti, Fase 9M
| ADR | Keputusan | Status | Diputuskan |
|---|---|---|---|
| [0034](adr/ADR-0034-phase-9m-optimisation-scope-wider-codec-byte-path-20-ns-seed.md) | Lingkup 9M: item 1 (codec dua byte), 2 (inti pada 20 ns), 3 (hash K0), 4 (tumpang-tindih muat dengan mesin). Item 5 (sampler kedua) disimpan sebagai ide, tidak dibangun. | Accepted | Faza Dzil, 2026-10-04 |
| [0036](adr/ADR-0036-phase-9f-fmax-plan-s0-s1-s2-latency-rule-and-reporting-at-a-.md) | Rencana Fmax S0 → S1 (→ S2); aturan adopsi berdasarkan latensi t = siklus / Fmax untuk KeyGen, Encaps, Decaps; Fmax dilaporkan pada batasan 15 ns di samping gerbang 40 ns. | Accepted | Faza Dzil, 2026-10-04 |
| [0039](adr/ADR-0039-phase-9f-15-ns-is-the-fmax-reporting-limit-14-ns-is-kept-for.md) | **15 ns adalah batas pelaporan Fmax**; 14 ns disimpan untuk dipertimbangkan nanti. | Accepted | Faza Dzil, 2026-10-04 |
| [0035](adr/ADR-0035-phase-9m-1-result-two-byte-codec-path-codec-w2-adopted-by-it.md) | Hasil 9M-1: jalur codec dua byte (`CODEC_W2 = 1`) diadopsi aturan. | Accepted | Jo, 2026-10-05 |
| [0037](adr/ADR-0037-phase-9m-3-result-k0-hash-sponge-hash-c5-0-adopted-by-its-ru.md) | Hasil 9M-3: sponge hash K0 (`HASH_C5 = 0`) diadopsi aturan sebagai opsi lebih kecil (−1.736,5 ALM, +120 siklus). | Accepted | Jo, 2026-10-05 |
| [0038](adr/ADR-0038-phase-9f-s1-result-k0-sampler-and-k0-hash-k1-adopted-by-its-.md) | Hasil S1: sampler K0 + hash K0 (K1) diadopsi aturan, **lebih kecil bukan lebih cepat** (terhadap MW pada batasan sama 3–6 % lebih lambat). | Accepted | Jo, 2026-10-05 |
| [0040](adr/ADR-0040-phase-9f-s1b-result-background-hash-k1b-adopted-by-its-rule-.md) | Hasil S1b: hash di latar belakang (K1b) diadopsi aturan, memulihkan biaya siklus K1 (8.404 / 10.236 / 15.597). | Accepted | Jo, 2026-10-05 |
| [0041](adr/ADR-0041-phase-9f-s2-result-register-after-the-barrett-reducer-k2-ado.md) | Hasil S2: register setelah reducer Barrett (K2) diadopsi aturan, tetapi **netral** untuk Fmax (+0,27 MHz, di dalam derau seed). | Accepted | Jo, 2026-10-05 |
| [0042](adr/ADR-0042-phase-9f-s2b-result-registered-ntt-issue-address-k3-not-adop.md) | Hasil S2b: alamat issue NTT terregistrasi (K3) **tidak diadopsi aturan seperti tertulis**, tetapi median Fmax +3,4 MHz dengan ekor seed rendah. | Accepted | Jo, 2026-10-05 |
| [0043](adr/ADR-0043-phase-9i-item-4-result-loads-behind-the-k-pke-engine-k4-adop.md) | Hasil item 4: pemuatan di belakang mesin K-PKE (K4) diadopsi aturan; Encaps −639 dan Decaps −2.630 siklus. | Accepted | Jo, 2026-10-05 |

### Rantai ketergantungan keputusan 9M
K4 (0043) berdiri di atas K3 (0042), K3 di atas K2 (0041), K2 di atas K1b (0040), K1b di atas K1 (0038). Tim dapat berhenti di tautan mana pun, tetapi pengukuran sesudahnya harus diulang pada dasar yang baru. Khusus K4: siklus yang dihemat tidak bergantung pada parameter NTT, tetapi Fmax-nya bergantung.

## 7. Pola yang berulang di seluruh keputusan
- **Aturan sebelum pengukuran.** Hampir setiap langkah teknis punya aturan adopsi yang ditulis lebih dulu; hasilnya dicatat apa adanya, juga saat aturan berkata tidak (0020, 0023, 0042) atau saat tim memilih berbeda dari aturan (0020).
- **Pengusul bukan pemutus.** ADR berstatus *Proposed* sampai anggota tim menyatakan keputusan. Hasil 9M diterima Jo (Team J5) pada 2026-10-05; hanya ADR 0033 yang masih *Proposed*.
- **Satu langkah, satu perubahan, satu STOP** (0017, 0032).
- **Batas kejujuran bukti:** tidak ada klaim papan, kecepatan terhadap perangkat lunak, atau ketahanan side-channel (0002); angka implementasi hanya dari Quartus (CLAUDE.md §6.2).

## 8. Pilihan yang masih terbuka
Daftar lengkap dan terkini ada di [`PENDING.md`](PENDING.md): sisi target (#1), subtema (#2), DMA atau akses biasa (#3), sumber keacakan (#4), mode hibrida (#5), baseline perangkat lunak kedua (#6), alur protokol (#7), ketersediaan papan DE10-Nano (#8), penelusuran karya terdahulu (#10), hitungan halaman lampiran (#12), hook rtl-agent-team (#13), dan penerimaan hasil Fase 9 serta 9M (#33–#40).

## 9. Menambah keputusan baru
`python3 .claude/skills/decision-record/scripts/new_adr.py "Judul"` membuat `adr/ADR-NNNN-judul.md` dengan nomor berikutnya. Setelah itu tambahkan satu baris di tabel yang sesuai pada ringkasan ini dan perbarui hitungan status.
