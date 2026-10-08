<!-- claim-lint: skip-file (result artifact: internal status page, not proposal text) -->
# Hasil - Fase 9M: optimasi inti ML-KEM-768 (siklus, area, Fmax), simulasi dan static timing

- Status: DONE (keputusan tim 2026-10-08, Faza Dzil: setiap langkah dibangun, diverifikasi, diukur, dan dilaporkan; tiga pemeriksaan formal berbatas yang habis waktu tetap dicatat sebagai batas evidence, lihat bagian 6)
- Catatan status: cakupan ADR 0034 (Accepted, Faza Dzil 2026-10-04: butir 1-4; butir 5, sampler kedua, disimpan sebagai gagasan dan tidak dibangun), rencana Fmax ADR 0036 dan batas pelaporan ADR 0039 (keduanya Accepted). Batch 1 (9M-1, 9M-2, 9M-3, S0, S1, S1b) dikerjakan di bawah Faza Dzil dan di-commit (16 commit pada cabang); Batch 2 (S2, S2b, butir 4) dikerjakan di bawah Jevan pada sesi yang sama dan belum di-commit pada saat penulisan. Setiap langkah punya rencana tes dengan aturan adopsinya; hanya rencana butir 4 yang ditulis setelah RTL-nya (dinyatakan di rencana itu). ADR 0035, 0037, 0038, 0040, 0041, 0042, 0043 berstatus Proposed; tidak ada yang diadopsi untuk tim.
- Tanggal (UTC): 2026-10-04 / 2026-10-05 (hasil ini: 2026-10-04 23:09 UTC, 2026-10-05 06:09 WIB)
- Git commit (HEAD saat diverifikasi): cf81581 pada cabang `phase9m-optimisation` (file Batch 2 belum di-commit di atasnya)
- Hasil: inti Fase 9 (`mlkem_core`, 17,620.5 ALM, 9,095 / 10,735 / 16,667 siklus untuk KeyGen / Encaps / Decaps) menjadi `mlkem_core4` (K4) dengan 14,222.0 ALM pada 40 ns (-19 %), 8,416 / 9,611 / 12,989 siklus (-7.5 % / -10.5 % / -22.1 %) dan timing terpenuhi pada 15.000 ns di 6 dari 6 seed (Fmax median 76.665 MHz, slow corner terendah). Latensi pada 15 ns (siklus / Fmax median, perhitungan tim, static timing kernel-only, bukan pengukuran papan): 109.8 / 125.4 / 169.4 us. ACVP 100 % di kedua simulator (keyGen 25, encapsulation 25, decapsulation 10), siklus Encaps dan Decaps identik pada masukan yang diuji. K4 bertumpu pada K3 (ADR 0042), yang aturannya sendiri tidak mengadopsinya sebagaimana tertulis. P1 dari K4 dan dua kontrol negatif tidak punya hasil formal (timeout).
- Lingkungan: Ubuntu 24.04 (Linux 7.0.0-34), OSS CAD Suite (Verilator 5.053 devel, Icarus 14.0 devel, Yosys 0.69, slang 11.0, SymbiYosys dengan boolector), cocotb 2.1.0, Python 3.12.3, Quartus Prime Lite 25.1std.0 Build 1129.
- Constraint: 40.000 ns adalah gerbang (`C.sdc` Fase 5-9); 15.000 ns adalah batas pelaporan Fmax (ADR 0039; tidak ada kompilasi di bawah 15 ns kecuali sapuan S0 sampai 13 ns yang menemukan batasnya); tidak ada hasil pin virtual yang merupakan hasil papan.

