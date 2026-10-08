<!-- claim-lint: skip-file (result artifact: internal status page, not proposal text) -->
# Hasil - Fase 1: Baseline RTL minimal (NTT/INTT L=1 + perkalian pointwise, konfigurasi C0)

- Status: DONE
- Tanggal (UTC): 2026-09-29 10:10
- Git commit (HEAD saat diverifikasi): 10bb3f8 (RTL tidak berubah sejak d8cb3cd; kompilasi Quartus untuk RTL itu, evidence ditambahkan di 42b9059/10bb3f8)
- Lingkungan: Ubuntu 24.04.4 LTS; OSS CAD Suite 2026-09-23 (Verilator 5.053 devel, Icarus
  Verilog 14.0 devel, slang 11.0.448, SymbiYosys + Yosys + Boolector); cocotb 2.1.0, pytest 9.1.1
  (`.venv`); Quartus Prime Lite 25.1std.0 Build 1129 (`~/altera_lite/25.1std`, kompilasi dijalankan
  oleh tim pada 2026-09-29, `quartus_sta` drill-down dijalankan read-only sesudahnya).
  *Catatan:* `scripts/tooling.env` masih berisi `QUARTUS_BIN=""`; Quartus dipanggil dengan path lengkap.

## 1. Kriteria selesai (Common RTL Gate, docs/ROADMAP.md, disalin tanpa perubahan)
| # | Kriteria | Evidence (`path` di bawah evidence/ atau tes, atau `cmd: ...`) | Status |
|---|---|---|---|
| CRG-1 | Lint bersih (`verilator --lint-only -Wall`) | `cmd: verilator --lint-only -Wall --timing -sv rtl/ntt/*.sv --top-module ntt_core` (0 peringatan) | PASS |
| CRG-2 | Elaborasi bersih (`slang`) | `cmd: slang --top ntt_core rtl/ntt/*.sv` (0 error, 0 peringatan) | PASS |
| CRG-3 | Bit-exact terhadap model acuan, pada kedua simulator | `evidence/phase01/cocotb_regression.txt` (10/10 di Icarus DAN Verilator) | PASS |
| CRG-4 | Kasus sudut didaftar sebelum tes ditulis | `evidence/phase01/test_plan.md` | PASS |
| CRG-5 | Regresi: tes fase sebelumnya masih lulus | `cmd: python3 -m pytest tb/golden/tests/ -q` (23/23 lulus) | PASS |
| CRG-6 | Parameter terkunci | `cmd: python3 .claude/skills/mlkem-guard/scripts/check_params.py` | PASS |
| CRG-7 | Evidence jumlah siklus konstan | `evidence/phase01/cocotb_regression.txt` (NTT=897, INTT=1153 siklus, konstan pada setiap kasus sudut + 20 masukan acak, kedua simulator) | PASS |
| CRG-8 | Properti formal (keselamatan FSM; rentang alamat) | `evidence/phase01/formal_ntt_core_safety.txt` (k-induction PASS pada properti keselamatan busy/done; rentang alamat diargumentasikan secara struktural -- lihat Bagian 5) | PASS |
| CRG-9 | Evidence Quartus (ALM, register, M10K, DSP, Fmax, slack); tidak ada worst slack negatif atau kegagalan didokumentasikan | `evidence/quartus/C0.md` dan `evidence/phase01/quartus_C0_timing_analysis.md` -- evidence ada dan kegagalan didokumentasikan, tetapi worst setup slack adalah -48.323 ns pada clock sementara 20.000 ns (timing TIDAK terpenuhi, di semua 4 corner; kegagalan didokumentasikan, dan itu yang diminta kriteria) | PASS |
| CRG-10 | Artefak hasil tervalidasi; pemeriksa klaim bersih | `cmd: python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase01.md` dan `cmd: python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal` | PASS |

CRG-9 semula ditandai FAIL. Pada 2026-10-05 tim memilih pembacaan bahwa kegagalan yang terdokumentasi
memenuhi kriteria ("atau kegagalan didokumentasikan"), sehingga kini PASS; slack terukur tidak berubah.

## 1b. Kriteria PASS tambahan Fase 1 (docs/ROADMAP.md Fase 1, di luar tabel CRG)
| # | Kriteria | Evidence | Status |
|---|---|---|---|
| 1 | ADR clock target tercatat | `docs/decisions/adr/ADR-0006-phase-4-target-clock.md` (Accepted 2026-09-30, setelah fase ini; 20.000 ns di `quartus/phase01_ntt_c0/C0.sdc` bersifat sementara) | PASS |
| 2 | Baris C0 pada matriks ablasi terisi nilai MEASURED | `evidence/phase01/quartus_C0_timing_analysis.md` (baris diisi di `docs/ROADMAP.md`; latensi dan AT sengaja tidak dinyatakan karena timing tidak terpenuhi pada clock yang dibatasi) | PASS |

