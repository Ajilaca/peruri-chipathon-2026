# Phase 9F S1b simulator runs, 2026-10-04 (V3, V5, V6)

MEASURED (simulation only). Commands (environment `CORE_TOP=mlkem_core3 CORE_SMP0=1 CORE_K0=1 CORE_W2=1`): `tb/mlkem/run_core_tests.py verilator core nclen ncoff ncrom`; `... icarus core nclen`; `... verilator ncprio ncwr ncjob ncthr ncthrnj`. `ncthr` must PASS (a throttled sidecar, one read per 32 cycles, so that the job outlasts the main work: the join waits); every other control must fail the named test. Only result lines are kept; the repository path prefix is shortened to <repo>.

## Verilator, core and controls
```
2166885.00ns INFO     cocotb.mlkem_core3                 ACVP keyGen: 25 vectors equal
4789110.00ns INFO     cocotb.mlkem_core3                 ACVP encapsulation: 25 vectors equal
6388905.00ns INFO     cocotb.mlkem_core3                 ACVP decapsulation: 10 vectors equal
16616280.00ns INFO     cocotb.mlkem_core3                 20 random cases equal (keygen, encaps, decaps valid and modified, chain)
23057740.00ns INFO     cocotb.mlkem_core3                 constant cycles: Encaps [10180], Decaps [15541]; KeyGen over the ACVP seeds: min 8332, max 8385
173515.00ns INFO     cocotb.mlkem_core3                 ACVP keyGen: 2 vectors equal
383460.00ns INFO     cocotb.mlkem_core3                 ACVP encapsulation: 2 vectors equal
173515.00ns INFO     cocotb.mlkem_core3                 ACVP keyGen: 2 vectors equal
[verilator] core: 6/6 PASS
[verilator] nclen: test_acvp_encaps failed as required: True; failed=['test_acvp_keygen', 'test_acvp_encaps', 'test_acvp_decaps', 'test_random_cross_check_and_chain', 'test_protocol_corner_cases', 'test_constant_cycles']
[verilator] ncoff: test_acvp_decaps failed as required: True; failed=['test_acvp_decaps', 'test_random_cross_check_and_chain', 'test_constant_cycles']
[verilator] ncrom: test_acvp_encaps failed as required: True; failed=['test_acvp_encaps', 'test_acvp_decaps', 'test_random_cross_check_and_chain', 'test_protocol_corner_cases', 'test_constant_cycles']
[verilator] TOTAL: 9/9 passed
```

## Icarus, core and control nclen
```
2166885.00ns INFO     cocotb.mlkem_core3                 ACVP keyGen: 25 vectors equal
4789110.00ns INFO     cocotb.mlkem_core3                 ACVP encapsulation: 25 vectors equal
6388905.00ns INFO     cocotb.mlkem_core3                 ACVP decapsulation: 10 vectors equal
16616280.00ns INFO     cocotb.mlkem_core3                 20 random cases equal (keygen, encaps, decaps valid and modified, chain)
23057740.00ns INFO     cocotb.mlkem_core3                 constant cycles: Encaps [10180], Decaps [15541]; KeyGen over the ACVP seeds: min 8332, max 8385
[icarus] core: 6/6 PASS
[icarus] nclen: test_acvp_encaps failed as required: True; failed=['test_acvp_keygen', 'test_acvp_encaps', 'test_acvp_decaps', 'test_random_cross_check_and_chain', 'test_protocol_corner_cases', 'test_constant_cycles']
[icarus] TOTAL: 7/7 passed
```

## Verilator, S1b controls (the first run of NC-PRIO expected test_acvp_keygen, which does not read while the job runs; the expected test was corrected to test_acvp_encaps and NC-PRIO rerun below)
```
173515.00ns INFO     cocotb.mlkem_core3                 ACVP keyGen: 2 vectors equal
296700.00ns INFO     cocotb.mlkem_core3                 ACVP encapsulation: 2 vectors equal
776965.00ns INFO     cocotb.mlkem_core3                 ACVP decapsulation: 3 vectors equal
3583560.00ns INFO     cocotb.mlkem_core3                 constant cycles: Encaps [10180], Decaps [15541]; KeyGen over the ACVP seeds: min 8356, max 8356
672045.00ns INFO     cocotb.mlkem_core3                 ACVP decapsulation: 3 vectors equal
252835.00ns INFO     cocotb.mlkem_core3                 ACVP keyGen: 2 vectors equal
537660.00ns INFO     cocotb.mlkem_core3                 ACVP encapsulation: 2 vectors equal
1017925.00ns INFO     cocotb.mlkem_core3                 ACVP decapsulation: 3 vectors equal
2193840.00ns INFO     cocotb.mlkem_core3                 2 random cases equal (keygen, encaps, decaps valid and modified, chain)
5140780.00ns INFO     cocotb.mlkem_core3                 constant cycles: Encaps [13924], Decaps [15541]; KeyGen over the ACVP seeds: min 12309, max 12341
2568635.00ns INFO     cocotb.mlkem_core3                 ACVP decapsulation: 3 vectors equal
[verilator] ncprio: test_acvp_keygen failed as required: False; failed=['test_acvp_encaps', 'test_acvp_decaps', 'test_random_cross_check_and_chain', 'test_protocol_corner_cases', 'test_constant_cycles']  NEGATIVE CONTROL VOID
[verilator] ncwr: test_acvp_keygen failed as required: True; failed=['test_acvp_keygen', 'test_random_cross_check_and_chain']
[verilator] ncjob: test_acvp_encaps failed as required: True; failed=['test_acvp_keygen', 'test_acvp_encaps', 'test_random_cross_check_and_chain', 'test_protocol_corner_cases', 'test_constant_cycles']
[verilator] ncthr: throttled sidecar passes the whole core target: True; failed=[]
[verilator] ncthrnj: test_acvp_encaps failed as required: True; failed=['test_acvp_keygen', 'test_acvp_encaps', 'test_random_cross_check_and_chain', 'test_protocol_corner_cases', 'test_constant_cycles']
[verilator] TOTAL: 4/5 passed
```

## Verilator, NC-PRIO rerun with the expected test test_acvp_encaps
```
173515.00ns INFO     cocotb.mlkem_core3                 ACVP keyGen: 2 vectors equal
[verilator] ncprio: test_acvp_encaps failed as required: True; failed=['test_acvp_encaps', 'test_acvp_decaps', 'test_random_cross_check_and_chain', 'test_protocol_corner_cases', 'test_constant_cycles']
[verilator] TOTAL: 1/1 passed
```
