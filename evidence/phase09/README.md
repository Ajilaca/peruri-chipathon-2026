# Phase 9: inti ML-KEM-768 penuh

Status: DONE. Halaman hasil: [../../docs/results/phase09.md](../../docs/results/phase09.md).

**Tujuan.** Menyatukan codec (9a), hash dan FO (9b), dan pengendali inti (9c).

**Yang diuji.** Semua vektor ACVP yang berlaku di dua simulator (keyGen 25, encapsulation 25, decapsulation 10), siklus konstan Decaps, formal, Quartus.

**Alat.** cocotb, SymbiYosys, Quartus.

**Hasil utama.** Inti `mlkem_core`: 9.095 / 10.735 / 16.667 siklus (KeyGen / Encaps / Decaps), 17.620,5 ALM, median 49,280 MHz pada 40 ns (kernel-only). Pemeriksaan masukan dikerjakan HPS (ADR 0031). Penerimaan ADR 0033 menunggu tim.

**File penting.**
- [phase9_plan.md](phase9_plan.md)
- [9a/formal.md](9a/formal.md)
- [9b/formal.md](9b/formal.md)
- [9c/result_9c.md](9c/result_9c.md)
- [9c/formal.md](9c/formal.md)

Semua file di folder ini dibuat oleh alat, bukan diketik tangan. Angka Quartus berasal dari kompilasi kernel-only dengan virtual pin.
