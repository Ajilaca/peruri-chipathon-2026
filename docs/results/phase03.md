<!-- claim-lint: skip-file (result artifact: internal status page, not proposal text) -->
# Hasil - Fase 3: Eksplorasi multi-lane (L = 1/2/4/8, konfigurasi C2)

- Status: DONE
- Tanggal (UTC): 2026-09-29 15:56; diperbarui 2026-09-30 (jalankan ulang formal; eksperimen tambahan K2/K1;
  ADR 0005)
- Git commit (HEAD saat diverifikasi): 7b1d467 untuk sapuan C2; dbefa86 untuk pembaruan 2026-09-30
- Titik operasi terpilih (ADR 0005, Accepted 2026-09-30): C2-K2-K1 pada L = 8 (Bagian 3b)
- Lingkungan: sama dengan Fase 1/2 -- Ubuntu 24.04.4 LTS, OSS CAD Suite 2026-09-23, cocotb 2.1.0,
  pytest 9.1.1, Quartus Prime Lite 25.1std.0 Build 1129 (`~/altera_lite/25.1std`).

Catatan proses, dinyatakan apa adanya: `QUARTUS_BIN` di `scripts/tooling.env` kosong pada awal
fase ini (Quartus sebelumnya dicari manual, sesuai butir terbuka Fase 1/2 sendiri); lokasinya
ditemukan di `~/altera_lite/25.1std/quartus/bin` dan diisi pada fase ini agar `scripts/env.sh` menaruh Quartus di
PATH seterusnya. Ini perbaikan konfigurasi mesin lokal, bukan perubahan desain.

## 1. Kriteria selesai (Common RTL Gate, docs/ROADMAP.md, disalin tanpa perubahan)
| # | Kriteria | Evidence | Status |
|---|---|---|---|
| CRG-1 | Lint bersih | `cmd: verilator --lint-only -Wall --timing -sv rtl/ntt/*.sv rtl/mem/*.sv --top-module ntt_core_c2 -GNUM_LANES=<L>` untuk L dalam {1,2,4,8} (masing-masing 0 peringatan) | PASS |
| CRG-2 | Elaborasi bersih (slang) | `cmd: slang --top ntt_core_c2 rtl/ntt/*.sv rtl/mem/*.sv` (0 error, 0 peringatan; elaborasi NUM_LANES=1 bawaan) | PASS |
| CRG-3 | Bit-exact terhadap model acuan, kedua simulator | `evidence/phase03/cocotb_regression.txt` (16/16 di Icarus DAN Verilator, keempat L) | PASS |
| CRG-4 | Kasus sudut sebelum tes | `evidence/phase03/test_plan.md`, ditulis sebelum `rtl/ntt/ntt_core_c2.sv` | PASS |
| CRG-5 | Regresi: tes Fase 0-2 masih lulus | `cmd: python3 -m pytest tb/golden/tests/ -q` (23/23), `cmd: python3 tb/ntt/run_ntt_tests.py icarus` (10/10, C0 tidak terpengaruh), `cmd: python3 tb/mem/run_mem_tests.py icarus` (12/12, C1 tidak terpengaruh) | PASS |
| CRG-6 | Parameter terkunci | `cmd: python3 .claude/skills/mlkem-guard/scripts/check_params.py` | PASS |
| CRG-7 | Evidence jumlah siklus konstan | `evidence/phase03/cocotb_regression.txt` -- konstan per L, dan L=1 sama persis dengan C0/C1 (897/1153); L>1 lebih rendah, tidak sama, yang merupakan efek lane paralel yang diharapkan/terukur, bukan stall | PASS |
| CRG-8 | Properti formal | `evidence/phase03/formal_rerun.md` (`cmd: python3 formal/run/run_formal_slang.py`, 19/19 hasil sesuai harapan): k-induction PASS untuk L=1, 2, 4, dan 8 pada C2 (dan pada C2-K2 / C2-K2-K1 tambahan) untuk bank_overflow_o == 0, handshake busy/done, dan invarian rentang t_q / layer_q; empat kontrol negatif gagal sebagaimana mestinya. UNKNOWN L=2/4/8 sebelumnya (`evidence/phase03/formal_verification.txt`) adalah artefak harness formal (ROM dimodelkan sebagai state memori bebas pada langkah induksi), dikoreksi hanya di harness -- RTL tidak berubah (Bagian 6). Cakupan: hanya properti ini, bukan bit-exactness NTT/INTT | PASS |
| CRG-9 | Evidence Quartus; tidak ada slack negatif atau kegagalan didokumentasikan | `evidence/quartus/C2-L1.md`, `evidence/quartus/C2-L2.md`, `evidence/quartus/C2-L4.md`, `evidence/quartus/C2-L8.md` -- keempatnya dikompilasi dan diukur; keempatnya punya worst setup slack negatif (timing TIDAK terpenuhi); L=8 juga melebihi anggaran 10,478 ALM pada ADR 0004 (11,446 ALM terukur); kegagalan didokumentasikan, dan itu yang diminta kriteria | PASS |
| CRG-10 | Artefak hasil + pemeriksa klaim | `cmd: python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase03.md` dan `cmd: python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal` | PASS |

