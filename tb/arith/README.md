# tb/arith/

Uji aritmetika Phase 5 untuk [`rtl/arith/`](../../rtl/arith/README.md).

| File / folder | Fungsi |
|---|---|
| `test_reducer_c4.py`, `test_reducer_c4_lazy_d6.py`, `test_lazy_corners.py` | reducer dan varian lazy terhadap rumus (a·b) mod q, kasus sudut |
| `c4_tb_wrappers.sv` | pembungkus simulasi: reducer Montgomery diberi masukan dalam bentuk Montgomery |
| `run_c4_unit_tests.py`, `run_c4_core_tests.py` | driver uji unit dan uji inti C4 di dua simulator |
| `reducer_exhaustive/` | Verilator + C++: semua 3.329² pasangan dalam [0, q) untuk fold, Barrett, Montgomery, dengan kontrol negatif |
| `lazy_exhaustive/` | hal yang sama untuk varian lazy |
| `check_mont_rom.py` | memeriksa ROM twiddle Montgomery |

Uji menyeluruh membandingkan keluaran dengan referensi untuk setiap pasangan, jadi untuk modul ini hasilnya penuh pada rentang itu.
Masukan di luar [0, q) hanya dilaporkan, tidak dipersyaratkan. Konteks: [../../evidence/phase05/](../../evidence/phase05/README.md).