Status adalah PASS, FAIL, atau MISSING. PASS memerlukan setidaknya satu item evidence berformat backtick yang ada.
Hasil simulasi bersifat hanya-simulasi; hasil Quartus adalah static timing pasca-fit, bukan
validasi perangkat keras (belum ada papan).

## 2. Yang dihasilkan
| Path | Fungsi |
|---|---|
| `rtl/ntt/ntt_pkg.sv` | Konstanta Q/N/CW/AW/ZW bersama dan fungsi `add_mod`/`sub_mod` |
| `rtl/ntt/twiddle_rom.sv` | ROM yang dibangkitkan (`scripts/build/gen_twiddle_rom.py` dari `tb/golden/primitives.py`) |
| `rtl/ntt/modmul_reduce.sv` | `(a*b) mod q`, kombinasional, `%` generik |
| `rtl/ntt/base_case_multiply.sv` | FIPS 203 Algoritma 12, bentuk langsung 5 perkalian |
| `rtl/ntt/butterfly.sv` | Butterfly NTT (Cooley-Tukey) / INTT (Gentleman-Sande), dipilih lewat mode |
| `rtl/ntt/poly_mem.sv` | Memori polinomial 256x12 bit, 2 port baca-asinkron/tulis-sinkron, tanpa bank |
| `rtl/ntt/ntt_core.sv` | FSM tingkat atas: L=1, satu butterfly/siklus, 7 layer + lintasan INTT x3303 |
| `scripts/build/gen_twiddle_rom.py` | Membangkitkan ulang `twiddle_rom.sv` dari model acuan |
| `tb/ntt/*.py` | Tes cocotb + runner, bit-exact terhadap `tb/golden/primitives.py` |
| `formal/phase01-ntt/*` | Bukti keselamatan SymbiYosys (CRG-8) |
| `quartus/phase01_ntt_c0/phase01_ntt_c0.qpf`, `C0.qsf`, `C0.sdc` | Proyek Quartus untuk revisi C0 (pin virtual, clock sementara 20.000 ns) |
| `quartus/phase01_ntt_c0/report_critical_paths.tcl` | Drill-down `quartus_sta` read-only pada netlist pasca-fit yang ada |
| `quartus/phase01_ntt_c0/segment_path.py`, `extract_c0_timing_evidence.py` | Mengubah laporan jalur Quartus menjadi file evidence (tanpa angka yang diketik tangan) |
| `evidence/quartus/C0.md` | Ekstrak ringkasan fitter/STA (`extract_quartus_report.py`) |
| `evidence/phase01/quartus_C0_timing_analysis.md` (+ `.json`) | Status tahap, sumber daya, semua corner, jalur terburuk, atribusi delay per struktur, klasifikasi endpoint, evidence metode clock |
| `evidence/phase01/test_plan.md`, `cocotb_regression.txt`, `formal_ntt_core_safety.txt` | Evidence Fase 1 sebelumnya |

## 3. Angka (masing-masing berlabel MEASURED, ESTIMATE, atau kutipan [n])
| Besaran | Nilai | Label | Evidence |
|---|---|---|---|
| Tes cocotb | 10/10 lulus, kedua simulator | MEASURED (simulasi) | `evidence/phase01/cocotb_regression.txt` |
| Jumlah siklus NTT / INTT (C0) | 897 / 1153, konstan pada semua masukan yang diuji | MEASURED (simulasi) | `evidence/phase01/cocotb_regression.txt` |
| Pemakaian logika | 7,010 / 41,910 ALM (17 %) | MEASURED | `evidence/quartus/C0.md` |
| Register | 3104 | MEASURED | `evidence/quartus/C0.md` |
| Blok RAM (M10K) / bit memori blok | 0 / 553; 0 / 5,662,720 | MEASURED | `evidence/quartus/C0.md` |
| Blok DSP | 3 / 112 (tiga "Two Independent 18x18", unsigned, tanpa register) | MEASURED | `evidence/phase01/quartus_C0_timing_analysis.md` |
| Fmax (clk_i) | 14.64 MHz (Slow 1100mV 100C); 14.69 MHz (Slow 1100mV -40C) | MEASURED | `evidence/quartus/C0.md` |
| Worst setup slack / TNS @ 20.000 ns | -48.323 ns / -143688.194 ns (Slow 1100mV 100C) | MEASURED | `evidence/quartus/C0.md` |
| Worst hold slack | 0.211 ns (Fast 1100mV -40C) -- terpenuhi | MEASURED | `evidence/quartus/C0.md` |
| Jalur terburuk | `layer_q[2]` -> `poly_mem:u_mem|mem[64][5]`, data delay 67.684 ns, 146 sel `lpm_divide` di jalur itu | MEASURED | `evidence/phase01/quartus_C0_timing_analysis.md` |
| Porsi pembagi modulo pada jalur data terburuk | 38.926 ns (57.5 %) | diturunkan dari laporan jalur MEASURED (`segment_path.py`) | `evidence/phase01/quartus_C0_timing_analysis.md` |
| Latensi / AT | tidak dinyatakan -- timing tidak terpenuhi pada clock yang dibatasi (`docs/ROADMAP.md`: latensi hanya pada clock yang memenuhi timing) | -- | -- |

