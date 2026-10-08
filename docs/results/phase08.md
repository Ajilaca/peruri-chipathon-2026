<!-- claim-lint: skip-file (result artifact: internal status page, not proposal text) -->
# Hasil - Fase 8: Optimasi Keccak dan streaming (sub-langkah 8a, 8b, 8c, 8d)

- Status: DONE (keempat sub-langkah dibangun, diverifikasi, dan diukur; penerimaan ADR 0027-0030 dan kotak Persetujuan adalah hak tim)
- Catatan status: ADR 0026 (Accepted) mendahulukan 8a, 8b, 8c, dan 8d. Chat 2026-10-03 (tanpa nama) meminta 8b pada dua lebar keluaran dan 8b, 8c, 8d dikerjakan berurutan, lalu hasil ini dan laporannya. Setiap sub-langkah punya rencana tes sendiri yang ditulis sebelum pengukurannya dan satu aturan adopsi; setiap aturan diterapkan pada file dan tidak ada yang diubah setelah pengukuran (Amandemen A1 pada rencana mencatat temuan dan satu nilai harapan yang diubah, bagian 6).
- Tanggal (UTC): 2026-10-03
- Git commit (HEAD saat diverifikasi): lihat `git log main..phase8-keccak-stream` (8a 02d41bd, af62526, 12e1663; rencana 8b dcae678, W1 794db0d, W2 fbca60f; rencana 8c/8d f614b79, RTL 7a21af0, konfigurasi Quartus d965b4d, evidence dan ADR sesudahnya), ditambah commit dokumentasi file ini
- Hasil: 8a C5 dua ronde per siklus (diadopsi oleh aturannya, ADR 0027); 8b sampler streaming tanpa penyimpanan antara sponge dan sampler: W2 (dua koefisien per siklus) dipilih oleh aturan atas W1 (ADR 0028): SampleNTT 206.48 siklus dan CBD 152 (W1: 305.23 dan 280), 5,290 ALM, 0 M10K, Fmax median 50.220 MHz; 8c matriks A di-stream ke unit PWM dan tidak disimpan: STREAM diadopsi atas STORE (ADR 0029): KeyGen 7,089 lawan 8,268 siklus, 44 lawan 55 M10K;
  8d sampling noise ditumpangtindihkan dengan transformasi: OVERLAP diadopsi atas STREAM (ADR 0030): KeyGen 6,344 dan Encrypt 7,655 siklus (STREAM 7,089 dan 8,549; aritmetika Fase 6 saja 5,475 dan 6,789), ALM dan M10K sama. Semua keluaran bit-exact terhadap model acuan dan K-PKE acuan yang tidak dimodifikasi di kedua simulator; bukti formal dan kontrol negatif sebagaimana disyaratkan; timing terpenuhi pada 40 ns di setiap seed dari setiap konfigurasi (kernel-only).
- Lingkungan: Ubuntu 24.04.4 LTS, OSS CAD Suite 2026-09-23 (Verilator 5.053, Icarus 14.0 devel, slang, SymbiYosys dengan boolector), cocotb 2.1.0, Quartus Prime Lite 25.1std.0 Build 1129.
- Constraint: 40.000 ns (`C.sdc` dari `quartus/phase08_keccak` dan `phase08b_sampler`, `P.sdc` dari `phase08c_smp`: identik dengan constraint Fase 5-7); kompilasi informasi pada 20.000 ns.

