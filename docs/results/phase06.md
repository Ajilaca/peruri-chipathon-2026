<!-- claim-lint: skip-file (result artifact: internal status page, not proposal text) -->
# Hasil - Fase 6: Penjadwalan NTT pada tingkat operasi (sequencer aritmetika K-PKE) dan S10 (memori 16-bank 1R1W)

- Status: DONE
- Catatan status: kriteria PASS Fase 6 terpenuhi (bit-exact, jumlah, siklus konstan, evidence Quartus). S10 diadopsi oleh aturannya yang ditetapkan sebelumnya (ADR 0025 Proposed: tim menerima atau menolak). Opsi 50 MHz nomor 1 dan 2 dari 2026-10-03 tercatat. Kotak Persetujuan (Bagian 10) kosong; kotak Fase 5 dan 5M juga masih kosong.
- Tanggal (UTC): 2026-10-02 sampai 2026-10-03
- Git commit (HEAD saat diverifikasi): 016bff0 (RTL Fase 6), 8d8cb6f (RTL S10), ditambah commit dokumentasi
- Hasil: aritmetika K-PKE untuk KeyGen, Encrypt, dan Decrypt berjalan sebagai program tetap di perangkat keras, bit-exact terhadap K-PKE acuan yang tidak dimodifikasi, dengan jumlah transformasi acuan dan siklus konstan (KeyGen 5,493, Encrypt 6,810, Decrypt 3,121 dengan inti S7). S10 menghapus arbitrasi slot: Fmax median 44.320 MHz pada 40 ns (S7 38.720), ALM 5,077 (S7 9,391), 118 siklus, dan timing terpenuhi pada 20.000 ns di 6 dari 6 seed (kernel-only).
- Lingkungan: Ubuntu 24.04.4 LTS, OSS CAD Suite 2026-09-23 (Verilator 5.053), cocotb 2.1.0, Quartus Prime Lite 25.1std.0 Build 1129.
- Constraint: 40.000 ns (`quartus/phase06_sched/P.sdc`); kompilasi informasi pada 20.000 ns (`P-20.sdc`, `quartus/phase05m_memsched/M-20.sdc`).

## 1. Kriteria selesai (Common RTL Gate, docs/ROADMAP.md)
| # | Kriteria | Evidence | Status |
|---|---|---|---|
| CRG-1 | Lint bersih | `evidence/phase06/verify.md`, `evidence/phase06/s10/verify.md` (Verilator -Wall: 0 peringatan pada kpke_sched_top, ntt_core_s10_p5, kpke_sched_top_s10) | PASS |
| CRG-2 | Elaborasi bersih (slang) | `evidence/phase06/verify.md`, `evidence/phase06/s10/verify.md` (slang rc 0) | PASS |
| CRG-3 | Bit-exact terhadap model acuan, kedua simulator | `evidence/phase06/verify.md` (model jadwal acuan 26 pytest; pwm_unit 20,035 pasangan; top 3 acak + 2 kasus sudut per program, ujung ke ujung terhadap K-PKE acuan; Verilator dan Icarus), `evidence/phase06/s10/verify.md` (memori S10, inti, top Fase 6 dengan S10) | PASS |
| CRG-4 | Kasus sudut sebelum tes | `evidence/phase06/test_plan.md`, `evidence/phase06/test_plan_s10.md` (ditulis sebelum RTL; Amandemen A1 S10 bertanggal dan dijelaskan) | PASS |
| CRG-5 | Regresi: fase sebelumnya masih lulus | Tidak ada file RTL, tes, atau bukti yang sudah ada diubah (semua file baru; git diff --name-status f5e4e21 HEAD mencantumkan penambahan ditambah satu dokumen, ADR 0019); regresi penuh Fase 0-5M dijalankan pada 300aaf3: `evidence/phase05m/s8/regression.md` | PASS |
| CRG-6 | Parameter terkunci | `evidence/phase06/verify.md` (ROM dibangkitkan ulang dari model acuan byte demi byte); tidak ada q, n, akar, atau aritmetika FIPS 203 yang berubah | PASS |
| CRG-7 | Evidence jumlah siklus konstan | `evidence/phase06/verify.md` (satu jumlah siklus per program atas masukan acak dan kasus sudut, kedua simulator), `evidence/phase06/s10/verification_status.json` (118 / 118) | PASS |
| CRG-8 | Properti formal | `evidence/phase06/formal.md` (sequencer H, T, C, R; NC-T gagal), `evidence/phase06/s10/formal.md` (S10 H, O, R, A, B, C; NC-O, NC-A gagal) | PASS |
| CRG-9 | Evidence Quartus; tidak ada slack negatif atau kegagalan didokumentasikan | `evidence/phase06/quartus_P6.md` (timing terpenuhi pada 40 ns), `evidence/phase06/s10/quartus_S10.md` (+ seed 2-6, akhiran -s2 sampai -s6, semua terpenuhi), `evidence/phase06/s10/quartus_S10-20.md` (+ seed 2-6, terpenuhi pada 20 ns). S7 pada 20 ns TIDAK memenuhi timing dan didokumentasikan: `evidence/phase05m/fmax50/quartus_S7-20.md` (+ seed 2-6) | PASS |
| CRG-10 | Artefak hasil + pemeriksa klaim | `cmd: python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase06.md` dan `cmd: python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal` | PASS |

