# Phase 9M-1 core simulator run (V3, V5), `CORE_W2=1 tb/mlkem/run_core_tests.py verilator core ncwcore`, 2026-10-04

MEASURED (simulation only), core with `CODEC_W2 = 1` (two-byte load / store tasks). The line `[verilator] core` is the whole set (ACVP keyGen 25, encapsulation 25, decapsulation 10; random cross-check with CORE_N=20; protocol; constant cycles); `ncwcore` is the negative control NC-W-CORE (the loader writes the coefficient index + 1), which must fail the ACVP encapsulation test. Only the result lines of the log are kept; the repository path prefix in the traceback of the expected control failure is shortened to <repo>.

```
2150515.00ns INFO     cocotb.mlkem_core                  ACVP keyGen: 25 vectors equal
2150515.00ns INFO     cocotb.regression                  test_mlkem_core.test_acvp_keygen passed
4755890.00ns INFO     cocotb.mlkem_core                  ACVP encapsulation: 25 vectors equal
4755890.00ns INFO     cocotb.regression                  test_mlkem_core.test_acvp_encaps passed
6348565.00ns INFO     cocotb.mlkem_core                  ACVP decapsulation: 10 vectors equal
6348565.00ns INFO     cocotb.regression                  test_mlkem_core.test_acvp_decaps passed
V4: random KeyGen, Encaps, Decaps (valid and one-bit-changed ciphertexts) against the unmodified golden, and the chain KeyGen -> Encaps -> Decaps through the RTL.
16521460.00ns INFO     cocotb.regression                  test_mlkem_core.test_random_cross_check_and_chain passed
V5: start, op and host write while busy are ignored; reset in the middle then a clean operation; back to back operations with other keys.
17005695.00ns INFO     cocotb.regression                  test_mlkem_core.test_protocol_corner_cases passed
17005695.00ns INFO     cocotb.regression                  running test_mlkem_core.test_constant_cycles (6/6)
V6: Decaps cycles identical for valid and rejected ciphertexts and for different secret keys with the same ek; Encaps identical for different m with the same ek; KeyGen spread reported.
22932310.00ns INFO     cocotb.mlkem_core                  constant cycles: Encaps [10115], Decaps [15471]; KeyGen over the ACVP seeds: min 8267, max 8308
22932310.00ns INFO     cocotb.regression                  test_mlkem_core.test_constant_cycles passed
** test_mlkem_core.test_constant_cycles                PASS     5926615.00          42.63     139009.81  **
172215.00ns INFO     cocotb.mlkem_core                  ACVP keyGen: 2 vectors equal
172215.00ns INFO     cocotb.regression                  test_mlkem_core.test_acvp_keygen passed
276590.00ns WARNING  cocotb.regression                  test_mlkem_core.test_acvp_encaps failed
436215.00ns WARNING  cocotb.regression                  test_mlkem_core.test_acvp_decaps failed
V4: random KeyGen, Encaps, Decaps (valid and one-bit-changed ciphertexts) against the unmodified golden, and the chain KeyGen -> Encaps -> Decaps through the RTL.
626000.00ns WARNING  cocotb.regression                  test_mlkem_core.test_random_cross_check_and_chain failed
V5: start, op and host write while busy are ignored; reset in the middle then a clean operation; back to back operations with other keys.
730375.00ns WARNING  cocotb.regression                  test_mlkem_core.test_protocol_corner_cases failed
730375.00ns INFO     cocotb.regression                  running test_mlkem_core.test_constant_cycles (6/6)
V6: Decaps cycles identical for valid and rejected ciphertexts and for different secret keys with the same ek; Encaps identical for different m with the same ek; KeyGen spread reported.
834570.01ns WARNING  cocotb.regression                  test_mlkem_core.test_constant_cycles failed
File "<repo>/tb/mlkem/test_mlkem_core.py", line 166, in test_constant_cycles
** test_mlkem_core.test_constant_cycles                FAIL      104195.00           0.62     167002.60  **
[verilator] core: 6/6 PASS
[verilator] ncwcore: test_acvp_encaps failed as required: True; failed=['test_acvp_encaps', 'test_acvp_decaps', 'test_random_cross_check_and_chain', 'test_protocol_corner_cases', 'test_constant_cycles']
[verilator] TOTAL: 7/7 passed
```
