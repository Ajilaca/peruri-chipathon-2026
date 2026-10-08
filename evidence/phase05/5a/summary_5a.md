<!-- claim-lint: skip-file (internal checkpoint record, not proposal text) -->
# Checkpoint Fase 5a - reducer fold khusus q (revisi C4a) lawan C3-P6

Label: MEASURED (laporan Quartus / log simulasi di repository ini), INFERENCE (aritmetika pada nilai terukur),
NOT MEASURED. Rencana: `evidence/phase05/test_plan.md` (amandemen A1, A2); keputusan ADR 0011.

## 1. Apa yang dibangun
| File | Isi |
|---|---|
| `rtl/arith/modmul_fold.sv` | (a·b) mod q dengan lima fold shift-and-add (2^12 ≡ 767 mod q) dan satu pilihan paralel di antara v, v − q, v − 2q; `REG_AFTER` atas 7 titik potong |
| `rtl/arith/modmul_sel.sv` | satu antarmuka untuk setiap reducer (`RED_KIND` 0 = reducer staged beku, 1 = fold) |
| `rtl/arith/butterfly_c4.sv` | persamaan `butterfly_shared_pipe.sv` dengan reducer dipilih oleh `RED_KIND` |
| `rtl/ntt/ntt_core_c4.sv`, `rtl/ntt/ntt_core_c4a.sv` | inti C3 dengan hanya instans reducer / butterfly yang diubah; pembungkus revisi C4a (potongan A_4, A_11, M, X, F_3, F_5; P = 6) |
| `tb/arith/` | harness menyeluruh (`reducer_exhaustive/`), unit test, runner inti yang memakai ulang `tb/ntt/test_ntt_core_c3.py` |
| `formal/phase05-arith/`, `formal/run/run_formal_phase5.py` | top formal untuk pembungkus C4, `.sby`, runner dengan kontrol negatif |
| `quartus/phase05_arith_c4/` | proyek, revisi `C4a`, `C4.sdc` (40.000 ns, isi identik dengan `C3.sdc`) |
| `scripts/test/phase5_verify.sh`, `phase5_regression.sh`, `phase5_segments.tcl`, `phase5_top_paths.tcl`, `phase5_path_classes.py` | skrip verifikasi dan analisis |

File beku Fase 1–4 tidak diedit.

## 2. Verifikasi (MEASURED; log di folder ini)
| Pemeriksaan | Hasil | Evidence |
|---|---|---|
| V1 lint | Verilator `-Wall` 0 peringatan dan slang 0 peringatan untuk `ntt_core_c4a` dan `ntt_core_c4` (modul daun sendiri: hanya UNUSEDPARAM untuk konstanta `ntt_pkg`, seperti di Fase 4) | `verify.txt` |
| V2 menyeluruh | 0 ketidakcocokan atas semua a, b di [0, q) (11,082,241 pasangan) pada REG_AFTER 0 dan 41; V2-info: juga 0 ketidakcocokan atas pasangan 12-bit lain (tepat untuk semua 2^24); kontrol negatif (768·h) gagal seperti disyaratkan | `verify.txt` |
| V3/V4 unit | kasus sudut reducer, 10,000 acak beruntun, masukan terisolasi; kasus sudut butterfly + acak - kedua simulator | `verify.txt` |
| V5/V6/V7 inti | C4a dan C4 dengan RED_KIND 0: NTT/INTT/round trip/data batas bit-exact terhadap `tb/golden`, scoreboard 0 pelanggaran, `bank_overflow_o` 0, siklus konstan dan = 119 / 375, kedua simulator; kontrol negatif (WrDly 8) memicu scoreboard (640 pelanggaran) dan memberi 5/5 hasil salah per arah | `verify.txt`; upaya kontrol negatif pertama yang tidak valid disimpan di `negctl_first_attempt_rd1_wr7.txt` (amandemen A2) |
| V8 formal | C4a: H, O, R, A, B, C PASS; NC-O dan NC-A FAIL seperti disyaratkan (3/3 sesuai harapan) | `formal.md` |
| V9 regresi | check_params OK; pytest 23 lulus; cocotb Fase 1–4 di kedua simulator; reducer menyeluruh Fase 4 PASS; formal Fase 1–3 19/19, Fase 4 9/9; OVERALL PASS | `regression.txt` |

