<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Fase 8c: matriks A dibangkitkan on the fly (tanpa penyimpanan Â) - test plan dan aturan adopsi

Ditulis 2026-10-03, sebelum RTL 8c apa pun dan sebelum pengukuran 8c apa pun (CRG-4). Lingkup: `docs/ROADMAP.md` Fase 8c; ADR 0026 (Accepted: 8a-8d lanjut, masing-masing dengan rencana dan aturan sendiri). Chat 2026-10-03 (tanpa nama): kerjakan 8b, 8c, dan 8d tanpa berhenti di antaranya, lalu laporan dan hasilnya.
Basis (semuanya tidak diedit, beku): sequencer dan store Fase 6 (`rtl/sched/kpke_sched.sv`, `poly_store.sv`, `pwm_unit.sv`, `gamma_rom.sv`), inti NTT/INTT S10 (`rtl/ntt/ntt_core_s10_p5.sv`, ADR 0025 Proposed), sampler 8b (`rtl/sample/`, tahap W2 bila ia yang dipilih oleh aturan bagian 5 `evidence/phase08/8b/`, selain itu W1) pada sponge C5 (ADR 0027 Proposed; PENDING #29 terbuka).
Label: MEASURED, INFERENCE, ESTIMATE, NOT MEASURED, perhitungan tim. Matematika terkunci (C1): satu-satunya perubahan adalah dari mana koefisien Â berasal.

## 1. Apa yang dibangun (satu perubahan: Â tidak disimpan, sampelnya langsung masuk ke unit pointwise)
Hari ini (Fase 6) sembilan polinomial matriks Â[i][j] (slot 3i + j) ditulis oleh testbench dan dibaca dari store oleh pass PWM. Di 8c sampler menghasilkannya saat pass PWM berjalan.
File baru (file Fase 6 tidak dimodifikasi; sequencer baru adalah modul terpisah agar evidence Fase 6 tetap valid):
- `tb/golden/kpke_smp_model.py`: program golden dengan sampling, ditulis lebih dulu. Operasi ditambahkan ke daftar Fase 6: `SMPN d ctr` (slot d <- SamplePolyCBD_2(PRF(seed, ctr)), FIPS 203 Algoritma 8 dengan eta = 2), `SMPA d m` (slot d <- SampleNTT(rho || j || i) dengan m = 3i + j, yaitu Â[i][j]; baseline),
  `PWMS d m b F L` (seperti PWM, tetapi operand a adalah aliran sampler Â[i][j] sebagai ganti slot a). Â[i][j] = SampleNTT(rho || j || i) adalah entri yang disimpan di slot 3i + j oleh model Fase 6 (`_matrix`), jadi setiap program menjaga aritmetika Fase 6 persis.
  Dua set program: STORE (baseline: `SMPA` untuk sembilan entri ke slot 0-8, lalu op `PWM` tidak berubah; nomor slot Fase 6, 24 slot) dan STREAM (`PWMS`; slot matriks tidak ada, jadi slot 9-20 dinomori ulang 0-11 dan store punya 12 slot).
  Decrypt tidak punya sampling dan sama di kedua set (dinomori ulang di STREAM).
- `scripts/build/gen_kpke_smp_roms.py` membangkitkan `rtl/sched/kpke_smp_prog_rom.sv` dari model (seperti ROM Fase 6 dibangkitkan). Word operasi: {opc[3:0], first, last, dst[4:0], a[4:0], b[4:0]}; opc 6 SMPN, 7 SMPA, 8 PWMS (opc 0-5 seperti di Fase 6).
- `rtl/sched/kpke_sched_smp.sv`: sequencer `kpke_sched` Fase 6 ditambah sampler: `parameter STREAM_A` (1 mengimplementasikan `PWMS`; 0 adalah build STORE), `NPOLY`, `CORE_RDLAT`; sampler `keccak_sampler` (C5) di dalamnya; feeder pesan (34 byte rho || j || i atau 33 byte seed || N berasal dari dua register seed 256-bit
  yang ditulis lewat port seed saat idle, ditambah byte indeks dari operasi); `SMPN`/`SMPA` memblokir (sequencer menunggu `done_o` sampler); beat (dua koefisien, satu pasangan store) ditulis ke slot d, pasangan demi pasangan.
  `PWMS`: beat sampler memberi makan operand a unit PWM; operand b (ŝ atau ŷ), word akumulator, dan gamma dialamati satu siklus lebih awal oleh counter beat (alamat beat berikutnya, jadi data selaras saat beat tiba);
  register geser valid/indeks/last selebar latensi PWM (7 siklus) menandai hasil, yang diakumulasi atau disimpan menurut indeks; gelembung (tanpa beat) tidak memberi makan apa pun; `coef_ready_i` selalu 1 di `PWMS`.
- `rtl/sched/kpke_smp_top_s10.sv`: top Quartus (sequencer + store + PWM + inti S10 + sampler), parameter `VAR` (0 STORE, 1 STREAM; memilih isi ROM saat kompilasi) dan `NPOLY` (24 atau 12).
Seed (rho, sigma atau r) adalah masukan yang ditulis testbench (tanpa G/H/J perangkat keras di sini; ROADMAP "belum boleh": kendali KEM penuh, hashing kunci).

## 2. Model golden lebih dulu
`tb/golden/tests/test_kpke_smp_model.py`: program STORE dan STREAM dijalankan pada slot Python dengan primitives golden yang tidak diubah (`sample_ntt`, `sample_poly_cbd`, `PRF`, `ntt`, `intt`, `multiply_ntts`), dan hasil akhir dibandingkan dengan K-PKE golden yang tidak diubah: t̂ KeyGen sama dengan `byte_decode(12, ek_PKE)`;
u dan v Encrypt (terkompresi, ter-encode) sama dengan ciphertext `k_pke_encrypt`; untuk seed acak; hasil STREAM sama dengan hasil STORE di slot logis 9-20.

## 3. Kasus sudut (didaftar sebelum test)
- Entri Â: kesembilan urutan byte (j, i), termasuk i = j dan pemakaian transposisi di Encrypt (slot 3j + i); rho yang entrinya butuh blok XOF ke-4 (nilai rho 4-blok dari 8b).
- Pipeline `PWMS`: stall sampler (gelembung triple ditolak) di tengah pass, di beat pertama, di beat terakhir, di batas blok (stall sponge 14 siklus); pass pertama/tengah/terakhir (akumulator tidak dipakai pada pass pertama, disimpan hanya pada yang terakhir); operand b dan gamma selaras dengan beat setelah setiap panjang gelembung.
- `SMPN`: nilai counter 0-6 (KeyGen 0-5, Encrypt 0-6); sigma dan r semua-nol dan semua-satu.
- Kedua register seed ditulis ulang di antara program; program dimulai saat port seed menulis (tulis saat sibuk diabaikan).
- Siklus konstan: rho tetap dan sigma/r bervariasi memberi jumlah siklus identik (rahasia hanya masuk ke CBD, yang punya hitungan tetap); masukan sama memberi hitungan sama; dengan rho bervariasi hitungan berbeda hanya lewat pola penolakan publik (dilaporkan, bagian 4 V6).
- Reset di tengah program; start saat sibuk diabaikan; perilaku Fase 6 operasi lain tidak berubah.

## 4. Test
| ID | Pemeriksaan | Alat | Disyaratkan |
|---|---|---|---|
| V1 | Lint sequencer, ROM, dan top baru, kedua `VAR` (CRG-1, CRG-2) | Verilator `-Wall`, slang | 0 peringatan, 0 error |
| V2 | Model golden sama dengan K-PKE golden yang tidak diubah; STREAM sama dengan STORE di slot logis 9-20; ROM dibangkitkan ulang byte demi byte (`scripts/build/gen_kpke_smp_roms.py --check`) | pytest | semua sama, 0 selisih |
| V3 | Top: KeyGen, Encrypt, Decrypt pada seed acak dan seed sudut, STORE dan STREAM: setiap slot logis (yang ada) yang dibaca balik sama dengan model, hasil akhir sama dengan K-PKE golden; counter (ntt, intt, pwm termasuk pwms, smp) sama dengan hitungan model | cocotb, kedua simulator (CRG-3) | semua sama |
| V4 | Cakupan stall `PWMS`: per pass jumlah gelembung dan posisinya dicatat dari handshake sampler; semua kasus bagian 3 terlihat (probe khusus test) | cocotb | setiap kasus terlihat, hasil sama |
| V5 | Siklus konstan (CRG-7): rho tetap, 8 seed berbeda: jumlah siklus identik per program; masukan sama dua kali: hitungan sama; siklus per program per rho dicatat (STORE dan STREAM) | cocotb | identik per rho tetap |
| V6 | Kontrol negatif (salinan khusus test): NC-IJ byte pesan i, j ditukar; NC-CTR counter CBD kurang satu; NC-ALIGN alamat b/acc/gamma PWMS terlambat satu beat; NC-VALID hasil PWM ditulis untuk gelembung; NC-ACC akumulator tidak dipakai pada pass tengah | cocotb | pemeriksaan bit-exact FAIL |
| V7 | Formal (file baru, SymbiYosys; sampler dan inti NTT diganti stub protokol): F1 state sequencer legal dan program counter dalam rentang; F2 sampler dimulai hanya saat idle dan tulis seed tidak pernah terjadi saat sibuk; F3 `PWMS` menerima paling banyak 128 beat per pass dan tag pipeline tidak pernah melebihinya; F4 tidak ada tulis store sequencer dan penulis beat pada siklus yang sama | SymbiYosys | PASS; kontrol NC-F3 GAGAL |
| V8 | Regresi: file Fase 6 tidak dimodifikasi (`git diff --name-status` `rtl/sched/kpke_sched.sv` dst. kosong); `scripts/test/phase8b_verify.sh` dan verifikasi Fase 6 dijalankan ulang | skrip | PASS |
| V9 | Quartus (kernel-only, virtual pin): `kpke_smp_top_s10` STORE (NPOLY 24) dan STREAM (NPOLY 12), 40.000 ns, seed 1-6 masing-masing, satu per satu; informasi: seed 1 pada 20.000 ns | `quartus_sh`, `/quartus-report` | evidence diekstrak |

## 5. Aturan adopsi (gaya ADR 0012, ditetapkan sebelum mengukur; tanpa toleransi)
STREAM diadopsi atas STORE hanya bila semua berikut berlaku:
1. V1-V8 PASS di kedua simulator dan setiap kontrol gagal seperti disyaratkan (kedua varian benar).
2. Fit berhasil untuk keduanya dan timing terpenuhi pada 40.000 ns di setiap seed untuk STREAM.
3. Dengan F median atas seed 1-6 dari Fmax slow corner terendah pada 40 ns dan c rata-rata siklus atas himpunan rho yang sama (himpunan V5, sponge C5): t = c / F lebih rendah untuk STREAM daripada STORE untuk KeyGen dan untuk Encrypt.
4. M10K(STREAM) <= M10K(STORE) di setiap seed (tujuan tidak menyimpan Â adalah memori; angka ALM dilaporkan terhadap denominator fitter; tidak ada batas ALM di sini karena tim tidak menetapkannya untuk sistem utuh, C5).
Jika aturan gagal, 8c dicatat sebagai terukur dan tidak diadopsi; STORE tetap menjadi acuan 8c dan 8d dibangun di atas varian yang ditinggalkan aturan.

## 6. ESTIMATE yang ditulis sebelum mengukur (metode dan asumsi; bukan pengukuran)
- Siklus (perhitungan tim dari Fase 6 dengan S10: KeyGen 5,475, Encrypt 6,789, Decrypt 3,109 MEASURED, dan sampler W2 8b: sekitar 210 siklus per entri matriks dan sekitar 152 per polinomial noise, ditambah sekitar 10 siklus overhead sequencer per operasi sampling):
  KeyGen STORE sekitar 5,475 + 9 x 220 + 6 x 162 = sekitar 8,400, Encrypt sekitar 6,789 + 1,980 + 7 x 162 = sekitar 9,900; STREAM mengganti setiap pass PWM 136 siklus dengan pass terbatas-sampler sekitar 228 siklus: KeyGen sekitar 7,300, Encrypt sekitar 8,750 (sekitar 15 % lebih sedikit siklus dari STORE).
  Decrypt tidak berubah (3,109). Ini memakai angka W2; dengan W1 setiap langkah sampling sekitar 100 siklus lebih panjang.
- Memori: STORE 24 slot (73,728 bit koefisien, 51 M10K di top Fase 6 dengan S10 sebagaimana MEASURED, 24 di antaranya di inti) terhadap STREAM 12 slot; store slot adalah sekitar separuh M10K di luar inti, jadi sekitar 10-14 blok M10K lebih sedikit (INFERENCE dari struktur blok, tidak diukur).
- ALM/register: sequencer + sampler di atas top Fase 6 (5,553 ALM MEASURED) dan sampler 8b (median W1 5,279 ALM MEASURED): sekitar 11,000-12,500 ALM untuk varian mana pun; STREAM menambah register geser valid/indeks (sekitar 9 bit x 7 stage) dan counter beat: beberapa puluh register. Fmax: sampler 8b (51.2 MHz W1) dan inti S10 (44.3 MHz) adalah jalur terpisah; jalur sambungan baru (beat ke operand PWM) pendek; harapkan sistem dekat inti S10, sekitar 40-44 MHz (keyakinan rendah).

## 7. Tidak dicakup
Perangkat keras (tanpa papan); hashing kunci (G, H, J) dan seluruh KEM; tumpang tindih sampling dengan aritmetika (8d); kompresi dan encoding; seed selain 6; seed expander perangkat keras untuk rho dan sigma.
Formal mencakup kendali, bukan nilai (simulasi terhadap golden mencakup nilai).

## 8. Amandemen A1 (2026-10-03, ditulis setelah run pertama RTL, test, dan bukti formal; aturan adopsi bagian 5 tidak berubah)
1. Kontrol formal diwujudkan secara berbeda: V7 rencana menyebut kontrol NC-F3 (batas beat PWMS). Pelanggaran F3 butuh 128 beat, yaitu lebih dari 128 siklus, melewati kedalaman dasar BMC (12), dan pelanggaran yang hanya dapat dicapai langkah induksi dilaporkan SymbiYosys sebagai UNKNOWN, bukan FAIL. Kontrolnya karenanya NC-F2 (register seed ditulis saat sequencer sibuk), yang gagal di base case;
   F3 sendiri dibuktikan (induksi lulus) dengan invarian pendukung: dalam pass PWMS counter beat sama dengan beat yang diserahkan stub sampler; counter drain 0 sampai beat terakhir; tag hasil yang lebih muda dari counter drain dikurangi satu kosong; tanpa OVERLAP penulis beat dipersenjatai hanya di state sampling memblokir.
2. Temuan run formal pertama (RTL berubah): tag valid `tag_v` pipeline hasil PWMS tidak punya reset, sehingga setelah power-up mereka bisa memuat sampah selama 7 siklus; tulis akumulator liar mungkin secara prinsip (tidak ada program yang mencapai PWMS dalam 7 siklus setelah reset, jadi tidak ada simulasi yang bisa menunjukkannya). `tag_v` kini punya reset asinkron; tag indeks tetap register data.
3. File baru akibat lint: Verilator `-Wall` menandai `poly_store.sv` Fase 6 untuk NPOLY < 17 (indeks word 12-bit lebih lebar dari indeks memori). File Fase 6 beku, jadi `rtl/sched/poly_store_smp.sv` adalah salinan dengan lebar indeks diambil dari kedalaman (perilaku sama). Inti sampler 8b menamai konstanta lokal `Q`, yang menyembunyikan `ntt_pkg::Q` saat dikompilasi bersama file Fase 6 (VARHIDDEN); kini `QC` (hanya ganti nama).
   Evidence Quartus W1 8b diambil pada commit 794db0d sebelum penggantian nama; set test W1 dijalankan ulang sesudahnya (verifikasi 8b, V10).
4. Masukan identik antar varian: testbench menarik masukan acaknya dengan seed yang sama untuk setiap varian agar rata-rata siklus dua varian atas himpunan rho yang sama, seperti disyaratkan bagian 5.
5. Angka siklus run smoke pertama (STORE KeyGen 8,268-8,276, Encrypt 9,716-9,738; STREAM KeyGen 7,076-7,092, Encrypt 8,546-8,559) dekat dengan ESTIMATE bagian 6 (sekitar 8,400 / 9,900 dan 7,300 / 8,750); angka akhir ada di worksheet pemilihan.
