# Phase 2: banking memori

Status: DONE. Halaman hasil: [../../docs/results/phase02.md](../../docs/results/phase02.md).

Tujuan. Peta bank memori bebas konflik untuk L = 1, 2, 4, 8 (C1).

Yang diuji. Bukti bebas konflik untuk keempat L, stall = 0 pada L = 1, bit-exact, properti formal peta bank.

Alat. Python (eksplorasi skema bank), cocotb, SymbiYosys, Quartus.

Hasil utama. Peta bank bebas konflik terbukti untuk keempat L; siklus sama dengan C0. M10K tidak tercapai (pembacaan asinkron), timing 20 ns tidak terpenuhi (didokumentasikan).

File penting.
- [bank_map_spec.md](bank_map_spec.md)
- [bank_scheme_exploration.txt](bank_scheme_exploration.txt)
- [formal_bank_map.txt](formal_bank_map.txt)
- [quartus_C1_vs_C0.md](quartus_C1_vs_C0.md)
- [cocotb_regression.txt](cocotb_regression.txt)

Semua file di folder ini dibuat oleh alat, bukan diketik tangan. Angka Quartus berasal dari kompilasi kernel-only dengan virtual pin.
