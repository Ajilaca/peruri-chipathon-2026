<!-- claim-lint: skip-file (result artifact: internal status page, not proposal text) -->
# Hasil - Fase 2: Arsitektur memori (penyimpanan M10K, banking, pembangkit alamat, konfigurasi C1)

- Status: DONE
- Tanggal (UTC): 2026-09-29 11:07
- Git commit (HEAD saat diverifikasi): 4e26498
- Lingkungan: sama dengan Fase 1 (`docs/results/phase01.md`) -- Ubuntu 24.04.4 LTS, OSS CAD
  Suite 2026-09-23, cocotb 2.1.0, pytest 9.1.1, Quartus Prime Lite 25.1std.0 Build 1129
  (`~/altera_lite/25.1std`).

Catatan proses, dinyatakan apa adanya: aturan gerbang `docs/ROADMAP.md` sendiri adalah "sebuah fase dimulai hanya setelah
artefak hasil fase sebelumnya lulus `check_result.py` dan anggota tim telah mencentang
kotak Persetujuannya." Kotak Persetujuan Fase 1 masih belum dicentang (`docs/results/phase01.md`
Bagian 9) dan CRG-9-nya FAIL. Fase ini tetap dimulai, atas instruksi eksplisit tim
("lanjut fase 2") untuk melanjutkan di sesi yang sama, bukan karena gerbang terpenuhi. Dicatat di sini
agar siapa pun yang hanya membaca file ini tidak mengira Fase 1 telah disetujui.

## 1. Kriteria selesai (Common RTL Gate, docs/ROADMAP.md, disalin tanpa perubahan)
| # | Kriteria | Evidence | Status |
|---|---|---|---|
| CRG-1 | Lint bersih | `cmd: verilator --lint-only -Wall --timing -sv rtl/ntt/*.sv rtl/mem/*.sv --top-module ntt_core_c1` (0 peringatan); juga diperiksa mandiri untuk ROM peta bank dan modul memori berbank pada NUM_BANKS∈{1,2,4,8} | PASS |
| CRG-2 | Elaborasi bersih (slang) | `cmd: slang --top ntt_core_c1 rtl/ntt/*.sv rtl/mem/*.sv` (0 error, 0 peringatan) | PASS |
| CRG-3 | Bit-exact terhadap model acuan, kedua simulator | `evidence/phase02/cocotb_regression.txt` (12/12 di Icarus DAN Verilator: bank_map_rom x4 nilai L + ntt_core_c1) | PASS |
| CRG-4 | Kasus sudut sebelum tes | `evidence/phase02/test_plan.md` | PASS |
| CRG-5 | Regresi: tes Fase 0 + Fase 1 masih lulus | `cmd: python3 -m pytest tb/golden/tests/ -q` (23/23) dan `cmd: python3 tb/ntt/run_ntt_tests.py icarus` (10/10, C0 tidak terpengaruh) | PASS |
| CRG-6 | Parameter terkunci | `cmd: python3 .claude/skills/mlkem-guard/scripts/check_params.py` | PASS |
| CRG-7 | Evidence jumlah siklus konstan | `evidence/phase02/cocotb_regression.txt` (NTT=897, INTT=1153, sama dengan C0, yaitu 0 siklus stall) | PASS |
| CRG-8 | Properti formal | `evidence/phase02/formal_bank_map.txt` (properti pasangan-sendiri, L=8, kedalaman BMC 1, PASS) dan `evidence/phase02/formal_ntt_core_c1_safety.txt` (keselamatan FSM, k-induction kedalaman 6, PASS) | PASS |
| CRG-9 | Evidence Quartus; tidak ada slack negatif atau kegagalan didokumentasikan | `evidence/quartus/C1.md`, `evidence/phase02/quartus_C1_vs_C0.md` -- evidence ada, kegagalan didokumentasikan, tetapi worst setup slack adalah -46.720 ns pada 20.000 ns (timing TIDAK terpenuhi, sama seperti C0; kegagalan didokumentasikan, dan itu yang diminta kriteria) | PASS |
| CRG-10 | Artefak hasil + pemeriksa klaim | `cmd: python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase02.md` dan `cmd: python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal` | PASS |

