# Phase 3: multi-lane

Status: DONE. Halaman hasil: [../../docs/results/phase03.md](../../docs/results/phase03.md).

**Tujuan.** Membandingkan L = 1, 2, 4, 8 dan memilih L (C2).

**Yang diuji.** Kebenaran tiap L, empat evidence Quartus, tabel perbandingan, ekuivalensi butterfly (K1) dan ukuran t_q (K2).

**Alat.** cocotb, SymbiYosys, uji menyeluruh Verilator (K1), Quartus.

**Hasil utama.** L = 8 dengan C2-K2-K1 dipilih (ADR 0005): NTT 113 dan INTT 369 siklus, 9.754 ALM. Timing 20 ns tidak terpenuhi pada semua L (didokumentasikan).

**File penting.**
- [test_plan.md](test_plan.md)
- [cocotb_regression.txt](cocotb_regression.txt)
- [k1_experiment.md](k1_experiment.md)
- [k2_experiment.md](k2_experiment.md)
- [k1_exhaustive_equivalence.txt](k1_exhaustive_equivalence.txt)
- [formal_verification.txt](formal_verification.txt)

Semua file di folder ini dibuat oleh alat, bukan diketik tangan. Angka Quartus berasal dari kompilasi kernel-only dengan virtual pin.