## 1. Kriteria selesai (Common RTL Gate, docs/ROADMAP.md), Fase 8
| # | Kriteria | Evidence | Status |
|---|---|---|---|
| CRG-1 | Lint bersih | `evidence/phase08/8a/verify.md`, `evidence/phase08/8b/verify_W1.md`, `evidence/phase08/8b/verify_W2.md`, `evidence/phase08/8c/verify.md` (Verilator -Wall: 0 peringatan untuk setiap modul dan varian) | PASS |
| CRG-2 | Elaborasi bersih (slang) | `evidence/phase08/8a/verify.md`, `evidence/phase08/8b/verify_W2.md`, `evidence/phase08/8c/verify.md` (slang: 0 error, 0 peringatan) | PASS |
| CRG-3 | Bit-exact terhadap model acuan, kedua simulator | 8a: setiap ronde Keccak dan sponge terhadap hashlib; 8b: SampleNTT dan CBD terhadap `tb/golden/sampler_model.py` (sama dengan primitif acuan yang tidak dimodifikasi) termasuk byte XOF yang dikonsumsi; 8c/8d: setiap slot dan hasil akhir terhadap `tb/golden/kpke_smp_model.py` dan K-PKE acuan yang tidak dimodifikasi (KeyGen, Encrypt, Decrypt) | PASS |
| CRG-4 | Kasus sudut sebelum tes | `evidence/phase08/8a/test_plan_8a.md`, `evidence/phase08/8b/test_plan_8b.md`, `evidence/phase08/8c/test_plan_8c.md`, `evidence/phase08/8d/test_plan_8d.md` (ditulis sebelum RTL dan pengukuran apa pun; rencana 8c dan 8d di-commit bersama amandemennya setelah jalankan pertama, lihat bagian 6) | PASS |
| CRG-5 | Regresi: fase sebelumnya masih lulus | `evidence/phase08/8b/verify_W2.md` (menjalankan ulang 8a, Fase 7, dan seluruh set W1), `evidence/phase08/8c/verify.md` (file Fase 6 dan inti tidak dimodifikasi: 0 file berbeda dari basis Fase 7 6874609) | PASS |
| CRG-6 | Parameter terkunci | `.claude/skills/mlkem-guard/scripts/check_params.py` di dalam regresi K0 (semua parameter terkunci sesuai); tidak ada yang berubah dari FIPS 202 atau FIPS 203; konstanta sampler adalah q = 3329 dan CBD eta = 2 dari ML-KEM-768 | PASS |
| CRG-7 | Evidence jumlah siklus konstan | `evidence/phase08/8a/keccak_cycles.md` (306 titik); `evidence/phase08/8b/sampler_cycles_W2.md`, `evidence/phase08/8c/cycles_v1.json`: siklus CBD 8b identik untuk setiap sigma dan N (102 titik), SampleNTT dapat diulang dan, pada W2, sama dengan triple yang dikonsumsi + 49 (3 blok XOF) atau + 61 (4 blok) pada 500 polinomial; 8c/8d: rho tetap dengan 8 rahasia berbeda menghasilkan siklus identik per program di setiap varian | PASS |
| CRG-8 | Properti formal | `evidence/phase08/8a/formal.md`, `evidence/phase08/8b/formal_W2.md` (S1-S6 pada kedua lebar), `evidence/phase08/8c/formal.md`, `evidence/phase08/8d/formal.md` (F1-F5); setiap kontrol negatif gagal sebagaimana disyaratkan | PASS |
| CRG-9 | Evidence Quartus; tidak ada slack negatif atau kegagalan didokumentasikan | `evidence/phase08/8a/selection_worksheet.md`, `evidence/phase08/8b/selection_worksheet.md`, `evidence/phase08/8c/selection_worksheet.md`, `evidence/phase08/8d/selection_worksheet.md`: seed 1-6 pada 40 ns untuk setiap konfigurasi, timing terpenuhi di setiap seed; kompilasi 20 ns (informasi) terpenuhi untuk konfigurasi 8a sampai 8d yang diukur pada 20 ns | PASS |
| CRG-10 | Artefak hasil + pemeriksa klaim | `cmd: python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase08.md` dan `cmd: python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal` | PASS |

## 1b. Sub-langkah Fase 8 (docs/ROADMAP.md Fase 8)
| # | Sub-langkah | Evidence | Status |
|---|---|---|---|
| 8a | Dua ronde per siklus (C5), terukur, aturan diterapkan | `evidence/phase08/8a/selection_worksheet.md`, `docs/decisions/adr/ADR-0027-phase-8a-two-keccak-rounds-per-cycle-c5-rule-result.md` | PASS |
| 8b | Sampler streaming (CBD dari aliran PRF, SampleNTT dari aliran XOF; byte XOF yang dikonsumsi tepat), W1 lalu W2, aturan diterapkan | `evidence/phase08/8b/selection_worksheet.md`, `docs/decisions/adr/ADR-0028-phase-8b-streaming-samplers-output-width-w2-two-coefficients.md` | PASS |
| 8c | Matriks A dibangkitkan on the fly (STREAM lawan STORE), aturan diterapkan | `evidence/phase08/8c/selection_worksheet.md`, `docs/decisions/adr/ADR-0029-phase-8c-matrix-a-streamed-from-the-sampler-into-the-pwm-uni.md` | PASS |
| 8d | Tumpang tindih sampler dengan aritmetika (OVERLAP lawan STREAM), aturan diterapkan | `evidence/phase08/8d/selection_worksheet.md`, `docs/decisions/adr/ADR-0030-phase-8d-noise-sampling-overlapped-with-the-transforms-overl.md` | PASS |

