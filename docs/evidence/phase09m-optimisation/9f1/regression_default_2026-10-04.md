# Phase 9F S1 regression at the defaults (V7), 2026-10-04

MEASURED (simulation). (a) `tb/mlkem/run_core_tests.py verilator core` at the defaults (`mlkem_core`, no CORE_* variable): the whole ACVP set and the other tests. (b) `tb/mlkem/profile_core.py` at the defaults for `mlkem_core` and for `mlkem_core2` at its defaults (`SMP_C5 = 1`, `HASH_C5 = 1`, `CODEC_W2 = 0`): both profile JSON files equal `../profile_verilator_2026-10-04.json` (Phase 9 profile: KeyGen 9,095, Encaps 10,735, Decaps 16,667 cycles, every per-state and per-micro-operation count). `rtl/mlkem/mlkem_core.sv` is unchanged by S1 and S1b (they use new modules). Only result lines are kept.

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
[verilator] core: 6/6 PASS
[verilator] TOTAL: 6/6 passed
```