CRG-9 semula ditandai FAIL, seperti pada Fase 1 (`docs/results/phase01.md`). Pada 2026-10-05 tim memilih
pembacaan bahwa kegagalan yang terdokumentasi memenuhinya, sehingga kini PASS; slack terukur tidak berubah.

## 1b. Kriteria PASS Fase 2 (docs/ROADMAP.md Fase 2, di luar tabel CRG)
| # | Kriteria | Evidence | Status |
|---|---|---|---|
| 1 | Bebas-konflik terbukti untuk keempat nilai L (1,2,4,8) | `evidence/phase02/bank_scheme_exploration.txt` (Python menyeluruh: pasangan-sendiri, keseimbangan, bijektivitas, multi-lane <=2/bank/siklus) + `evidence/phase02/formal_bank_map.txt` (formal, pada ROM sebenarnya) | PASS |
| 2 | Siklus stall terukur = 0 pada L = 1 | `evidence/phase02/cocotb_regression.txt` (siklus C1 == siklus C0 persis, kedua arah) | PASS |
| 3 | Bit-exact | log cocotb yang sama | PASS |
| 4 | Jumlah siklus konstan | log cocotb yang sama | PASS |
| 5 | Baris C1 pada matriks ablasi terisi | `docs/ROADMAP.md` matriks ablasi, baris C1 | PASS |

Kelima kriteria PASS yang dinyatakan fase ini sendiri terpenuhi. Status semula PARTIAL
karena CRG-9 (timing) dan karena gerbang Fase 1 sendiri belum terpenuhi saat fase ini
dimulai (lihat catatan proses di atas); sejak 2026-10-05 statusnya DONE (lihat pembaruan status di bagian akhir).

## 2. Yang dihasilkan
| Path | Fungsi |
|---|---|
| `tb/mem/bank_model.py` | Model acuan: skema bank grup-XOR, penetapan offset, pengelompokan lane, dan aritmetika pembangkit alamat persis yang diambil dari `rtl/ntt/ntt_core.sv` |
| `scripts/build/gen_bank_map.py` | Menjalankan bukti bebas-konflik menyeluruh; membangkitkan `rtl/mem/bank_map_rom.sv` dari model acuan (tidak pernah diketik tangan) |
| `rtl/mem/bank_map_rom.sv` | ROM yang dibangkitkan: `addr -> (bank, offset)` untuk NUM_BANKS ∈ {1,2,4,8} |
| `rtl/mem/poly_mem_banked.sv` | Memori polinomial berbank (NUM_BANKS generik; hanya NUM_BANKS=1 yang dijalankan/diuji pada fase ini) |
| `rtl/mem/ntt_core_c1.sv` | Konfigurasi C1: FSM/butterfly/ROM twiddle C0 tidak berubah, memori diganti dengan versi berbank pada NUM_BANKS=1 |
| `tb/mem/test_bank_map.py` | cocotb, menyeluruh (256/256 alamat) terhadap `tb/mem/bank_model.py`, keempat nilai L |
| `tb/mem/test_ntt_core_c1.py` | Regresi cocotb: bit-exact + siklus-exact (== C0) terhadap `tb/golden/primitives.py` |
| `tb/mem/run_mem_tests.py` | Menjalankan semua tes cocotb Fase 2 pada satu simulator |
| `formal/phase02-mem/bank_map_props.sv`, `bank_map_safety.sby` | Bukti formal pasangan-sendiri pada ROM sebenarnya (L=8) |
| `formal/phase02-mem/ntt_core_c1_formal_top.sv`, `ntt_core_c1_safety.sby` | Bukti ulang formal keselamatan FSM pada `ntt_core_c1` |
| `quartus/phase02_mem_c1/` | Proyek Quartus untuk C1 (metodologi pin virtual dan clock sementara yang sama seperti C0) |
| `evidence/phase02/test_plan.md` | Rencana tes CRG-4, ditulis sebelum kode tes apa pun |
| `evidence/phase02/bank_map_spec.md` | Spesifikasi skema pemetaan bank dan alasannya |
| `evidence/phase02/bank_scheme_exploration.txt` | Log mentah bukti menyeluruh |
| `evidence/phase02/formal_bank_map.txt`, `formal_ntt_core_c1_safety.txt` | Log mentah SymbiYosys |
| `evidence/phase02/cocotb_regression.txt` | Log mentah lulus/gagal cocotb + jumlah siklus, kedua simulator |
| `evidence/quartus/C1.md` | Ekstrak ringkasan fitter/STA standar |
| `evidence/phase02/quartus_C1_vs_C0.md` | Perbandingan C1 lawan C0, pemeriksaan ulang jalur terburuk, temuan M10K yang jujur |

