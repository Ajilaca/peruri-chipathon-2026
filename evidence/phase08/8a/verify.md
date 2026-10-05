<!-- claim-lint: skip-file (internal evidence record, not proposal text) -->
# Phase 8a verification run (test plan V1, V4-V7, V9), 2026-10-03

Command: `. scripts/env.sh && scripts/test/phase8a_verify.sh` (KK_SEEDS = 20). It first reruns the K0 verification (`scripts/test/phase7_verify.sh`, V9 regression: the K0 test files now take environment parameters whose defaults reproduce
K0), then lints and tests `keccak_f1600_r2` and `keccak_sponge_r2` (two rounds per cycle) with `KK_RPC=2`. Environment: Ubuntu 24.04, OSS CAD Suite (Verilator 5.053, Icarus 14.0, slang, SymbiYosys), cocotb 2.1.0.
Label: MEASURED (simulation and lint output of this run; not hardware). Filtered output of the script:

```
## V9 regression: scripts/test/phase7_verify.sh (K0)
Build succeeded: 0 errors, 0 warnings
16 passed in 12.94s
rtl/keccak/keccak_pkg.sv: 0 differences; rc 24 entries, rho 25 entries
846235.00ns INFO     cocotb.regression                  test_keccak_f1600.test_permutation_every_round_and_24_cycles passed
847940.00ns INFO     cocotb.regression                  test_keccak_f1600.test_ports passed
1274895.00ns INFO     cocotb.regression                  test_keccak_sponge.test_modes_bit_exact passed
1317220.00ns INFO     cocotb.regression                  test_keccak_sponge.test_backpressure passed
1338415.00ns INFO     cocotb.regression                  test_keccak_sponge.test_stop_start_reset passed
2656430.00ns INFO     cocotb.regression                  test_keccak_sponge.test_constant_cycles passed
[verilator] perm: 2/2 PASS
[verilator] sponge: 4/4 PASS  cycle points: 306
[verilator] ncrc: permutation test failed as required: True; failed=['test_permutation_every_round_and_24_cycles', 'test_ports']
[verilator] ncr: permutation test failed as required: True; failed=['test_permutation_every_round_and_24_cycles', 'test_ports']
[verilator] ncpad: bit-exact test failed as required: True; failed=['test_modes_bit_exact', 'test_backpressure', 'test_stop_start_reset', 'test_constant_cycles']
[verilator] TOTAL: 9/9 passed
846235.00ns INFO     cocotb.regression                  test_keccak_f1600.test_permutation_every_round_and_24_cycles passed
847940.00ns INFO     cocotb.regression                  test_keccak_f1600.test_ports passed
1274895.00ns INFO     cocotb.regression                  test_keccak_sponge.test_modes_bit_exact passed
1317220.00ns INFO     cocotb.regression                  test_keccak_sponge.test_backpressure passed
1338415.00ns INFO     cocotb.regression                  test_keccak_sponge.test_stop_start_reset passed
2656430.00ns INFO     cocotb.regression                  test_keccak_sponge.test_constant_cycles passed
[icarus] perm: 2/2 PASS
[icarus] sponge: 4/4 PASS  cycle points: 306
[icarus] ncrc: permutation test failed as required: True; failed=['test_permutation_every_round_and_24_cycles', 'test_ports']
[icarus] ncr: permutation test failed as required: True; failed=['test_permutation_every_round_and_24_cycles', 'test_ports']
[icarus] ncpad: bit-exact test failed as required: True; failed=['test_modes_bit_exact', 'test_backpressure', 'test_stop_start_reset', 'test_constant_cycles']
[icarus] TOTAL: 9/9 passed
check_params: all locked parameters match.
OVERALL: PASS
rc=0
## V1 verilator --lint-only -Wall keccak_f1600_r2
rc=0
## V1 verilator --lint-only -Wall keccak_sponge_r2
rc=0
## V1 slang keccak_sponge_r2
Build succeeded: 0 errors, 0 warnings
rc=0
## V4-V7 verilator (C5, two rounds per cycle)
650395.00ns INFO     cocotb.regression                  test_keccak_f1600.test_permutation_every_round_and_24_cycles passed
651860.00ns INFO     cocotb.regression                  test_keccak_f1600.test_ports passed
886915.00ns INFO     cocotb.regression                  test_keccak_sponge.test_modes_bit_exact passed
918030.00ns INFO     cocotb.regression                  test_keccak_sponge.test_backpressure passed
933105.00ns INFO     cocotb.regression                  test_keccak_sponge.test_stop_start_reset passed
1893280.00ns INFO     cocotb.regression                  test_keccak_sponge.test_constant_cycles passed
[verilator] perm: 2/2 PASS
[verilator] sponge: 4/4 PASS  cycle points: 306
[verilator] ncrc: permutation test failed as required: True; failed=['test_permutation_every_round_and_24_cycles', 'test_ports']
[verilator] ncr: permutation test failed as required: True; failed=['test_permutation_every_round_and_24_cycles', 'test_ports']
[verilator] ncpad: bit-exact test failed as required: True; failed=['test_modes_bit_exact', 'test_backpressure', 'test_stop_start_reset', 'test_constant_cycles']
[verilator] TOTAL: 9/9 passed
rc=0
## V4-V7 icarus (C5, two rounds per cycle)
650395.00ns INFO     cocotb.regression                  test_keccak_f1600.test_permutation_every_round_and_24_cycles passed
651860.00ns INFO     cocotb.regression                  test_keccak_f1600.test_ports passed
886915.00ns INFO     cocotb.regression                  test_keccak_sponge.test_modes_bit_exact passed
918030.00ns INFO     cocotb.regression                  test_keccak_sponge.test_backpressure passed
933105.00ns INFO     cocotb.regression                  test_keccak_sponge.test_stop_start_reset passed
1893280.00ns INFO     cocotb.regression                  test_keccak_sponge.test_constant_cycles passed
[icarus] perm: 2/2 PASS
[icarus] sponge: 4/4 PASS  cycle points: 306
[icarus] ncrc: permutation test failed as required: True; failed=['test_permutation_every_round_and_24_cycles', 'test_ports']
[icarus] ncr: permutation test failed as required: True; failed=['test_permutation_every_round_and_24_cycles', 'test_ports']
[icarus] ncpad: bit-exact test failed as required: True; failed=['test_modes_bit_exact', 'test_backpressure', 'test_stop_start_reset', 'test_constant_cycles']
[icarus] TOTAL: 9/9 passed
rc=0
OVERALL: PASS
```

