<!-- claim-lint: skip-file (internal analysis record, not proposal text) -->
# Analisis jalur kritis C3-P6 (baseline Fase 5, sebelum RTL Fase 5 apa pun)

Label: MEASURED = dicetak oleh Quartus Timing Analyzer untuk database yang tercantum di bawah; INFERENCE = diturunkan
dari angka terukur; ESTIMATE = proyeksi, tidak terukur.

## 1. Sumber dan metode
- Database: kompilasi Fase 4 revisi `C3-P6` (seed bawaan, 40.000 ns, Quartus Prime Lite 25.1std.0 Build 1129),
  kompilasi yang sama dengan `evidence/phase04/quartus_C3-P6.md`. File `db/C3-P6.*` dan
  `output_files_P6/` disalin ke folder di luar repository dan dianalisis di sana (menjalankan `project_open` pada
  `.qpf` repository menulis ulang file itu). Tidak ada kompilasi yang dijalankan; tidak ada yang diubah di folder Quartus repository.
- Pemeriksaan bahwa salinan adalah kompilasi yang terukur (MEASURED): slack setup terburuk pada Slow 1100mV 100C = 10.753 ns,
  identik dengan file evidence di atas.
- Skrip (di repository): `scripts/quartus/phase5_top_paths.tcl` (300 jalur setup terburuk, ringkasan + 3 jalur penuh, Slow
  1100mV 100C), `scripts/quartus/phase5_path_classes.py` (mengelompokkan 300 jalur menurut blok awal/akhir; keluaran
  `c3p6_top300_path_classes_slow100.txt` di folder ini). Jalur terburuk per segmen diambil dengan
  `get_timing_paths -from <register potong> -to <potongan berikutnya>` dalam sesi yang sama.
- Hanya corner Slow 1100mV 100C yang dianalisis (corner dengan slack setup terburuk). Corner lain: NOT MEASURED.

## 2. 300 jalur setup terburuk (MEASURED, Slow 1100mV 100C)
| Awal | Akhir | Slack terburuk | Jalur di antara 300 |
|---|---|---:|---:|
| register arbitrasi slot memori (potongan M: `g_arb[*].g_reg.slot_q`) | register keluaran pengali (potongan X, `u_mul.cut0`) | 10.753 ns | 168 |
| register arbitrasi slot memori (potongan M: `g_arb[*].g_reg.bank_q`) | potongan X | 11.654 ns | 24 |
| potongan M | register data-tulis M10K (RAM hasil inferensi Quartus) | 11.495–15.022 ns | 96 |
| register write-enable M10K | counter arbitrasi `count_q` | 15.469 ns | 12 |

Rentang slack 300 jalur: 10.753 sampai 15.566 ns. Tidak ada jalur di dalam reducer (stage `modmul_reduce_staged`
setelah potongan X) di antara 300 yang terburuk.

## 3. Jalur terburuk dirinci per blok (MEASURED, inkremen delay dari laporan jalur penuh)
Jalur: `g_arb[15].g_reg.slot_q[26]` → lajur 6 `u_mul|g_cut[0]` (masukan INTT `sub_mod(b, a)` → pengali DSP),
jalur data 29.345 ns.

| Segmen (kedatangan kumulatif, ns) | Delay (ns) | Blok |
|---|---:|---|
| 6.045 → 27.337 | 21.292 | dekode alamat baca dan mux baca `poly_mem_multiport_pipe` (`raddr0`, `Mux111`, `Mux376`, `Mux368`) |
| 27.337 → 31.685 | 4.348 | masukan butterfly `sub_mod(b, a)` (dua carry chain + select) |
| 31.685 → 35.390 | 3.705 | routing ke blok DSP + pengali DSP sampai potongan X |

Batas segmen adalah nama blok dalam laporan (INFERENCE tentang elemen mana milik blok mana).

## 4. Jalur terburuk per segmen register jalur pengali (slack MEASURED; kolom delay INFERENCE)
| Segmen | Slack terburuk @ 40.000 ns | ≈ periode terpakai (40 − slack) |
|---|---:|---:|
| potongan M → potongan X (mux baca + `sub_mod` + pengali) | 10.753 | ≈ 29.2 ns |
| potongan lajur X → potongan D_5 (5 stage reduksi) | 24.457 | ≈ 15.5 ns |
| potongan lajur D_5 → potongan D_11 (6 stage reduksi) | 23.592 | ≈ 16.4 ns |
| potongan lajur D_11 → memori (2 stage reduksi + `add_mod`/`sub_mod` + tulis) | 16.382 | ≈ 23.6 ns |
| potongan skala X → D_5 / D_5 → D_11 / D_11 → memori | 24.457 / 24.781 / 19.994 | ≈ 15.5 / 15.2 / 20.0 ns |

"40 − slack" mencakup clock skew, uncertainty, dan waktu setup; ia hanya pendekatan porsi segmen terhadap
periode, bukan delay logika murni.

## 5. Pembacaan (INFERENCE)
- Pada P = 6 clock dibatasi oleh jalur baca memori ditambah masukan butterfly dan pengali, bukan oleh
  reduksi. Segmen reduksi memakai sekitar 15–16 ns dari periode 40 ns; segmen D_11 → memori sekitar 23.6 ns.
- Bagian baca memori saja (sekitar 21.3 ns delay data) lebih panjang dari periode 20.000 ns. Perubahan reducer tidak bisa
  memendekkannya, dan Fase 5 menjaga memori, jadwal, L, dan P tetap (`docs/ROADMAP.md` Fase 5). Berdasarkan evidence ini,
  20.000 ns (50 MHz) tidak dapat dicapai hanya dengan perubahan aritmetika Fase 5; ADR 0006 mengharapkan Fase 5 diperlukan
  untuk 50 MHz, berdasarkan rincian P = 0 yang pembaginya sekitar 44 ns.
- Apa yang masih bisa dipengaruhi aritmetika pada segmen kritis: `sub_mod(b, a)` sebelum pengali (sekitar 4.3 ns)
  dan pengali itu sendiri (sekitar 3.7 ns). Menghapus semuanya akan menyisakan segmen M → X sekitar 25 ns
  (ESTIMATE: 29.2 − 4.3; mengabaikan penempatan ulang), yaitu sekitar 40 MHz, masih kurang dari 50 MHz.
- Apa yang bisa dipengaruhi perubahan reducer: ALM, segmen D_11 → memori, dan - hanya bila tim mengizinkan posisi
  register di dalam P = 6 berpindah - keseimbangan antar segmen. Per entitas di `C3-P6.fit.rpt` (MEASURED): reducer
  lajur `modmul_reduce_staged:u_mul` 153.2–157.2 ALM masing-masing (305 ALUT, 1 DSP masing-masing), reducer skala `u_scale_mul`
  148.9 ALM; logika butterfly di luar reducer 103.8–112.8 ALM per lajur; `poly_mem_multiport_pipe` 7,660.7 ALM;
  `ntt_core_c3` 10,484.5 ALM. Jumlah sembilan reducer: 1,395.8 ALM (INFERENCE), batas atas yang dapat dihemat
  dengan mengganti reducer saja.
- Satu seed, satu corner, satu revisi. Sebaran seed Fase 4: 32.60–34.20 MHz untuk C3-P6.
