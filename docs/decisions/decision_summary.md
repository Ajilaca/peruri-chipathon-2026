# Keputusan desain aktif

Ringkasan keputusan yang membentuk desain akhir. Sumber kebenaran tetap file ADR di [`adr/`](adr/).
Ringkasan semua 43 ADR menurut tema: [SUMMARY.md](SUMMARY.md). Pilihan yang masih terbuka: [PENDING.md](PENDING.md).
Keputusan di bawah berstatus *Accepted* oleh tim kecuali dinyatakan lain.

## Aktif

| ADR | Keputusan | Alasan singkat | Dampak pada desain |
|---|---|---|---|
| [0001](adr/ADR-0001-project-idea-mlkem768-accelerator.md) | Membangun akselerator ML-KEM-768 dengan HW/SW co-design di DE10-Nano. | Ide proyek yang dipilih tim. | Fabric: NTT/INTT, Keccak, sampler. HPS: alur protokol dan baseline. |
| [0002](adr/ADR-0002-scope-and-claims.md) | Matematika FIPS 203 dikunci; inovasi hanya di arsitektur. Bahasa keamanan dibatasi. | Mengubah q, n, η, du, dv atau sampling menghasilkan skema lain yang tidak terbukti. | Semua RTL bit-exact terhadap model acuan. Tidak ada klaim side-channel atau kebal kuantum. |
| [0003](adr/ADR-0003-fips-203-errata-findings-and-golden-model-handling.md) | Errata FIPS 203 dua item (non-normatif) tidak mengubah implementasi. | Standar diikuti apa adanya. | Model acuan dan vektor ACVP memakai standar tanpa penyimpangan. |
| [0005](adr/ADR-0005-apply-adr-0004-l-selection-to-the-c2-k2-k1-supplementary-con.md) | L = 8 lajur dengan konfigurasi C2-K2-K1 (satu pengali per butterfly). | Siklus terendah dalam anggaran ALM (ADR 0004). | NTT 113 siklus (sebelum pipeline); dasar semua inti NTT berikutnya. |
| [0006](adr/ADR-0006-phase-4-target-clock.md) | Dua tingkat clock: 40 ns sebagai gerbang, 20 ns sebagai tujuan. | Jalur kritis dikoreksi ke pembacaan memori (ADR 0010). | Gerbang timing 40 ns; 20 ns dan 15 ns dilaporkan. |
| [0009](adr/ADR-0009-phase-4-final-decision-l-8-p-6-c3-p6-and-a-30-alm-design-bud.md) | L = 8, P = 6 (C3-P6); anggaran inti NTT 30 % ALM. | Pipeline P = 6 memenuhi 40 ns dalam anggaran. | NTT 119, INTT 375 siklus pada C3-P6. |
| [0011](adr/ADR-0011-phase-5-plan-decisions-d1-d8-and-the-5b-selection-rule.md) | Aturan seleksi aritmetika Phase 5: Fmax median tertinggi, pita seri 5 %, lalu ALM. | Aturan ditulis sebelum pengukuran. | Memilih Barrett atas fold dan Montgomery. |
| [0012](adr/ADR-0012-rules-for-timing-work-beyond-phase-5-cycle-increase-judged-b.md) | Kenaikan siklus diterima hanya bila t_NTT dan t_INTT terukur membaik. | Menjaga perbandingan jujur antar konfigurasi. | Dasar aturan adopsi Phase 5M dan 9M (latensi = siklus / Fmax). |
| [0013](adr/ADR-0013-phase-5b-choice-barrett-reducer-selected-by-the-adr-0011-rul.md) | Reducer Barrett (k = 24, M = 5039). | Dipilih aturan 0011; DSP naik dari 9 ke 18. | Semua inti sesudahnya memakai Barrett. |
| [0014](adr/ADR-0014-phase-5c-lazy-intt-butterfly-inputs-operand-contract-d6-amen.md) | Butterfly INTT dengan masukan malas (5c) tidak diadopsi. | Median Fmax 33,100 MHz, di bawah syarat. | Tidak ada di inti akhir. |
| [0015](adr/ADR-0015-phase-5d-karatsuba-style-base-case-not-attempted-in-phase-5-.md) | Basis perkalian ala Karatsuba (5d) tidak dicoba di Phase 5. | Dipindah; tidak ada hasil. | Tidak ada di inti akhir. |
| [0020](adr/ADR-0020-phase-5m-s6-intt-without-the-scaling-pass-halving-in-every-l.md) | S6: INTT tanpa lintasan skala (pembagian dua di tiap layer). | Aturan tidak mengadopsi (selisih 0,008 µs), tim memilih M6 sebagai basis. | INTT 375 menjadi 119 siklus; `half_mod`, `twiddle_rom_half`. |
| [0025](adr/ADR-0025-s10-inside-phase-6-16-x-1r1w-bank-memory-without-slot-arbitr.md) | S10: memori 16 bank 1R1W tanpa arbitrasi slot diterima sebagai inti NTT/INTT. | Lolos aturan; peta bank bebas konflik (studi S9). | `ntt_core_s10`, `poly_mem_m10k`; 118 siklus, median 44,320 MHz di 40 ns, 5.077 ALM. |
| [0027](adr/ADR-0027-phase-8a-two-keccak-rounds-per-cycle-c5-rule-result.md) | Keccak dua ronde per siklus (C5). | Lolos aturan 8a. | `keccak_f1600_r2`, `keccak_sponge_r2`; 12 siklus sibuk per permutasi. |
| [0028](adr/ADR-0028-phase-8b-streaming-samplers-output-width-w2-two-coefficients.md) | Sampler streaming W2 (dua koefisien per siklus). | Dipilih aturan atas W1. | `rtl/sample/`, SampleNTT dan CBD2 langsung dari aliran Keccak. |
| [0029](adr/ADR-0029-phase-8c-matrix-a-streamed-from-the-sampler-into-the-pwm-uni.md) | Matriks A dialirkan dari sampler ke unit PWM (STREAM), tidak disimpan. | Lolos aturan 8c. | Slot matriks A tidak dibutuhkan. |
| [0030](adr/ADR-0030-phase-8d-noise-sampling-overlapped-with-the-transforms-overl.md) | Pengambilan sampel noise ditumpangkan dengan transformasi (OVERLAP). | Lolos aturan 8d. | Program ROM varian OVERLAP di `kpke_sched_smp`. |
| [0031](adr/ADR-0031-phase-9-fips-203-input-checks-are-done-by-the-hps-not-in-the.md) | Pemeriksaan masukan FIPS 203 dikerjakan HPS, bukan RTL, untuk sekarang. | Tidak ada akses papan. | Grup key-check ACVP tidak dijalankan di RTL. |
| [0034](adr/ADR-0034-phase-9m-optimisation-scope-wider-codec-byte-path-20-ns-seed.md) | Lingkup 9M: codec dua byte, inti pada 20 ns, hash K0, pemuatan di belakang mesin; sampler kedua tidak dibangun. | Lingkup ditetapkan sebelum pengukuran; item 5 hanya disimpan sebagai ide. | Menentukan K1 sampai K4. |
| [0036](adr/ADR-0036-phase-9f-fmax-plan-s0-s1-s2-latency-rule-and-reporting-at-a-.md) | Rencana Fmax S0, S1, S2; aturan adopsi pada latensi KeyGen, Encaps, Decaps. | Latensi = siklus / Fmax menghindari pemilihan yang hanya mengejar Fmax. | Dipakai oleh seluruh keputusan hasil 9M. |
| [0039](adr/ADR-0039-phase-9f-15-ns-is-the-fmax-reporting-limit-14-ns-is-kept-for.md) | 15 ns adalah batas pelaporan Fmax; 14 ns disimpan. | Memberi satu batas pelaporan yang tetap. | Hasil 9M dilaporkan pada 40 ns (gerbang) dan 15 ns. |