Reading:
- V9 regression: the K0 verification (lint, golden vs hashlib 16 pytest, constants 0 differences, K0 permutation and sponge on both simulators with the three negative controls, `check_params`) is **OVERALL: PASS** again after the test-file change.
- V1: Verilator `-Wall` and slang clean for `keccak_f1600_r2` and `keccak_sponge_r2` (0 warnings, 0 errors).
- V4 (`perm`, C5): zero, all-ones, 1,600 single-bit, 200 random states and a chain of 10: the state after every cycle equals the golden trace after rounds 1, 3, ..., 23, the first-round output `mid` equals the golden trace
  after rounds 0, 2, ..., 22 (so all 24 rounds are compared), `busy_o` is high for exactly 12 cycles, `done_o` pulses once; port tests (read, lane >= 25, xor and run while busy, clear mid-permutation).
- V5 and V6 (`sponge`, C5): all four modes bit-exact against hashlib and the golden sponge; permutation counts equal the golden counts; back-pressure, stop, start while busy, reset; 306 (mode, length, output) points with identical cycle
  counts for three messages each, every point equal to the formula with p = 14 (`cycles_c5.json`). Identical on Verilator and Icarus.
- V7: NC-RC (one bit of round constant 1, used by the second round of cycle 0), NC-R (11 cycles) and NC-PAD fail as required on both simulators.
