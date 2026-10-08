<!-- claim-lint: skip-file (result artifact: internal status page, not proposal text) -->
# Hasil - Fase 7: Keccak-f[1600] + baseline SHA3/SHAKE (konfigurasi K0)

- Status: DONE
- Catatan status: kriteria PASS Fase 7 terpenuhi (keempat mode bit-exact, latensi permutasi tetap ditunjukkan, baris K0 terisi). Kotak Persetujuan (Bagian 10) kosong. Ini bukan tier T1 ADR 0019: T1 juga membutuhkan sampler (Fase 8b), yang belum dibangun.
- Tanggal (UTC): 2026-10-03
- Git commit (HEAD saat diverifikasi): c69d62f (RTL Fase 7, tes, formal, revisi Quartus, dan evidence), ditambah commit dokumentasi file ini
- Hasil: Keccak-f[1600] iteratif (satu ronde per siklus, `busy_o` tinggi tepat 24 siklus untuk setiap state) dan sponge untuk SHA3-256, SHA3-512, SHAKE128, dan SHAKE256 dengan absorb dan squeeze multi-blok, sama dengan hashlib untuk setiap panjang dan ukuran keluaran yang diuji di Verilator dan Icarus, dengan jumlah siklus yang tidak bergantung data. Quartus (kernel-only, pin virtual): 3,572 ALM, 1,653 register, 0 M10K, 0 DSP, timing terpenuhi pada 40 ns (setup +22.452 ns, Fmax 56.99 MHz, seed 1) dan pada 20 ns (setup +6.893 ns, Fmax 76.30 MHz, seed 1).
- Lingkungan: Ubuntu 24.04.4 LTS, OSS CAD Suite 2026-09-23 (Verilator 5.053, Icarus 14.0 devel), cocotb 2.1.0, Quartus Prime Lite 25.1std.0 Build 1129.
- Constraint: 40.000 ns (`quartus/phase07_keccak/K.sdc`, identik dengan `quartus/phase06_sched/P.sdc`); kompilasi informasi pada 20.000 ns (`K-20.sdc`).

## 1. Kriteria selesai (Common RTL Gate, docs/ROADMAP.md)
| # | Kriteria | Evidence | Status |
|---|---|---|---|
| CRG-1 | Lint bersih | `evidence/phase07/verify.md` (Verilator -Wall: 0 peringatan pada keccak_f1600 dan keccak_sponge) | PASS |
| CRG-2 | Elaborasi bersih (slang) | `evidence/phase07/verify.md` (slang: 0 error, 0 peringatan) | PASS |
| CRG-3 | Bit-exact terhadap model acuan, kedua simulator | `evidence/phase07/verify.md` (model acuan lawan hashlib 16 pytest; permutasi: setiap ronde dari 1,802 state; sponge: semua mode, panjang batas dan panjang ML-KEM, back-pressure, stop, reset; Verilator dan Icarus) | PASS |
| CRG-4 | Kasus sudut sebelum tes | `evidence/phase07/test_plan.md` (ditulis sebelum model acuan dan RTL; Amandemen A1 bertanggal dan dijelaskan, tidak ada ambang yang diubah) | PASS |
| CRG-5 | Regresi: fase sebelumnya masih lulus | Tidak ada file RTL, tes, bukti, skrip, atau Quartus yang sudah ada diubah (`cmd: git diff --name-status b1b5789 HEAD -- rtl tb formal scripts quartus` hanya mencantumkan penambahan). Regresi penuh fase sebelumnya karenanya tidak diperlukan (Amandemen A1 Fase 5M) | PASS |
| CRG-6 | Parameter terkunci | `evidence/phase07/verify.md` (`cmd: python3 .claude/skills/mlkem-guard/scripts/check_params.py`: semua parameter terkunci sesuai; paket konstanta dibangkitkan ulang dari model acuan, 0 perbedaan); tidak ada yang berubah dari FIPS 203 atau FIPS 202 | PASS |
| CRG-7 | Evidence jumlah siklus konstan | `evidence/phase07/keccak_cycles.md` (306 titik, tiga pesan masing-masing, satu jumlah per titik; setiap titik sama dengan rumus FSM), `evidence/phase07/cycles_k0.json` | PASS |
| CRG-8 | Properti formal | `evidence/phase07/formal.md` (K1-K5 PASS dengan induksi; NC-K1 dan NC-K4 gagal sebagaimana disyaratkan) | PASS |
| CRG-9 | Evidence Quartus; tidak ada slack negatif atau kegagalan didokumentasikan | `evidence/phase07/quartus_K0.md` (terpenuhi pada 40 ns), `evidence/phase07/quartus_K0-20.md` (terpenuhi pada 20 ns, informasi) | PASS |
| CRG-10 | Artefak hasil + pemeriksa klaim | `cmd: python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase07.md` dan `cmd: python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal` | PASS |