## 2. Yang dihasilkan
| Path | Fungsi |
|---|---|
| `rtl/keccak/keccak_f1600_r2.sv`, `keccak_sponge_r2.sv` | 8a: dua ronde per siklus (12 siklus busy); salinan sponge pada inti itu (14 siklus per permutasi) |
| `rtl/sample/sample_ntt_core.sv`, `cbd2_core.sv`, `keccak_sampler.sv` | 8b: SampleNTT dan CBD streaming (`OUTW` 1 atau 2), wrapper dengan sponge C5 atau K0 (`CORE_R2`) |
| `rtl/sched/kpke_sched_smp.sv`, `kpke_smp_top_s10.sv`, `poly_store_smp.sv`, `kpke_smp_prog_rom.sv` (dibangkitkan) | 8c/8d: sequencer Fase 6 ditambah sampler (`SMPN`, `SMPA`, `PWMS`, `WAIT`, sampling non-blocking, arbitrasi port tulis penyimpanan); top dengan inti S10 |
| `tb/golden/sampler_model.py`, `tb/golden/kpke_smp_model.py` dan tesnya | model acuan lebih dahulu (sampler dengan jumlah byte yang dikonsumsi; program dengan sampling dan pemeriksa hazard) |
| `tb/keccak/`, `tb/sample/`, `tb/smp/` | tes cocotb di kedua simulator dengan kontrol negatif |
| `formal/phase08-keccak-stream/`, `formal/run/run_formal_phase8a.py` sampai `8d.py` | bukti SymbiYosys dan kontrol (8c/8d dengan stub protokol sampler) |
| `quartus/phase08_keccak/`, `phase08b_sampler/`, `phase08c_smp/` | revisi Quartus (kernel-only, pin virtual) |
| `scripts/test/phase8a_verify.sh`, `phase8b_verify.sh`, `phase8cd_verify.sh`, `select_8a.py`, `select_8b.py`, `select_8cd.py`, `gen_kpke_smp_roms.py`, `phase8b_cycles.py`, `build_phase8_report.py` | verifikasi, aturan dari file, pembangkitan ROM, ringkasan siklus, laporan PDF |
| `evidence/phase08/8a`, `8b`, `8c`, `8d` | rencana tes, log verifikasi dan formal, tabel siklus, ekstrak Quartus, worksheet |
| `docs/decisions/0026` sampai `0030` | Cakupan Fase 8 (Accepted), hasil 8a sampai 8d (Proposed) |
| `docs/reports/CHIPATON_Phase8_Report.pdf` | laporan (Bahasa Indonesia) |

## 3. Angka (MEASURED: laporan Quartus dan simulasi; median, t, dan jumlah per operasi adalah INFERENSI / perhitungan tim)
### 3a. 8a, inti Keccak (C5 lawan K0)
| Besaran | K0 (seed 1-6) | C5 (seed 1-6) | Estimasi yang ditulis sebelum pengukuran (ESTIMATE) |
|---|---|---|---|
| ALM, median (min-maks) | 3,566.5 (3,558-3,572) | 6,167.0 (6,152-6,169) | 5,500-7,500: di dalam |
| Register | 1,653 | 1,652 | 1,653 diharapkan: 1 lebih sedikit (penghitung siklus 4 bit, bukan 5) |
| M10K / DSP | 0 / 0 | 0 / 0 | 0 / 0 |
| Timing pada 40.000 ns | terpenuhi di setiap seed | terpenuhi di setiap seed | - |
| Fmax slow corner terendah pada 40 ns, median (min-maks) MHz | 67.675 (56.99-70.39) | 50.655 (47.38-51.67) | "lebih rendah dari K0": ya (-25 %) |
| Siklus per permutasi (sponge) | 26 | 14 | 14 |
| H(ek) 1184 B (siklus) | 389 | 281 | - |
| t per permutasi pada Fmax median (us) | 0.3842 | 0.2764 | rasio 0.538 dari siklus, aturan: C5 harus melebihi 36.440 MHz: terpenuhi (50.655) |
| Siklus Keccak per operasi ML-KEM, median (KeyGen / Encaps / Decaps) | 2,026 / 2,078 / 2,070 | 1,510 / 1,550 / 1,542 | sekitar 1,500: di dalam |
Informasi pada 20.000 ns (seed 1): C5-20 6,178 ALM, setup +4.591 ns (terpenuhi), 64.90 MHz; K0-20 3,573 ALM, +6.893 ns, 76.30 MHz. Fmax di bawah constraint 20 ns tidak dapat dibandingkan dengan angka 40 ns.
Sumber: `evidence/phase08/8a/selection_worksheet.md`, `keccak_cycles.md`, `quartus_C5*.md`, `evidence/phase07/quartus_K0*.md`.