## 1. Kriteria selesai (diturunkan dari ADR 0034, 0036, dan 0039; Fase 9M tidak punya entri di docs/ROADMAP.md)
| # | Kriteria | Evidence | Status |
|---|---|---|---|
| M-1 | Butir 1: dua byte per siklus pada jalur codec, aturan terpenuhi, ACVP 100 % di kedua simulator | `evidence/phase9m/batch1/9m1/result_9m1.md`, `evidence/phase9m/batch1/9m1/sim_verilator.md`, `evidence/phase9m/batch1/9m1/sim_icarus.md` | PASS |
| M-2 | Butir 2: inti pada 20 ns dengan enam seed | `evidence/phase9m/batch1/9m2/result_9m2.md` (timing terpenuhi pada 20 ns di 6 dari 6 seed untuk kedua inti) | PASS |
| M-3 | Butir 3: sponge hash K0, aturan terpenuhi | `evidence/phase9m/batch1/9m3/result_9m3.md` (ALM -1,736.5, +120 siklus) | PASS |
| M-4 | S0, S1, S1b: batas ditemukan; sampler K0; hash latar belakang; masing-masing dengan rencana, aturan, Quartus enam seed pada 40 ns dan 15 ns | `evidence/phase9m/batch1/9f0/result_9f0.md`, `evidence/phase9m/batch1/9f1/result_9f1.md`, `evidence/phase9m/batch1/9f1b/result_9f1b.md` | PASS |
| M-5 | S2 (P = 6), S2b (alamat teregister): rencana sebelum pengukuran, aturan diterapkan, hasil dilaporkan jujur (S2 netral; S2b tidak diadopsi oleh aturan sebagaimana tertulis) | `evidence/phase9m/batch2/9s2/result_9s2.md`, `evidence/phase9m/batch2/9s2b/result_9s2b.md` | PASS |
| M-6 | Butir 4: pemuatan di belakang mesin (K4), aturan terpenuhi | `evidence/phase9m/batch2/9i4/result_9i4.md`, `evidence/phase9m/batch2/9i4/selection_worksheet.md` | PASS |
| M-7 | Bit-exact terhadap model acuan dan ACVP, kedua simulator, untuk K4 akhir (hanya simulasi) | `evidence/phase9m/batch2/9i4/sim.md` (Verilator 6/6, Icarus 6/6), `evidence/phase9m/batch2/9s2b/sim.md` | PASS |
| M-8 | Evidence siklus konstan (Encaps dan Decaps identik pada masukan yang diuji) | `evidence/phase9m/batch2/9i4/cycles_verilator_core_k4.json`, `evidence/phase9m/batch2/9i4/cycles_icarus_core_k4.json` | PASS |
| M-9 | Kontrol negatif gagal sebagaimana disyaratkan (dan port host yang diperlambat lulus dengan interlock) | `evidence/phase9m/batch2/9i4/sim.md`, `evidence/phase9m/batch2/9s2b/sim.md` | PASS |
| M-10 | Evidence Quartus untuk setiap konfigurasi yang dilaporkan; slack negatif atau kegagalan didokumentasikan | worksheet di `evidence/phase9m/batch1/9m1` ... `evidence/phase9m/batch2/9i4`; K4: timing terpenuhi pada 40 ns dan 15 ns di 6 dari 6 seed masing-masing | PASS |
| M-11 | Evidence formal lengkap (setiap properti dan setiap kontrol punya hasil) | `evidence/phase9m/batch2/9i4/formal.md`, `evidence/phase9m/batch1/9f1b/formal.md`: P1 core4, NC-E1-4 dan NC-B7 core3 habis waktu; semua properti lain PASS dan kontrol lain FAIL sebagaimana disyaratkan | MISSING |
| M-12 | Regresi: nilai bawaan mereproduksi jumlah siklus sebelumnya; file Fase 6-8 yang dibekukan tidak berubah | `evidence/phase9m/batch2/9s2b/sim.md` (bawaan 118 / 118, 13/13, inti 6/6), `evidence/phase9m/batch1/9m1/regression_default.md` | PASS |
| M-13 | Parameter terkunci | `cmd: python3 .claude/skills/mlkem-guard/scripts/check_params.py` (dijalankan 2026-10-05: semua parameter terkunci sesuai); tidak ada aritmetika FIPS 203 yang berubah | PASS |
| M-14 | Artefak hasil dan pemeriksa klaim | `cmd: python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase9m.md` dan `cmd: python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results` | PASS |

