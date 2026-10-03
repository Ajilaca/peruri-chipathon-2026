# peruri-chipathon-2026

Tim J5 (Institut Teknologi Bandung), CHIP 2026 Hackathon (PERURI Digital Summit),
kategori *IC Chip Design & FPGA Implementation*.

**Ide:** akselerator perangkat keras **ML-KEM-768** (NIST FIPS 203, kriptografi pasca-kuantum)
dengan pendekatan *hardware/software co-design* pada Terasic DE10-Nano (Intel Cyclone V SoC
5CSEBA6U23I7): Keccak-f[1600] dan NTT/INTT di FPGA, alur protokol dan baseline perangkat lunak
di HPS (ARM Cortex-A9). Target utama: eksekusi waktu-konstan yang dibuktikan, hasil bit-exact
terhadap vektor uji resmi, dan angka sumber daya/timing yang diukur dari Quartus.

## Status
Fase 0–5 dan Fase 5M selesai secara teknis (lihat `docs/results/` dan `HANDOFF.md`). Konfigurasi inti NTT/INTT saat ini: **C4 = C4b-B**
(8 lajur, pipeline 6 tahap, reduksi Barrett, ADR 0013 masih *Proposed*), dari basis **C3-P6** (ADR 0009). Hasil Fase 5
(`docs/results/result_phase5.md`, laporan `docs/report/CHIPATON_Phase5_Report.pdf`):
- Siklus tetap NTT 119 dan INTT 375 (MEASURED, simulasi, `docs/evidence/phase05-arith/regression_2026-10-01.md`); hasil bit-exact terhadap model golden di dua simulator.
- C4b-B memakai 9.166–9.208 ALM (seed 1–6) dibanding 10.484–10.516 pada C3-P6, dengan 18 DSP (C3-P6: 9) (MEASURED, `docs/evidence/phase05-arith/5b/selection_worksheet_2026-10-01.md`).
- Fmax tidak naik di luar sebaran seed; kompilasi informasi 20 ns **tidak memenuhi timing** (MEASURED, `docs/evidence/phase05-arith/closure/info_20ns_2026-10-01.md`: C3-P6 setup −2,059 ns,
  C4b-B −2,557 ns). Jalur kritis ada di pembacaan memori, bukan di aritmetika.
- 5c (lazy reduction) diukur dan tidak diadopsi; 5d (Karatsuba) tidak dicoba (ADR 0015, *Proposed*).

Fase 5M (memori dan jadwal, S6–S9; `docs/results/result_phase5m.md`, laporan `docs/report/CHIPATON_Phase5M_Report.pdf`, disetujui tim 2026-10-03):
- S6 (M6, INTT tanpa *scaling pass*): INTT 375 → 119 siklus, 16 DSP (MEASURED, `docs/evidence/phase05m-memsched/s6/selection_worksheet_2026-10-02.md`); dipakai sebagai basis atas keputusan tim (ADR 0020), meski aturan adopsi tidak terpenuhi.
- **S7 (pembelahan jalur baca memori):** median Fmax **38,720 MHz** (M6 34,430), NTT = INTT = 120 siklus, 9.361–9.405 ALM (MEASURED, `docs/evidence/phase05m-memsched/s7/selection_worksheet_2026-10-02.md`); aturan terpenuhi (ADR 0021, digantikan S10 oleh ADR 0025).
- S8 (register jalur tulis, 122 siklus): median Fmax 37,990 MHz (MEASURED, `docs/evidence/phase05m-memsched/s8/selection_worksheet_2026-10-03.md`), **tidak diadopsi** oleh aturan (ADR 0023, digantikan S10 oleh ADR 0025); kompilasi 20 ns tidak memenuhi timing (setup −2,242 ns).
- S9 (studi M10K, tanpa RTL): peta 16 bank 1R1W bebas konflik ada pada jadwal nyata (perhitungan tim, `docs/evidence/phase05m-memsched/s9/port_analysis_2026-10-03.txt`); opsi ini kemudian dibangun sebagai S10 (ADR 0022, digantikan oleh ADR 0025).