## Hasil Phase 9 dan 9M yang menunggu keputusan tim

Berstatus *Proposed*. Pengusul bukan pemutus; ADR tidak diterima sebelum anggota tim menyatakannya.
Rantai: K4 (0043) berdiri di atas K3 (0042), K2 (0041), K1b (0040), K1 (0038). Tim dapat berhenti di tautan mana pun, tetapi angka sesudahnya harus diukur ulang di dasar baru.

| ADR | Isi | PENDING |
|---|---|---|
| [0033](adr/ADR-0033-phase-9-c7-core-as-built-ml-kem-768-in-simulation-acvp-100-p.md) | Inti Phase 9 (`mlkem_core`) apa adanya, ACVP 100 % dalam simulasi. | #33 |
| [0035](adr/ADR-0035-phase-9m-1-result-two-byte-codec-path-codec-w2-adopted-by-it.md) | 9M-1: jalur codec dua byte (`CODEC_W2 = 1`). | #34 |
| [0037](adr/ADR-0037-phase-9m-3-result-k0-hash-sponge-hash-c5-0-adopted-by-its-ru.md) | 9M-3: sponge hash K0 (`HASH_C5 = 0`), lebih kecil, +120 siklus. | #35 |
| [0038](adr/ADR-0038-phase-9f-s1-result-k0-sampler-and-k0-hash-k1-adopted-by-its-.md) | S1: sampler K0 + hash K0 (K1), lebih kecil bukan lebih cepat. | #36 |
| [0040](adr/ADR-0040-phase-9f-s1b-result-background-hash-k1b-adopted-by-its-rule-.md) | S1b: hash di latar belakang (K1b, `mlkem_core3`). | #37 |
| [0041](adr/ADR-0041-phase-9f-s2-result-register-after-the-barrett-reducer-k2-ado.md) | S2: register setelah Barrett (K2), netral untuk Fmax. | #38 |
| [0042](adr/ADR-0042-phase-9f-s2b-result-registered-ntt-issue-address-k3-not-adop.md) | S2b: alamat issue NTT terregistrasi (K3), tidak diadopsi aturan seperti tertulis. | #39 |
| [0043](adr/ADR-0043-phase-9i-item-4-result-loads-behind-the-k-pke-engine-k4-adop.md) | Item 4: pemuatan di belakang mesin K-PKE (K4, `mlkem_core4`). | #40 |

