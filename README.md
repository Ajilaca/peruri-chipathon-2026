# peruri-chipathon-2026

Tim J5 (Institut Teknologi Bandung), CHIP 2026 Hackathon (PERURI Digital Summit),
kategori *IC Chip Design & FPGA Implementation*.

**Ide:** akselerator perangkat keras **ML-KEM-768** (NIST FIPS 203, kriptografi pasca-kuantum)
dengan pendekatan *hardware/software co-design* pada Terasic DE10-Nano (Intel Cyclone V SoC
5CSEBA6U23I7): Keccak-f[1600] dan NTT/INTT di FPGA, alur protokol dan baseline perangkat lunak
di HPS (ARM Cortex-A9). Target utama: eksekusi waktu-konstan yang dibuktikan, hasil bit-exact
terhadap vektor uji resmi, dan angka sumber daya/timing yang diukur dari Quartus.

## Status
Fase 0–5 selesai secara teknis (lihat `docs/results/` dan `HANDOFF.md`). Konfigurasi inti NTT/INTT saat ini: **C4 = C4b-B**
(8 lajur, pipeline 6 tahap, reduksi Barrett, ADR 0013 masih *Proposed*), dari basis **C3-P6** (ADR 0009). Hasil Fase 5
(`docs/results/result_phase5.md`, laporan `docs/report/CHIPATON_Phase5_Report.pdf`):
- Siklus tetap NTT 119 dan INTT 375 (MEASURED, simulasi, `docs/evidence/phase05-arith/regression_2026-10-01.md`); hasil bit-exact terhadap model golden di dua simulator.
- C4b-B memakai 9.166–9.208 ALM (seed 1–6) dibanding 10.484–10.516 pada C3-P6, dengan 18 DSP (C3-P6: 9) (MEASURED, `docs/evidence/phase05-arith/5b/selection_worksheet_2026-10-01.md`).
- Fmax tidak naik di luar sebaran seed; kompilasi informasi 20 ns **tidak memenuhi timing** (MEASURED, `docs/evidence/phase05-arith/closure/info_20ns_2026-10-01.md`: C3-P6 setup −2,059 ns,
  C4b-B −2,557 ns). Jalur kritis ada di pembacaan memori, bukan di aritmetika.
- 5c (lazy reduction) diukur dan tidak diadopsi; 5d (Karatsuba) tidak dicoba (ADR 0015, *Proposed*).

Semua hasil **terukur di simulasi, analisis formal dan laporan Quartus saja** (kernel-only, virtual pin); batasan 40 ns
terpenuhi di semua seed yang diuji, target 50 MHz belum tercapai. **Belum ada pengukuran pada papan.** Setiap angka berasal
dari laporan Quartus atau simulasi dan disimpan sebagai bukti di `docs/evidence/`. Berikutnya: keputusan tim atas
ADR 0013/0015 dan fase "memori dan jadwal" (PENDING #19). Rencana: `docs/ROADMAP.md`.

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