## 1b. Kriteria PASS Fase 7 (docs/ROADMAP.md Fase 7)
| # | Kriteria | Evidence | Status |
|---|---|---|---|
| 1 | Semua mode bit-exact (SHA3-256 136 B, SHA3-512 72 B, SHAKE128 168 B, SHAKE256 136 B; panjang 0, rate -1, rate, rate +1, kelipatan, acak; squeeze multi-blok) | `evidence/phase07/verify.md` | PASS |
| 2 | Latensi permutasi tetap ditunjukkan (24 siklus, tidak bergantung data); total siklus hanya bergantung pada panjang publik | `evidence/phase07/verify.md` (busy_o = 24 untuk state semua-nol, semua-satu, 1,600 satu-bit, dan 200 acak), `evidence/phase07/formal.md` (K1), `evidence/phase07/keccak_cycles.md` | PASS |
| 3 | Baris K0 terisi (ALM, register, Fmax, slack) | `docs/ROADMAP.md` (baris K0 dan K0-20), `evidence/phase07/quartus_K0.md` | PASS |

## 2. Yang dihasilkan
| Path | Fungsi |
|---|---|
| `tb/golden/keccak.py`, `tb/golden/tests/test_keccak.py` | Keccak-f[1600] acuan (konstanta ronde dan offset rho dihitung dari FIPS 202 Algoritma 2, 5, 6), sponge, empat fungsi; terbukti sama dengan hashlib |
| `scripts/build/gen_keccak_consts.py`, `rtl/keccak/keccak_pkg.sv` | Konstanta ronde dan offset rho yang dibangkitkan |
| `rtl/keccak/keccak_round.sv`, `keccak_f1600.sv`, `keccak_sponge.sv` | Satu ronde kombinasional; inti permutasi (24 siklus busy); pengendali sponge dan top Quartus |
| `tb/keccak/` (`test_keccak_f1600.py`, `test_keccak_sponge.py`, `run_keccak_tests.py`) | Tes cocotb, kontrol negatif (NC-RC, NC-R, NC-PAD), runner untuk kedua simulator |
| `formal/phase07-keccak/`, `formal/run/run_formal_phase7.py` | Top formal (K1-K5), file sby, runner dengan NC-K1 dan NC-K4 |
| `quartus/phase07_keccak/` | Revisi K0 (40 ns) dan K0-20 (20 ns), constraint, skrip jalankan |
| `scripts/test/phase7_verify.sh`, `scripts/test/phase7_op_cycles.py` | Skrip verifikasi; siklus Keccak per operasi ML-KEM (perhitungan tim) |
| `evidence/phase07/` | Rencana tes, verify, formal, tabel siklus, ekstrak Quartus |
| `scripts/build/build_phase7_report.py`, `docs/reports/CHIPATON_Phase7_Report.pdf` | Laporan (Bahasa Indonesia, 4 halaman); angka diurai dari file evidence, rumus siklus diperiksa ulang pada semua 306 titik |

