<!-- claim-lint: skip-file (result artifact: internal status page, not proposal text) -->
# Hasil - Fase 4: Sapuan pipeline butterfly (P = 0 / 2 / 4 / 6, konfigurasi C3)

- Status: DONE
- Catatan status: selesai secara teknis atas keputusan tim 2026-10-01 (ADR 0009); Persetujuan dicentang 2026-10-01 (Bagian 9).
- Tanggal (UTC): 2026-09-30; diperbarui 2026-10-01 (sapuan seed fitter untuk P = 4 dan P = 6; evidence shell GHRD dan integrasi GHRD + C3-P4; keputusan akhir)
- Git commit (HEAD saat diverifikasi): c2cc16c ditambah working tree Fase 4, di-commit bersama file ini
- Keputusan saat ini (ADR 0009, Accepted 2026-10-01, Faza Dzil, Tim J5): L = 8, P = 6, implementasi C3-P6; anggaran desain inti NTT 30% = 12,573 ALM.
- Historis: ADR 0008 (Proposed 2026-09-30, tidak pernah diterima, kini digantikan) menerapkan anggaran 25% / 10,478 ALM saat itu dan mengusulkan P = 4. Bagian 3 dan 5 menyimpan angka tersebut sebagaimana terukur.
- Lingkungan: seperti Fase 3 -- Ubuntu 24.04.4 LTS, OSS CAD Suite 2026-09-23, cocotb 2.1.0, Quartus Prime Lite 25.1std.0 Build 1129.
- Constraint: `create_clock -period 40.000` untuk keempat revisi (ADR 0006: target tonggak eksperimental, bukan persyaratan perangkat keras atau sistem).

## 1. Kriteria selesai (Common RTL Gate, docs/ROADMAP.md)
| # | Kriteria | Evidence | Status |
|---|---|---|---|
| CRG-1 | Lint bersih | `evidence/phase04/cocotb_regression.txt` (Verilator -Wall, 0 peringatan, tiga wrapper plus inti bawaan) | PASS |
| CRG-2 | Elaborasi bersih (slang) | `evidence/phase04/cocotb_regression.txt` (0 error, 0 peringatan, tiga wrapper) | PASS |
| CRG-3 | Bit-exact terhadap model acuan, kedua simulator | `evidence/phase04/cocotb_regression.txt` (inti 16/16 dan unit 32/32 di Icarus DAN Verilator), `evidence/phase04/v2_modmul_staged_exhaustive.txt` (reducer bertingkat sama dengan reducer beku untuk semua 2^24 masukan, 0 ketidakcocokan) | PASS |
| CRG-4 | Kasus sudut sebelum tes | `evidence/phase04/test_plan.md`, di-commit sebelum RTL apa pun | PASS |
| CRG-5 | Regresi: Fase 0-3 masih lulus | `evidence/phase04/regression.txt` (pytest 23/23; C0 10/10; C1 12/12; C2, K2, K1 masing-masing 16/16, kedua simulator) | PASS |
| CRG-6 | Parameter terkunci | `evidence/phase04/regression.txt` (check_params: semua parameter terkunci sesuai) | PASS |
| CRG-7 | Evidence jumlah siklus konstan | `evidence/phase04/cocotb_regression.txt` (konstan per P dan arah, identik di kedua simulator) | PASS |
| CRG-8 | Properti formal | `evidence/phase04/formal.md` (P = 2/4/6 k-induction PASS, 9/9 sesuai harapan termasuk kontrol negatif); `evidence/phase04/regression.txt` (bukti Fase 1-3 19/19 tidak berubah). Hanya properti kontrol dan kapasitas bank, bukan aritmetika | PASS |
| CRG-9 | Evidence Quartus; tidak ada slack negatif atau kegagalan didokumentasikan | `evidence/phase04/quartus_C3-P6.md` (C3-P6 terpilih: timing terpenuhi pada 40.000 ns, juga pada seed 2–6, `evidence/phase04/seed_sweep.md`); `evidence/phase04/quartus_C3-P0.md` dan `evidence/phase04/quartus_C3-P2.md` mencatat setup slack negatif untuk P = 0 / P = 2 yang tidak terpilih (didokumentasikan, tidak disembunyikan) | PASS |
| CRG-10 | Artefak hasil + pemeriksa klaim | `cmd: python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase04.md` dan `cmd: python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal` | PASS |