## Historis (superseded)

Tetap disimpan sebagai riwayat. Tidak berlaku untuk desain akhir.

| ADR | Isi | Digantikan oleh |
|---|---|---|
| [0008](adr/ADR-0008-apply-adr-0007-to-the-phase-4-pipeline-sweep-proposed-pipeli.md) | Usulan P = 4 (anggaran 25 %), tidak pernah diterima | [0009](adr/ADR-0009-phase-4-final-decision-l-8-p-6-c3-p6-and-a-30-alm-design-bud.md) |
| [0018](adr/ADR-0018-scope-and-order-until-the-thursday-deadline-finis.md) | Urutan sampai 2026-10-08 (tunda Phase 6) | [0019](adr/ADR-0019-minimal-path-to-a-full-ml-kem-768-core-before-thursday-2026-.md) |
| [0021](adr/ADR-0021-phase-5m-s7-split-memory-read-path-rd-split-p-7-rule-result-.md) | S7 split baca lolos aturan, sebagai konfigurasi | [0025](adr/ADR-0025-s10-inside-phase-6-16-x-1r1w-bank-memory-without-slot-arbitr.md) |
| [0022](adr/ADR-0022-phase-5m-s9-m10k-study-result-options-for-the-memory-team-ch.md) | S9 studi M10K, opsi A dibangun sebagai S10 | [0025](adr/ADR-0025-s10-inside-phase-6-16-x-1r1w-bank-memory-without-slot-arbitr.md) |
| [0023](adr/ADR-0023-phase-5m-s8-write-path-register-and-one-bubble-per-direction.md) | S8 register jalur tulis, tidak lolos aturan | [0025](adr/ADR-0025-s10-inside-phase-6-16-x-1r1w-bank-memory-without-slot-arbitr.md) |

## Keputusan proses (tidak mengubah desain)

0004 (kriteria pemilihan L), 0007 (kriteria pemilihan P), 0010 (50 MHz target terbaik-upaya), 0016 (lisensi MIT), 0017 (Phase 5M), 0019 (jalur minimal ke inti penuh), 0024 (Phase 6 dan S10), 0026 (sub-langkah Phase 8), 0032 (satu STOP per blok). Isinya ada di [SUMMARY.md](SUMMARY.md).
