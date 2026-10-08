<!-- claim-lint: skip-file (result artifact: internal status page, not proposal text) -->
# Hasil - Fase 5: Optimasi aritmetika modular (konfigurasi C4: 5a fold, 5b Barrett lawan Montgomery, 5c INTT lazy, 5d tidak dicoba)

- Status: DONE
- Catatan status: selesai secara teknis menurut rencana Fase 5 (setiap sub-langkah yang dicoba benar dan terukur; 5d ditandai "tidak dicoba"). Dua catatan masih Proposed dan menunggu tim: ADR 0013 (pilihan 5b: Barrett, DSP 9 -> 18; PENDING #23) dan ADR 0015 (5d tidak dicoba, dipindah ke Fase 6). Kotak Persetujuan (Bagian 10) kosong.
- Tanggal (UTC): 2026-10-01 sampai 2026-10-02
- Git commit (HEAD saat diverifikasi): c572864 ditambah working tree penutupan Fase 5, di-commit bersama file ini
- Konfigurasi hasil: C4 = C4b-B (reducer Barrett pada inti C3-P6, L = 8, P = 6), dipilih oleh aturan ADR 0011; 5c (C4c) terukur dan TIDAK diadopsi (aturan ADR 0014). Siklus tidak berubah: NTT 119, INTT 375.
- Lingkungan: Ubuntu 24.04.4 LTS, OSS CAD Suite 2026-09-23 (Verilator 5.053), cocotb 2.1.0, Quartus Prime Lite 25.1std.0 Build 1129.
- Constraint: `create_clock -period 40.000` (`quartus/phase05_arith_c4/C4.sdc`) untuk setiap revisi C4 (ADR 0011 D1); kompilasi informasi C4b-B dan C3-P6 pada 20.000 ns (`C4-20.sdc`). 50 MHz bersifat usaha terbaik, bukan gerbang (ADR 0010).

## 1. Kriteria selesai (Common RTL Gate, docs/ROADMAP.md)
| # | Kriteria | Evidence | Status |
|---|---|---|---|
| CRG-1 | Lint bersih | `evidence/phase05/5a/verify.txt`, `evidence/phase05/5b/verify.txt`, `evidence/phase05/5c/verify.txt`, `evidence/phase05/regression.md` (Verilator -Wall 0 peringatan pada setiap wrapper dan inti bawaan; modul daun sendiri hanya memberi UNUSEDPARAM untuk konstanta ntt_pkg, seperti Fase 4) | PASS |
| CRG-2 | Elaborasi bersih (slang) | `evidence/phase05/regression.md` (slang 0 error, 0 peringatan, wrapper C4a, C4b-B, C4b-M, C4c dan inti bawaan) | PASS |
| CRG-3 | Bit-exact terhadap model acuan, kedua simulator | `evidence/phase05/regression.md` (tes unit dan tes inti di Verilator DAN Icarus; reducer menyeluruh: fold 0 ketidakcocokan atas semua a, b dalam [0, q), Barrett dan Montgomery demikian pula, Barrett lazy 0 ketidakcocokan atas 22,164,482 pasangan) | PASS |
| CRG-4 | Kasus sudut sebelum tes | `evidence/phase05/test_plan.md` (di-commit sebelum RTL Fase 5 apa pun; amandemen A1-A4 bertanggal dan dijelaskan) | PASS |
| CRG-5 | Regresi: Fase 0-4 masih lulus | `evidence/phase05/regression.md` (skrip Fase 0-4: 21 langkah, 0 gagal, OVERALL PASS, pada git b418d1e; pytest golden, cocotb Fase 1-4 di kedua simulator, reducer bertingkat menyeluruh Fase 4, formal Fase 1-3 dan Fase 4) | PASS |
| CRG-6 | Parameter terkunci | `evidence/phase05/regression.md` (check_params: semua parameter terkunci sesuai); tidak ada q, n, akar kesatuan, atau aritmetika FIPS 203 yang berubah | PASS |
| CRG-7 | Evidence jumlah siklus konstan | `evidence/phase05/regression.md` (C4a, C4b-B, C4b-M, C4c: NTT 119 dan INTT 375, 0 stall, identik di kedua simulator), `evidence/phase05/5b/verification_status.json`, `evidence/phase05/5c/verification_status.json` | PASS |
| CRG-8 | Properti formal | `evidence/phase05/regression.md` (formal Fase 5: 14/14 sesuai harapan, termasuk kontrol negatif), `evidence/phase05/5a/formal.md`, `evidence/phase05/5b/formal.md`, `evidence/phase05/5c/formal.md` (properti kontrol dan kapasitas bank untuk setiap wrapper; bukti batas nilai logika masukan/keluaran butterfly lazy dengan kontrol negatif yang gagal). Kesamaan aritmetika bertumpu pada pemeriksaan menyeluruh, bukan formal | PASS |
| CRG-9 | Evidence Quartus; tidak ada slack negatif atau kegagalan didokumentasikan | `evidence/phase05/5a/quartus_C4a.md`, `evidence/phase05/5b/quartus_C4b-B.md` (+ seed 2-6, nama sama dengan akhiran -s2 sampai -s6), `evidence/phase05/5b/quartus_C4b-M.md` (+ seed 2-6, nama sama dengan akhiran -s2 sampai -s6), `evidence/phase05/5c/quartus_C4c.md` (+ seed 2-6, nama sama dengan akhiran -s2 sampai -s6): timing terpenuhi pada 40.000 ns di setiap kompilasi. Dua kompilasi informasi 20.000 ns TIDAK memenuhi timing dan didokumentasikan demikian: `evidence/phase05/closure/info_20ns.md` | PASS |
| CRG-10 | Artefak hasil + pemeriksa klaim | `cmd: python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase05.md` dan `cmd: python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal` | PASS |

## 1b. Kriteria PASS Fase 5 (docs/ROADMAP.md Fase 5)
| # | Kriteria | Evidence | Status |
|---|---|---|---|
| 1 | Setiap sub-langkah yang dicoba benar dan terukur | 5a: `evidence/phase05/5a/summary_5a.md`; 5b: `evidence/phase05/5b/selection_worksheet.md`; 5c: `evidence/phase05/5c/summary_5c.md` dan `evidence/phase05/5c/selection_worksheet.md` | PASS |
| 2 | Pilihan 5b tercatat dalam ADR | `docs/decisions/adr/ADR-0013-phase-5b-choice-barrett-reducer-selected-by-the-adr-0011-rul.md` (Proposed: Barrett dipilih oleh aturan ADR 0011, DSP 9 -> 18 dinyatakan; penerimaan adalah hak tim, PENDING #23) | PASS |
| 3 | Sub-langkah opsional diselesaikan dengan evidence atau secara eksplisit "tidak dicoba" | 5c selesai dan tidak diadopsi: `docs/decisions/adr/ADR-0014-phase-5c-lazy-intt-butterfly-inputs-operand-contract-d6-amen.md` (Accepted, catatan hasil). 5d "tidak dicoba": `docs/decisions/adr/ADR-0015-phase-5d-karatsuba-style-base-case-not-attempted-in-phase-5-.md` (Proposed) dan baris C4d pada `docs/ROADMAP.md` | PASS |
| 4 | Baris ablasi C4 terisi | `docs/ROADMAP.md`, baris C4a / C4b-B / C4b-M / C4c / C4d dan dua baris informasi 20 ns | PASS |
| 5 | Artefak evidence dengan satu bagian per sub-langkah | `evidence/phase05/` (`baseline/`, `5a/`, `5b/`, `5c/`, `closure/`; tidak ada `5d/` karena 5d tidak dicoba) dan Bagian 3b file ini | PASS |

## 2. Yang dihasilkan
| Path | Fungsi |
|---|---|
| `rtl/arith/modmul_fold.sv`, `modmul_barrett.sv`, `modmul_montgomery.sv`, `twiddle_rom_mont.sv`, `modmul_sel.sv` | Tiga reducer di balik satu antarmuka (`RED_KIND` 0 bertingkat beku, 1 fold, 2 Barrett, 3 Montgomery) dan ROM twiddle bentuk Montgomery (dibangkitkan skrip) |
| `rtl/arith/butterfly_c4.sv`, `rtl/ntt/ntt_core_c4.sv` | Butterfly dan inti dengan reducer dipilih lewat parameter; wrapper `ntt_core_c4a.sv`, `ntt_core_c4b_b.sv`, `ntt_core_c4b_m.sv`, `ntt_core_c4c.sv` |
| `rtl/arith/lazy_bfly_io.sv`, `modmul_barrett_lazy.sv`, `butterfly_c4_lazy.sv` | 5c: logika masukan/keluaran INTT lazy, varian Barrett dengan operand 13-bit, butterfly lazy (hanya eksperimen, tidak diadopsi) |
| `tb/arith/` | Harness menyeluruh (`reducer_exhaustive/`, `lazy_exhaustive/`), tes unit, runner inti, pemeriksaan ROM Montgomery |
| `formal/phase05-arith/`, `formal/run/run_formal_phase5.py` | Top formal dan file `.sby` per wrapper, bukti batas logika lazy, runner dengan kontrol negatif |
| `quartus/phase05_arith_c4/` | Proyek, revisi `C4a`, `C4b-{B,M}[-s2..s6]`, `C4c[-s2..s6]`, `C4b-B-20`, `C3-P6-20`, `C4.sdc` (40 ns), `C4-20.sdc` (20 ns), skrip sapuan |
| `scripts/test/phase5_verify.sh`, `phase5_regression.sh`, `phase5_select_5b.py`, `phase5_select_5c.py`, `phase5_segments.tcl`, `phase5_top_paths.tcl`, `phase5_path_classes.py`, `phase5_stall_cycles.py`, `gen_twiddle_rom_mont.py`, `build_phase5_report.py` | Verifikasi, aturan pemilihan (hanya membaca file evidence), analisis timing pada salinan, pembangun laporan |
| `evidence/phase05/` | Rencana tes, analisis jalur kritis baseline, evidence per sub-langkah, regresi, kompilasi informasi 20 ns |
| `docs/decisions/0010` sampai `0015` | Tujuan timing Fase 5, keputusan rencana D1-D8, aturan siklus dan ALM, pilihan 5b (Proposed), 5c (Accepted), 5d (Proposed) |
| `docs/reports/CHIPATON_Phase5_Report.pdf`, `scripts/build/build_phase5_report.py` | Laporan Fase 5 (Bahasa Indonesia, tata letak sama dengan Fase 0-4) dan skrip yang membangunnya ulang dari file evidence |

File beku Fase 1-4 (RTL, tes, formal, evidence, ADR) tidak diedit; satu-satunya catatan yang sudah ada dan disentuh adalah `docs/decisions/adr/ADR-0006-phase-4-target-clock.md` (catatan amandemen, teks tidak berubah) dan `docs/decisions/PENDING.md` (diperiksa dengan `git diff --name-status 5a1eec0 HEAD`).

## 3. Angka (MEASURED: laporan Quartus; siklus dari simulasi)
| Besaran | C3-P6 (Fase 4) | C4a (fold) | C4b-B (Barrett) | C4b-M (Montgomery) | C4c (INTT lazy, tidak diadopsi) |
|---|---|---|---|---|---|
| ALM, seed bawaan (dari 41,910) | 10,505 | 9,847 | 9,208 | 9,249 | 9,043 |
| ALM, seed 1-6 (min-maks) | 10,484-10,516 | hanya satu kompilasi | 9,166-9,208 | 9,249-9,297 | 9,032-9,094 |
| Dalam 12,573 ALM (ADR 0009)? | ya | ya | ya | ya | ya |
| Register (seed bawaan) | 4,168 | 4,109 | 4,115 | 4,297 | 4,076 |
| M10K / DSP | 29 / 9 | 29 / 9 | 29 / 18 | 29 / 9 | 29 / 18 |
| Worst setup slack @ 40.000 ns (seed bawaan) | +10.753 | +10.352 | +11.044 | +9.526 | +9.682 |
| Timing terpenuhi pada 40.000 ns, setiap seed yang diukur | ya | ya | ya | ya | ya |
| Fmax slow corner terendah, seed bawaan (MHz) | 34.19 | 33.73 | 34.54 | 32.81 | 32.98 |
| Fmax median atas seed 1-6 (rentang) (MHz) | 33.11 (32.60-34.20) | hanya satu kompilasi | 34.515 (33.46-34.84) | 33.780 (32.81-34.25) | 33.100 (32.27-35.26) |
| Siklus NTT / INTT | 119 / 375 | 119 / 375 | 119 / 375 | 119 / 375 | 119 / 375 |
| t_NTT / t_INTT pada Fmax median (us, perhitungan tim) | 3.594 / 11.326 | tidak dihitung | 3.448 / 10.865 | 3.523 / 11.101 | 3.595 / 11.329 |

Sumber: `evidence/phase04/quartus_C3-P6.md` dan `seed_sweep.md` (median seed C3-P6 dihitung ulang dari file-file itu), `evidence/phase05/5a/quartus_C4a.md`, `evidence/phase05/5b/selection_worksheet.md`, `evidence/phase05/5c/selection_worksheet.md`, `evidence/phase05/regression.md`. Median, rentang, dan t = siklus / Fmax adalah INFERENSI / perhitungan tim.

Kompilasi informasi pada 20.000 ns (MEASURED, seed bawaan, `evidence/phase05/closure/info_20ns.md`): timing tidak terpenuhi oleh keduanya. C3-P6: 10,557 ALM, setup -2.059 ns, Fmax corner terendah 45.33 MHz. C4b-B: 9,305 ALM, setup -2.557 ns, Fmax corner terendah 44.33 MHz. Target 50 MHz tidak tercapai; Fmax yang dilaporkan di bawah constraint yang lebih ketat tidak dapat dibandingkan dengan angka 40 ns.

## 3b. Per sub-langkah
- 5a (C4a, reducer fold): -658 ALM terhadap C3-P6 (INFERENSI dari dua kompilasi), Fmax -0.46 MHz pada corner terendah (dalam sebaran seed), siklus tidak berubah. `evidence/phase05/5a/summary_5a.md`.
- 5b (Barrett lawan Montgomery, seed 1-6): aturan ADR 0011 memilih Barrett: Fmax median lebih tinggi (34.515 lawan 33.780 MHz, berbeda 2.13 %, dalam pita hampir-seri 5 %), lalu ALM median lebih rendah (9,171.0 lawan 9,286.5). Biaya dicatat di ADR 0013: DSP 9 -> 18. Montgomery tetap 9 DSP. ADR berstatus Proposed. `evidence/phase05/5b/selection_worksheet.md`.
- 5c (C4c, masukan INTT lazy, seed 1-6): benar, 119 / 375, ALM dan timing lulus, tetapi Fmax median 33.100 MHz di bawah 34.84 MHz yang disyaratkan aturan dan ADR 0012 tidak terpenuhi, sehingga tidak diadopsi. Rentang seed tumpang tindih (seed 2 C4c adalah 35.26 MHz), jadi selisihnya tidak dapat dibedakan dari noise seed. Analisis jalur post-hoc (slack MEASURED, hipotesis untuk penyebab): kelas terburuk tetap sisi baca memori -> masukan pengali. `evidence/phase05/5c/summary_5c.md`. Amandemen kontrak operand D6 ([0, 2q)) hanya berlaku untuk eksperimen ini; C4 mempertahankan [0, q).
- 5d: tidak dicoba (ADR 0015 Proposed). `base_case_multiply.sv` bukan bagian dari inti C3-P6 / C4.

Pembacaan teknis (INFERENSI): perubahan reducer menghemat area (C4b-B sekitar 1,300 ALM di bawah C3-P6) tetapi tidak menggeser Fmax melebihi sebaran seed; jalur kritisnya adalah pembacaan memori (analisis baseline `evidence/phase05/baseline/c3p6_critical_path.md`, ADR 0010).

## 4. Standar dan sumber yang dipatok
Tidak ada pembacaan FIPS 203 pada fase ini; tidak ada parameter, algoritma, nilai twiddle, atau hasil yang berubah (`check_params.py` lulus; setiap reducer sama dengan `(a*b) mod q` untuk semua a, b dalam [0, q), secara menyeluruh). ROM twiddle Montgomery dibangkitkan oleh `scripts/build/gen_twiddle_rom_mont.py` dari model acuan dan diperiksa oleh `tb/arith/check_mont_rom.py`. Barrett: k = 24, M = 5039. Montgomery: R = 2^12, q' = 3327.

## 5. Cakupan dan batas
- Hanya simulasi, formal, dan static timing. Tidak ada papan terpasang; tidak ada yang di sini merupakan validasi perangkat keras. Fmax bersifat kernel-only dengan pin virtual, bukan clock sistem.
- Formal mencakup kontrol, kapasitas bank, dan (5c) batas nilai. Kesamaan aritmetika bertumpu pada pemeriksaan menyeluruh (11,082,241 pasangan per reducer; 22,164,482 untuk domain operand lazy).
- C4a dan dua kompilasi 20 ns adalah kompilasi tunggal pada seed bawaan. Selisih Fmax antara C3-P6, C4a, C4b-B, C4b-M, dan C4c kecil dibanding sebaran seed (C4b-B 33.46-34.84 MHz, C4c 32.27-35.26 MHz), sehingga tidak ada peringkat Fmax di antara mereka yang diklaim melebihi yang dihitung aturan yang dinyatakan.
- Pilihan 5b mengikuti aturan yang ditetapkan sebelumnya; hampir-seri (2.13 %) dan biaya DSP (9 -> 18) adalah trade-off tim, tidak diselesaikan oleh pengukuran.
- Tidak ada analisis jalur pada 20 ns; penyebab hasil 5c adalah hipotesis.
- Tidak diukur: integrasi HPS inti C4, daya, anggaran sumber daya tingkat sistem apa pun.

## 6. Penyimpangan, kegagalan, dan masalah terbuka
- Kontrol negatif inti pertama (RdLat 1 + WrDly 7) tidak valid (0/5 hasil salah): hazard fisik bergantung pada WrDly, bukan P. Disimpan sebagai `evidence/phase05/5a/negctl_first_attempt_rd1_wr7.txt`; diganti dengan RED_KIND 0 dengan RdLat 0 + WrDly 8 (rencana tes A2).
- Pratinjau pemilihan 5b memakai kolom Fmax yang salah (34.74 / 33.93); dihitung ulang oleh skrip menjadi 34.515 / 33.780; hasilnya tidak berubah.
- Skrip kelas jalur melewatkan register potongan di dalam `modmul_sel:...u_red`; polanya diperbaiki dan keluaran baseline diverifikasi tidak berubah.
- Sebuah `git stash` sekitar 2 detik terjadi saat pekerjaan verifikasi berjalan; log tidak menunjukkan error.
- Kedua kompilasi informasi 20.000 ns berakhir dengan setup slack negatif (Critical Warning 332148 x2 masing-masing, ditambah 15725 untuk clock pin virtual seperti Fase 1-4). Ditriase di `evidence/phase05/closure/info_20ns.md`; tidak ada yang di-waive.
- `claim_lint` melaporkan 1 error yang sudah ada sebelumnya di `docs/AI_TOOLING_RESEARCH.md:197`, tidak ditimbulkan pada Fase 5 (ia memindai `docs/results docs/proposal` untuk CRG-10; lihat Bagian 9).

## 7. Keputusan yang diperlukan
- ADR 0013 (5b: Barrett, DSP 9 -> 18) berstatus Proposed: terima, atau pilih Montgomery (9 DSP) dengan menyadari bahwa aturan memilih Barrett karena hampir-seri (PENDING #23).
- ADR 0015 (5d tidak dicoba, pindah ke Fase 6) berstatus Proposed: terima, atau minta C4d mandiri.
- PENDING #19: fase "memori dan jadwal" di antara Fase 5 dan Fase 6 (batas terukur adalah jalur baca memori); belum dimulai.
- Baris ablasi untuk C4b-B dan C4b-M menyebut Barrett sebagai konfigurasi C4 selagi ADR 0013 berstatus Proposed.

## 8. Klaim yang dibuat pada fase ini
Tidak ada yang ditulis untuk juri/teks proposal. Baris C4 ROADMAP diisi dari evidence di atas.

## 9. Mereproduksi
```bash
. scripts/env.sh
scripts/test/phase5_verify.sh                      # lint, exhaustive reducers, unit and core tests on both simulators
python3 formal/run/run_formal_phase5.py           # formal incl. negative controls
scripts/test/phase5_regression.sh                  # Phase 0-4 regression
cd quartus/phase05_arith_c4
# one revision at a time (parallel runs corrupt the shared .qpf): C4a, C4b-B[-s2..s6], C4b-M[-s2..s6], C4c[-s2..s6]
./run_5b_sweep.sh; ./run_5c_sweep.sh; ./run_20ns_info.sh
cd ../..
python3 scripts/quartus/phase5_select_5b.py           # ADR 0011 rule
python3 scripts/quartus/phase5_select_5c.py --date 20261001   # ADR 0014 rule
python3 scripts/build/build_phase5_report.py        # PDF report
python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase05.md
python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal
```

## 10. Persetujuan
- [x] Penyetuju manusia (nama, tanggal): Jevan (Tim J5), 2026-10-03
      Fase berikutnya dimulai hanya setelah anggota tim mencentang kotak ini. Claude tidak pernah mencentangnya.