CRG-9 semula ditandai FAIL, seperti pada Fase 1 dan 2: timing tidak terpenuhi pada clock sementara 20.000 ns
sudah diperkirakan (belum ada ADR clock target) dan didokumentasikan, tidak disembunyikan. Pada 2026-10-05 tim
memilih pembacaan bahwa kegagalan yang terdokumentasi dihitung PASS; slack terukur tidak berubah. CRG-8 berstatus FAIL pada versi pertama file ini (2026-09-29: L=1 terbukti, L=2/4/8
UNKNOWN). Statusnya PASS sejak 2026-09-30, setelah penyebab UNKNOWN ditemukan di harness formal
dan setiap L dibuktikan ulang dengan kontrol negatif (Bagian 6); PASS ini mencakup properti
kontrol/kapasitas bank yang dinyatakan, bukan kebenaran aritmetika.

## 1b. Kriteria PASS Fase 3 (docs/ROADMAP.md Fase 3, di luar tabel CRG)
| # | Kriteria | Evidence | Status |
|---|---|---|---|
| 1 | Keempat konfigurasi benar | `evidence/phase03/cocotb_regression.txt` (bit-exact + roundtrip, semua L, kedua simulator) | PASS |
| 2 | Empat file evidence Quartus | `evidence/quartus/C2-L1.md` .. `C2-L8.md` | PASS |
| 3 | Tabel perbandingan lengkap | `docs/ROADMAP.md` matriks ablasi, baris C2-L1/L2/L4/L8 | PASS |
| 4 | ADR yang memilih L (atau mempertahankan L dapat dikonfigurasi) ditandatangani tim | `docs/decisions/adr/ADR-0004-phase-3-lane-count-l-selection-criterion.md` (Accepted, Faza Dzil, 2026-09-29) menetapkan *kriteria* sebelum pengukuran; `docs/decisions/adr/ADR-0005-apply-adr-0004-l-selection-to-the-c2-k2-k1-supplementary-con.md` (Accepted, Faza Dzil, 2026-09-30) menerapkannya dan memilih L = 8 pada konfigurasi C2-K2-K1 yang dioptimasi (Bagian 3b) | PASS |

