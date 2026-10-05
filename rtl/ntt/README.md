# rtl/ntt/

Inti NTT/INTT dari baseline sampai inti terpilih. NTT *incomplete*: 7 layer, 128 butterfly per layer.

## Inti yang dipakai

`ntt_core_s10.sv` (S10): 8 butterfly per siklus, memori `rtl/mem/poly_mem_m10k.sv` (16 bank 1R1W), reducer Barrett,
118 siklus untuk NTT dan INTT, INTT dengan pembagian dua di tiap layer (ADR 0020, 0025).
`ntt_core_s10_p5.sv` adalah wrapper Quartus revisi S10. Parameter `RD_LAT` dan `MUL_REG` menentukan kedalaman pipeline.

## Riwayat (dibekukan sebagai bukti)

| File | Fase | Isi |
|---|---|---|
| `ntt_core.sv`, `butterfly.sv`, `modmul_reduce.sv`, `poly_mem.sv`, `twiddle_rom.sv` | 1 | baseline L = 1 (C0) |
| `ntt_core_c2*.sv` | 3 | multi-lane L = 1, 2, 4, 8; `_k2`, `_k1` menambah ukuran t_q dan satu pengali per butterfly |
| `ntt_core_c3*.sv`, `butterfly_shared_pipe.sv`, `modmul_reduce_staged.sv`, `pipe_delay.sv` | 4 | pipeline P = 2, 4, 6 |
| `ntt_core_c4*.sv` | 5 | reducer fold, Barrett, Montgomery, lazy |
| `ntt_core_m6*.sv`, `ntt_core_s7*.sv`, `ntt_core_s8*.sv` | 5M | INTT tanpa lintasan skala, split baca, register tulis |
| `ntt_core_s10*.sv` | 6 | memori 16 bank |
| `base_case_multiply.sv` | 4 | BaseCaseMultiply (FIPS 203 Alg. 12); inti penuh memakai `rtl/sched/pwm_unit.sv` |
| `ntt_pkg.sv` | | parameter bersama |

Konfigurasi yang tidak dipilih tetap ada karena bukti Quartus dan formalnya merujuk ke file ini.
Uji: [../../tb/ntt/](../../tb/README.md), [../../tb/phase5m/](../../tb/README.md), [../../tb/s10/](../../tb/README.md).
Formal: [../../formal/](../../formal/README.md).