## 3. Angka (masing-masing berlabel MEASURED, ESTIMATE, atau kutipan [n])
| Besaran | C0 | C1 | Evidence |
|---|---|---|---|
| ALM | 7,010 / 41,910 | 6,749 / 41,910 | MEASURED, `evidence/phase02/quartus_C1_vs_C0.md` |
| Register | 3,104 | 3,105 | MEASURED, sama |
| Blok RAM (M10K) | 0 / 553 | 0 / 553 | MEASURED, sama (tujuan M10K tidak tercapai -- Bagian 5) |
| DSP | 3 / 112 | 3 / 112 | MEASURED, sama |
| Fmax (Slow 100C) | 14.64 MHz | 14.99 MHz | MEASURED, sama |
| Worst setup slack @ 20.000 ns | -48.323 ns | -46.720 ns | MEASURED, sama |
| Siklus NTT / INTT (simulasi) | 897 / 1153 | 897 / 1153 (identik) | MEASURED (simulasi), `evidence/phase02/cocotb_regression.txt` |
| Bebas-konflik peta bank, semua L∈{1,2,4,8} | n/a | 0 tabrakan (menyeluruh + formal) | MEASURED, `evidence/phase02/bank_scheme_exploration.txt` |

## 4. Standar dan sumber yang dipatok
Tidak ada pembacaan FIPS 203 baru pada fase ini; tidak ada parameter atau algoritma yang disentuh (`check_params.py` tetap
lulus). Toolchain identik dengan Fase 1 (OSS CAD Suite `2026-09-23`, Quartus 25.1std.0 Build 1129).

## 5. Cakupan dan batas
- M10K TIDAK dipakai, meskipun judul fase ini sendiri ("penyimpanan polinomial M10K"). Terukur 0/553
  blok RAM, identik dengan C0. Akar masalah (dari log Quartus, bukan dugaan): baik `poly_mem.sv`
  maupun `poly_mem_banked.sv` memakai pembacaan asinkron (kombinasional), dan inferensi RAM Quartus
  memerlukan pembacaan sinkron agar dipetakan ke M10K. Ini celah yang nyata dan dilaporkan jujur terhadap
  tujuan fase yang dinyatakan, bukan sesuatu yang kriteria PASS roadmap sendiri wajibkan
  diperbaiki pada fase ini -- lihat `evidence/phase02/quartus_C1_vs_C0.md` Bagian 4
  untuk penjelasan lengkap dan alasan mengapa hal ini tidak ditambal diam-diam.
- Hanya NUM_BANKS=1 yang dibangun menjadi datapath teruji dan terukur. `rtl/mem/poly_mem_banked.sv`
  dapat dikompilasi (lint bersih) untuk NUM_BANKS∈{2,4,8}, dan fungsi alamat `rtl/mem/bank_map_rom.sv`
  terbukti bebas-konflik secara menyeluruh untuk keempat nilai L -- tetapi crossbar baca/tulis multi-bank
  untuk L>1 tidak punya tes cocotb dan tidak diukur Quartus pada fase ini. Membangun dan
  mengukur datapath L-lane yang sebenarnya adalah cakupan Fase 3.
- Timing masih tidak terpenuhi (akar masalah sama dengan C0, pembagi hasil inferensi `modmul_reduce.sv`,
  tidak disentuh pada fase ini) -- perbaikan slack sekitar 1.6 ns dikaitkan dengan perbedaan routing/penempatan
  di sekitar memori yang diganti, bukan perbaikan timing apa pun.
- Gerbang Fase 1 sendiri (Persetujuan dicentang) belum terpenuhi saat fase ini dimulai -- lihat catatan
  proses di bagian atas file ini.