## 2. Yang dihasilkan
| Path | Fungsi |
|---|---|
| `tb/mem/bank_model.py` (diperluas) | Menambah `zeta_index_of` (indeks twiddle per lane dalam bentuk tertutup) dan `reference_zeta_trace` (aturan sekuensial C0, dinyatakan ulang sebagai kebenaran dasar) |
| `scripts/build/gen_lane_schedule.py` | Memverifikasi rumus zeta bentuk tertutup terhadap aturan sekuensial (0 ketidakcocokan, kedua arah) dan cakupan lane p per sub-siklus (tanpa duplikat, tanpa celah), untuk keempat L |
| `rtl/mem/poly_mem_multiport.sv` | Memori berbank multi-port: 2*NUM_LANES port vektor packed (bukan array unpacked -- lihat Bagian 6), `en_i` aktif per port, diagnostik `bank_overflow_o` |
| `rtl/ntt/ntt_core_c2.sv` | Konfigurasi C2: NUM_LANES butterfly paralel/siklus, tanpa penghitung zeta sekuensial bersama (diganti bentuk tertutup kombinasional per lane), FSM/lintasan penskalaan selebihnya tidak berubah dari C0/C1 |
| `rtl/ntt/ntt_core_c2_l1.sv` .. `_l8.sv` | Pembungkus top-level Quartus tipis, masing-masing mengunci satu nilai NUM_LANES (pola sama dengan C0 lawan C1: satu entitas top yang dapat disintesis per konfigurasi) |
| `tb/ntt/test_ntt_core_c2.py` | cocotb: bit-exact, roundtrip, siklus-konstan-per-L, `bank_overflow_o` diperiksa setiap siklus |
| `tb/ntt/run_ntt_c2_tests.py` | Menjalankan keempat L melalui satu simulator |
| `formal/phase03-multilane/ntt_core_c2_formal_top.sv`, `ntt_core_c2_l{1,2,4,8}_safety.sby` | Bukti ulang formal properti keselamatan FSM + bank_overflow_o==0, per L |
| `quartus/phase03_multilane_c2/` | Proyek Quartus, revisi C2-L1/L2/L4/L8, metodologi pin virtual dan clock sementara yang sama dengan C0/C1 |
| `docs/decisions/adr/ADR-0004-phase-3-lane-count-l-selection-criterion.md` | ADR: kriteria pemilihan L, ditetapkan sebelum sapuan diukur |
| `evidence/phase03/test_plan.md` | Rencana tes CRG-4, ditulis sebelum RTL apa pun |
| `evidence/phase03/lane_schedule_verification.txt` | Log mentah bukti rumus zeta + cakupan p |
| `evidence/phase03/cocotb_regression.txt` | Log mentah lulus/gagal cocotb + jumlah siklus, kedua simulator, keempat L |
| `evidence/phase03/formal_verification.txt` | Hasil formal pertama per L (L>1 UNKNOWN) dan tulisan penyelidikan pertama; kesimpulannya digantikan oleh baris berikutnya |
| `formal/run/run_formal_slang.py`, `evidence/phase03/formal_rerun.md` | Alur formal yang dikoreksi: menjalankan setiap bukti Fase 1-3 plus kontrol negatif; analisis akar masalah dan tabel hasil 19/19 |
| `evidence/quartus/C2-L1.md` .. `C2-L8.md` | Ekstrak fitter/STA/Fmax standar, satu per L |
| `rtl/ntt/ntt_core_c2_k2.sv`, `rtl/ntt/ntt_core_c2_k2_l{1,2,4,8}.sv` | Eksperimen tambahan K2 (2026-09-30): C2 dengan `t_q` berukuran sesuai L; file terpisah, C2 tidak disentuh |
| `rtl/ntt/butterfly_shared.sv`, `rtl/ntt/ntt_core_c2_k2_k1.sv`, `rtl/ntt/ntt_core_c2_k2_k1_l{1,2,4,8}.sv` | Eksperimen tambahan K1 di atas K2 (konfigurasi C2-K2-K1): satu pengali bersama per butterfly. Konfigurasi terpilih pada L=8 (ADR 0005) |
| `tb/ntt/run_k1_unit_tests.py`, `tb/ntt/k1_exhaustive/`, `formal/phase03-multilane/k1_*`, `formal/phase03-multilane/modmul_reduce_uf.sv` | Verifikasi K1: tes unit butterfly, harness ekuivalensi menyeluruh, ekuivalensi formal dengan kontrol negatif |
| `scripts/quartus/quartus_entity_breakdown.py` | Mengelompokkan tabel per-entitas fitter menurut fungsi (dipakai untuk audit ALM L=8) |
| `docs/decisions/adr/ADR-0005-apply-adr-0004-l-selection-to-the-c2-k2-k1-supplementary-con.md` | ADR: mengadopsi C2-K2-K1 dan memilih L = 8 |
| `evidence/phase03/k2_experiment.md`, `k1_experiment.md` dan file `k1_*` / `k2_*` / `l8_opt_*` di sampingnya; `evidence/quartus/C2-L{1,2,4,8}-K2.md`, `C2-K2-K1-L{1,2,4,8}.md` | Catatan eksperimen, log regresi/formal/ekuivalensi, rincian per-entitas, ekstrak Quartus |