## 3. Angka (MEASURED: laporan Quartus dan simulasi; ESTIMATE dan perhitungan tim ditandai)
| Besaran | K0 pada 40.000 ns | K0-20 pada 20.000 ns | Estimasi yang ditulis sebelum pengukuran (ESTIMATE) |
|---|---|---|---|
| ALM (seed 1) | 3,572 / 41,910 (9 %) | 3,573 / 41,910 (9 %) | 1,500-3,500: terukur 2 % di atas batas atas rentang |
| Register | 1,653 | 1,653 | 1,700-2,000: terukur di bawah rentang (1,600 bit state + 53 kontrol; estimasi menghitung buffer tambahan yang tidak ada pada desain) |
| M10K / DSP | 0 / 0 | 0 / 0 | sekitar 0 / 0 |
| Timing | terpenuhi; worst setup +22.452 ns (Slow 100 C), worst hold +0.163 ns (Fast -40 C) | terpenuhi; worst setup +6.893 ns, worst hold +0.164 ns | tidak diperkirakan membatasi sistem (INFERENSI) |
| Fmax slow corner terendah (MHz) | 56.99 (seed 1) | 76.30 (seed 1) | - |
| Siklus per permutasi | 24 busy (`keccak_f1600`), 26 sebagaimana terlihat oleh sponge | sama | 24 |
| H(ek), 1184 B, 4 word keluaran | 389 siklus | - | sekitar 370 (digantikan) |

Throughput pada panjang besar (perhitungan tim dari rumus terukur; absorb atau squeeze blok penuh, tanpa tumpang tindih): SHA3-256 dan SHAKE256 17 word + 26 siklus = 43 siklus per 136 B (3.16 B per siklus); SHA3-512 35 siklus per 72 B (2.06); squeeze SHAKE128 47 siklus per 168 B (3.57).
Waktu per permutasi pada Fmax seed tunggal: 26 / 56.99 MHz = 0.456 us (K0), 26 / 76.30 MHz = 0.341 us (K0-20); ini nilai satu seed, bukan median, dan angka 20 ns tidak dapat dibandingkan dengan angka 40 ns.
Siklus Keccak satu operasi ML-KEM-768 dengan K0, setiap panggilan dijalankan sendiri dan tidak ada yang tumpang tindih (perhitungan tim, `evidence/phase07/keccak_cycles.md`): KeyGen sekitar 2,026, Encaps sekitar 2,078, Decaps sekitar 2,070 (median atas 200 rho acak; rentang 2,013-2,088, 2,065-2,140, 2,057-2,132), 43-44 permutasi.
Itu sekitar dua kali angka sebelum pengukuran yaitu 1,060 (44 x 24), yang tidak menghitung siklus kontrol dan transfer word. Sebagai skala: aritmetika Fase 6 dengan S10 memakai 5,475 / 6,789 / 3,109 siklus (MEASURED, simulasi); blok-blok ini belum dihubungkan.
Sumber: `evidence/phase07/quartus_K0.md`, `quartus_K0-20.md`, `keccak_cycles.md`, `verify.md`.

## 4. Standar dan sumber yang dipatok
FIPS 202 (Keccak-p[1600, 24], Algoritma 2, 5, 6 untuk offset rho dan konstanta ronde, pad10*1, SHA3-256, SHA3-512, SHAKE128, SHAKE256, byte domain 0x06 dan 0x1F) sebagaimana dipakai FIPS 203 (H, J, G, PRF, XOF); keluaran acuan dari hashlib Python. Tidak ada parameter atau aritmetika FIPS 203 yang berubah (C1); `check_params.py` lulus.

## 5. Cakupan dan batas
- Hanya simulasi, formal, dan static timing. Tidak ada papan; Fmax dan slack bersifat kernel-only dengan pin virtual dan satu seed (ADR 0019: satu kompilasi untuk blok tanpa aturan adopsi). "Timing terpenuhi pada 20 ns" adalah static timing alur ini, bukan sistem pada 50 MHz.
- Formal mencakup kontrol (K1-K5), bukan nilai digest; digest dicakup oleh simulasi terhadap hashlib.
- Hanya satu ronde per siklus (dua ronde per siklus, unrolling, sampler streaming, dan koneksi ke unit aritmetika tidak diizinkan pada fase ini dan tidak dibangun).
- Waktu-konstan di sini berarti jumlah siklus hanya bergantung pada panjang publik dan jumlah word keluaran; ini bukan pernyataan side-channel.
- Antarmuka K0 memindahkan satu word 64-bit per siklus dan dimulai ulang untuk setiap panggilan; 2,000 siklus Keccak per operasi adalah angka untuk antarmuka itu, bukan batas untuk desain lain.

