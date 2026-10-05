# Phase 1: NTT satu lajur

Status: DONE. Halaman hasil: [../../docs/results/phase01.md](../../docs/results/phase01.md).

Tujuan. RTL NTT/INTT dan perkalian titik paling sederhana (C0), sebagai titik acuan.

Yang diuji. Bit-exact terhadap model acuan, siklus konstan, properti FSM dan rentang alamat (formal), Quartus kernel-only.

Alat. cocotb (Verilator, Icarus), SymbiYosys, Quartus.

Hasil utama. NTT 897 dan INTT 1153 siklus (simulasi). Timing pada 20 ns tidak terpenuhi (slack negatif), didokumentasikan; ADR target clock (0006) baru ada sesudah fase ini.

File penting.
- [test_plan.md](test_plan.md)
- [cocotb_regression.txt](cocotb_regression.txt)
- [formal_ntt_core_safety.txt](formal_ntt_core_safety.txt)
- [quartus_C0_timing_analysis.md](quartus_C0_timing_analysis.md)

Semua file di folder ini dibuat oleh alat, bukan diketik tangan. Angka Quartus berasal dari kompilasi kernel-only dengan virtual pin.