## 3. Angka (masing-masing berlabel MEASURED, ESTIMATE, atau kutipan [n])
| Besaran | L=1 | L=2 | L=4 | L=8 |
|---|---|---|---|---|
| ALM | 6,018 / 41,910 (14%) | 5,728 / 41,910 (14%) | 7,629 / 41,910 (18%) | 11,446 / 41,910 (27%) |
| Dalam anggaran ADR 0004 (10,478 ALM)? | ya | ya | ya | tidak |
| Register | 3,100 | 3,098 | 3,102 | 3,100 |
| Blok RAM (M10K) | 0 / 553 | 0 / 553 | 0 / 553 | 0 / 553 |
| DSP | 3 / 112 | 5 / 112 | 9 / 112 | 17 / 112 |
| Fmax (Slow 100C) | 14.76 MHz | 13.54 MHz | 11.60 MHz | 7.62 MHz |
| Worst setup slack @ 20.000 ns | -47.733 ns | -54.644 ns | -66.690 ns | -111.219 ns |
| Siklus NTT (simulasi) | 897 | 449 | 225 | 113 |
| Siklus INTT (simulasi) | 1,153 | 705 | 481 | 369 |
| Formal (bank_overflow_o + keselamatan FSM), alur terkoreksi 2026-09-30 | PASS (k-induction) | PASS (k-induction) | PASS (k-induction) | PASS (k-induction) |

Semua MEASURED, `evidence/quartus/C2-L{1,2,4,8}.md` dan
`evidence/phase03/cocotb_regression.txt`.

Menerapkan kriteria ADR 0004 (utama: jumlah siklus minimum dalam anggaran 10,478 ALM; L=8
digugurkan oleh pemeriksaan anggaran di atas): di antara L∈{1,2,4}, jumlah siklus menurun ketat seiring L
(897/1153 -> 449/705 -> 225/481), sehingga L=4 memiliki jumlah siklus terendah di antara
kandidat yang masuk anggaran. Sesuai ADR 0004 hal ini dilaporkan sebagai hasil kriteria utama, bukan
diadopsi sepihak sebagai pilihan akhir tim -- Bagian 7 meminta tim untuk mengonfirmasinya. Kriteria
sekunder (pemeriksaan ulang AT bersifat informasi) belum dapat dijalankan: tidak ada L yang memenuhi timing pada clock mana pun, sehingga tidak ada
Fmax valid-timing untuk menghitung AT (ADR 0004 memperkirakan kasus ini).

## 3b. Eksperimen optimasi tambahan dan L terpilih (2026-09-30)
Setelah sapuan C2, tim bertanya apakah L=8 dapat dibawa ke bawah anggaran ALM tanpa mengurangi
8 butterfly per siklusnya. Dua eksperimen dijalankan sebagai konfigurasi terpisah (RTL C2 dan
evidence di atas tidak berubah dan tetap menjadi baseline):
- K2 -- penghitung sub-siklus `t_q` berukuran sesuai kebutuhan tiap L. Valid tetapi tidak cukup, dan bukan
  perbaikan yang seragam (`evidence/phase03/k2_experiment.md`).
