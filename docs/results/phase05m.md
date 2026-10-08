<!-- claim-lint: skip-file (result artifact: internal status page, not proposal text) -->
# Hasil - Fase 5M: Memori dan jadwal (S6 INTT tanpa lintasan penskalaan, S7 pembacaan memori terbelah, S8 register jalur tulis, S9 studi M10K)

- Status: DONE
- Catatan status: selesai secara teknis menurut ADR 0017 / 0019 (S6, S7, S8 benar dan terukur; S9 adalah studi yang hanya berupa dokumentasi). Catatan yang menunggu tim: ADR 0021 (S7, Proposed), ADR 0022 (S9, Proposed), ADR 0023 (S8, Proposed). Kotak Persetujuan (Bagian 10) kosong; kotak Persetujuan Fase 5 juga masih kosong.
- Tanggal (UTC): 2026-10-02 sampai 2026-10-03
- Git commit (HEAD saat diverifikasi): 300aaf3 (RTL, tes, dan bukti S6-S8; regresi penuh dijalankan pada commit ini), ditambah commit dokumentasi yang mengikutinya
- Hasil: S6 (M6) menjadi basis atas keputusan tim meskipun aturan yang ditetapkan sebelumnya tidak mengadopsinya (ADR 0020); S7 diadopsi oleh aturan (Fmax median 38.720 MHz, NTT = INTT = 120 siklus); S8 tidak diadopsi oleh aturan (Fmax median 37.990 MHz, 122 siklus); S9 menunjukkan bahwa peta 16-bank 1R1W bebas-konflik ada, tanpa angka perangkat keras.
- Lingkungan: Ubuntu 24.04.4 LTS, OSS CAD Suite 2026-09-23 (Verilator 5.053), cocotb 2.1.0, Quartus Prime Lite 25.1std.0 Build 1129.
- Constraint: `create_clock -period 40.000` (`quartus/phase05m_memsched/M.sdc`) untuk setiap revisi; satu kompilasi informasi S8 pada 20.000 ns (`M-20.sdc`).

## 1. Kriteria selesai (Common RTL Gate, docs/ROADMAP.md)
| # | Kriteria | Evidence | Status |
|---|---|---|---|
| CRG-1 | Lint bersih | `evidence/phase05m/s6/verify.md`, `evidence/phase05m/s7/verify.md`, `evidence/phase05m/s8/verify.md` (Verilator -Wall dan slang: 0 peringatan, 0 error pada setiap wrapper) | PASS |
| CRG-2 | Elaborasi bersih (slang) | `evidence/phase05m/s6/verify.md`, `evidence/phase05m/s7/verify.md`, `evidence/phase05m/s8/verify.md` (slang: 0 error, 0 peringatan) | PASS |
| CRG-3 | Bit-exact terhadap model acuan, kedua simulator | `evidence/phase05m/s6/verify.md`, `evidence/phase05m/s7/verify.md`, `evidence/phase05m/s8/verify.md` (tes inti termasuk 512 vektor unit INTT; half_mod menyeluruh; tes unit dan diferensial memori) | PASS |
| CRG-4 | Kasus sudut sebelum tes | `evidence/phase05m/test_plan.md`, `evidence/phase05m/test_plan_s7.md`, `evidence/phase05m/test_plan_s8.md`, `evidence/phase05m/test_plan_s9.md` (masing-masing di-commit sebelum pengukurannya; amandemen bertanggal) | PASS |
| CRG-5 | Regresi: Fase 0-5 masih lulus | `evidence/phase05m/s8/regression.md` (satu jalankan pada pohon akhir, Amandemen A1: regresi Fase 0-5, verifikasi Fase 5, verifikasi S6 dan S7: OVERALL PASS; 95 file ditambahkan, 2 dokumen diubah, tidak ada file RTL, tes, atau bukti Fase 1-5 yang diubah) | PASS |
| CRG-6 | Parameter terkunci | `evidence/phase05m/s8/regression.md` (check_params lulus); pembagian dua INTT terbukti sama dengan FIPS 203 Algoritma 10 (ADR 0020, `tb/golden/tests/test_intt_halving.py`) | PASS |
| CRG-7 | Evidence jumlah siklus konstan | `evidence/phase05m/s6/verification_status.json` (119 / 119), `evidence/phase05m/s7/verification_status.json` (120 / 120), `evidence/phase05m/s8/verification_status.json` (122 / 122), identik di kedua simulator | PASS |
| CRG-8 | Properti formal | `evidence/phase05m/s6/formal.md`, `evidence/phase05m/s7/formal.md`, `evidence/phase05m/s8/formal.md` (properti kontrol dan kapasitas bank H, O, R, A, B, C; kontrol negatif gagal). Kebenaran data bertumpu pada simulasi, bukan formal | PASS |
| CRG-9 | Evidence Quartus; tidak ada slack negatif atau kegagalan didokumentasikan | `evidence/phase05m/s6/quartus_M6.md`, `evidence/phase05m/s7/quartus_S7.md`, `evidence/phase05m/s8/quartus_S8.md` (masing-masing dengan seed 2-6 sebagai akhiran -s2 sampai -s6): timing terpenuhi pada 40.000 ns di setiap seed. Kompilasi informasi 20.000 ns TIDAK memenuhi timing dan didokumentasikan demikian: `evidence/phase05m/s8/quartus_S8-20.md` | PASS |
| CRG-10 | Artefak hasil + pemeriksa klaim | `cmd: python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase05m.md` dan `cmd: python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal` | PASS |