## 4. Standar dan sumber yang dipatok
- FIPS 203 Algoritma 9-12, sebagaimana diverifikasi di Fase 0 (`evidence/phase00/fips203_errata.md`);
  tidak ada parameter atau algoritma yang berubah (`check_params.py` lulus).
- OSS CAD Suite tag `2026-09-23`; Quartus Prime Lite 25.1std.0 Build 1129 (dari header laporan).
- Constraint timing: `create_clock -period 20.000 [get_ports {clk_i}]`, `derive_clock_uncertainty`,
  `set_false_path -from [get_ports {rst_ni}]` -- sementara, bukan keputusan tim.

## 5. Cakupan dan batas
- Timing tidak terpenuhi. Setiap dari 3072 register penyimpanan `poly_mem` punya jalur yang gagal
  (slack antara -50 dan -40 ns), ditambah 2 jalur `layer_q`; semua 3074 endpoint yang gagal dicapai
  dari `layer_q`. Rincian dan atribusi struktural ada di file evidence analisis timing.
- Fmax sekitar 14.6 MHz adalah pengukuran baseline yang belum dioptimasi, bukan target. SDC tidak
  dilonggarkan dan RTL tidak diubah setelah kompilasi.
- Catatan metodologi clock: `clk_i` adalah pin virtual, sehingga Quartus mengeluarkan Critical Warning
  15725 ("ripple clock"); clock masuk ke jaringan global (`CLKCTRL_G3`, fan-out 3104) dari sebuah
  sel logika. Pada jalur terburuk, suku clock adalah skew -0.579 ns dan uncertainty 0.060 ns dibanding
  data delay 67.684 ns, sehingga tidak mengubah kesimpulan; delay penyisipan clock absolut
  tidak mewakili pin clock papan yang sebenarnya.
- Jalur I/O tidak dianalisis: 23 port masukan dan 14 port keluaran tidak punya `set_input_delay` /
  `set_output_delay` (kompilasi kernel-only). Semua jalur yang gagal adalah register-ke-register.
- Cakupan formal sebagian secara sengaja (hanya properti keselamatan; liveness dari simulasi;
  rentang alamat diargumentasikan secara struktural).
- Metode reduksi adalah `%` biasa, diuji dengan 2000 pasangan acak ditambah kasus sudut; sapuan
  menyeluruh 3329² termasuk cakupan Fase 5.
- Hanya C0 yang ada (L=1, memori tanpa bank, tanpa pipeline); semua yang "belum boleh" di
  roadmap untuk Fase 1 memang benar-benar belum ada.

## 6. Penyimpangan, kegagalan, dan masalah terbuka
- CRG-9 FAIL: setup timing tidak terpenuhi pada 20.000 ns (worst slack -48.323 ns). Evidence akar masalah
  dari laporan (bukan dugaan): pada jalur terburuk, `lpm_divide` kombinasional 24-bit/12-bit yang
  di-infer dari `%` di `rtl/ntt/modmul_reduce.sv` menyumbang 38.926 ns (57.5 %) dari
  data delay 67.684 ns; sisa jalur baca-hitung-tulis satu siklus yang sama (aritmetika FSM/alamat
  9.952 ns, mux baca memori berbasis register 5.504 ns, perkalian DSP 3.780 ns, add/sub
  mod 3.060 ns, mux tulis ke register penyimpanan 6.462 ns) berjumlah 28.758 ns, yang dengan
  sendirinya sudah melebihi periode 20.000 ns. Jalur INTT (`u_inv_mul`) dan penskalaan (`u_scale_mul`)
  menunjukkan pola yang sama (-47.787 ns dan -46.444 ns). Jalur kontrol saja (`layer_q[1]` -> `layer_q[2]`,
  -3.829 ns) 92.7 % berupa interkoneksi, termasuk satu lompatan 11.986 ns dari baris Y37 ke baris Y4.