## 2. Yang dihasilkan
| Path | Fungsi |
|---|---|
| `rtl/mlkem/mlkem_pack2.sv`, `mlkem_unpack2.sv`, `mlkem_wordbytes2.sv`, `mlkem_bytedst2.sv`, `mlkem_ldpoly2.sv`, `mlkem_stpoly2.sv` | jalur codec dua byte (`CODEC_W2`) |
| `rtl/mlkem/mlkem_core2.sv`, `mlkem_core3.sv`, `rtl/sample/*` (parameter sampler K0) | sampler dan hash K0 (`SMP_C5`, `HASH_C5`), sidecar hash latar belakang (K1b) |
| `rtl/ntt/ntt_core_s10.sv`, `ntt_core_s10_p5.sv`, `rtl/sched/kpke_smp_top_s10.sv` (parameter `NTT_P6`, `NTT_AR`, bawaan 0) | P = 6 dan alamat issue teregister (S2, S2b) |
| `rtl/mlkem/mlkem_core4.sv`, `mlkem_ldpoly2o.sv`, `mlkem_ctl_rom3.sv`, `rtl/sched/kpke_sched_smp4.sv`, `kpke_smp_top_s10o.sv` | pemuatan di belakang mesin (butir 4, K4) |
| `evidence/phase9m/` | rencana, hasil, worksheet, simulasi, formal, dan ekstrak Quartus per langkah (9m1, 9m2, 9m3, 9f0, 9f1, 9f1b, 9s2, 9s2b, 9i4) |
| `quartus/phase09*_core/` | proyek Quartus setiap langkah (keluaran tidak di-commit; diarsipkan di luar repositori) |
| `formal/run/run_formal_phase9*.py`, `formal/phase09m-optimisation/` | runner dan top formal |
| `docs/decisions/0034 .. 0043`, `docs/decisions/PENDING.md` #34 - #40 | keputusan (0034, 0036, 0039 Accepted; sisanya Proposed) |
| `docs/reports/CHIPATON_Phase9M_Report.pdf` (dibangun oleh `scripts/build/build_phase9m_report.py`), `docs/reports/CHIPATON_COMPLETE_REPORT.pdf` (dibangun oleh `scripts/build/build_complete_report.py`) | laporan naratif |

## 3. Angka (masing-masing MEASURED, static timing kernel-only dengan pin virtual kecuali dinyatakan lain; latensi = siklus / Fmax median, perhitungan tim)
Median enam seed. Denominator fitter: 41,910 ALM, 553 blok RAM, 112 DSP. Blok RAM 53-54 dan DSP 28 pada setiap konfigurasi.
| Konfigurasi | Perubahan | ALM 40 ns | Fmax 15 ns (MHz) | Siklus KeyGen / Encaps / Decaps | Latensi pada 15 ns (us) | Evidence |
|---|---|---|---|---|---|---|
| Inti Fase 9 (C7-core) | baseline | 17,620.5 | tidak diukur (20 ns: 63.645) | 9,095 / 10,735 / 16,667 | (20 ns: 142.9 / 168.7 / 261.9) | `evidence/phase9m/batch1/9m2/result_9m2.md` |
| MW (9M-1) | + codec dua byte | 17,654.0 | 73.635 (2 seed) | 8,327 / 10,159 / 15,515 | 113.6 / 138.5 / 211.6 (yang lebih rendah dari 2 seed) | `evidence/phase9m/batch1/9m1/result_9m1.md`, `evidence/phase9m/batch1/9f0/result_9f0.md` |
| MK (9M-3) | + hash K0 | 15,917.5 | tidak diukur | 8,447 / 10,279 / 15,635 | (hanya 40 ns) | `evidence/phase9m/batch1/9m3/result_9m3.md` |
| K1 (S1) | + sampler K0 | 14,061.0 | 73.070 | 8,795 / 10,627 / 15,983 | 120.4 / 145.4 / 218.7 | `evidence/phase9m/batch1/9f1/result_9f1.md` |
| K1b (S1b) | + hash latar belakang | 14,335.0 | 73.855 | 8,404 / 10,236 / 15,597 | 113.8 / 138.6 / 211.2 | `evidence/phase9m/batch1/9f1b/result_9f1b.md` |
| K2 (S2) | + P = 6 | 14,213.0 | 74.125 | 8,416 / 10,250 / 15,619 | 113.5 / 138.3 / 210.7 | `evidence/phase9m/batch2/9s2/result_9s2.md` |
| K3 (S2b) | + alamat teregister | 14,115.5 | 77.555 | 8,416 / 10,250 / 15,619 | 108.5 / 132.2 / 201.4 | `evidence/phase9m/batch2/9s2b/result_9s2b.md` |
| K4 (butir 4) | + pemuatan di belakang mesin | 14,222.0 | 76.665 | 8,416 / 9,611 / 12,989 | 109.8 / 125.4 / 169.4 | `evidence/phase9m/batch2/9i4/result_9i4.md` |
Timing pada 15.000 ns terpenuhi di 6 dari 6 seed untuk K1, K1b, K2, K3, dan K4 (sembilan dari sembilan untuk K3) dan pada 40.000 ns di 6 dari 6 seed untuk setiap konfigurasi. K4 lawan MW pada 15 ns (indikatif, MW punya dua seed): latensi KeyGen -3.3 %, Encaps -9.5 %, Decaps -19.9 %. K4 lawan inti Fase 9: ALM -3,398.5 (-19.3 %), siklus -7.5 % / -10.5 % / -22.1 % (inti Fase 9 tidak diukur pada 15 ns, sehingga latensinya pada 15 ns tidak dinyatakan).
Fmax seed K4 pada 15 ns: 80.99, 74.97, 78.27, 75.67, 77.66, 69.43 MHz (sebaran 11.56 MHz); noise seed adalah 3 MHz untuk konfigurasi awal dan lebih besar untuk K3 dan K4. S0 menemukan batas inti 9M-1 di antara 13 dan 14 ns (14 ns terpenuhi di kedua seed, 75.3-77.3 MHz; 13 ns terpenuhi di 1 dari 2 seed), itulah sebabnya 15 ns adalah batas pelaporan.