- K1 -- satu pengali modular bersama per butterfly, bukan satu per mode, di atas K2
  (konfigurasi C2-K2-K1, `rtl/ntt/butterfly_shared.sv`, `rtl/ntt/ntt_core_c2_k2_k1.sv`). Ini mengubah
  datapath butterfly, yaitu di luar cakupan tertulis Fase 3 ("butterfly, aritmetika, dan
  memori seperti pada Fase 2"); tim menyetujuinya sebagai eksperimen tambahan lalu mengadopsinya
  (ADR 0005). `modmul_reduce.sv` dan parameter terkunci tidak berubah
  (`evidence/phase03/k1_experiment.md`).

| Besaran (MEASURED) | L=1 | L=2 | L=4 | L=8 |
|---|---|---|---|---|
| ALM, C2 (Bagian 3) | 6,018 | 5,728 | 7,629 | 11,446 |
| ALM, C2-K2 | 6,389 | 5,788 | 7,600 | 11,232 |
| ALM, C2-K2-K1 | 5,566 | 5,374 | 6,775 | 9,754 |
| C2-K2-K1 dalam anggaran 10,478 ALM? | ya | ya | ya | ya (724 di bawah) |
| Register, C2-K2-K1 | 3,099 | 3,095 | 3,098 | 3,094 |
| M10K, C2-K2-K1 | 0 / 553 | 0 / 553 | 0 / 553 | 0 / 553 |
| DSP, C2-K2-K1 | 2 / 112 | 3 / 112 | 5 / 112 | 9 / 112 |
| Fmax (Slow 100C), C2-K2-K1 | 14.33 MHz | 12.63 MHz | 10.89 MHz | 7.68 MHz |
| Worst setup slack @ 20.000 ns, C2-K2-K1 | -49.804 ns | -59.148 ns | -71.868 ns | -110.494 ns |
| Siklus NTT / INTT (simulasi), identik dengan C2 | 897 / 1153 | 449 / 705 | 225 / 481 | 113 / 369 |
| Formal (bank_overflow_o + keselamatan FSM), C2-K2-K1 | PASS | PASS | PASS | PASS |

Evidence: `evidence/quartus/C2-K2-K1-L1.md`, `evidence/quartus/C2-K2-K1-L2.md`,
`evidence/quartus/C2-K2-K1-L4.md`, `evidence/quartus/C2-K2-K1-L8.md`,
`evidence/quartus/C2-L1-K2.md`, `evidence/quartus/C2-L2-K2.md`,
`evidence/quartus/C2-L4-K2.md`, `evidence/quartus/C2-L8-K2.md`,
`evidence/phase03/k1_cocotb_regression.txt` (unit 2/2 dan inti 16/16 pada kedua
simulator), `evidence/phase03/k1_entity_breakdown.txt`,
`evidence/phase03/formal_rerun.md`. Ekuivalensi butterfly
(`butterfly.sv` lawan `butterfly_shared.sv`): bukti formal dengan pengali diabstraksikan, PASS dengan
kontrol negatif (`evidence/phase03/k1_equiv_abstraction.txt`), dan
simulasi menyeluruh atas semua 73,785,560,578 masukan, 0 ketidakcocokan
(`evidence/phase03/k1_exhaustive_equivalence.txt`).

L terpilih (ADR 0005, Accepted, Faza Dzil, Tim J5, 2026-09-30): menerapkan aturan ADR 0004
tanpa perubahan pada C2-K2-K1, keempat L berada dalam anggaran dan L=8 memiliki jumlah siklus terendah, sehingga tim
memilih L = 8 pada C2-K2-K1 (9,754 ALM; NTT 113 / INTT 369 siklus). Fase 4 dimulai dari konfigurasi
itu. Hasil C2 di atas (L=4) disimpan sebagai pembanding baseline.

Batas yang menyertai pilihan ini (tidak diselesaikan olehnya): timing tidak terpenuhi untuk konfigurasi mana pun;
margin 724 ALM lebih besar dari, tetapi tidak jauh di atas, ayunan packing fitter terbesar yang teramati
di antara kompilasi logika identik (~370 ALM, K2 pada L=1; tidak ada sapuan seed); K1 menurunkan Fmax
sedikit pada L=1/2/4; 0 blok M10K dipakai.

## 4. Standar dan sumber yang dipatok
Tidak ada pembacaan FIPS 203 baru pada fase ini; tidak ada parameter atau algoritma yang disentuh (`check_params.py` tetap
lulus). Toolchain identik dengan Fase 1/2 (OSS CAD Suite `2026-09-23`, Quartus 25.1std.0 Build 1129).

## 5. Cakupan dan batas
- M10K masih tidak dipakai (0/553, keempat L) -- celah Fase 2 yang diwarisi dan belum terselesaikan; kriteria PASS
  Fase 3 sendiri tidak mewajibkan perbaikannya, dan tidak ditambal diam-diam.
- Timing memburuk seiring L membesar, secara monoton (Fmax 14.76 -> 7.62 MHz; worst slack -47.7 ->
  -111.2 ns). Ini biaya yang diharapkan dari lebih banyak logika kombinasional per siklus (NUM_LANES butterfly paralel,
  pembangkit alamat, dan pembacaan ROM twiddle, semuanya masih murni kombinasional, tanpa
  pipelining -- cakupan Fase 4) dan dilaporkan apa adanya, tidak dikaitkan dengan noise.
- Belum ada ADR clock target (diwarisi dari Fase 1/2, masih terbuka) -- setiap angka Fmax/slack
  di atas hanya relatif, bukan klaim terhadap target nyata.
- Formal hanya mencakup kontrol dan kapasitas bank. Per 2026-09-30 `bank_overflow_o`==0 (jaminan
  bebas-konflik yang menjadi dasar memori multi-lane), handshake busy/done, dan rentang
  `t_q`/`layer_q` terbukti dengan k-induction untuk keempat L (Bagian 6). Bit-exactness NTT/INTT,
  integritas data memori, dan liveness TIDAK terbukti secara formal; semuanya bertumpu pada
  regresi cocotb di dua simulator.
- Metode reduksi, argumen rentang alamat (masih berlaku di sini: `AW=8` tidak dapat merepresentasikan alamat
  di luar [0,255] secara konstruksi): catatan yang sama seperti Fase 1/2, tidak berubah.

## 6. Penyimpangan, kegagalan, dan masalah terbuka
- Port `poly_mem_multiport.sv` didesain ulang dari array unpacked ke vektor packed
  di tengah fase. Versi pertama yang berfungsi memakai port array unpacked bergaya `input wire we_i [0:2*NUM_LANES-1]`
  (tersimulasi dan tersintesis baik di Verilator/Icarus). Pembaca SystemVerilog terbatas `read -formal`
  SymbiYosys menolak port modul array unpacked sama sekali (`syntax
  error, unexpected '['`), sehingga setiap port array dan beberapa array internal ditulis ulang sebagai
  vektor packed dengan pemotongan bit `[i*W +: W]` sebelum verifikasi formal bahkan dapat melakukan elaborasi
  desain. Ini kini satu-satunya gaya yang dipakai di `rtl/mem/poly_mem_multiport.sv` dan
  sinyal per-port `rtl/ntt/ntt_core_c2.sv`. cocotb (kedua simulator) dijalankan ulang setelah
  penulisan ulang dan tetap menunjukkan 16/16 lulus dengan jumlah siklus identik, jadi ini perubahan
  bentuk port, bukan perubahan perilaku.
- Icarus Verilog tidak mendukung penimpaan masa hidup penyimpanan `automatic` di dalam blok prosedural
  (`sorry: Overriding the default variable lifetime is not yet supported`), terjadi dua kali
  (sekali di loop penghitungan slot bank, sekali di helper yang ditinggalkan). Diperbaiki dengan mendeklarasikan
  variabel helper di luar `always_comb` alih-alih memakai `automatic logic ... = ...;` secara inline
  -- secara fungsional identik karena nilainya ditimpa sepenuhnya pada setiap evaluasi.
- `bind` juga tidak didukung pembaca formal terbatas SymbiYosys (kelas
  galat yang sama dengan array unpacked). Upaya menambah invarian induktif tambahan
  (`t_q <= TMax`, `layer_q <= 6`) lewat `bind` ke modul khusus-formal dibatalkan dan diganti dengan
  menambahkan `assert` langsung di dalam `rtl/ntt/ntt_core_c2.sv`, dijaga oleh `` `ifdef FORMAL ``
  (tidak pernah aktif pada sintesis atau simulasi normal).
- Celah formal CRG-8 untuk L=2/4/8: terselesaikan 2026-09-30 -- itu artefak harness formal, dan
  penjelasan yang pertama kali ditulis di sini keliru tentang mekanismenya. Statusnya saat itu UNKNOWN (kasus
  dasar lulus, induksi gagal), bukan FAIL dan bukan timeout. Akar masalah, dari jejak induksi
  (L=2, siklus NTT pertama, alamat 0/128/64/192 persis sesuai jadwal, namun instance `bank_map_rom`
  untuk alamat 0 mengeluarkan bank 1 padahal sumbernya 0): `proc_rom` Yosys mengubah
  `case` 256 entri `bank_map_rom` dan `twiddle_rom` menjadi sel `$mem`, yang isinya adalah state
  bebas pada langkah induksi, sehingga solver memakai ROM yang isinya bukan tabel sebenarnya --
  state yang tidak terjangkau. Perbaikan hanya di harness: `memory_map -rom-only` (isi ROM adalah
  konstanta: fakta desain, bukan asumsi), ditambah frontend yosys-slang (`read -formal` bawaan membiarkan `add_mod`/`sub_mod`
  milik `ntt_pkg` tidak ter-drive) dan asumsi reset yang setara. RTL tidak berubah. Hasil: keempat L PASS; kontrol negatif (salinan rusak
  `bank_map_rom`) gagal di kasus dasar atau di induksi sebagaimana mestinya; bukti Fase 1/2 tetap PASS
  dengan alur yang sama. Analisis lengkap: `evidence/phase03/formal_rerun.md`.
  *Koreksi atas teks sebelumnya (disimpan di bawah sebagai catatan):* teks itu mengaitkan ketidakcocokan dengan
  "cara frontend `-formal` Yosys mengevaluasi ROM `unique case` 256 entri" dan menyebut state contoh-balik
  "tampak terjangkau"; state FSM memang terjangkau, isi ROM tidak,
  dan invarian `t_q`/`layer_q` yang ditambahkan saat itu tidak menangani penyebabnya.
- *Teks 2026-09-29 yang digantikan, disimpan sebagai catatan:* penambahan invarian rentang
  `t_q`/`layer_q` tidak memperbaiki apa pun untuk L=2/4/8; k-induction masih melaporkan contoh-balik
  `bank_overflow_o`, kali ini pada state yang *tampak terjangkau* (L=2, `layer_q=3`,
  `t_q=32`, `state_q=S_RUN`). Didekode manual dari jejak VCD contoh-balik itu sendiri dan
  diperiksa silang dengan tiga cara independen:
  1. `tb/mem/bank_model.py`: `bank_of(64,2)=1`, `bank_of(80,2)=0`, `bank_of(192,2)=0`,
     `bank_of(208,2)=1` -- tepat 2 akses per bank, tanpa overflow.
  2. Teks sumber `rtl/mem/bank_map_rom.sv` untuk `NUM_BANKS==2`: entri case
     untuk alamat 64/80/192/208 sama persis dengan model Python (`bank_o=1'd1`/`1'd0`/`1'd0`/
     `1'd1` secara berurutan).
  3. `evidence/phase03/cocotb_regression.txt`: setiap jalankan NTT L=2 penuh
     pasti menyapu setiap pasangan `(layer, t)` termasuk yang ini, dan `bank_overflow_o`
     diperiksa (di-assert 0) setiap siklus pada setiap tes, di kedua simulator -- 16/16 lulus.
  Namun keluaran `bank_o` per-instance pada jejak SMT untuk instance `bank_map_rom` yang menangani
  alamat 80/192/208 tidak cocok dengan teks sumber atau model Python (instance untuk
  alamat 64 terbaca benar; tiga lainnya tidak). Ini melokalisasi ketidaksesuaian pada cara
  frontend `-formal` Yosys mengevaluasi ROM `unique case` 256 entri di bawah k-induction, bukan pada
  desain. Kesimpulan ini dinyatakan sebagai *diselidiki dan diyakini*, bukan terbukti -- menyelesaikannya
  sepenuhnya (kasus reproduksi yang lebih kecil, laporan bug Yosys, atau encoding ROM lain yang
  menghindari masalah) dibiarkan sebagai butir terbuka, bukan dinyatakan selesai.