## 1b. Kriteria PASS Fase 6 (docs/ROADMAP.md Fase 6)
| # | Kriteria | Evidence | Status |
|---|---|---|---|
| 1 | Aritmetika tingkat operasi bit-exact, matriks dan noise disuntikkan dari model acuan | `evidence/phase06/verify.md` | PASS |
| 2 | Penghitung transformasi sama dengan jumlah yang direproduksi (KeyGen 6/0/9, Encaps 3/4/12, Decaps 6/5/15) | `tb/golden/op_counts.py`, `evidence/phase06/verify.md` (penghitung perangkat keras 6/0/9, 3/4/12, 3/1/3; Decaps = Decrypt + Encrypt) | PASS |
| 3 | Jumlah siklus konstan; siklus dan evidence Quartus tercatat | `evidence/phase06/verify.md`, `evidence/phase06/quartus_P6.md` | PASS |
| 4 | Sub-langkah 6b (radix-4) terukur atau "tidak dicoba" | tidak dicoba (tidak diminta; cakupan ADR 0024) | PASS |

## 2. Yang dihasilkan
| Path | Fungsi |
|---|---|
| `tb/golden/op_counts.py`, `tb/golden/kpke_sched_model.py`, `tb/golden/tests/test_kpke_sched_model.py` | Jumlah transformasi yang direproduksi; model jadwal acuan terbukti sama dengan K-PKE acuan |
| `scripts/build/gen_kpke_sched_roms.py`, `rtl/sched/gamma_rom.sv`, `rtl/sched/kpke_prog_rom.sv` | Tabel γ dan program operasi yang dibangkitkan |
| `rtl/sched/poly_store.sv`, `pwm_unit.sv`, `kpke_sched.sv`, `kpke_sched_top.sv`, `kpke_sched_top_s10.sv` | Blok Fase 6: slot, perkalian-akumulasi pointwise, sequencer, top dengan inti S7 dan S10 |
| `rtl/mem/poly_mem_m10k.sv`, `rtl/ntt/ntt_core_s10.sv`, `ntt_core_s10_p5.sv` | S10: memori 16-bank 1R1W, inti, dan wrapper |
| `tb/sched/`, `tb/s10/`, `formal/phase06-scheduling/`, `formal/s10/`, `formal/run/run_formal_phase6.py`, `formal/run/run_formal_s10.py` | Tes, top formal dan runner dengan kontrol negatif |
| `quartus/phase06_sched/`, `quartus/phase05m_memsched/S7-20*.qsf` | Revisi P6, S10[-s2..s6], S10-20[-s2..s6], P6S10, P6S10-20, S7-20[-s2..s6] |
| `scripts/test/phase6_verify.sh`, `s10_verify.sh`, `select_s10.py`, `phase5m_top_paths.tcl`, `build_phase6_report.py` | Verifikasi, aturan, analisis jalur, laporan |
| `evidence/phase06/`, `evidence/phase05m/fmax50/` | Evidence |
| `docs/decisions/0024`, `0025` | Urutan Fase 6 / S10 (Accepted), hasil S10 (Proposed) |
| `docs/reports/CHIPATON_Phase6_Report.pdf` | Laporan (Bahasa Indonesia) |

## 3. Angka (MEASURED: laporan Quartus; siklus dari simulasi; median dan t INFERENSI / perhitungan tim)
| Besaran | Inti S7 | Inti S10 | P6 (sequencer + S7) |
|---|---|---|---|
| ALM (median seed 1-6, min-maks; P6 seed 1) | 9,391.0 (9,361-9,405) | 5,077.0 (5,045-5,091) | 9,840 |
| Register | 4,296-4,324 | 543-555 | 4,589 |
| M10K / DSP | 31 / 16 | 24 / 16 | 58 / 26 |
| Timing pada 40.000 ns | terpenuhi, setiap seed | terpenuhi, setiap seed | terpenuhi |
| Fmax slow corner terendah pada 40 ns (MHz) | median 38.720 (37.89-40.29) | median 44.320 (42.34-46.65) | 37.59 (seed 1) |
| Timing pada 20.000 ns, seed terpenuhi | 0 / 6 (worst setup -1.388 sampai -2.431 ns) | 6 / 6 (worst setup +0.792 sampai +1.718 ns) | tidak dikompilasi dengan S7; dengan S10 (P6S10-20, seed 1): terpenuhi, +0.619 ns, 51.60 MHz, 5,643 ALM |
| Siklus NTT / INTT | 120 / 120 | 118 / 118 | - |
| t_NTT pada Fmax median (us) | 3.099 | 2.662 | - |
| Siklus K-PKE KeyGen / Encrypt / Decrypt | 5,493 / 6,810 / 3,121 (P6 dengan S7) | 5,475 / 6,789 / 3,109 (P6 dengan S10) | |

