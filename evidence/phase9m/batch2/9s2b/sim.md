# Phase 9F S2b simulator runs, 2026-10-05 (V1-V3, V5-V7; the runs were made on 2026-10-04 and 2026-10-05)

MEASURED (simulation only). Commands: V2 and V3 `tb/s10/run_s10_tests.py <sim> s10p6a ncar`; V5 `KP_VAR=2 KP_CORE_R2=0 KP_NTT_P6=1 KP_NTT_AR=1 tb/smp/run_smp_tests.py <sim> top nchaz`; V6 environment `CORE_TOP=mlkem_core3 CORE_SMP0=1 CORE_K0=1 CORE_W2=1 CORE_P6=1 CORE_AR=1`: `tb/mlkem/run_core_tests.py <sim> core` (Verilator also `nclen ncoff ncrom`, Icarus also `nclen`); V7 defaults without the environment: `tb/s10/run_s10_tests.py verilator` and `tb/mlkem/run_core_tests.py verilator core`. Raw cycle files: `cycles_*_k3.json` in this directory.

## V2-V3 NTT core at P = 6 with the registered issue address
```
[verilator] s10p6a: 6/6 PASS  {'P': 6, 'RDLAT': 2, 'WRDLY': 4, 'cycles_NTT': 119, 'cycles_INTT': 119, 'stall_NTT': 0, 'stall_INTT': 0}
[verilator] ncar: bit-exact NTT and INTT failed as required: True; failed=['test_ntt_bit_exact', 'test_intt_bit_exact', 'test_ntt_intt_roundtrip', 'test_boundary_directed', 'test_cycle_count_constant', 'test_intt_unit_vectors']
[verilator] TOTAL: 7/7 passed
[icarus] s10p6a: 6/6 PASS  {'P': 6, 'RDLAT': 2, 'WRDLY': 4, 'cycles_NTT': 119, 'cycles_INTT': 119, 'stall_NTT': 0, 'stall_INTT': 0}
[icarus] ncar: bit-exact NTT and INTT failed as required: True; failed=['test_ntt_bit_exact', 'test_intt_bit_exact', 'test_ntt_intt_roundtrip', 'test_boundary_directed', 'test_cycle_count_constant', 'test_intt_unit_vectors']
```
Run note: the Icarus chain of 2026-10-05 (`s10p6a ncar`) ended after `s10p6a` without the control (the process was gone, no total line); the control was run again alone the same morning (the `ncar` line above). The control (the registered address taken from the values of the current cycle, one cycle late) fails on both simulators as required.

## V5 sequencer tests, `NTT_P6 = 1`, `NTT_AR = 1`, K0 sampler
```
[verilator] top (VAR=2): 3/3 PASS
[verilator] nchaz: test_programs_bit_exact failed as required: True; failed=['test_programs_bit_exact', 'test_constant_cycles_fixed_rho']
[verilator] TOTAL: 4/4 passed
[icarus] top (VAR=2): 3/3 PASS
[icarus] nchaz: test_programs_bit_exact failed as required: True; failed=['test_programs_bit_exact', 'test_constant_cycles_fixed_rho']
[icarus] TOTAL: 4/4 passed
```

## V6 core `mlkem_core3` at K3 (`NTT_P6 = 1`, `NTT_AR = 1`)
Verilator (the Icarus run printed the same values):
```
ACVP keyGen: 25 vectors equal
ACVP encapsulation: 25 vectors equal
ACVP decapsulation: 10 vectors equal
20 random cases equal (keygen, encaps, decaps valid and modified, chain)
constant cycles: Encaps [10194], Decaps [15563]; KeyGen over the ACVP seeds: min 8344, max 8397
[verilator] core: 6/6 PASS
[verilator] nclen: failed as required: True   (test_acvp_encaps and the others fail)
[verilator] ncoff: failed as required: True
[verilator] ncrom: failed as required: True
[verilator] TOTAL: 9/9 passed
[icarus] core: 6/6 PASS
[icarus] nclen: test_acvp_encaps failed as required: True
[icarus] TOTAL: 7/7 passed
```
The cycle counts of the test inputs are **identical to K2** (Encaps 10,194, Decaps 15,563, KeyGen 8,344-8,397): the registered address changes no cycle. The profile inputs (`profile_k3_verilator.json`) give 8,416 / 10,250 / 15,619, as K2.

## V7 regression at the defaults (Verilator)
```
[verilator] mem (RD_LAT=2, WR_DELAY=3): 4/4 PASS
[verilator] s10: 6/6 PASS  {'P': 5, 'RDLAT': 2, 'WRDLY': 3, 'cycles_NTT': 118, 'cycles_INTT': 118, 'stall_NTT': 0, 'stall_INTT': 0}
[verilator] ncm / ncw: bit-exact NTT and INTT failed as required: True
[verilator] p6 (Phase 6 top with S10): 1/1 PASS  {'keygen': 5475, 'encrypt': 6789, 'decrypt': 3109}
[verilator] TOTAL: 13/13 passed
[verilator] core (mlkem_core defaults): 6/6 PASS   constant cycles: Encaps [10691], Decaps [16623]; KeyGen 9,035-9,076
```
The defaults (`AREG = 0`, `NTT_AR = 0`) keep the 118-cycle core and the Phase 9 core; the K1b and K2 profiles are unchanged (`../9s2/`).

## What this does not show
Simulation only; the equivalence argument (registered address = combinational address in every cycle of a run) is tested by bit-exact results and by cycle equality with K2, and by the memory-facing formal properties (`formal.md`); it is not proven for every input sequence.