### 3b. 8b, sampler streaming (sampler + sponge C5; sumber: `8b/selection_worksheet.md`, `8b/sampler_cycles_W1.md`, `8b/sampler_cycles_W2.md`)
| Besaran | W1 (satu koefisien per siklus) | W2 (dua per siklus) | ESTIMATE yang ditulis sebelum pengukuran |
|---|---|---|---|
| ALM, median (min-maks) | 5,279.0 (5,271-5,311) | 5,290.0 (5,282-5,308) | W1 6,400-6,700 (hasilnya lebih kecil daripada sponge 8a sendiri, 6,167: tidak diselidiki); W2 +100-300 atas W1: terukur +11 |
| Register / M10K / DSP | 1,913 / 0 / 0 | 1,947 / 0 / 0 | 150-350 lebih banyak daripada sponge; 0 / 0 |
| Timing pada 40.000 ns | terpenuhi di setiap seed | terpenuhi di setiap seed | - |
| Fmax slow corner terendah, median (min-maks) MHz | 51.220 (50.10-55.79) | 50.220 (48.46-53.42) | sekitar 47-51: W2 di dalam, W1 sedikit di atas |
| Siklus SampleNTT per polinomial (rata-rata 500, min-maks) | 305.23 (298-323) | 206.48 (194-231) | sekitar 310 / sekitar 210: di dalam |
| Siklus CBD per polinomial | 280 | 152 | sekitar 280 / sekitar 150: di dalam |
| Siklus sampling per operasi, KeyGen / Encaps (perhitungan tim: 9 SampleNTT + 6 atau 7 CBD) | 4,427 / 4,707 | 2,770 / 2,922 | sekitar 4,500 / 4,800 dan 2,800 / 2,900: di dalam |
| Gerbang (M10K 0, DSP 0, ALM paling banyak 12,573, timing terpenuhi, Fmax median setidaknya median S10 44.320 MHz) | LULUS | LULUS | |
| Aturan W1 lawan W2 (t = siklus / Fmax, SampleNTT dan CBD) | t 5.959 / 5.467 us | t 4.111 / 3.027 us: W2 dipilih | |
Dengan sponge K0 (informasi, seed 1): W1 3,470 ALM, W2 3,551 ALM, setup +23.9 dan +23.5 ns pada 40 ns; pada 20 ns dengan sponge C5 keduanya terpenuhi (+3.892 dan +4.214 ns). Siklus SampleNTT W2 sama dengan triple yang dikonsumsi + 49 (3 blok XOF) atau + 61 (4 blok) pada setiap dari 500 polinomial; pada W1 besaran yang sama bervariasi (41-48 untuk 3 blok).

