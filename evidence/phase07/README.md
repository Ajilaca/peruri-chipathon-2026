# Phase 7: Keccak-f[1600]

Status: DONE. Halaman hasil: [../../docs/results/phase07.md](../../docs/results/phase07.md).

**Tujuan.** Permutasi Keccak satu ronde per siklus (K0) dan sponge SHA3/SHAKE.

**Yang diuji.** SHA3-256, SHA3-512, SHAKE128, SHAKE256 terhadap `hashlib`, formal K1 sampai K5, Quartus enam seed.

**Alat.** cocotb, `hashlib`, SymbiYosys, Quartus.

**Hasil utama.** Bit-exact pada semua panjang yang diuji di dua simulator. 24 siklus sibuk per permutasi. K0: 3.572 ALM (seed 1), 40 ns dan 20 ns terpenuhi, kernel-only.

**File penting.**
- [test_plan.md](test_plan.md)
- [verify.md](verify.md)
- [formal.md](formal.md)
- [keccak_cycles.md](keccak_cycles.md)
- [quartus_K0.md](quartus_K0.md)

Semua file di folder ini dibuat oleh alat, bukan diketik tangan. Angka Quartus berasal dari kompilasi kernel-only dengan virtual pin.
