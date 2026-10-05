# Phase 6: sequencer K-PKE dan S10

Status: DONE. Halaman hasil: [../../docs/results/phase06.md](../../docs/results/phase06.md).

**Tujuan.** Menjalankan aritmetika K-PKE (KeyGen, Encrypt, Decrypt) sebagai program tetap, dan membangun memori S10.

**Yang diuji.** Bit-exact terhadap model acuan, siklus konstan, formal sequencer, Quartus S10 (seed 1 sampai 6, 40 ns dan 20 ns).

**Alat.** cocotb, SymbiYosys, Quartus.

**Hasil utama.** KeyGen 5.493, Encrypt 6.810, Decrypt 3.121 siklus. S10 diterima sebagai inti NTT/INTT (ADR 0025): median 44,320 MHz pada 40 ns, 5.077 ALM, 118 siklus.

**File penting.**
- [test_plan.md](test_plan.md)
- [test_plan_s10.md](test_plan_s10.md)
- [verify.md](verify.md)
- [formal.md](formal.md)
- [s10/selection_worksheet.md](s10/selection_worksheet.md)
- [quartus_P6S10.md](quartus_P6S10.md)

Semua file di folder ini dibuat oleh alat, bukan diketik tangan. Angka Quartus berasal dari kompilasi kernel-only dengan virtual pin.