## 4. Standar dan sumber yang dipatok
FIPS 203 ML-KEM-768, vektor sampel ACVP sebagaimana dipatok di `reference/kat_sources.md` (set sampel NIST; keyGen 25, encapsulation 25, decapsulation 10; grup pemeriksaan kunci dijalankan di HPS menurut ADR 0031). Model acuan: `tb/golden/` (independen dari RTL); hashlib untuk SHA-3 dan SHAKE. Tidak ada konstanta FIPS 203 yang berubah (check_params).

## 5. Cakupan dan batas
- Hanya simulasi, formal dengan stub protokol, dan static timing dengan pin virtual: tidak ada hasil papan, tidak ada hasil HPS, tidak ada klaim kecepatan terhadap perangkat lunak. Latensi adalah siklus dibagi Fmax slow corner terendah dari satu jalankan static timing (perhitungan tim).
- Noise seed adalah 3 MHz (awal) sampai 11 MHz (sebaran K4); kenaikan di bawah itu tidak disebut kenaikan. S2 (+0.27 MHz) dan penurunan K4 (-0.89 MHz terhadap K3) berada di dalamnya. S2b (+3.43 MHz) adalah kenaikan median yang tidak diterima oleh aturannya sendiri sebagaimana tertulis.
- ACVP mencakup vektor keyGen, encapsulation, dan decapsulation (25, 25, 10); interlock butir 4 diuji oleh ACVP dan oleh satu pola stall (port host yang diperlambat), bukan oleh semuanya.
- Waktu-konstan hanya berarti invariansi jumlah siklus (Encaps dan Decaps identik pada masukan yang diuji; KeyGen bervariasi dengan rejection sampling publik matriks A, 8,344-8,397 siklus atas seed ACVP). Ini bukan ketahanan side-channel.
- Model formal memakai stub protokol untuk mesin, sampler, dan sponge; ia membuktikan properti kontrol dan rentang, bukan nilai.
- Penyimpanan masih serial dengan mesin dan KeyGen tidak berubah oleh butir 4; sampler kedua (butir 5) tidak dibangun (diperkirakan 1 sampai 4 % latensi dengan sekitar +3,500 ALM, ESTIMATE).

## 6. Penyimpangan, kegagalan, dan masalah terbuka
1. Timeout formal (M-11). P1 `mlkem_core4` (tidak ada STP atau SDL selagi mesin sibuk; kedalaman terbatas 160) dan kontrol negatif NC-E1-4 habis waktu pada 1,800 s; percobaan ulang 4 jam dihentikan setelah sekitar 2 jam 40 menit atas keputusan tim; NC-B7 `mlkem_core3` (Batch 1) juga habis waktu (percobaan ulang 3 jam dimatikan oleh restart). P1 bertumpu pada simulasi dan pada NC-JOIN4, yang gagal sebagaimana disyaratkan. P2 (`pend_q` sama dengan 0 saat idle) dibuang karena gagal pada induksi tanpa invarian posisi program; tidak terbukti. `evidence/phase9m/batch2/9i4/formal.md`, `evidence/phase9m/batch1/9f1b/formal.md`.
2. S2b tidak diadopsi oleh aturannya sebagaimana tertulis (kenaikan median, +3.430 MHz, lebih kecil daripada sebaran seed K3, 6.35 MHz; seed 4 pada 73.02 MHz berada di bawah seed tertinggi K2). Tiga seed tambahan dijalankan atas permintaan setelah hasil dan dilaporkan di sampingnya (median sembilan seed 77.320 MHz). K4 diukur di atas basis ini: jika K3 ditolak, K4 harus diukur ulang di atas K2.
3. S2 netral: +0.27 MHz, di dalam sebaran; aturan mengadopsinya, evidence mengatakan netral. Beberapa estimasi rencana meleset dan dicatat di hasil (siklus S2 +12 / +14 / +22 terhadap +6 / +7 / +11; Fmax S2 74.1 terhadap 76-80 MHz).
4. Proses butir 4: rencananya ditulis setelah RTL dan simulasi inti pertama (rencana menyatakannya); aturan ditulis sebelum kompilasi apa pun dan sebelum kontrol. Dua kontrol semula dibangun salah (`ncthrld`, `ncgrant`), diperbaiki dan dijalankan ulang (`evidence/phase9m/batch2/9i4/sim.md`).
5. Seed K4 terlemah (69.43 MHz) dibatasi oleh jalur S2b (`cnt_q` melalui enable tulis host dan `start_go` ke alamat teregister), bukan oleh butir 4 (`evidence/phase9m/batch2/9i4/critical_paths_K4-15.md`).
6. Insiden perkakas: editor crash mematikan dua kompilasi Quartus paralel dan satu jalankan formal (tidak ada keluarannya yang dipakai; kompilasi dijalankan satu per satu dengan setidaknya 2 GB RAM bebas); sebuah pertanyaan status salah dibaca sekali dan antrean kompilasi dihentikan dan dipulihkan (`evidence/phase9m/batch2/9s2b/test_plan_9s2b.md` A1).
7. Keluaran Quartus diarsipkan di luar repositori dan tidak pernah di-commit.