## 1b. Kriteria PASS Fase 4 (docs/ROADMAP.md Fase 4)
| # | Kriteria | Evidence | Status |
|---|---|---|---|
| 1 | Benar untuk setiap P | `evidence/phase04/cocotb_regression.txt` (P = 2, 4, 6; P = 0 adalah inti Fase 3 yang dibekukan, `evidence/phase04/regression.txt`) | PASS |
| 2 | Perbandingan terukur lengkap | `evidence/phase04/selection_worksheet.md` | PASS |
| 3 | ADR untuk P terpilih | `docs/decisions/adr/ADR-0009-phase-4-final-decision-l-8-p-6-c3-p6-and-a-30-alm-design-bud.md` (Accepted: P = 6, anggaran 30%); ADR 0008 digantikan | PASS |
| 4 | Baris C3 terisi | `docs/ROADMAP.md`, baris C3-P0 / P2 / P4 / P6 | PASS |
| 5 | Tes hazard pada batas layer; siklus stall per P | `evidence/phase04/cocotb_regression.txt` (scoreboard 0 pelanggaran, data terarah ke batas, kontrol negatif pada kedalaman 8 memicunya; siklus stall 0 untuk setiap P) | PASS |

## 2. Yang dihasilkan
| Path | Fungsi |
|---|---|
| `rtl/ntt/modmul_reduce_staged.sv` | `(a*b) mod q` dengan reduksi ditulis sebagai 13 tahap pengurangan bersyarat dan register opsional di antaranya; fungsi sama dengan `modmul_reduce.sv` |
| `rtl/ntt/butterfly_shared_pipe.sv`, `rtl/ntt/pipe_delay.sv` | Butterfly pengali-bersama dengan reducer bertingkat; jalur tunda untuk operand yang melewatinya |
| `rtl/mem/poly_mem_multiport_pipe.sv` | Memori dengan permintaan/baca/tulis dalam waktu, arbitrasi slot dengan tahap register opsional; (bank, offset, slot) dari pembacaan dipakai ulang untuk penulisan |
| `rtl/ntt/ntt_core_c3.sv`, `rtl/ntt/ntt_core_c3_p2.sv`, `_p4.sv`, `_p6.sv` | Inti konfigurasi C3 (jadwal C2-K2-K1 + drain) dan tiga wrapper Quartus; posisi register sesuai bagian 2 rencana tes |
| `tb/ntt/test_modmul_staged.py`, `test_butterfly_pipe.py`, `test_poly_mem_pipe.py`, `run_p4_unit_tests.py`, `tb/ntt/p4_reducer/` | Tes unit (V2-V4) dan harness reducer menyeluruh |
| `tb/ntt/test_ntt_core_c3.py`, `tb/ntt/run_ntt_c3_tests.py` | Tes inti (V5-V8) dengan scoreboard hazard dan kontrol negatif kedalaman 8 |
| `formal/phase04-pipeline/`, `formal/run/run_formal_phase4.py` | Top formal, tiga `.sby`, runner dengan kontrol negatif |
| `quartus/phase04_pipeline_c3/` | Empat revisi, satu SDC pada 40.000 ns |
| `scripts/quartus/phase4_select_p.py`, `evidence/phase04/verification_status.json` | Aturan ADR 0007, hanya membaca file evidence |
| `quartus/phase04_pipeline_c3/C3-P{4,6}-s{2..6}.qsf`, `run_seed_sweep.sh`, `scripts/quartus/phase4_seed_sweep_summary.py`, `evidence/phase04/seed_sweep/` | Sapuan seed fitter (2026-10-01), masukan untuk ADR 0008 |
| `docs/decisions/adr/ADR-0008-apply-adr-0007-to-the-phase-4-pipeline-sweep-proposed-pipeli.md` | ADR Proposed dengan tabel terukur (digantikan ADR 0009) |
| `docs/decisions/adr/ADR-0009-phase-4-final-decision-l-8-p-6-c3-p6-and-a-30-alm-design-bud.md` | Keputusan akhir: L = 8, P = 6, anggaran inti NTT 30% |
| `evidence/phase04/ghrd_shell_measured.md`, `quartus_GHRD-de10-nano-base.md` | Shell GHRD DE10-Nano, MEASURED (tanpa inti NTT) |
| `evidence/phase04/ghrd_plus_c3p4_integration.md` | GHRD + C3-P4 dalam satu kompilasi (baseline integrasi) |
| `evidence/phase04/ghrd_plus_c3p6_integration.md` | GHRD + C3-P6 dalam satu kompilasi (konfigurasi terpilih), plus C3-P6 mandiri dengan pengaturan GHRD dan build GHRD baru; ditambahkan 2026-10-01 setelah persetujuan untuk menutup celah evidence |
| `evidence/phase04/fabric_estimate_DRAFT.md` | DRAFT, ESTIMATE: isi fabric Fase 5–10 |
| `docs/reports/CHIPATON_Phase4_Report.pdf`, `scripts/build/build_phase4_report.py` | Laporan Fase 4 (Bahasa Indonesia, tata letak sama dengan Fase 0–3) dan skrip yang membangunnya ulang dari file evidence |