## 1b. Kriteria PASS Fase 5M (ADR 0017, ADR 0019)
| # | Kriteria | Evidence | Status |
|---|---|---|---|
| 1 | Setiap langkah punya rencana tes dan aturan yang ditulis sebelum pengukuran | empat rencana tes di atas (rencana S7 dan S8 di-commit sebelum RTL-nya dijalankan / dikompilasi; RTL S8 sudah ditulis dan di-lint, diungkapkan di headernya) | PASS |
| 2 | Setiap langkah diukur dengan seed 1-6 dan aturan diterapkan tanpa perubahan | `evidence/phase05m/s6/selection_worksheet.md`, `evidence/phase05m/s7/selection_worksheet.md`, `evidence/phase05m/s8/selection_worksheet.md` | PASS |
| 3 | Setiap hasil tercatat dalam ADR | `docs/decisions/adr/ADR-0020-phase-5m-s6-intt-without-the-scaling-pass-halving-in-every-l.md` (Accepted), `docs/decisions/adr/ADR-0021-phase-5m-s7-split-memory-read-path-rd-split-p-7-rule-result-.md`, `docs/decisions/adr/ADR-0023-phase-5m-s8-write-path-register-and-one-bubble-per-direction.md`, `docs/decisions/adr/ADR-0022-phase-5m-s9-m10k-study-result-options-for-the-memory-team-ch.md` (Proposed) | PASS |
| 4 | Studi S9 dengan kebutuhan port, opsi, dan kondisi evidence, tanpa RTL | `evidence/phase05m/s9/study_m10k.md`, `evidence/phase05m/s9/port_analysis.txt` | PASS |
| 5 | Baris ablasi ROADMAP M6, S7, S8, S8-20 | `docs/ROADMAP.md` | PASS |

## 2. Yang dihasilkan
| Path | Fungsi |
|---|---|
| `rtl/arith/half_mod.sv`, `butterfly_m6.sv`, `twiddle_rom_half.sv`, `rtl/ntt/ntt_core_m6.sv`, `ntt_core_m6_p6.sv` | S6: pembagian dua INTT di setiap layer, tanpa lintasan penskalaan; NTT = INTT = 119 siklus |
| `rtl/mem/poly_mem_multiport_split.sv`, `rtl/ntt/ntt_core_s7.sv`, `ntt_core_s7_p7.sv` | S7: satu tahap register di dalam pembacaan memori (RD_SPLIT), P = 7, 120 siklus |
| `rtl/ntt/ntt_core_s8.sv`, `ntt_core_s8_p8.sv` | S8: register jalur tulis (WR_REG), P = 8, satu gelembung per arah, 122 siklus |
| `tb/golden/intt_halving.py`, `tb/phase5m/`, `formal/phase05m-memsched/`, `formal/run/run_formal_phase5m*.py` | Model acuan INTT berbagi-dua, tes per langkah, top formal dan runner dengan kontrol negatif |
| `quartus/phase05m_memsched/` | Proyek, revisi `M6[-s2..s6]`, `S7[-s2..s6]`, `S8[-s2..s6]`, `S8-20`, `M.sdc`, `M-20.sdc`, skrip sapuan |
| `scripts/phase5m_verify*.sh`, `phase5m_select_s6.py`, `phase5m_select_s7.py`, `phase5m_select_s8.py`, `phase5m_final_regression.sh`, `phase5m_s9_port_analysis.py`, `build_phase5m_report.py` | Verifikasi, aturan (hanya membaca file evidence), satu regresi, analisis S9, pembangun laporan |
| `evidence/phase05m/` | Rencana tes, evidence per langkah (`s6/`, `s7/`, `s8/`, `s9/`), regresi |
| `docs/decisions/0017` sampai `0023` | Cakupan Fase 5M, jalur minimal, basis M6, catatan S7, S9, S8 |
| `docs/reports/CHIPATON_Phase5M_Report.pdf` | Laporan Fase 5M (Bahasa Indonesia, tata letak sama dengan Fase 0-5) |

