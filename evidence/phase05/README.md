# Phase 5: aritmetika modular

Status: DONE. Halaman hasil: [../../docs/results/phase05.md](../../docs/results/phase05.md).

Tujuan. Memilih reducer: fold (5a), Barrett atau Montgomery (5b), lazy (5c).

Yang diuji. Uji reducer menyeluruh, kebenaran inti, formal per varian, seed sweep, kompilasi informasi 20 ns.

Alat. cocotb, Verilator C++ (menyeluruh), SymbiYosys, Quartus.

Hasil utama. Barrett (C4b-B) dipilih oleh aturan ADR 0011: 9.166 sampai 9.208 ALM, 18 DSP, siklus 119 / 375. 5c diukur dan tidak diadopsi. Kompilasi 20 ns tidak memenuhi timing; jalur kritis ada di pembacaan memori.

File penting.
- [test_plan.md](test_plan.md)
- [regression.md](regression.md)
- [5b/selection_worksheet.md](5b/selection_worksheet.md)
- [5c/summary_5c.md](5c/summary_5c.md)
- [closure/info_20ns.md](closure/info_20ns.md)

Semua file di folder ini dibuat oleh alat, bukan diketik tangan. Angka Quartus berasal dari kompilasi kernel-only dengan virtual pin.