### 3c. 8c dan 8d, seluruh program K-PKE dengan sampling (inti S10, sampler W2, sponge C5; sumber: `8c/selection_worksheet.md`, `8d/selection_worksheet.md`, tabel siklus)
| Besaran | STORE (acuan 8c) | STREAM (8c) | OVERLAP (8d) | ESTIMATE yang ditulis sebelum pengukuran |
|---|---|---|---|---|
| ALM, median (min-maks) | 10,958.0 (10,941-10,969) | 10,995.5 (10,958-11,032) | 10,992.5 (10,954-11,012) | sekitar 11,000-12,500: di dalam |
| Register | 3,342-3,378 | 3,377-3,395 | 3,368-3,414 | beberapa puluh lebih banyak untuk STREAM: sekitar +35 |
| M10K / DSP | 55 / 26 | 44 / 26 | 44 / 26 | STREAM sekitar 10-14 M10K lebih sedikit: 11 lebih sedikit |
| Timing pada 40.000 ns | terpenuhi di setiap seed | terpenuhi di setiap seed | terpenuhi di setiap seed | - |
| Fmax slow corner terendah, median (min-maks) MHz | 42.270 (41.21-44.28) | 43.355 (40.37-45.66) | 43.755 (42.14-46.38) | sekitar 40-44: di dalam |
| Siklus KeyGen (rata-rata atas masukan yang sama) | 8,268.1 | 7,089.1 | 6,344.1 | STORE sekitar 8,400, STREAM sekitar 7,300, OVERLAP sekitar 6,300: di dalam |
| Siklus Encrypt | 9,727.6 | 8,548.6 | 7,654.6 | sekitar 9,900 / 8,750 / 7,600: di dalam |
| Siklus Decrypt (tanpa sampling) | 3,109 | 3,109 | 3,109 | Fase 6: 3,109 |
| t = siklus / Fmax median, KeyGen / Encrypt (us) | 195.6 / 230.1 | 163.5 / 197.2 | 145.0 / 174.9 | |
| Aturan | acuan | STREAM atas STORE: diadopsi | OVERLAP atas STREAM: diadopsi | |
Informasi pada 20.000 ns (seed 1): STORE terpenuhi (+0.992 ns, 52.61 MHz, 11,058 ALM), STREAM terpenuhi (+1.783 ns, 54.89 MHz, 11,031 ALM), OVERLAP terpenuhi (+1.535 ns, 54.16 MHz, 11,049 ALM); static timing kernel-only, bukan sistem pada 50 MHz.
Sebagai pembanding, top Fase 6 dengan inti S10 (hanya aritmetika, masukan diberikan oleh testbench): 5,553 ALM, 51 M10K, 5,475 / 6,789 / 3,109 siklus (MEASURED, Fase 6). Sistem fase ini menambah sampler (sekitar 5,300 ALM) dan siklus sampling; hashing kunci dan kontrol KEM belum ada di dalamnya.
Pada STRESS (hanya untuk tes) 763 siklus beat sampler ditahan oleh penulisan sequencer: arbitrasi port tulis penyimpanan teruji, hasil tetap bit-exact.

## 4. Standar dan sumber yang dipatok
FIPS 202 seperti di Fase 7; FIPS 203 Algoritma 7 (SampleNTT) dan Algoritma 8 (SamplePolyCBD) dengan eta = 2 (ML-KEM-768), dengan PRF = SHAKE256 dan XOF = SHAKE128 seperti di `tb/golden/primitives.py` acuan yang tidak dimodifikasi. Permutasi tetap 24 ronde; tidak ada parameter atau aritmetika FIPS 203 yang berubah (C1).

## 5. Cakupan dan batas
- Hanya simulasi, formal, dan static timing. Tidak ada papan; Fmax bersifat kernel-only dengan pin virtual. "Timing terpenuhi pada 20 ns" adalah static timing alur ini, bukan sistem pada 50 MHz. Tidak ada klaim tentang kecepatan terhadap perangkat lunak, daya, atau side channel (C3).
- Siklus per operasi adalah aritmetika Fase 6 ditambah sampling di dalam satu sequencer, MEASURED dalam simulasi per program; hashing kunci (G, H, J), kompresi, encoding, transformasi FO, dan kontrol KEM belum ada di perangkat keras (Fase 9); seed ditulis oleh testbench.
- Hanya satu sampler: matriks dan noise disampel satu demi satu. Tumpang tindih 8d menyembunyikan sampling noise di balik transformasi; streaming matriks (terikat sampler, sekitar 206 siklus per entri) tidak disembunyikan.
- Formal mencakup properti kontrol dan rentang (inti NTT diabstraksikan, sampler diganti stub protokol pada 8c/8d), bukan nilai; nilai dicakup oleh simulasi terhadap model acuan dan hashlib. `bytes_o` inti SampleNTT adalah 16 bit dan bukti mengasumsikan paling banyak 8,000 word aliran per polinomial.
- Register seed tidak dihapus setelah program (tidak ada klaim side-channel; waktu-konstan di sini berarti jumlah siklus tidak bergantung pada nilai rahasia).
- Angka Quartus: seed 1-6 per konfigurasi (kernel-only), beberapa kompilasi dijalankan paralel pada salinan direktori proyek dengan sumber dan pengaturan identik (disebut di ekstrak).

