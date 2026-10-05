# Phase 9M-3 core simulator run (V2, V4), `CORE_W2=1 CORE_K0=1 tb/mlkem/run_core_tests.py icarus core nclen`, 2026-10-04

MEASURED (simulation only), core with `HASH_C5 = 0` (K0 sponge for the hash instance) and `CODEC_W2 = 1`. `[icarus] core` is the whole set (ACVP keyGen 25, encapsulation 25, decapsulation 10; random cross-check with CORE_N=20; protocol; constant cycles); `nclen` is the control (every hash one byte short), which must fail the ACVP encapsulation test. Only the result lines of the log are kept; the repository path prefix in tracebacks is shortened to <repo>.

```
2180515.00ns INFO     cocotb.mlkem_core                  ACVP keyGen: 25 vectors equal
2180515.00ns INFO     cocotb.regression                  test_mlkem_core.test_acvp_keygen passed
4815890.00ns INFO     cocotb.mlkem_core                  ACVP encapsulation: 25 vectors equal
4815890.00ns INFO     cocotb.regression                  test_mlkem_core.test_acvp_encaps passed
6420565.00ns INFO     cocotb.mlkem_core                  ACVP decapsulation: 10 vectors equal
6420565.00ns INFO     cocotb.regression                  test_mlkem_core.test_acvp_decaps passed
V4: random KeyGen, Encaps, Decaps (valid and one-bit-changed ciphertexts) against the unmodified golden, and the chain KeyGen -> Encaps -> Decaps through the RTL.
16689460.00ns INFO     cocotb.regression                  test_mlkem_core.test_random_cross_check_and_chain passed
V5: start, op and host write while busy are ignored; reset in the middle then a clean operation; back to back operations with other keys.
17178495.00ns INFO     cocotb.regression                  test_mlkem_core.test_protocol_corner_cases passed
17178495.00ns INFO     cocotb.regression                  running test_mlkem_core.test_constant_cycles (6/6)
V6: Decaps cycles identical for valid and rejected ciphertexts and for different secret keys with the same ek; Encaps identical for different m with the same ek; KeyGen spread reported.
23153110.00ns INFO     cocotb.mlkem_core                  constant cycles: Encaps [10235], Decaps [15591]; KeyGen over the ACVP seeds: min 8387, max 8428
23153110.00ns INFO     cocotb.regression                  test_mlkem_core.test_constant_cycles passed
** test_mlkem_core.test_constant_cycles                PASS     5974615.00         992.31       6020.91  **
2000175.00ns WARNING  cocotb.regression                  test_mlkem_core.test_acvp_keygen failed
2105740.00ns WARNING  cocotb.regression                  test_mlkem_core.test_acvp_encaps failed
2266555.00ns WARNING  cocotb.regression                  test_mlkem_core.test_acvp_decaps failed
V4: random KeyGen, Encaps, Decaps (valid and one-bit-changed ciphertexts) against the unmodified golden, and the chain KeyGen -> Encaps -> Decaps through the RTL.
4266730.00ns WARNING  cocotb.regression                  test_mlkem_core.test_random_cross_check_and_chain failed
V5: start, op and host write while busy are ignored; reset in the middle then a clean operation; back to back operations with other keys.
4372295.00ns WARNING  cocotb.regression                  test_mlkem_core.test_protocol_corner_cases failed
4372295.00ns INFO     cocotb.regression                  running test_mlkem_core.test_constant_cycles (6/6)
V6: Decaps cycles identical for valid and rejected ciphertexts and for different secret keys with the same ek; Encaps identical for different m with the same ek; KeyGen spread reported.
4477680.00ns WARNING  cocotb.regression                  test_mlkem_core.test_constant_cycles failed
File "<repo>/tb/mlkem/test_mlkem_core.py", line 166, in test_constant_cycles
** test_mlkem_core.test_constant_cycles                FAIL      105385.00          21.08       4998.23  **
[icarus] core: 6/6 PASS
[icarus] nclen: test_acvp_encaps failed as required: True; failed=['test_acvp_keygen', 'test_acvp_encaps', 'test_acvp_decaps', 'test_random_cross_check_and_chain', 'test_protocol_corner_cases', 'test_constant_cycles']
[icarus] TOTAL: 7/7 passed
```