## 6. Penyimpangan, kegagalan, dan masalah terbuka
- Amandemen A1 rencana tes mendaftarkannya: nama paket konstanta, 26 bukan 24 siklus per permutasi pada ESTIMATE siklus, penghapusan state tambahan, NC-K4 sebagai BMC kedalaman 40.
- Jalankan verifikasi pertama: testbench sponge punya tiga kesalahan (pemeriksaan akhir digest menurunkan `out_ready_i` sebelum tepi clock, tes stop meminta satu word keluaran dari SHA3, log siklus tertimpa oleh build berikutnya); diperbaiki di testbench, RTL tidak berubah karenanya. Satu suntingan RTL: ternary enum ditulis ulang sebagai if/else karena Icarus menolaknya.
- Tes acuan semula meng-assert 24 konstanta ronde berbeda; tabel sebenarnya mengulang dua nilai (22 berbeda); assertion dikoreksi, hash sudah sama dengan hashlib.
- ESTIMATE lawan pengukuran: ALM 2 % di atas rentang yang tertulis, register di bawahnya (Bagian 3).
- Critical Warning 15725 (clock pin virtual) di kedua kompilasi, seperti fase sebelumnya; Warning 10036 (sinyal sink `unused_ok`, disengaja, perangkat yang sama dengan `unused_widx` pada Fase 6); tidak ada critical warning lain; tidak ada yang di-waive.

## 7. Keputusan yang diperlukan
- Kotak Persetujuan Fase 7 (Bagian 10).
- PENDING #26 (protokol checkpoint sampai 2026-10-08) masih terbuka; fase ini berhenti di akhirnya mengikuti bawaan yang disarankan (satu STOP per blok).
- Langkah berikutnya menurut ADR 0019: sampler (SampleNTT dan CBD streaming dari keluaran Keccak, tier T1) - urutan dan cakupan adalah pilihan tim; PENDING #25 (pemeriksaan masukan FIPS 203 di perangkat keras atau di HPS) sebelum pekerjaan pengendali.

## 8. Klaim yang dibuat pada fase ini
Tidak ada yang ditulis untuk juri/teks proposal. Baris ROADMAP diisi dari evidence di atas.

## 9. Mereproduksi
```bash
. scripts/env.sh
scripts/test/phase7_verify.sh; python3 formal/run/run_formal_phase7.py
python3 scripts/build/gen_keccak_consts.py --check
cd quartus/phase07_keccak && ./run_k0.sh; cd ../..
python3 scripts/test/phase7_op_cycles.py 200
python3 scripts/build/build_phase7_report.py
python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase07.md
python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal
```

## 9b. Catatan amandemen 1 (2026-10-03, setelah persetujuan; tidak ada yang di atas diedit)
Seed 2-6 K0 dikompilasi sebagai baseline aturan Fase 8a (`evidence/phase07/quartus_K0-s2.md` .. `quartus_K0-s6.md`). Atas seed 1-6: ALM 3,558-3,572, register 1,653, Fmax slow corner terendah median 67.675 MHz (56.99-70.39), timing terpenuhi pada 40 ns di setiap seed. Angka 56.99 MHz pada Bagian 3 adalah seed 1 dan yang terendah dari keenamnya; jangan dibaca sebagai nilai tipikal.

## 10. Persetujuan
- [x] Penyetuju manusia (nama, tanggal): Jose (Tim J5), 2026-10-03
      Fase berikutnya dimulai hanya setelah anggota tim mencentang kotak ini. Claude tidak pernah mencentangnya.
