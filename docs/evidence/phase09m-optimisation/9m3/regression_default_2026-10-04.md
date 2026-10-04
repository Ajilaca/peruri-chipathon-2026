# Phase 9M-3 regression at the default parameters (V6), 2026-10-04

MEASURED (simulation). The core at the defaults (`HASH_C5 = 1`, `CODEC_W2 = 0`) must behave as in Phase 9. `tb/mlkem/run_core_tests.py verilator core` (no CORE_K0 / CORE_W2) and `tb/mlkem/profile_core.py` at the defaults; the profile JSON is byte-for-byte equal in content to `../profile_verilator_2026-10-04.json` (Phase 9 profile: KeyGen 9,095, Encaps 10,735, Decaps 16,667 cycles, every per-state and per-micro-operation count equal). No RTL file was changed in this item. Only the result lines of the log are kept.

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