File beku (`modmul_reduce.sv`, `butterfly*.sv`, `twiddle_rom.sv`, `bank_map_rom.sv`, `poly_mem_multiport.sv`, `ntt_core_c2*.sv`, evidence Fase 1-3, ADR 0004) tidak diedit.

## 3. Angka (MEASURED: laporan Quartus; siklus dari simulasi)
| Besaran | P = 0 | P = 2 | P = 4 | P = 6 |
|---|---|---|---|---|
| ALM (dari 41,910) | 9,723 | 9,696 | 10,439 | 10,505 |
| Dalam anggaran 25% historis (10,478; ADR 0004, dipakai ADR 0008)? | ya | ya | ya (39 di bawah) | tidak (27 di atas) |
| Dalam anggaran 30% saat ini (12,573; ADR 0009)? | ya | ya | ya (2,134 di bawah) | ya (2,068 di bawah) |
| Kandidat di bawah anggaran saat ini (aturan ADR 0007, seed bawaan)? | tidak (timing) | tidak (timing) | ya (d = 0.051) | ya, terpilih (t_NTT minimum) |
| Register | 3,097 | 3,817 | 4,145 | 4,168 |
| Blok RAM (M10K) | 0 / 553 | 16 / 553 | 26 / 553 | 29 / 553 |
| DSP | 9 / 112 | 9 / 112 | 9 / 112 | 9 / 112 |
| Worst setup slack @ 40.000 ns | -90.653 ns | -0.368 ns | +8.734 ns | +10.753 ns |
| Worst hold slack | +0.207 ns | +0.174 ns | +0.157 ns | +0.140 ns |
| Timing terpenuhi pada 40.000 ns? | tidak | tidak | ya | ya |
| Fmax, slow corner terendah (MHz) | 7.65 | 24.77 | 31.98 | 34.19 |
| Siklus NTT / INTT | 113 / 369 | 115 / 371 | 117 / 373 | 119 / 375 |
| Siklus stall terhadap 113+P / 369+P | 0 | 0 | 0 | 0 |
| t_NTT / t_INTT (us) = siklus / Fmax | 14.771 / 48.235 | 4.643 / 14.978 | 3.659 / 11.664 | 3.481 / 10.968 |
| Kandidat (ADR 0007)? | tidak | tidak | ya | tidak |

Sumber: `evidence/phase04/quartus_C3-P<n>.md`, `selection_worksheet.md`,
`cocotb_regression.txt`. Angka P = 0 adalah kompilasi baru pada 40.000 ns, bukan hasil Fase 3 pada 20.000 ns. Hasil
historis di bawah 25%: P = 4 satu-satunya kandidat, diusulkan oleh ADR 0008 dan tidak pernah diterima. Di bawah anggaran 30% ADR 0009 kandidatnya {4, 6} dan aturan memilih P = 6 pada seed bawaan; lintas seed 1–6 aturan memilih P = 6 pada seed 1, 4, 5 dan P = 4 pada seed 2, 3, 6 (dekat garis seri 5%). Latensi C3-P6 pada constraint 40.000 ns yang terpenuhi (perhitungan tim): NTT 119 × 40 ns = 4.76 µs, INTT 375 × 40 ns = 15.00 µs.