- Sengaja tidak dilakukan di sini: tidak ada perubahan RTL, tidak ada perubahan SDC, tidak ada clock yang lebih rendah. Jalur kritis
  kini teridentifikasi dan terdokumentasi; perbaikan apa pun adalah langkah terpisah yang ditinjau (Fase 4/5 pada roadmap mencakup
  pipelining dan aritmetika; Fase 2 mencakup memori).
- Kejadian sebelumnya (sudah teratasi): race pulsa start pada testbench diperbaiki di testbench; properti
  formal yang keliru tertangkap oleh k-induction dan dikoreksi. Keduanya tidak mengubah RTL.

## 7. Keputusan yang diperlukan
- Clock target untuk C0 (ADR diperlukan pada gerbang Fase 1). Baseline terukur tidak dapat berjalan pada
  50 MHz sementara; tim memutuskan clock apa yang akan dipakai dan apakah perubahan RTL Fase 1
  termasuk cakupan sebelum C0 dibekukan, atau C0 tetap menjadi baseline (yang gagal) terdokumentasi
  dan perbaikan dilakukan pada fase yang ditetapkan roadmap.
- Cara membaca CRG-9 ("atau kegagalan didokumentasikan"): PASS-dengan-kegagalan-terdokumentasi atau FAIL.
- Apakah `QUARTUS_BIN` diatur di `scripts/tooling.env` agar `scripts/env.sh` menemukan Quartus.

## 8. Klaim yang dibuat pada fase ini
Tidak ada yang ditulis untuk juri/teks proposal. Hanya `docs/ROADMAP.md` (baris status dan baris C0
pada matriks ablasi) yang diperbarui, dari file evidence di atas.

## 9. Mereproduksi
```bash
# from repo root, branch phase1-ntt-baseline
. scripts/env.sh
verilator --lint-only -Wall --timing -sv rtl/ntt/*.sv --top-module ntt_core
slang --top ntt_core rtl/ntt/*.sv
python3 tb/ntt/run_ntt_tests.py icarus
python3 tb/ntt/run_ntt_tests.py verilator
python3 -m pytest tb/golden/tests/ -q
python3 .claude/skills/mlkem-guard/scripts/check_params.py
(cd formal/phase01-ntt && sby -f ntt_core_safety.sby)

# Quartus (paths for this machine)
export PATH=$HOME/altera_lite/25.1std/quartus/bin:$PATH
(cd quartus/phase01_ntt_c0 && quartus_sh --flow compile phase01_ntt_c0 -c C0)
python3 .claude/skills/quartus-report/scripts/extract_quartus_report.py \
    quartus/phase01_ntt_c0/output_files C0 --log quartus/phase01_ntt_c0/output_files/C0.flow.rpt
(cd quartus/phase01_ntt_c0 && quartus_sta -t report_critical_paths.tcl \
    && python3 extract_c0_timing_evidence.py)

python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase01.md
python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal
```

## 10. Persetujuan
- [x] Penyetuju manusia (nama, tanggal): Faza Dzil, 2026-09-29
      Fase berikutnya dimulai hanya setelah anggota tim mencentang kotak ini. Dengan CRG-9 FAIL dan
      ADR clock target belum ada, fase ini PARTIAL; menyetujuinya berarti tim menerima C0 sebagai
      baseline gagal yang terdokumentasi dan memutuskan langkah berikutnya (Bagian 7).

## Pembaruan status (2026-10-05)
Tim menetapkan fase ini DONE karena tujuannya dipenuhi oleh fase-fase akhir: konfigurasi berikutnya memenuhi timing (40 ns pada 6 dari 6 seed, dan 15 ns untuk inti Fase 9M, `docs/results/phase9m.md`). Pengukuran fase ini tidak berubah (angka slack dan ALM di atas tetap sebagaimana terukur). CRG-9 berbunyi "tidak ada slack negatif atau kegagalan didokumentasikan"; kegagalan itu didokumentasikan pada evidence yang disebut di barisnya. Kotak Persetujuan di atas dicentang sebelumnya dan tidak diedit.
