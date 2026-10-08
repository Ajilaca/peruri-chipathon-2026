# Regresi Fase 9M-3 pada parameter bawaan (V6), 2026-10-04

MEASURED (simulasi). Inti pada nilai bawaan (`HASH_C5 = 1`, `CODEC_W2 = 0`) harus berperilaku seperti di Fase 9. `tb/mlkem/run_core_tests.py verilator core` (tanpa CORE_K0 / CORE_W2) dan `tb/mlkem/profile_core.py` pada nilai bawaan; JSON profil sama persis isinya dengan `../../profile_verilator.json` (profil Fase 9: KeyGen 9.095, Encaps 10.735, Decaps 16.667 siklus, setiap hitungan per-state dan per-micro-operation sama). Tidak ada file RTL yang diubah di butir ini. Hanya baris hasil log yang disimpan.

```
2342515.00ns INFO     cocotb.mlkem_core                  ACVP keyGen: 25 vectors equal
2342515.00ns INFO     cocotb.regression                  test_mlkem_core.test_acvp_keygen passed
5091890.00ns INFO     cocotb.mlkem_core                  ACVP encapsulation: 25 vectors equal
5091890.00ns INFO     cocotb.regression                  test_mlkem_core.test_acvp_encaps passed
6799765.00ns INFO     cocotb.mlkem_core                  ACVP decapsulation: 10 vectors equal
6799765.00ns INFO     cocotb.regression                  test_mlkem_core.test_acvp_decaps passed
17702260.00ns INFO     cocotb.mlkem_core                  20 random cases equal (keygen, encaps, decaps valid and modified, chain)
17702260.00ns INFO     cocotb.regression                  test_mlkem_core.test_random_cross_check_and_chain passed
18217215.00ns INFO     cocotb.regression                  test_mlkem_core.test_protocol_corner_cases passed
24558550.00ns INFO     cocotb.mlkem_core                  constant cycles: Encaps [10691], Decaps [16623]; KeyGen over the ACVP seeds: min 9035, max 9076
24558550.00ns INFO     cocotb.regression                  test_mlkem_core.test_constant_cycles passed
[verilator] TOTAL: 6/6 passed
```