Tidak ada file beku Fase 1-5 (RTL, tes, formal, evidence) yang diedit. Catatan yang sudah ada dan diedit: `docs/decisions/0017-...` (catatan amandemen), `docs/decisions/0019-...` dan `docs/decisions/0020-...` (pernyataan bahwa S7-S9 belum selesai diedit di tempat dengan jejak dalam tanda kurung, 2026-10-03, atas permintaan tim), `docs/decisions/PENDING.md`, `docs/ROADMAP.md`, `CLAUDE.md`, `HANDOFF.md`, `README.md` (baris status).

## 3. Angka (MEASURED: laporan Quartus; siklus dari simulasi; median dan t INFERENSI)
| Besaran | C4b-B (Fase 5) | M6 (S6) | S7 | S8 |
|---|---|---|---|---|
| ALM median (seed 1-6, min-maks) | 9,171.0 (9,166-9,208) | 9,421.5 (9,394-9,441) | 9,391.0 (9,361-9,405) | 9,443.5 (9,402-9,471) |
| Dalam 12,573 ALM (ADR 0009)? | ya | ya | ya | ya |
| Register (min-maks) | 4,083-4,115 | 4,030-4,080 | 4,296-4,324 | 4,130-4,144 |
| M10K / DSP | 29 / 18 | 29 / 16 | 31 / 16 | 33 / 16 |
| Timing terpenuhi pada 40.000 ns, setiap seed | ya | ya | ya | ya |
| Fmax slow corner terendah, median (min-maks) MHz | 34.515 (33.46-34.84) | 34.430 (32.35-35.04) | 38.720 (37.89-40.29) | 37.990 (36.76-40.22) |
| Siklus NTT / INTT | 119 / 375 | 119 / 119 | 120 / 120 | 122 / 122 |
| t_NTT / t_INTT pada Fmax median (us, perhitungan tim) | 3.448 / 10.865 | 3.456 / 3.456 | 3.099 / 3.099 | 3.211 / 3.211 |
| Hasil aturan | (basis Fase 5) | tidak diadopsi oleh aturan; basis atas keputusan tim (ADR 0020) | diadopsi | tidak diadopsi |

Sumber: `evidence/phase05m/s8/selection_worksheet.md` (keempat baris, dihitung ulang dari file evidence), `s7/selection_worksheet.md`, `s6/selection_worksheet.md`.
Kompilasi informasi pada 20.000 ns (MEASURED, S8, seed 1, `s8/quartus_S8-20.md`): 9,443 ALM, setup -2.242 ns, Fmax 44.96 MHz, timing tidak terpenuhi. Kompilasi 20 ns sebelumnya: C3-P6 10,557 ALM, -2.059 ns; C4b-B 9,305 ALM, -2.557 ns (`evidence/phase05/closure/info_20ns.md`).
S9 (model jadwal sebenarnya, perhitungan tim): peta 8-bank membutuhkan 2 baca + 2 tulis per bank per siklus; peta 16-bank `bank = (a1^a2^a3^a4, a7, a6, a5)`, `offset = a[3:0]` membutuhkan 1 + 1 di sepanjang lini waktu (`s9/port_analysis.txt`).

## 3b. Per langkah
- S6 (M6): INTT 375 -> 119 siklus, DSP 18 -> 16, Fmax median -0.25 % dibanding C4b-B (dalam noise seed); aturan gagal hanya pada bagian NTT sebesar 0.008 us; tim tetap mengadopsi M6 (ADR 0020).
- S7: Fmax median +12.5 % (38.720 lawan 34.430 MHz), seed S7 terendah di atas seed M6 tertinggi, ALM tidak lebih tinggi; diadopsi oleh aturan (ADR 0021, Proposed).
- S8: siklus sesuai prediksi, Fmax median 0.73 MHz di bawah S7 (dalam sebaran seed), +2 siklus: tidak diadopsi oleh aturan (ADR 0023, Proposed). Penyebab tidak dianalisis (hipotesis ada di ADR).
- S9: peta 16-bank 1R1W bebas-konflik ada; daftar opsi dan kondisi evidence untuk memori M10K (ADR 0022, Proposed). Peta pertama yang diturunkan tangan salah dan dibantah oleh skrip (amandemen rencana A1).

## 4. Standar dan sumber yang dipatok
Tidak ada pembacaan FIPS 203 pada fase ini; tidak ada parameter, algoritma, nilai twiddle, atau hasil yang berubah (`check_params.py` lulus). INTT berbagi-dua sama dengan FIPS 203 Algoritma 10 menurut argumen dan pemeriksaan yang tercatat di ADR 0020 (3303 = 2^-7 mod q, 128 x 3303 = 127 x 3329 + 1). Fakta perangkat M10K Intel yang dipakai di S9 BELUM DIVERIFIKASI terhadap handbook (dinyatakan dalam studi).