Sumber: `evidence/phase06/s10/selection_worksheet.md`, `evidence/phase06/quartus_P6.md`, `evidence/phase05m/fmax50/path_analysis.md`, file verify di atas.
Top Fase 6 dengan inti S10 (informasi, seed 1; `evidence/phase06/quartus_P6S10.md`, `evidence/phase06/quartus_P6S10-20.md`): 40 ns 5,553 ALM, 840 register, 26 DSP, 51 M10K, 43.26 MHz; 20 ns timing terpenuhi, setup +0.619 ns, 51.60 MHz, 5,643 ALM.
Perpindahan data lewat port host inti (satu koefisien per siklus): transformasi x (257 muat + 260 baca-balik) siklus = 3,102 dari 5,493 siklus KeyGen (56 %, perhitungan tim dari panjang operasi RTL).

## 4. Standar dan sumber yang dipatok
FIPS 203 Algoritma 11 (MultiplyNTTs), 12 (BaseCaseMultiply), 13-15 (K-PKE) sebagaimana ditranskripsi di `tb/golden/`; tabel γ dan program dibangkitkan dari model acuan; tidak ada parameter atau aritmetika yang berubah (`check_params.py` tidak berubah dan lulus pada regresi terakhir).

## 5. Cakupan dan batas
- Hanya simulasi, formal, dan static timing. Tidak ada papan; Fmax bersifat kernel-only dengan pin virtual. "Timing terpenuhi pada 20 ns" adalah static timing alur ini, bukan sistem pada 50 MHz.
- Keccak, sampler, kompresi, encoding, dan transformasi FO tidak ada di perangkat keras (masukan disuntikkan oleh testbench, sebagaimana disyaratkan ROADMAP untuk Fase 6).
- Formal mencakup kontrol, bukan data. P6 adalah satu kompilasi (seed 1). Tidak ada analisis jalur setelah S10.
- Port host inti (satu koefisien per siklus) mendominasi siklus operasi; antarmuka yang lebih lebar adalah pekerjaan mendatang (tidak diukur).

## 6. Penyimpangan, kegagalan, dan masalah terbuka
- Tes inti S10: jalankan pertama gagal hanya pada batas latensi start dari tes S7 yang dipakai ulang; dicatat sebagai Amandemen A1 rencana S10 dengan penurunannya (tidak ada ambang yang diubah).
- Kompilasi informasi pertama P6S10 dimulai dengan nama entitas top yang salah (`kpke_sched_top_s10_s10`, selip penggantian teks), dihentikan, diperbaiki, dan dimulai ulang; perkakas menulis ulang `.qpf` proyek sementara itu; daftar revisi dipulihkan.
- Sebuah pesan status mengutip "-0.836 ns" untuk S7 pada 20 ns seed 1; itu satu corner; yang terburuk di semua corner adalah -1.388 ns (dikoreksi di `fmax50/path_analysis.md`).
- `%Warning-UNOPTFLAT` pada build Verilator cocotb untuk reducer Barrett yang dibekukan (seperti Fase 5): pemberitahuan penjadwalan simulasi, dicatat di file verify.
- Critical Warning 15725 (clock pin virtual) di setiap kompilasi, seperti fase sebelumnya; tidak ada 332148 di kompilasi S10 mana pun; ditriase, tidak ada yang di-waive.

## 7. Keputusan yang diperlukan
- ADR 0025 (S10 diadopsi oleh aturan): terima S10 sebagai memori inti (dan top Fase 6 dengan S10) untuk fase berikutnya?
- ADR 0021 (S7), ADR 0022 (S9), ADR 0023 (S8) masih Proposed (S10 menggantikan pertanyaan S9 jika ADR 0025 diterima). PENDING #25, #26, #27. Kotak Persetujuan Fase 5, 5M, dan 6.

## 8. Klaim yang dibuat pada fase ini
Tidak ada yang ditulis untuk juri/teks proposal. Baris ROADMAP diisi dari evidence di atas.

## 9. Mereproduksi
```bash
. scripts/env.sh
scripts/test/phase6_verify.sh; python3 formal/run/run_formal_phase6.py
scripts/test/s10_verify.sh;    python3 formal/run/run_formal_s10.py
cd quartus/phase06_sched && ./run_p6.sh && ./run_s10_sweep.sh && ./run_p6s10.sh; cd ../..
cd quartus/phase05m_memsched && ./run_s7_20_sweep.sh; cd ../..
python3 scripts/quartus/select_s10.py
python3 scripts/build/build_phase6_report.py
python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase06.md
python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal
```

## 10. Persetujuan
- [x] Penyetuju manusia (nama, tanggal): Jevan (Tim J5), 2026-10-03
      Fase berikutnya dimulai hanya setelah anggota tim mencentang kotak ini. Claude tidak pernah mencentangnya.