- Tidak ditemukan bug kebenaran RTL pada `ntt_core_c2`/`poly_mem_multiport` itu sendiri kapan pun;
  setiap masalah di atas adalah masalah kompatibilitas perkakas/sintaks, tertangkap oleh lint/build/formal
  seketika, tidak ditemukan setelah tes dinyatakan lulus.

## 7. Keputusan yang diperlukan
- Semua yang sudah terbuka dari Fase 1/2 (`docs/results/phase02.md` Bagian 7): ADR clock
  target, apakah mengejar pemetaan M10K pembacaan-sinkron, cara membaca CRG-9.
- ~~Konfirmasi atau ganti hasil kriteria utama ADR 0004 (L=4 pada C2)~~ -- diputuskan 2026-09-30
  oleh ADR 0005: tim mengadopsi konfigurasi C2-K2-K1 yang dioptimasi dan memilih L = 8 (Bagian 3b).
- Baru (opsional): sapuan seed fitter pada C2-K2-K1 L=8 untuk mengukur margin packing ALM
  terhadap anggaran 10,478 ALM (batas Bagian 3b).
- ~~Cara memperlakukan celah formal CRG-8 untuk L=2/4/8~~ -- ditutup 2026-09-30: celah itu artefak
  harness dan keempat L terbukti (Bagian 6). Tersisa, opsional: properti formal di luar
  kontrol/kapasitas bank (integritas data memori, liveness) jika tim menginginkannya.
