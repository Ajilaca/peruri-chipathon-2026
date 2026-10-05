# Phase 4: pipeline

Status: DONE. Halaman hasil: [../../docs/results/phase04.md](../../docs/results/phase04.md).

Tujuan. Memilih kedalaman pipeline P untuk inti L = 8 (C3).

Yang diuji. P = 0, 2, 4, 6: kebenaran, hazard di batas layer, stall, sapuan seed, Quartus pada 40 ns, integrasi dengan GHRD.

Alat. cocotb, SymbiYosys, Quartus (seed 1 sampai 6), GHRD DE10-Nano.

Hasil utama. C3-P6 dipilih (ADR 0009): NTT 119 dan INTT 375 siklus, 10.484 sampai 10.516 ALM, timing 40 ns terpenuhi.

File penting.
- [test_plan.md](test_plan.md)
- [quartus_C3-P6.md](quartus_C3-P6.md)
- [seed_sweep.md](seed_sweep.md)
- [selection_worksheet.md](selection_worksheet.md)
- [ghrd_plus_c3p6_integration.md](ghrd_plus_c3p6_integration.md)
- [formal.md](formal.md)

Semua file di folder ini dibuat oleh alat, bukan diketik tangan. Angka Quartus berasal dari kompilasi kernel-only dengan virtual pin.