## 3. Quartus, C4a lawan C3-P6 (perangkat sama, assignment QSF, SDC 40.000 ns, bawaan Quartus, seed bawaan)
| Besaran | C3-P6 (MEASURED) | C4a (MEASURED) | Δ (INFERENCE) |
|---|---:|---:|---:|
| ALM (dari 41,910) | 10,505 | 9,847 | −658 (−6.3 %) |
| Register | 4,168 | 4,109 | −59 |
| M10K / DSP | 29 / 9 | 29 / 9 | 0 / 0 |
| Slack setup / hold terburuk @ 40 ns | +10.753 / +0.140 | +10.352 / +0.107 | −0.401 / −0.033 |
| Fmax Slow 100C / Slow −40C (MHz) | 34.19 / 34.5 | 33.73 / 33.86 | −0.46 (−1.3 %) pada corner terendah |
| Timing terpenuhi pada 40.000 ns | ya | ya | - |
| Siklus NTT / INTT (simulasi) | 119 / 375 | 119 / 375 | 0 |
| t_NTT / t_INTT pada Fmax slow corner terendah | 3.481 / 10.968 µs | 3.528 / 11.118 µs | +1.3 % |
| Margin ke 12,573 ALM | 2,068 | 2,726 | +658 |
| Peringatan kritis | hanya 15725 | hanya 15725 (virtual pin `clk_i`, seperti di setiap kompilasi kernel-only) | - |

Sumber: `evidence/phase04/quartus_C3-P6.md`, `quartus_C4a.md` (folder ini).

Per entitas (MEASURED, `C4a.fit.rpt` lawan `C3-P6.fit.rpt`):
| Entitas | C3-P6 | C4a | Δ |
|---|---:|---:|---:|
| reducer, 8 lajur + skala (jumlah) | 1,395.8 ALM (153.2–157.2 per lajur, 148.9 skala) | 846.8 ALM (94.4–96.7 per lajur, 85.0 skala) | −549.0 |
| ALUT reducer per lajur | 305 | 193 | −112 |
| memori `poly_mem_multiport_pipe` | 7,660.7 | 7,611.1 | −49.6 |
| `ntt_core_c3` / `ntt_core_c4` | 10,484.5 | 9,826.0 | −658.5 |

Struktur timing (MEASURED, `c4a_top300_path_classes_slow100.txt`, `c4a_vs_c3p6_segments_slow100.txt`):
- 300 jalur setup terburuk C4a dimulai dari register arbitrasi slot memori, seperti di C3-P6; slack terburuk
  +10.352 ns (baca memori → `sub_mod` → pengali → potongan X). Tidak ada jalur internal reducer di antaranya.
- Segmen reducer (lajur, terburuk): C4a X → F_3 +23.970, F_3 → F_5 +32.488, F_5 → memori +16.599 ns; C3-P6 X → D_5
  +24.457, D_5 → D_11 +23.592, D_11 → memori +16.382 ns.

## 4. Pembacaan (INFERENCE)
- Area: reducer fold menghemat sekitar 549 ALM pada sembilan reducer (−39 %), dan total inti turun 658 ALM -
  jauh melampaui sebaran seed 32–64 ALM Fase 4, jadi pengurangan itu bukan efek seed. Pemakaian DSP tidak berubah (hasil kali
  tetap memakai satu DSP per pengali).
- Timing: Fmax 1.3 % lebih rendah, dalam rentang seed C3-P6 sendiri (32.60–34.20 MHz); satu seed tidak dapat membedakannya
  dari variasi fitter. Seperti diharapkan dari analisis baseline, jalur kritis adalah jalur baca memori dan tidak
  disentuh reducer. Segmen terakhir (F_5 → memori) membaik hanya 0.2 ns padahal kini memuat satu stage
  reduksi, bukan dua: segmen itu didominasi `add_mod`/`sub_mod` butterfly dan jalur tulis.
- Reducer kini punya banyak slack di segmen tengahnya (F_3 → F_5 +32.5 ns); registernya bisa dipakai di tempat lain -
  memindahkan register antar jalur dikecualikan di Fase 5 (ADR 0011 D5) dan menjadi bagian fase memori / P berikutnya.
- t_NTT 1.3 % lebih tinggi daripada C3-P6 pada Fmax terukur (satu seed). Tujuan Fase 5 adalah aritmetika yang benar dan terukur
  (ADR 0010); 5a tidak memperbaiki waktu per transformasi.

## 5. Tidak terukur / batas
- Satu seed untuk C4a (ADR 0011 D7: seed 1–6 hanya untuk kandidat 5b). Corner selain Slow 100C untuk analisis jalur: NOT MEASURED.
  Setelan GHRD, kompilasi 20 ns, papan: NOT MEASURED (20 ns untuk C4 akhir menurut D1).
