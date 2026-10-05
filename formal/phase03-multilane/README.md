# formal/phase03-multilane/

Properti untuk inti multi-lane (`ntt_core_c2*`).

- `ntt_core_c2_l{1,2,4,8}_safety.sby`, `ntt_core_c2_k2_l*`, `ntt_core_c2_k2_k1_l*`: keselamatan per jumlah lajur dan per varian; tops `*_formal_top.sv`.
- `k1_butterfly_equiv*.sby` dan `.sv`: ekuivalensi butterfly dengan satu pengali (K1) terhadap acuan, dengan `modmul_reduce_uf.sv` (fungsi tak-terinterpretasi untuk reducer) dan versi abstrak.
- `k1_negctl_*`: kontrol negatif K1 (operand salah, tanpa ack); harus gagal.

Hasil: [../../evidence/phase03/](../../evidence/phase03/README.md).
