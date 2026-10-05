# rtl/arith/

Aritmetika modular untuk q = 3329 dan butterfly yang memakainya. Dibuat di Phase 5 dan 5M.

| File | Fungsi |
|---|---|
| `modmul_barrett.sv` | (a·b) mod q dengan Barrett, k = 24, M = 5039. Reducer yang dipakai (ADR 0013) |
| `modmul_fold.sv` | reducer fold (2^12 ≡ 767 mod q), kandidat 5a |
| `modmul_montgomery.sv` | Montgomery R = 2^12, kandidat 5b, tidak dipilih |
| `modmul_barrett_lazy.sv`, `butterfly_c4_lazy.sv`, `lazy_bfly_io.sv` | varian lazy 5c, diukur dan tidak diadopsi (ADR 0014) |
| `modmul_sel.sv` | memilih reducer lewat `RED_KIND` (1 fold, 2 Barrett, 3 Montgomery) |
| `butterfly_c4.sv` | butterfly CT (maju) dan GS (mundur) dengan reducer terpilih |
| `butterfly_m6.sv`, `half_mod.sv` | butterfly S6: INTT membagi dua di tiap layer, `half_mod` menghitung x/2 mod q |
| `twiddle_rom_half.sv`, `twiddle_rom_mont.sv` | ROM twiddle dibangkitkan oleh `scripts/build/gen_twiddle_rom_*.py` |

Semua perkalian dengan q memakai penjumlahan geser. Tidak ada pembagian atau modulo.
Reducer diuji pada semua pasangan masukan dalam [0, q) di [../../tb/arith/](../../tb/arith/README.md).
Keputusan pemilihan: ADR 0011 (aturan), 0013 (Barrett), 0020 (S6). Hasil: [../../evidence/phase05/](../../evidence/phase05/README.md).