- ADR clock target masih belum ada (diwarisi dari Fase 1, masih terbuka).
- Metode reduksi, cakupan liveness formal, dan argumen rentang alamat: catatan yang sama seperti Fase 1
  (`docs/results/phase01.md` Bagian 5), tidak berubah pada fase ini.

## 6. Penyimpangan, kegagalan, dan masalah terbuka
- Tidak ada bug RTL yang ditemukan atau diperbaiki pada fase ini. Dua percobaan "membangkitkan fungsi ROM dengan
  argumen keluaran" yang gagal di Icarus Verilog (`function` SV dengan port `output` tidak
  diterima Icarus) dan sintaks header "`module X import pkg::*; #(...)`" yang ditolak oleh
  `read -formal` Yosys (masalah yang sama dengan Fase 1, diperbaiki dengan cara yang sama) keduanya tertangkap oleh
  lint/formal seketika dan diperbaiki di generator/RTL sebelum tes apa pun dinyatakan
  lulus -- bukan ditemukan belakangan.
- Kesalahan perkakas, diungkapkan: saat kompilasi Quartus C1, direktori kerja
  (`db/`, `incremental_db/`) tidak sengaja terhapus saat `quartus_fit` masih berjalan,
  merusak kompilasi itu (`Fitter Status: Failed`). Direktori dibersihkan dan kompilasi
  dijalankan ulang dari awal; angka MEASURED dalam dokumen ini berasal dari jalankan ulang yang bersih. Tidak ada
  keluaran rusak yang dipakai sebagai evidence di mana pun.
- CRG-9 (Quartus) FAIL karena alasan substantif yang sama dengan Fase 1 (timing tidak terpenuhi pada
  clock sementara); ini diharapkan, bukan kejutan, karena Fase 2 tidak menyentuh aritmetika.

## 7. Keputusan yang diperlukan
- Semua yang sudah terbuka dari Fase 1 (`docs/results/phase01.md` Bagian 7): ADR clock
  target, cara membaca CRG-9, `QUARTUS_BIN` di `scripts/tooling.env`.
- Baru: apakah akan mengejar pemetaan M10K pembacaan-sinkron (perubahan penjadwalan) pada fase
  berikutnya, mengingat hal itu tidak diwajibkan kriteria PASS Fase 2 sendiri tetapi merupakan tujuan
  fase yang dinyatakan.
- Baru: apakah memulai Fase 2 sebelum kotak Persetujuan Fase 1 dicentang dapat diterima sebagai
  proses bagi tim ini, atau Fase 1 perlu disetujui secara formal (atau digantikan secara eksplisit)
  sebelum Fase 3 dimulai.

## 8. Klaim yang dibuat pada fase ini
Tidak ada yang ditulis untuk juri/teks proposal. Baris ablasi C1 di `docs/ROADMAP.md` diisi dari
evidence di atas; tidak ada angka proposal yang dikarang.

## 9. Persetujuan
- [x] Penyetuju manusia (nama, tanggal): Faza Dzil, 2026-09-29
      Fase berikutnya dimulai hanya setelah anggota tim mencentang kotak ini. Mengingat CRG-9 FAIL, menyetujui
      status PARTIAL ini berarti tim secara eksplisit menerima penyimpangan proses yang dicatat di
      bagian atas file ini (Fase 2 dimulai sebelum kotak Fase 1 sendiri dicentang), bukan hanya angka
      fase ini. Kotak Fase 1 dicentang pada hari yang sama, setelah kejadian.

## Pembaruan status (2026-10-05)
Tim menetapkan fase ini DONE karena tujuannya dipenuhi oleh fase-fase akhir: konfigurasi berikutnya memenuhi timing (40 ns pada 6 dari 6 seed, dan 15 ns untuk inti Fase 9M, `docs/results/phase9m.md`). Pengukuran fase ini tidak berubah (angka slack dan ALM di atas tetap sebagaimana terukur). CRG-9 berbunyi "tidak ada slack negatif atau kegagalan didokumentasikan"; kegagalan itu didokumentasikan pada evidence yang disebut di barisnya. Kotak Persetujuan di atas dicentang sebelumnya dan tidak diedit.