## 4. Standar dan sumber yang dipatok
Tidak ada pembacaan FIPS 203 pada fase ini; tidak ada parameter, algoritma, nilai twiddle, atau hasil reduksi yang berubah
(`check_params.py` lulus; reducer bertingkat sama dengan `modmul_reduce` untuk semua 2^24 pasangan masukan).

## 5. Cakupan dan batas
- Hanya simulasi dan static timing. Tidak ada papan terpasang; tidak ada yang di sini merupakan validasi perangkat keras. Fmax bersifat kernel-only, pin virtual, dan bukan clock sistem.
- Margin ALM dan sapuan seed (2026-10-01). P = 4 berada 39 ALM di bawah anggaran dan P = 6 27 ALM di atasnya pada seed bawaan. Sapuan atas seed fitter 1–6 (`evidence/phase04/seed_sweep.md`) menemukan P = 6 melebihi anggaran pada setiap seed (10,484–10,516 ALM) dan P = 4 dalam anggaran pada 4 dari 6 seed (10,439–10,503 ALM); semua 12 kompilasi memenuhi 40.000 ns. Aturan karenanya tidak pernah memilih P = 6; untuk P = 4 margin anggaran hanya beberapa puluh ALM dan bergantung seed.
- Inferensi perkakas mengubah gambaran sumber daya. Dengan register di jalur memori, Quartus meng-infer `bank_map_rom` dan beberapa rantai register ke M10K (16 / 26 / 29 blok). Ini tidak dirancang; inilah sebabnya P = 2 memiliki ALM lebih sedikit daripada P = 0 meskipun registernya lebih banyak.
- Hampir seri (seed bawaan). P = 6 memiliki t_NTT terendah (3.481 us); P = 4 berada 5.1% di atasnya. Syarat ALM menjaga P = 6 tetap di luar, pada setiap seed yang diukur.
- P = 2 gagal timing sebesar 0.368 ns pada satu slow corner (slow 100C adalah +0.061 ns); tidak ada pengecualian yang ditambahkan.
- Formal hanya mencakup kontrol dan kapasitas bank. Aritmetika dan integritas data bertumpu pada simulasi dan pemeriksaan reducer menyeluruh. Dua kontrol negatif (NC-B, NC-C) berstatus UNKNOWN pada alur pembuktian, bukan kegagalan yang didemonstrasikan; NC-B didemonstrasikan lewat BMC kedalaman 125, NC-C hanya lewat induksi yang gagal.
- Hasil yang diharapkan yang dinyatakan pada rencana tes sebelum pengukuran (P = 0 dan kemungkinan P = 2 bukan kandidat) terbukti.

## 5b. Evidence shell sistem dan integrasi (2026-10-01)
- MEASURED, `evidence/phase04/ghrd_shell_measured.md`: GHRD DE10-Nano Intel (`de10-nano-base`, tanpa inti NTT) memakai 1,304–1,309 ALM (dua build), 35 M10K, 0 DSP; blok keras HPS memakai 0 ALM fabric.
- MEASURED, `evidence/phase04/ghrd_plus_c3p4_integration.md`: GHRD + C3-P4 dalam satu kompilasi = 12,754 ALM; C3-P4 sendiri dengan pengaturan kompilasi GHRD = 11,432; GHRD sendiri = 1,304; timing terpenuhi pada setiap clock termasuk clock NTT pada 40.000 ns; kesulitan packing Low; interkoneksi puncak 48.2 %.
- INFERENSI: delta integrasi +18 ALM dengan pengaturan konsisten; pengaturan optimasi global GHRD menyumbang +993 ALM pada inti.
- MEASURED, `evidence/phase04/ghrd_plus_c3p6_integration.md` (ditambahkan 2026-10-01, setelah Persetujuan, untuk C3-P6 terpilih): GHRD + C3-P6 dalam satu kompilasi = 12,375 ALM (29.53 % dari perangkat), 62 M10K, 9 DSP; C3-P6 sendiri dengan pengaturan kompilasi GHRD = 11,053; GHRD sendiri (build penuh baru) = 1,304; timing terpenuhi pada setiap clock termasuk clock NTT pada 40.000 ns (setup +11.364 ns, Fmax 34.92 MHz pada slow corner terendah); kesulitan packing Low; interkoneksi puncak 37.0 %.
- INFERENSI: delta integrasi +18 ALM dengan pengaturan konsisten (sama seperti C3-P4); pengaturan global GHRD menyumbang +548 ALM pada inti C3-P6 (+993 pada C3-P4). 12,375 adalah desain gabungan, bukan pemeriksaan terhadap anggaran inti NTT 12,573 pada ADR 0009.
- TIDAK DIUKUR: koneksi jembatan HPS–NTT yang sebenarnya; seed lain dari kompilasi gabungan.