## 5. Cakupan dan batas
- Hanya simulasi, formal, dan static timing. Tidak ada papan terpasang; tidak ada yang di sini merupakan validasi perangkat keras. Fmax bersifat kernel-only dengan pin virtual, bukan clock sistem.
- Formal mencakup kontrol dan kapasitas bank, bukan data. Satu kompilasi 20 ns (hanya S8). Sebaran seed: M6 2.69, S7 2.40, S8 3.46 MHz; S8 lawan S7 berada di dalamnya, tetapi aturan tidak memakai toleransi.
- Tidak ada analisis jalur setelah S7 atau S8: mengapa S7 naik dan S8 tidak adalah hipotesis. Jumlah register dan M10K berubah antar langkah tanpa penjelasan per entitas.
- S9 tidak menghasilkan angka Quartus. Tidak diukur: integrasi HPS, daya, anggaran tingkat sistem.

## 6. Penyimpangan, kegagalan, dan masalah terbuka
- Quartus menolak `$error` di `ntt_core_m6.sv` (syntax error): diganti dengan pemeriksaan localparam dengan sink; sapuan dimulai ulang dari db yang bersih.
- `phase5m_verify.sh` mula-mula mencetak "0 warnings" dengan modul top yang tidak ditemukan (lulus palsu, newline pada daftar sumber); diperbaiki dengan fungsi `lint_v` yang dipakai di Fase 5 dan seluruh verifikasi S6 dijalankan ulang.
- Dua panggilan `pkill`/`pgrep -f` cocok dengan shell asisten sendiri dan mematikannya; tidak ada data hilang. Laptop dimatikan saat regresi pertama: keluaran ditemukan kembali dengan menjalankan ulang; regresi kemudian dijalankan sekali pada S8 (Amandemen A1).
- Peta 16-bank S9 yang diturunkan tangan salah (menempatkan bit lane pada bit alamat yang salah); tertangkap oleh skrip, dicatat di amandemen rencana A1, peta yang dikoreksi diverifikasi.
- RTL S8 ditulis dan di-lint sebelum rencana tesnya di-commit (diungkapkan di header rencana); tidak ada simulasi atau kompilasi yang dijalankan, dan aturan hanya membandingkan dengan pengukuran S7 yang sudah tetap.
- Ambang 34.720 MHz pada rencana S7 adalah nilai pembulatan dari 34.7193; tidak berdampak. Baris `%Warning-WIDTHEXPAND` pada build Verilator cocotb berasal dari nilai parameter ARB_REG runner, bukan dari lint RTL.
- Kompilasi 20 ns: Critical Warning 15725 dan 332148 x2 seperti fase sebelumnya, ditriase, tidak ada yang di-waive.

## 7. Keputusan yang diperlukan
- ADR 0021 (S7, aturan lulus): terima S7 sebagai konfigurasi NTT/INTT untuk Fase 6 dan 7? ADR 0023 (S8, tidak diadopsi): pertahankan S7, atau basis lain? ADR 0022 (S9): opsi mana, dan kapan (saran: S7 sekarang, eksperimen M10K setelah blok yang kritis terhadap tenggat)?
- PENDING #25 (pemeriksaan masukan FIPS 203: perangkat keras atau HPS) dan #26 (satu STOP per blok atau per langkah). Kotak Persetujuan Fase 5 dan Fase 5M.

## 8. Klaim yang dibuat pada fase ini
Tidak ada yang ditulis untuk juri/teks proposal. Baris ROADMAP diisi dari evidence di atas.

## 9. Mereproduksi
```bash
. scripts/env.sh
scripts/test/phase5m_verify.sh; scripts/test/phase5m_verify_s7.sh; scripts/test/phase5m_verify_s8.sh
python3 formal/run/run_formal_phase5m.py; python3 formal/run/run_formal_phase5m_s7.py; python3 formal/run/run_formal_phase5m_s8.py
cd quartus/phase05m_memsched
# one revision at a time (parallel runs corrupt the shared .qpf)
./run_m6_sweep.sh; ./run_s7_sweep.sh; ./run_s8_sweep.sh
cd ../..
scripts/test/phase5m_final_regression.sh
python3 scripts/quartus/phase5m_select_s6.py; python3 scripts/quartus/phase5m_select_s7.py; python3 scripts/quartus/phase5m_select_s8.py
python3 scripts/test/phase5m_s9_port_analysis.py
python3 scripts/build/build_phase5m_report.py
python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase05m.md
python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal
```

## 10. Persetujuan
- [x] Penyetuju manusia (nama, tanggal): Jevan (Tim J5), 2026-10-03
      Fase berikutnya dimulai hanya setelah anggota tim mencentang kotak ini. Claude tidak pernah mencentangnya.