- Baru: `QUARTUS_BIN` diisi di `scripts/tooling.env` pada fase ini (bagian "Catatan proses"
  di atas) -- konfirmasi bahwa path benar untuk mesin setiap anggota tim atau setiap anggota
  mengatur nilai lokalnya sendiri (file ini di-git-ignore, jadi tidak dibagikan otomatis).

## 8. Klaim yang dibuat pada fase ini
Tidak ada yang ditulis untuk juri/teks proposal. Baris ablasi C2-L1/L2/L4/L8 di `docs/ROADMAP.md`
diisi dari evidence di atas; tidak ada angka proposal yang dikarang.

## 9. Mereproduksi
```bash
# from repo root, branch phase3-multilane
. scripts/env.sh

python3 scripts/build/gen_lane_schedule.py   # zeta-formula + p-coverage proof

for L in 1 2 4 8; do
  verilator --lint-only -Wall --timing -sv rtl/ntt/*.sv rtl/mem/*.sv --top-module ntt_core_c2 -GNUM_LANES=$L
done
slang --top ntt_core_c2 rtl/ntt/*.sv rtl/mem/*.sv

python3 tb/ntt/run_ntt_c2_tests.py icarus
python3 tb/ntt/run_ntt_c2_tests.py verilator
python3 tb/ntt/run_ntt_tests.py icarus   # Phase 1 regression, unaffected
python3 tb/mem/run_mem_tests.py icarus   # Phase 2 regression, unaffected
python3 -m pytest tb/golden/tests/ -q
python3 .claude/skills/mlkem-guard/scripts/check_params.py

python3 formal/run/run_formal_slang.py   # every Phase 1-3 proof + negative controls (19 results)

# Supplementary experiments (Section 3b): K2 and K2+K1 regressions, butterfly equivalence
python3 tb/ntt/run_ntt_c2_tests.py verilator k2 && python3 tb/ntt/run_ntt_c2_tests.py icarus k2
python3 tb/ntt/run_ntt_c2_tests.py verilator k1 && python3 tb/ntt/run_ntt_c2_tests.py icarus k1
python3 tb/ntt/run_k1_unit_tests.py verilator && python3 tb/ntt/run_k1_unit_tests.py icarus
(cd formal/phase03-multilane && sby -f k1_butterfly_equiv_abs.sby)   # PASS; k1_negctl_*.sby must FAIL
tb/ntt/k1_exhaustive/run_k1_exhaustive.sh                            # ~20 min on 8 cores
# Quartus revisions: C2-L<n>-K2 and C2-K2-K1-L<n> in quartus/phase03_multilane_c2/ (same flow as below)

# Quartus (paths for this machine; QUARTUS_BIN in scripts/tooling.env, git-ignored)
cd quartus/phase03_multilane_c2
for L in 1 2 4 8; do
  quartus_sh --flow compile C2-L$L
  python3 ../../.claude/skills/quartus-report/scripts/extract_quartus_report.py \
      output_files_L$L C2-L$L --log compile_L$L.log
done

python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase03.md
python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal
```