## 6. Penyimpangan, kegagalan, dan masalah terbuka
- Rencana mengharapkan jumlah tahap register menghasilkan P = RdLat + WrDly dengan WrDly = P/2; begitulah cara potongan ditempatkan (potongan A/M sebelum data baca, potongan X/D sesudahnya), dan jumlah siklus terukur sama dengan 113 + P dan 369 + P untuk setiap P.
- Jenis peringatan baru dibanding Fase 3: Warning 10036 (x8 per revisi, net dummy `unused_clk` / `unused_ck_rst` yang sengaja tidak dipakai di `modmul_reduce_staged.sv` dan `pipe_delay.sv`; tidak berbahaya, ada untuk menjaga port tetap bersih lint). Critical warning: 15725 (clock pin virtual, semua revisi, seperti Fase 1-3) dan 332148 (timing tidak terpenuhi; P = 0 x4, P = 2 x1, P = 4 dan P = 6 tidak ada). Tidak ada waiver, false path selain input reset, atau constraint multicycle yang ditambahkan.
- Tes memori Icarus/Verilator awalnya gagal di Icarus karena penyimpanan tidak di-reset (X); tes dikoreksi agar hanya mengonversi port pada alamat yang sudah ditulis. RTL tidak berubah karenanya.
- Icarus menolak gaya desain yang mencampur driver kontinu dan prosedural pada satu array; RTL (`pipe_delay`, register arbitrasi) diubah menjadi register per tahap plus assign. Fungsi tidak berubah, diverifikasi ulang.

## 7. Keputusan yang diperlukan
- ~~Terima, ubah, atau tolak ADR 0008 (P = 4 diusulkan)~~ - diputuskan 2026-10-01 oleh ADR 0009: P = 6 dengan anggaran inti NTT 30%; ADR 0008 digantikan.
- ~~Cara membaca CRG-9 untuk P = 0 / 2~~ - C3-P6 terpilih memenuhi 40.000 ns; kegagalan P = 0 / 2 tetap didokumentasikan sebagai non-kandidat terukur.
- Terbuka untuk fase berikutnya: pengaturan kompilasi build sistem (pengaturan GHRD menaikkan C3-P4 dari 10,439 ke 11,432 ALM, MEASURED); kompilasi P = 6 + GHRD sudah dilakukan (Bagian 5b, MEASURED); anggaran sumber daya tingkat sistem (belum didefinisikan).

## 8. Klaim yang dibuat pada fase ini
Tidak ada yang ditulis untuk juri/teks proposal. Baris C3 ROADMAP diisi dari evidence di atas.

## 9. Persetujuan
- [x] Penyetuju manusia (Faza Dzil, 2026-10-01; dicentang oleh asisten atas instruksi eksplisit penyetuju):
      Fase berikutnya dimulai hanya setelah anggota tim mencentang kotak ini. Tim menyatakan Fase 4 selesai secara teknis
      pada 2026-10-01 dan mencatat keputusan sebagai ADR 0009 (L = 8, P = 6, anggaran inti NTT 30%).
