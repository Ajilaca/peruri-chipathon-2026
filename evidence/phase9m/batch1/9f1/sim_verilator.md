# Run simulator Fase 9F S1, Verilator (V2, V3, V5), 2026-10-04

MEASURED (hanya simulasi). (a) `CORE_TOP=mlkem_core2 CORE_SMP0=1 CORE_K0=1 CORE_W2=1 tb/mlkem/run_core_tests.py verilator core nclen`: inti pada K1 (`SMP_C5 = 0`, `HASH_C5 = 0`, `CODEC_W2 = 1`); `nclen` adalah kontrol (setiap hash kurang satu byte), yang harus menggagalkan test enkapsulasi ACVP. (b) `KP_VAR=2 KP_CORE_R2=0 tb/smp/run_smp_tests.py verilator top`: test sequencer Fase 8c / 8d dengan sampler K0. Hanya baris hasil yang disimpan; awalan path repository dipendekkan menjadi <repo>.

## (a) inti
```
2264635.00ns INFO     cocotb.mlkem_core2                 ACVP keyGen: 25 vectors equal
2264635.00ns INFO     cocotb.regression                  test_mlkem_core.test_acvp_keygen passed
4984610.00ns INFO     cocotb.mlkem_core2                 ACVP encapsulation: 25 vectors equal
4984610.00ns INFO     cocotb.regression                  test_mlkem_core.test_acvp_encaps passed
6623005.00ns INFO     cocotb.mlkem_core2                 ACVP decapsulation: 10 vectors equal
6623005.00ns INFO     cocotb.regression                  test_mlkem_core.test_acvp_decaps passed
17161180.00ns INFO     cocotb.mlkem_core2                 20 random cases equal (keygen, encaps, decaps valid and modified, chain)
17161180.00ns INFO     cocotb.regression                  test_mlkem_core.test_random_cross_check_and_chain passed
17664015.00ns INFO     cocotb.regression                  test_mlkem_core.test_protocol_corner_cases passed
23773030.00ns INFO     cocotb.mlkem_core2                 constant cycles: Encaps [10571], Decaps [15927]; KeyGen over the ACVP seeds: min 8723, max 8776
23773030.00ns INFO     cocotb.regression                  test_mlkem_core.test_constant_cycles passed
[verilator] core: 6/6 PASS
[verilator] nclen: test_acvp_encaps failed as required: True; failed=['test_acvp_keygen', 'test_acvp_encaps', 'test_acvp_decaps', 'test_random_cross_check_and_chain', 'test_protocol_corner_cases', 'test_constant_cycles']
[verilator] TOTAL: 7/7 passed
```

## (b) sequencer dengan sampler K0
```
                                                        ** test_kpke_smp.test_programs_bit_exact          PASS     1928135.00          16.18     119158.65  **
                                                        ** test_kpke_smp.test_constant_cycles_fixed_rho   PASS     1646445.00          10.20     161345.01  **
                                                        ** test_kpke_smp.test_stall_coverage              PASS           0.00           0.00          0.00  **
                                                        ** TESTS=3 PASS=3 FAIL=0 SKIP=0                            3574580.00          26.39     135465.21  **
[verilator] top (VAR=2): 3/3 PASS
[verilator] TOTAL: 3/3 passed
```

Siklus test mesin (`cycles_smp_v2_verilator_k0sampler.json`) terhadap sampler C5 8d (`../../../phase08/8d/cycles_v2.json`): KeyGen 6.352 -> 6.688, Encrypt 7.653 -> 7.989 (+336 masing-masing), Decrypt 3.109 tidak berubah. Jadi sampler K0 benar-benar dipakai.
