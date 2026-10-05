<!-- claim-lint: skip-file (internal evidence record, not proposal text) -->
# Phase 7 verification run (test plan V1-V7, V9), 2026-10-03

Command: `. scripts/env.sh && scripts/test/phase7_verify.sh` (KK_SEEDS = 20). Environment: Ubuntu 24.04, OSS CAD Suite (Verilator 5.053, Icarus, slang, SymbiYosys), cocotb 2.1.0.
Label: MEASURED (simulation and lint output of this run; not hardware). Output of the script (filtered by the script itself):

```
## V1 verilator --lint-only -Wall keccak_f1600
rc=0
## V1 verilator --lint-only -Wall keccak_sponge
rc=0
## V1 slang keccak_sponge
Build succeeded: 0 errors, 0 warnings
rc=0
## V2 pytest tb/golden/tests/test_keccak.py (golden vs hashlib)
16 passed in 14.80s
rc=0
## V3 gen_keccak_consts.py --check
rtl/keccak/keccak_pkg.sv: 0 differences; rc 24 entries, rho 25 entries
rc=0
## V4-V7 verilator
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
rc=0
## V4-V7 icarus
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
rc=0
## V9 check_params
check_params: all locked parameters match.
rc=0
OVERALL: PASS
```

Reading:
- V1 lint: Verilator `-Wall` and slang clean for `keccak_f1600` and `keccak_sponge` (0 warnings, 0 errors).
- V2: golden `tb/golden/keccak.py` equals hashlib (16 pytest cases: every length 0..3 rate + 1 per mode, ML-KEM lengths, random lengths up to 2,000 bytes, SHAKE output lengths, per-round trace, 1,600 single-bit states
  all distinct after the permutation, round constants and rho offsets against the FIPS 202 values).
- V3: `rtl/keccak/keccak_pkg.sv` regenerated from the golden model, 0 differences.
- V4 (`perm`): zero state, all-ones state, 1,600 single-bit states, 200 random states and a chain of 10: the state after every round equals the golden trace; `busy_o` is high for exactly 24 cycles and `done_o` pulses once
  for every state; lane read port, xor to lane >= 25 ignored, xor and run while busy ignored, clear in the middle of a permutation.
- V5 (`sponge`): all four modes bit-exact against hashlib and the golden sponge for the boundary lengths of the test plan, ML-KEM lengths, 20 random lengths per mode and all output sizes of the plan; permutation
  counter equal to the golden count; random back-pressure on both interfaces; garbage in the ignored bytes of the last word; stop in absorb, in a permutation and in a squeeze (including between two squeeze blocks);
  start while busy ignored; reset in the middle of a message.
- V6: 306 (mode, length, output words) points, each with three messages (random, all-0x00, all-0xFF) and identical cycle counts; every point equals the FSM formula (`cycles_k0.json`, `cycles_k0_table.md`).
- V7: negative controls fail as required on both simulators: NC-RC (one bit of round constant 1), NC-R (23 rounds, also fails the 24-cycle check), NC-PAD (SHA3 domain byte 0x1F).
- V9: `check_params.py`: all locked parameters match. No existing RTL or test file was modified in Phase 7 (new files only), so the regression of Phases 0-6 is not required (Phase 5M Amendment A1).
