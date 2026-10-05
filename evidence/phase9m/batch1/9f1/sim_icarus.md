# Phase 9F S1 simulator run, Icarus (V2, V3, V5), 2026-10-04

MEASURED (simulation only). Same commands as `sim_verilator.md` with the simulator `icarus`: (a) `CORE_TOP=mlkem_core2 CORE_SMP0=1 CORE_K0=1 CORE_W2=1 tb/mlkem/run_core_tests.py icarus core nclen`; (b) `KP_VAR=2 KP_CORE_R2=0 tb/smp/run_smp_tests.py icarus top`. Only result lines are kept.

## (a) core
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
[icarus] core: 6/6 PASS
[icarus] nclen: test_acvp_encaps failed as required: True; failed=['test_acvp_keygen', 'test_acvp_encaps', 'test_acvp_decaps', 'test_random_cross_check_and_chain', 'test_protocol_corner_cases', 'test_constant_cycles']
[icarus] TOTAL: 7/7 passed
```

## (b) sequencer with the K0 sampler
```
                                                        ** test_kpke_smp.test_programs_bit_exact          PASS     1928135.00         329.95       5843.79  **
                                                        ** test_kpke_smp.test_constant_cycles_fixed_rho   PASS     1646445.00         369.93       4450.74  **
                                                        ** test_kpke_smp.test_stall_coverage              PASS           0.00           0.00          0.00  **
                                                        ** TESTS=3 PASS=3 FAIL=0 SKIP=0                            3574580.00         699.88       5107.43  **
[icarus] top (VAR=2): 3/3 PASS
[icarus] TOTAL: 3/3 passed
```