## 6. Penyimpangan, kegagalan, dan masalah terbuka
- Dua cacat RTL ditemukan oleh verifikasi dan diperbaiki: (1) tag valid pipeline hasil PWMS tidak punya reset (ditemukan oleh jalankan formal pertama; tidak terlihat dalam simulasi); (2) start sampler pada siklus yang sama dengan pulsa `done_o` sampel sebelumnya menghapus penanda PWMS dan menggantung program (ditemukan hanya oleh program STRESS khusus-tes). Kedua bukti dan semua simulasi dijalankan ulang pada RTL akhir; revisi Quartus 8c dikompilasi ulang dua kali untuk perubahan RTL.
- Satu nilai harapan berubah setelah melihat hasil (Amandemen A1 8b): penghitung permutasi sponge boleh satu di atas hitungan acuan ketika jendela byte sudah mengambil word terakhir blok akhir sementara keluaran ditahan (1 dari 500 kasus K0 pada W1, kedua simulator); keluaran tidak terpengaruh. Versi tes pertama juga salah menghitung permutasi absorb untuk pesan 168 byte atau lebih (kesalahan tes, dikoreksi sebelum jalankan tercatat mana pun).
- Kontrol formal: NC-F3 dan NC-F4 tidak dapat gagal di dalam kedalaman BMC (pelanggarannya hanya terjangkau oleh langkah induksi, yang dilaporkan SymbiYosys sebagai UNKNOWN); NC-F2 adalah kontrol yang dipakai untuk 8c dan 8d (Amandemen A1). NC-HAZ 8d adalah mutasi ROM, karena mengabaikan `WAIT` tidak merusak jadwal (transformasi yang ditumpangtindihkan lebih panjang daripada satu sampel noise).
- ESTIMATE meleset: ALM yang ditambah W2 (diperkirakan 100-300, terukur +11); top sampler + C5 lebih kecil daripada sponge sendiri (tidak diselidiki); estimasi lain pada rencana berada dalam rentangnya (bagian 3b, 3c).
- Proses: rencana 8c dan 8d ditulis sebelum RTL tetapi di-commit bersama amandemennya (commit rencana f614b79 mengikuti pekerjaan model acuan, bukan RTL); satu jalankan verifikasi W2 8b dibuang karena suatu perintah sesi operator mematikan proses simulatornya, dan skrip dijalankan ulang dari awal (`8b/verify_W2.md`); evidence Quartus W1 8b diambil pada commit 794db0d, sebelum penggantian nama konstanta lokal (`Q` menjadi `QC`) pada inti sampler, dan set tes W1 dijalankan ulang sesudahnya.
- Baseline K0 8a, catatan 8a, dan angka Quartus-nya ada di bagian 3a dan di `evidence/phase08/8a/`.
- Critical Warning 15725 (clock pin virtual) di setiap kompilasi, seperti fase sebelumnya; Warning 10036 (sink `unused_ok`); tidak ada yang di-waive.

## 7. Keputusan yang diperlukan
- ADR 0027 (C5 sebagai inti Keccak, PENDING #29), ADR 0028 (W2 sebagai sampler 8b, PENDING #30), ADR 0029 (STREAM, PENDING #31), ADR 0030 (OVERLAP, PENDING #32): semuanya Proposed; tim menerima atau menolak masing-masing. PENDING #25 (pemeriksaan masukan FIPS 203 di perangkat keras atau di HPS) dan #26 (protokol checkpoint) masih terbuka.
- Fase 9 (integrasi ML-KEM-768 penuh dalam simulasi) belum dimulai; risiko jadwal terhadap tier T2 dan T3 sebelum 2026-10-08 dinyatakan di ADR 0026 dan merupakan hak tim.

## 8. Klaim yang dibuat pada fase ini
Tidak ada yang ditulis untuk juri atau teks proposal. Baris ROADMAP C5, C6b-W1, C6b-W2, C6c-STORE, C6c, dan C6d diisi dari evidence di atas.

## 9. Mereproduksi
```bash
. scripts/env.sh
scripts/test/phase8a_verify.sh; KS_OUTW=2 scripts/test/phase8b_verify.sh; scripts/test/phase8cd_verify.sh
python3 formal/run/run_formal_phase8a.py; python3 formal/run/run_formal_phase8b.py all; python3 formal/run/run_formal_phase8c.py; python3 formal/run/run_formal_phase8d.py
cd quartus/phase07_keccak && ./run_k0_seeds.sh; cd ../phase08_keccak && ./run_c5.sh; cd ../phase08b_sampler && ./run_sm1.sh && ./run_sm2.sh; cd ../phase08c_smp && ./run_smp.sh; cd ../..
python3 scripts/quartus/select_8a.py; python3 scripts/quartus/select_8b.py; python3 scripts/quartus/select_8cd.py
python3 scripts/build/gen_kpke_smp_roms.py --check
python3 scripts/build/build_phase8_report.py
python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase08.md
python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal
```

## 10. Persetujuan
- [x] Penyetuju manusia (nama, tanggal): Jose (Tim J5), 2026-10-03
      Fase berikutnya dimulai hanya setelah anggota tim mencentang kotak ini. Claude tidak pernah mencentangnya.