## 7. Keputusan yang diperlukan
PENDING #34 (ADR 0035, codec dua byte), #35 (ADR 0037, hash K0), #36 (ADR 0038, K1), #37 (ADR 0040, K1b), #38 (ADR 0041, K2), #39 (ADR 0042, K3: aturan mengatakan tidak, median mengatakan +3.4 MHz), #40 (ADR 0043, K4: aturan mengatakan ya, di atas basis K3). Rantainya bersarang: K4 membutuhkan K3, K3 membutuhkan K2, K2 membutuhkan K1b; tim dapat berhenti di mata rantai mana pun, tetapi pengukuran berikutnya lalu harus diulang di atas basis baru. Lihat `docs/decisions/PENDING.md`.

## 8. Klaim yang dibuat pada fase ini
Setiap angka di atas berlabel MEASURED (static timing kernel-only atau simulasi) atau perhitungan tim (latensi). Tidak ada klaim validasi perangkat keras, kecepatan terhadap perangkat lunak, daya, atau ketahanan side-channel. Satu-satunya pernyataan keamanan adalah invariansi jumlah siklus Encaps dan Decaps pada masukan yang diuji. Tidak ada yang di sini merupakan teks proposal; klaim untuk juri melalui `/proposal-claims`.

## 9. Mereproduksi
```bash
. scripts/env.sh
python3 .claude/skills/mlkem-guard/scripts/check_params.py
# K4 core target on both simulators (about 2 minutes on Verilator, about 1 hour on Icarus):
CORE_TOP=mlkem_core4 CORE_SMP0=1 CORE_K0=1 CORE_W2=1 CORE_P6=1 CORE_AR=1 python3 tb/mlkem/run_core_tests.py verilator core
CORE_TOP=mlkem_core4 CORE_SMP0=1 CORE_K0=1 CORE_W2=1 CORE_P6=1 CORE_AR=1 python3 tb/mlkem/run_core_tests.py icarus core nclen
# controls of item 4 (Verilator):
CORE_TOP=mlkem_core4 CORE_SMP0=1 CORE_K0=1 CORE_W2=1 CORE_P6=1 CORE_AR=1 python3 tb/mlkem/run_core_tests.py verilator nclen ncoff ncrom ncprio ncwr ncjob ncthr ncilk ncthrld ncgrant ncjoin
python3 tb/s10/run_s10_tests.py verilator s10p6a ncar s10p6 s10      # NTT core at P = 6 with the registered address, and the defaults
python3 formal/run/run_formal_phase9i4.py proofs                         # item 4 formal (P1 and NC-E1-4 time out)
cd quartus/phase09i4_core && quartus_sh --flow compile phase09i4_core -c K4-15-s1   # one Quartus compile (about 12 min)
python3 scripts/quartus/select_9i4.py                                       # worksheet of K4 against K3
python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase9m.md
```

## 10. Persetujuan
- [x] Penyetuju manusia (Faza Dzil, 2026-10-05; dicentang oleh asisten atas instruksi Jo, Tim J5):
      Fase berikutnya dimulai hanya setelah anggota tim mencentang kotak ini. Claude tidak pernah mencentangnya.
