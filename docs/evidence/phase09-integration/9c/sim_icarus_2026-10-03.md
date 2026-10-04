# Phase 9c simulator run (V3-V8), `tb/mlkem/run_core_tests.py icarus`, 2026-10-03

MEASURED (simulation only). The line `[icarus] core` is the whole set (ACVP keyGen 25, encapsulation 25, decapsulation 10; random cross-check; protocol; constant cycles); the lines `[icarus] nc...` are the negative controls (test-only copies of the RTL / ROM, reduced vector set) that must fail the test named on the line.

```
                                                            V3: ACVP keyGen: ek and dk of every vector.
2342515.00ns INFO     cocotb.mlkem_core                  ACVP keyGen: 25 vectors equal
2342515.00ns INFO     cocotb.regression                  test_mlkem_core.test_acvp_keygen passed
                                                            V3: ACVP encapsulation: c and k of every vector.
5091890.00ns INFO     cocotb.mlkem_core                  ACVP encapsulation: 25 vectors equal
5091890.00ns INFO     cocotb.regression                  test_mlkem_core.test_acvp_encaps passed
                                                            V3: ACVP decapsulation (valid and modified ciphertexts): k of every vector.
6799765.00ns INFO     cocotb.mlkem_core                  ACVP decapsulation: 10 vectors equal
6799765.00ns INFO     cocotb.regression                  test_mlkem_core.test_acvp_decaps passed
17702260.00ns INFO     cocotb.mlkem_core                  20 random cases equal (keygen, encaps, decaps valid and modified, chain)
17702260.00ns INFO     cocotb.regression                  test_mlkem_core.test_random_cross_check_and_chain passed
18217215.00ns INFO     cocotb.regression                  test_mlkem_core.test_protocol_corner_cases passed
24558550.00ns INFO     cocotb.mlkem_core                  constant cycles: Encaps [10691], Decaps [16623]; KeyGen over the ACVP seeds: min 9035, max 9076
24558550.00ns INFO     cocotb.regression                  test_mlkem_core.test_constant_cycles passed
                                                        ** TESTS=6 PASS=6 FAIL=0 SKIP=0                                24558550.00        2844.69       8633.11  **
                                                            V3: ACVP keyGen: ek and dk of every vector.
187575.00ns INFO     cocotb.mlkem_core                  ACVP keyGen: 2 vectors equal
187575.00ns INFO     cocotb.regression                  test_mlkem_core.test_acvp_keygen passed
                                                            V3: ACVP encapsulation: c and k of every vector.
407740.00ns INFO     cocotb.mlkem_core                  ACVP encapsulation: 2 vectors equal
407740.00ns INFO     cocotb.regression                  test_mlkem_core.test_acvp_encaps passed
                                                            V3: ACVP decapsulation (valid and modified ciphertexts): k of every vector.
749435.00ns WARNING  cocotb.regression                  test_mlkem_core.test_acvp_decaps failed
1293660.00ns WARNING  cocotb.regression                  test_mlkem_core.test_random_cross_check_and_chain failed
1808015.00ns WARNING  cocotb.regression                  test_mlkem_core.test_protocol_corner_cases failed
2088660.00ns WARNING  cocotb.regression                  test_mlkem_core.test_constant_cycles failed
                                                        ** TESTS=6 PASS=2 FAIL=4 SKIP=0                                 2088660.00         263.09       7938.96  **
                                                            V3: ACVP keyGen: ek and dk of every vector.
187575.00ns INFO     cocotb.mlkem_core                  ACVP keyGen: 2 vectors equal
187575.00ns INFO     cocotb.regression                  test_mlkem_core.test_acvp_keygen passed
                                                            V3: ACVP encapsulation: c and k of every vector.
407740.00ns INFO     cocotb.mlkem_core                  ACVP encapsulation: 2 vectors equal
407740.00ns INFO     cocotb.regression                  test_mlkem_core.test_acvp_encaps passed
                                                            V3: ACVP decapsulation (valid and modified ciphertexts): k of every vector.
578885.00ns WARNING  cocotb.regression                  test_mlkem_core.test_acvp_decaps failed
952610.00ns WARNING  cocotb.regression                  test_mlkem_core.test_random_cross_check_and_chain failed
1466965.00ns WARNING  cocotb.regression                  test_mlkem_core.test_protocol_corner_cases failed
1747610.00ns WARNING  cocotb.regression                  test_mlkem_core.test_constant_cycles failed
                                                        ** TESTS=6 PASS=2 FAIL=4 SKIP=0                                 1747610.00         213.83       8172.77  **
                                                            V3: ACVP keyGen: ek and dk of every vector.
2000175.00ns WARNING  cocotb.regression                  test_mlkem_core.test_acvp_keygen failed
                                                            V3: ACVP encapsulation: c and k of every vector.
2110300.00ns WARNING  cocotb.regression                  test_mlkem_core.test_acvp_encaps failed
                                                            V3: ACVP decapsulation (valid and modified ciphertexts): k of every vector.
2281435.00ns WARNING  cocotb.regression                  test_mlkem_core.test_acvp_decaps failed
4281610.00ns WARNING  cocotb.regression                  test_mlkem_core.test_random_cross_check_and_chain failed
4391735.00ns WARNING  cocotb.regression                  test_mlkem_core.test_protocol_corner_cases failed
4501680.00ns WARNING  cocotb.regression                  test_mlkem_core.test_constant_cycles failed
                                                        ** TESTS=6 PASS=0 FAIL=6 SKIP=0                                 4501680.00         114.06      39468.06  **
                                                            V3: ACVP keyGen: ek and dk of every vector.
187575.00ns INFO     cocotb.mlkem_core                  ACVP keyGen: 2 vectors equal
187575.00ns INFO     cocotb.regression                  test_mlkem_core.test_acvp_keygen passed
                                                            V3: ACVP encapsulation: c and k of every vector.
407740.00ns INFO     cocotb.mlkem_core                  ACVP encapsulation: 2 vectors equal
407740.00ns INFO     cocotb.regression                  test_mlkem_core.test_acvp_encaps passed
                                                            V3: ACVP decapsulation (valid and modified ciphertexts): k of every vector.
578885.00ns WARNING  cocotb.regression                  test_mlkem_core.test_acvp_decaps failed
952610.00ns WARNING  cocotb.regression                  test_mlkem_core.test_random_cross_check_and_chain failed
1467565.00ns INFO     cocotb.regression                  test_mlkem_core.test_protocol_corner_cases passed
2260280.00ns WARNING  cocotb.regression                  test_mlkem_core.test_constant_cycles failed
                                                        ** TESTS=6 PASS=3 FAIL=3 SKIP=0                                 2260280.00         280.16       8067.92  **
                                                            V3: ACVP keyGen: ek and dk of every vector.
187575.00ns INFO     cocotb.mlkem_core                  ACVP keyGen: 2 vectors equal
187575.00ns INFO     cocotb.regression                  test_mlkem_core.test_acvp_keygen passed
                                                            V3: ACVP encapsulation: c and k of every vector.
297710.00ns WARNING  cocotb.regression                  test_mlkem_core.test_acvp_encaps failed
                                                            V3: ACVP decapsulation (valid and modified ciphertexts): k of every vector.
468855.00ns WARNING  cocotb.regression                  test_mlkem_core.test_acvp_decaps failed
672080.00ns WARNING  cocotb.regression                  test_mlkem_core.test_random_cross_check_and_chain failed
782215.00ns WARNING  cocotb.regression                  test_mlkem_core.test_protocol_corner_cases failed
892170.01ns WARNING  cocotb.regression                  test_mlkem_core.test_constant_cycles failed
                                                        ** TESTS=6 PASS=1 FAIL=5 SKIP=0                                  892170.01         110.09       8103.69  **
[icarus] core: 6/6 PASS
[icarus] nccmp: test_acvp_decaps failed as required: True; failed=['test_acvp_decaps', 'test_random_cross_check_and_chain', 'test_protocol_corner_cases', 'test_constant_cycles']
[icarus] ncsel: test_acvp_decaps failed as required: True; failed=['test_acvp_decaps', 'test_random_cross_check_and_chain', 'test_protocol_corner_cases', 'test_constant_cycles']
[icarus] nclen: test_acvp_encaps failed as required: True; failed=['test_acvp_keygen', 'test_acvp_encaps', 'test_acvp_decaps', 'test_random_cross_check_and_chain', 'test_protocol_corner_cases', 'test_constant_cycles']
[icarus] ncoff: test_acvp_decaps failed as required: True; failed=['test_acvp_decaps', 'test_random_cross_check_and_chain', 'test_constant_cycles']
[icarus] ncrom: test_acvp_encaps failed as required: True; failed=['test_acvp_encaps', 'test_acvp_decaps', 'test_random_cross_check_and_chain', 'test_protocol_corner_cases', 'test_constant_cycles']
[icarus] TOTAL: 11/11 passed
```