## 10. Persetujuan
- [x] Penyetuju manusia (faza dzil, 30-09-2026):
      Fase berikutnya dimulai hanya setelah anggota tim mencentang kotak ini. Di luar pola CRG-9
      (timing tidak terpenuhi) yang sudah diterima untuk C0/C1, fase ini memiliki dua butir yang memerlukan
      keputusan tim eksplisit sebelum persetujuan bermakna seperti biasanya; keduanya diselesaikan pada
      2026-09-30: (1) L terpilih adalah L = 8 pada konfigurasi C2-K2-K1 yang dioptimasi (ADR 0005,
      Bagian 3b), dan (2) celah formal CRG-8 untuk L=2/4/8 adalah artefak harness dan telah ditutup
      (Bagian 6). Menyetujui status PARTIAL ini karenanya berarti menerima CRG-9 (timing tidak
      terpenuhi) dan batas Bagian 3b sebagai titik awal terdokumentasi untuk Fase 4.

## Pembaruan status (2026-10-05)
Tim menetapkan fase ini DONE karena tujuannya dipenuhi oleh fase-fase akhir: konfigurasi berikutnya memenuhi timing (40 ns pada 6 dari 6 seed, dan 15 ns untuk inti Fase 9M, `docs/results/phase9m.md`). Pengukuran fase ini tidak berubah (angka slack dan ALM di atas tetap sebagaimana terukur). CRG-9 berbunyi "tidak ada slack negatif atau kegagalan didokumentasikan"; kegagalan itu didokumentasikan pada evidence yang disebut di barisnya. Kotak Persetujuan di atas dicentang sebelumnya dan tidak diedit.