Fase 6 (penjadwalan tingkat operasi + S10; `docs/results/result_phase6.md`, laporan `docs/report/CHIPATON_Phase6_Report.pdf`, disetujui tim 2026-10-03):
- Aritmetika K-PKE (KeyGen, Encrypt, Decrypt) berjalan sebagai program tetap di perangkat keras, bit-exact terhadap model golden, siklus konstan: KeyGen 5.493, Encrypt 6.810, Decrypt 3.121 (MEASURED, simulasi, `docs/evidence/phase06-scheduling/verify_2026-10-03.md`).
- **S10 (memori 16 bank tanpa arbitrasi):** median Fmax 44,320 MHz di 40 ns, 5.077 ALM, 118 siklus; batasan 20 ns terpenuhi di 6 dari 6 seed (MEASURED, kompilasi kernel-only, `docs/evidence/phase06-scheduling/s10/selection_worksheet_2026-10-03.md`); dipilih tim sebagai inti NTT/INTT untuk fase berikutnya (ADR 0025, *Accepted*).

Fase 7 (Keccak-f[1600] dan SHA3/SHAKE, konfigurasi K0; `docs/results/result_phase7.md`, disetujui tim 2026-10-03):
- Permutasi 1 ronde per siklus (24 siklus sibuk untuk semua data) dan sponge SHA3-256, SHA3-512, SHAKE128, SHAKE256 sama dengan `hashlib` pada semua panjang yang diuji, di dua simulator; analisis formal K1–K5 lolos; siklus hanya bergantung pada panjang publik (MEASURED, simulasi, `docs/evidence/phase07-keccak/verify_2026-10-03.md`).
- K0: 3.572 ALM, 1.653 register, 0 M10K, 0 DSP; batasan 40 ns terpenuhi (Fmax 56,99 MHz) dan 20 ns terpenuhi (76,30 MHz), satu seed, kernel-only (MEASURED, `docs/evidence/phase07-keccak/quartus_K0_20261003.md`). Belum termasuk sampler.

Semua hasil **terukur di simulasi, analisis formal dan laporan Quartus saja** (kernel-only, virtual pin); batasan 40 ns
terpenuhi di semua seed yang diuji; batasan 20 ns (50 MHz) terpenuhi hanya oleh inti S10 dan unit Fase 6 dengan S10 (kompilasi kernel-only). **Belum ada pengukuran pada papan.** Setiap angka berasal
dari laporan Quartus atau simulasi dan disimpan sebagai bukti di `docs/evidence/`. Berikutnya: Fase 8 (8a, 8b, 8c, 8d, ADR 0026)
dan blok ML-KEM lainnya (ADR 0019). Rencana: `docs/ROADMAP.md`.

## Batas klaim
- Parameter ML-KEM tidak diubah; inovasi hanya pada arsitektur perangkat keras.
- Ketahanan terhadap serangan side-channel (daya/EM) **tidak diklaim** pada tahap inti; itu tahap lanjut.
- Tidak ada klaim "kebal kuantum" atau percepatan sebelum ada pengukuran.

## Peta repositori
| Folder | Isi |
|---|---|
| `rtl/` | SystemVerilog yang dapat disintesis |
| `tb/` | testbench cocotb dan model acuan Python (`tb/golden/`) |
| `formal/` | properti SymbiYosys |
| `quartus/` | proyek Quartus, Platform Designer, `.sdc` |
| `sw/hps/` | kode sisi HPS (ARM Linux) |
| `docs/` | brief proyek, roadmap, keputusan (ADR), bukti, referensi proposal |
| `scripts/` | penyiapan lingkungan dan uji dasar |
| `.claude/` | pengaturan dan skill Claude Code untuk tim |

## Lisensi
MIT License, lihat `LICENSE` (ADR 0016). Berkas pihak ketiga yang membawa lisensi sendiri tetap memakai lisensinya.
