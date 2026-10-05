<!-- claim-lint: skip-file (internal evidence record, not proposal text) -->
# Phase 8b stage W2 verification run (test plan V1-V10), 2026-10-03

Command: `. scripts/env.sh && KS_OUTW=2 scripts/test/phase8b_verify.sh` (KS_OUTW = 2, KS_N = 500). Same structure as the W1 run; additionally the whole W1 test set is rerun against the current RTL (V10, `OUTW` = 1) on both simulators, and the formal runner runs the W1 and W2 rows.
Environment: Ubuntu 24.04, OSS CAD Suite (Verilator 5.053, Icarus 14.0, slang, SymbiYosys), cocotb 2.1.0, git HEAD 794db0d plus the working-tree files of this stage (committed afterwards).
Label: MEASURED (simulation, lint and formal output of this run; not hardware). An earlier run of the same script was discarded because the simulator processes of one test step were killed by a command of the operator session (0/8 in that step); the same step passed when rerun alone and the whole script was then rerun from the start; this file is that clean run.
The cycle tables of Verilator and Icarus are byte-identical (checked with cmp). Filtered output of the script:

```
KS_OUTW=2 KS_N=500
## V10 regression: scripts/test/phase8a_verify.sh (K0 and C5)
Build succeeded: 0 errors, 0 warnings
16 passed in 65.82s (0:01:05)
rtl/keccak/keccak_pkg.sv: 0 differences; rc 24 entries, rho 25 entries
846235.00ns INFO     cocotb.regression                  test_keccak_f1600.test_permutation_every_round_and_24_cycles passed
847940.00ns INFO     cocotb.regression                  test_keccak_f1600.test_ports passed
1274895.00ns INFO     cocotb.regression                  test_keccak_sponge.test_modes_bit_exact passed
1317220.00ns INFO     cocotb.regression                  test_keccak_sponge.test_backpressure passed
1338415.00ns INFO     cocotb.regression                  test_keccak_sponge.test_stop_start_reset passed
2656430.00ns INFO     cocotb.regression                  test_keccak_sponge.test_constant_cycles passed
   545.00ns WARNING  cocotb.regression                  test_keccak_f1600.test_permutation_every_round_and_24_cycles failed
  1380.00ns WARNING  cocotb.regression                  test_keccak_f1600.test_ports failed
   535.00ns WARNING  cocotb.regression                  test_keccak_f1600.test_permutation_every_round_and_24_cycles failed
  1360.00ns WARNING  cocotb.regression                  test_keccak_f1600.test_ports failed
   375.00ns WARNING  cocotb.regression                  test_keccak_sponge.test_modes_bit_exact failed
   770.00ns WARNING  cocotb.regression                  test_keccak_sponge.test_backpressure failed
  2825.00ns WARNING  cocotb.regression                  test_keccak_sponge.test_stop_start_reset failed
  3200.00ns WARNING  cocotb.regression                  test_keccak_sponge.test_constant_cycles failed
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
   545.00ns WARNING  cocotb.regression                  test_keccak_f1600.test_permutation_every_round_and_24_cycles failed
  1380.00ns WARNING  cocotb.regression                  test_keccak_f1600.test_ports failed
   535.00ns WARNING  cocotb.regression                  test_keccak_f1600.test_permutation_every_round_and_24_cycles failed
  1360.00ns WARNING  cocotb.regression                  test_keccak_f1600.test_ports failed
   375.00ns WARNING  cocotb.regression                  test_keccak_sponge.test_modes_bit_exact failed
   770.00ns WARNING  cocotb.regression                  test_keccak_sponge.test_backpressure failed
  2825.00ns WARNING  cocotb.regression                  test_keccak_sponge.test_stop_start_reset failed
  3200.00ns WARNING  cocotb.regression                  test_keccak_sponge.test_constant_cycles failed
[icarus] perm: 2/2 PASS
[icarus] sponge: 4/4 PASS  cycle points: 306
[icarus] ncrc: permutation test failed as required: True; failed=['test_permutation_every_round_and_24_cycles', 'test_ports']
[icarus] ncr: permutation test failed as required: True; failed=['test_permutation_every_round_and_24_cycles', 'test_ports']
[icarus] ncpad: bit-exact test failed as required: True; failed=['test_modes_bit_exact', 'test_backpressure', 'test_stop_start_reset', 'test_constant_cycles']
[icarus] TOTAL: 9/9 passed
check_params: all locked parameters match.
OVERALL: PASS
Build succeeded: 0 errors, 0 warnings
650395.00ns INFO     cocotb.regression                  test_keccak_f1600.test_permutation_every_round_and_24_cycles passed
651860.00ns INFO     cocotb.regression                  test_keccak_f1600.test_ports passed
886915.00ns INFO     cocotb.regression                  test_keccak_sponge.test_modes_bit_exact passed
918030.00ns INFO     cocotb.regression                  test_keccak_sponge.test_backpressure passed
933105.00ns INFO     cocotb.regression                  test_keccak_sponge.test_stop_start_reset passed
1893280.00ns INFO     cocotb.regression                  test_keccak_sponge.test_constant_cycles passed
   425.00ns WARNING  cocotb.regression                  test_keccak_f1600.test_permutation_every_round_and_24_cycles failed
  1140.00ns WARNING  cocotb.regression                  test_keccak_f1600.test_ports failed
   415.00ns WARNING  cocotb.regression                  test_keccak_f1600.test_permutation_every_round_and_24_cycles failed
  1120.00ns WARNING  cocotb.regression                  test_keccak_f1600.test_ports failed
   255.00ns WARNING  cocotb.regression                  test_keccak_sponge.test_modes_bit_exact failed
   510.00ns WARNING  cocotb.regression                  test_keccak_sponge.test_backpressure failed
  1965.00ns WARNING  cocotb.regression                  test_keccak_sponge.test_stop_start_reset failed
  2220.00ns WARNING  cocotb.regression                  test_keccak_sponge.test_constant_cycles failed
[verilator] perm: 2/2 PASS
[verilator] sponge: 4/4 PASS  cycle points: 306
[verilator] ncrc: permutation test failed as required: True; failed=['test_permutation_every_round_and_24_cycles', 'test_ports']
[verilator] ncr: permutation test failed as required: True; failed=['test_permutation_every_round_and_24_cycles', 'test_ports']
[verilator] ncpad: bit-exact test failed as required: True; failed=['test_modes_bit_exact', 'test_backpressure', 'test_stop_start_reset', 'test_constant_cycles']
[verilator] TOTAL: 9/9 passed
650395.00ns INFO     cocotb.regression                  test_keccak_f1600.test_permutation_every_round_and_24_cycles passed
651860.00ns INFO     cocotb.regression                  test_keccak_f1600.test_ports passed
886915.00ns INFO     cocotb.regression                  test_keccak_sponge.test_modes_bit_exact passed
918030.00ns INFO     cocotb.regression                  test_keccak_sponge.test_backpressure passed
933105.00ns INFO     cocotb.regression                  test_keccak_sponge.test_stop_start_reset passed
1893280.00ns INFO     cocotb.regression                  test_keccak_sponge.test_constant_cycles passed
   425.00ns WARNING  cocotb.regression                  test_keccak_f1600.test_permutation_every_round_and_24_cycles failed
  1140.00ns WARNING  cocotb.regression                  test_keccak_f1600.test_ports failed
   415.00ns WARNING  cocotb.regression                  test_keccak_f1600.test_permutation_every_round_and_24_cycles failed
  1120.00ns WARNING  cocotb.regression                  test_keccak_f1600.test_ports failed
   255.00ns WARNING  cocotb.regression                  test_keccak_sponge.test_modes_bit_exact failed
   510.00ns WARNING  cocotb.regression                  test_keccak_sponge.test_backpressure failed
  1965.00ns WARNING  cocotb.regression                  test_keccak_sponge.test_stop_start_reset failed
  2220.00ns WARNING  cocotb.regression                  test_keccak_sponge.test_constant_cycles failed
[icarus] perm: 2/2 PASS
[icarus] sponge: 4/4 PASS  cycle points: 306
[icarus] ncrc: permutation test failed as required: True; failed=['test_permutation_every_round_and_24_cycles', 'test_ports']
[icarus] ncr: permutation test failed as required: True; failed=['test_permutation_every_round_and_24_cycles', 'test_ports']
[icarus] ncpad: bit-exact test failed as required: True; failed=['test_modes_bit_exact', 'test_backpressure', 'test_stop_start_reset', 'test_constant_cycles']
[icarus] TOTAL: 9/9 passed
OVERALL: PASS
rc=0
## V10 regression: formal/run/run_formal_phase7.py
| Group | Proof | Expected | Result | Engine detail | Time (s) | As expected |
| A Phase 7 | keccak_sponge + keccak_f1600 (K1, K2, K3, K4, K5) | PASS | PASS | basecase=pass, induction=pass | 31.8 | yes |
| B Negative control | NC-K1: 23 rounds per permutation (K1 busy length) | FAIL | FAIL | basecase=FAIL; failed assert keccak_sponge_formal_top.sv:105 | 64.1 | yes |
| B Negative control | NC-K4: output data depends on out_ready_i (K4 hold; BMC depth 40: the squeeze phase is reached after about 30 cycles) | FAIL | FAIL | bmc=FAIL; failed assert keccak_sponge_formal_top.sv:122 | 59.4 | yes |
ALL AS EXPECTED
rc=0
## V10 regression: formal/run/run_formal_phase8a.py
| Group | Proof | Expected | Result | Engine detail | Time (s) | As expected |
| A Phase 8a | keccak_sponge_r2 + keccak_f1600_r2 (K1, K2, K3, K4, K5) | PASS | PASS | basecase=pass, induction=pass | 98.0 | yes |
| B Negative control | NC-K1: 11 cycles per permutation (K1 busy length) | FAIL | FAIL | basecase=FAIL; failed assert keccak_sponge_r2_formal_top.sv:105 | 41.9 | yes |
| B Negative control | NC-K4: output data depends on out_ready_i (K4 hold; BMC depth 40: the squeeze phase is reached after about 30 cycles) | FAIL | FAIL | bmc=FAIL; failed assert keccak_sponge_r2_formal_top.sv:122 | 40.0 | yes |
ALL AS EXPECTED
rc=0
## V1 verilator --lint-only -Wall sample_ntt_core (OUTW = 2)
rc=0
## V1 verilator --lint-only -Wall cbd2_core (OUTW = 2)
rc=0
## V1 verilator --lint-only -Wall keccak_sampler (CORE_R2 = 1, OUTW = 2)
rc=0
## V1 verilator --lint-only -Wall keccak_sampler (CORE_R2 = 0, OUTW = 2)
rc=0
## V1 slang keccak_sampler (OUTW = 2)
Build succeeded: 0 errors, 0 warnings
rc=0
## V2 golden sampler model against the unmodified golden primitives
6 passed in 0.47s
rc=0
## V3-V8 verilator (OUTW = 2)
604926.00ns INFO     cocotb.sample_ntt_core             196 crafted runs equal to the golden (coefficients and consumed bytes)
604926.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_crafted_streams passed
1850092.00ns INFO     cocotb.sample_ntt_core             500 XOF streams equal to the golden; blocks needed: [(3, 496), (4, 4)]
1850092.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_random_xof_streams passed
1865228.00ns INFO     cocotb.sample_ntt_core             6 polynomials that need a 4th XOF block equal to the golden
1865228.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_four_block_streams passed
1877674.00ns INFO     cocotb.sample_ntt_core             abort at 4 points and reset in the middle clear the window, triple and output registers; the core runs again
1877674.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_abort_reset_zeroisation passed
1882660.00ns INFO     cocotb.sample_ntt_core             start while busy ignored; back-to-back polynomials correct
1882660.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_start_while_busy_and_back_to_back passed
2064556.00ns INFO     cocotb.sample_ntt_core             all six pool combinations (carry, accepted) seen: [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
2064556.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_w2_pool_coverage passed
536146.00ns INFO     cocotb.cbd2_core                   133 special streams equal to the golden; the 16 nibble values give only [0, 1, 2, 3327, 3328]
536146.00ns INFO     cocotb.regression                  test_cbd2_core.test_nibble_table_and_special_streams passed
1568182.00ns INFO     cocotb.cbd2_core                   500 random streams equal to the golden; exactly 16 words taken each time
1568182.00ns INFO     cocotb.regression                  test_cbd2_core.test_random_streams passed
1626258.00ns INFO     cocotb.cbd2_core                   cycles per polynomial with a stream word available every cycle: 134, the same for 43 inputs
1626258.00ns INFO     cocotb.regression                  test_cbd2_core.test_cycles_independent_of_data passed
1637164.00ns INFO     cocotb.cbd2_core                   abort at 4 points and reset in the middle clear the word and output registers; the core runs again
1637164.00ns INFO     cocotb.regression                  test_cbd2_core.test_abort_reset_zeroisation passed
1380766.00ns INFO     cocotb.keccak_sampler              500 SampleNTT polynomials (rho || j || i) and 6 other message lengths equal to the golden fed with hashlib SHAKE128; perm_cnt_o minus blocks needed: [(0, 505), (1, 1)]
1380766.00ns INFO     cocotb.regression                  test_keccak_sampler.test_sample_ntt_bit_exact passed
1401952.00ns INFO     cocotb.keccak_sampler              6 polynomials that need a 4th XOF block (rho values from a fixed PRNG seed) equal to the golden; perm_cnt_o = 4
1401952.00ns INFO     cocotb.regression                  test_keccak_sampler.test_four_block_polynomials passed
2521568.00ns INFO     cocotb.keccak_sampler              500 CBD2 polynomials (sigma || N) equal to the golden fed with hashlib SHAKE256; exactly 16 sponge words taken each time
2521568.00ns INFO     cocotb.regression                  test_keccak_sampler.test_cbd_bit_exact passed
2557794.00ns INFO     cocotb.keccak_sampler              20 CBD polynomials: the sponge word handshake count is 16 up to 30 cycles after done_o
2557794.00ns INFO     cocotb.regression                  test_keccak_sampler.test_cbd_words_17th_not_taken passed
2562320.00ns INFO     cocotb.keccak_sampler              after done_o the sponge is idle (stop_i issued) and its permutation counter is stable, SampleNTT and CBD
2562320.00ns INFO     cocotb.regression                  test_keccak_sampler.test_stop_wipes_sponge passed
3851406.00ns INFO     cocotb.keccak_sampler              CBD cycles identical at 102 points: 152; SampleNTT repeatable (40 repeats); r = cycles - base per blocks: B=3: [49], B=4: [61]
3851406.00ns INFO     cocotb.regression                  test_keccak_sampler.test_constant_cycles_and_cycle_table passed
3882422.01ns INFO     cocotb.keccak_sampler              abort at 5 points per kind and reset in the middle: busy low, window/word/output registers zero, sponge idle, the next polynomial correct
3882422.01ns INFO     cocotb.regression                  test_keccak_sampler.test_abort_reset_zeroisation passed
3884508.01ns INFO     cocotb.keccak_sampler              start requests while busy (both kinds) are ignored; the polynomial is unchanged
3884508.01ns INFO     cocotb.regression                  test_keccak_sampler.test_start_while_busy passed
1578356.00ns INFO     cocotb.keccak_sampler              500 SampleNTT polynomials (rho || j || i) and 6 other message lengths equal to the golden fed with hashlib SHAKE128; perm_cnt_o minus blocks needed: [(0, 506)]
1578356.00ns INFO     cocotb.regression                  test_keccak_sampler.test_sample_ntt_bit_exact passed
1602142.00ns INFO     cocotb.keccak_sampler              6 polynomials that need a 4th XOF block (rho values from a fixed PRNG seed) equal to the golden; perm_cnt_o = 4
1602142.00ns INFO     cocotb.regression                  test_keccak_sampler.test_four_block_polynomials passed
2777498.00ns INFO     cocotb.keccak_sampler              500 CBD2 polynomials (sigma || N) equal to the golden fed with hashlib SHAKE256; exactly 16 sponge words taken each time
2777498.00ns INFO     cocotb.regression                  test_keccak_sampler.test_cbd_bit_exact passed
2816124.00ns INFO     cocotb.keccak_sampler              20 CBD polynomials: the sponge word handshake count is 16 up to 30 cycles after done_o
2816124.00ns INFO     cocotb.regression                  test_keccak_sampler.test_cbd_words_17th_not_taken passed
2821130.00ns INFO     cocotb.keccak_sampler              after done_o the sponge is idle (stop_i issued) and its permutation counter is stable, SampleNTT and CBD
2821130.00ns INFO     cocotb.regression                  test_keccak_sampler.test_stop_wipes_sponge passed
4318386.00ns INFO     cocotb.keccak_sampler              CBD cycles identical at 102 points: 164; SampleNTT repeatable (40 repeats); r = cycles - base per blocks: B=3: [85], B=4: [109]
4318386.00ns INFO     cocotb.regression                  test_keccak_sampler.test_constant_cycles_and_cycle_table passed
4352762.01ns INFO     cocotb.keccak_sampler              abort at 5 points per kind and reset in the middle: busy low, window/word/output registers zero, sponge idle, the next polynomial correct
4352762.01ns INFO     cocotb.regression                  test_keccak_sampler.test_abort_reset_zeroisation passed
4355208.01ns INFO     cocotb.keccak_sampler              start requests while busy (both kinds) are ignored; the polynomial is unchanged
4355208.01ns INFO     cocotb.regression                  test_keccak_sampler.test_start_while_busy passed
  1826.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_crafted_streams failed
 23362.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_random_xof_streams failed
 38498.00ns INFO     cocotb.sample_ntt_core             6 polynomials that need a 4th XOF block equal to the golden
 38498.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_four_block_streams passed
 50944.00ns INFO     cocotb.sample_ntt_core             abort at 4 points and reset in the middle clear the window, triple and output registers; the core runs again
 50944.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_abort_reset_zeroisation passed
 55930.00ns INFO     cocotb.sample_ntt_core             start while busy ignored; back-to-back polynomials correct
 55930.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_start_while_busy_and_back_to_back passed
 57536.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_w2_pool_coverage failed
  6126.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_crafted_streams failed
 17072.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_random_xof_streams failed
 32208.00ns INFO     cocotb.sample_ntt_core             6 polynomials that need a 4th XOF block equal to the golden
 32208.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_four_block_streams passed
 44654.00ns INFO     cocotb.sample_ntt_core             abort at 4 points and reset in the middle clear the window, triple and output registers; the core runs again
 44654.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_abort_reset_zeroisation passed
 49640.00ns INFO     cocotb.sample_ntt_core             start while busy ignored; back-to-back polynomials correct
 49640.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_start_while_busy_and_back_to_back passed
 67136.01ns WARNING  cocotb.regression                  test_sample_ntt_core.test_w2_pool_coverage failed
  2006.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_crafted_streams failed
  3632.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_random_xof_streams failed
  5548.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_four_block_streams failed
  7194.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_abort_reset_zeroisation failed
  8840.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_start_while_busy_and_back_to_back failed
 10766.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_w2_pool_coverage failed
  1376.00ns WARNING  cocotb.regression                  test_cbd2_core.test_nibble_table_and_special_streams failed
  2752.00ns WARNING  cocotb.regression                  test_cbd2_core.test_random_streams failed
  6828.00ns WARNING  cocotb.regression                  test_cbd2_core.test_cycles_independent_of_data failed
  8204.00ns WARNING  cocotb.regression                  test_cbd2_core.test_abort_reset_zeroisation failed
1380766.00ns INFO     cocotb.keccak_sampler              500 SampleNTT polynomials (rho || j || i) and 6 other message lengths equal to the golden fed with hashlib SHAKE128; perm_cnt_o minus blocks needed: [(0, 505), (1, 1)]
1380766.00ns INFO     cocotb.regression                  test_keccak_sampler.test_sample_ntt_bit_exact passed
1401952.00ns INFO     cocotb.keccak_sampler              6 polynomials that need a 4th XOF block (rho values from a fixed PRNG seed) equal to the golden; perm_cnt_o = 4
1401952.00ns INFO     cocotb.regression                  test_keccak_sampler.test_four_block_polynomials passed
1403528.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_cbd_bit_exact failed
1405364.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_cbd_words_17th_not_taken failed
1409490.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_stop_wipes_sponge failed
1411066.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_constant_cycles_and_cycle_table failed
1429992.01ns WARNING  cocotb.regression                  test_keccak_sampler.test_abort_reset_zeroisation failed
1432078.01ns INFO     cocotb.keccak_sampler              start requests while busy (both kinds) are ignored; the polynomial is unchanged
1432078.01ns INFO     cocotb.regression                  test_keccak_sampler.test_start_while_busy passed
  5206.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_sample_ntt_bit_exact failed
 10492.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_four_block_polynomials failed
 14598.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_cbd_bit_exact failed
 18114.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_cbd_words_17th_not_taken failed
 20309.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_stop_wipes_sponge failed
 23305.01ns WARNING  cocotb.regression                  test_keccak_sampler.test_constant_cycles_and_cycle_table failed
 42101.01ns WARNING  cocotb.regression                  test_keccak_sampler.test_abort_reset_zeroisation failed
 44187.01ns INFO     cocotb.keccak_sampler              start requests while busy (both kinds) are ignored; the polynomial is unchanged
 44187.01ns INFO     cocotb.regression                  test_keccak_sampler.test_start_while_busy passed
  2366.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_crafted_streams failed
  4002.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_random_xof_streams failed
  5918.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_four_block_streams failed
  7614.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_abort_reset_zeroisation failed
  9250.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_start_while_busy_and_back_to_back failed
 11356.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_w2_pool_coverage failed
 12106.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_crafted_streams failed
 79731.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_random_xof_streams failed
 89337.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_four_block_streams failed
 91033.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_abort_reset_zeroisation failed
 96019.00ns INFO     cocotb.sample_ntt_core             start while busy ignored; back-to-back polynomials correct
 96019.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_start_while_busy_and_back_to_back passed
107785.01ns WARNING  cocotb.regression                  test_sample_ntt_core.test_w2_pool_coverage failed
[verilator] ntt (OUTW=2): 6/6 PASS
[verilator] cbd (OUTW=2): 4/4 PASS
[verilator] top1 (OUTW=2): 8/8 PASS
[verilator] top0 (OUTW=2): 8/8 PASS
[verilator] nclt: test_crafted_streams failed as required: True; failed=['test_crafted_streams', 'test_random_xof_streams', 'test_w2_pool_coverage']
[verilator] nc2nd: test_crafted_streams failed as required: True; failed=['test_crafted_streams', 'test_random_xof_streams', 'test_w2_pool_coverage']
[verilator] ncord: test_crafted_streams failed as required: True; failed=['test_crafted_streams', 'test_random_xof_streams', 'test_four_block_streams', 'test_abort_reset_zeroisation', 'test_start_while_busy_and_back_to_back', 'test_w2_pool_coverage']
[verilator] nccbd: test_nibble_table_and_special_streams failed as required: True; failed=['test_nibble_table_and_special_streams', 'test_random_streams', 'test_cycles_independent_of_data', 'test_abort_reset_zeroisation']
[verilator] nc17: test_cbd_words_17th_not_taken failed as required: True; failed=['test_cbd_bit_exact', 'test_cbd_words_17th_not_taken', 'test_stop_wipes_sponge', 'test_constant_cycles_and_cycle_table', 'test_abort_reset_zeroisation']
[verilator] ncstop: test_stop_wipes_sponge failed as required: True; failed=['test_sample_ntt_bit_exact', 'test_four_block_polynomials', 'test_cbd_bit_exact', 'test_cbd_words_17th_not_taken', 'test_stop_wipes_sponge', 'test_constant_cycles_and_cycle_table', 'test_abort_reset_zeroisation']
[verilator] nccarry: test_crafted_streams failed as required: True; failed=['test_crafted_streams', 'test_random_xof_streams', 'test_four_block_streams', 'test_abort_reset_zeroisation', 'test_start_while_busy_and_back_to_back', 'test_w2_pool_coverage']
[verilator] ncleak: test_abort_reset_zeroisation failed as required: True; failed=['test_crafted_streams', 'test_random_xof_streams', 'test_four_block_streams', 'test_abort_reset_zeroisation', 'test_w2_pool_coverage']
[verilator] TOTAL: 34/34 passed
rc=0
## V3-V8 icarus (OUTW = 2)
604926.00ns INFO     cocotb.sample_ntt_core             196 crafted runs equal to the golden (coefficients and consumed bytes)
604926.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_crafted_streams passed
1850092.00ns INFO     cocotb.sample_ntt_core             500 XOF streams equal to the golden; blocks needed: [(3, 496), (4, 4)]
1850092.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_random_xof_streams passed
1865228.00ns INFO     cocotb.sample_ntt_core             6 polynomials that need a 4th XOF block equal to the golden
1865228.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_four_block_streams passed
1877674.00ns INFO     cocotb.sample_ntt_core             abort at 4 points and reset in the middle clear the window, triple and output registers; the core runs again
1877674.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_abort_reset_zeroisation passed
1882660.00ns INFO     cocotb.sample_ntt_core             start while busy ignored; back-to-back polynomials correct
1882660.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_start_while_busy_and_back_to_back passed
2064556.00ns INFO     cocotb.sample_ntt_core             all six pool combinations (carry, accepted) seen: [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
2064556.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_w2_pool_coverage passed
536146.00ns INFO     cocotb.cbd2_core                   133 special streams equal to the golden; the 16 nibble values give only [0, 1, 2, 3327, 3328]
536146.00ns INFO     cocotb.regression                  test_cbd2_core.test_nibble_table_and_special_streams passed
1568182.00ns INFO     cocotb.cbd2_core                   500 random streams equal to the golden; exactly 16 words taken each time
1568182.00ns INFO     cocotb.regression                  test_cbd2_core.test_random_streams passed
1626258.00ns INFO     cocotb.cbd2_core                   cycles per polynomial with a stream word available every cycle: 134, the same for 43 inputs
1626258.00ns INFO     cocotb.regression                  test_cbd2_core.test_cycles_independent_of_data passed
1637164.00ns INFO     cocotb.cbd2_core                   abort at 4 points and reset in the middle clear the word and output registers; the core runs again
1637164.00ns INFO     cocotb.regression                  test_cbd2_core.test_abort_reset_zeroisation passed
1380766.00ns INFO     cocotb.keccak_sampler              500 SampleNTT polynomials (rho || j || i) and 6 other message lengths equal to the golden fed with hashlib SHAKE128; perm_cnt_o minus blocks needed: [(0, 505), (1, 1)]
1380766.00ns INFO     cocotb.regression                  test_keccak_sampler.test_sample_ntt_bit_exact passed
1401952.00ns INFO     cocotb.keccak_sampler              6 polynomials that need a 4th XOF block (rho values from a fixed PRNG seed) equal to the golden; perm_cnt_o = 4
1401952.00ns INFO     cocotb.regression                  test_keccak_sampler.test_four_block_polynomials passed
2521568.00ns INFO     cocotb.keccak_sampler              500 CBD2 polynomials (sigma || N) equal to the golden fed with hashlib SHAKE256; exactly 16 sponge words taken each time
2521568.00ns INFO     cocotb.regression                  test_keccak_sampler.test_cbd_bit_exact passed
2557794.00ns INFO     cocotb.keccak_sampler              20 CBD polynomials: the sponge word handshake count is 16 up to 30 cycles after done_o
2557794.00ns INFO     cocotb.regression                  test_keccak_sampler.test_cbd_words_17th_not_taken passed
2562320.00ns INFO     cocotb.keccak_sampler              after done_o the sponge is idle (stop_i issued) and its permutation counter is stable, SampleNTT and CBD
2562320.00ns INFO     cocotb.regression                  test_keccak_sampler.test_stop_wipes_sponge passed
3851406.00ns INFO     cocotb.keccak_sampler              CBD cycles identical at 102 points: 152; SampleNTT repeatable (40 repeats); r = cycles - base per blocks: B=3: [49], B=4: [61]
3851406.00ns INFO     cocotb.regression                  test_keccak_sampler.test_constant_cycles_and_cycle_table passed
3882422.01ns INFO     cocotb.keccak_sampler              abort at 5 points per kind and reset in the middle: busy low, window/word/output registers zero, sponge idle, the next polynomial correct
3882422.01ns INFO     cocotb.regression                  test_keccak_sampler.test_abort_reset_zeroisation passed
3884508.01ns INFO     cocotb.keccak_sampler              start requests while busy (both kinds) are ignored; the polynomial is unchanged
3884508.01ns INFO     cocotb.regression                  test_keccak_sampler.test_start_while_busy passed
1578356.00ns INFO     cocotb.keccak_sampler              500 SampleNTT polynomials (rho || j || i) and 6 other message lengths equal to the golden fed with hashlib SHAKE128; perm_cnt_o minus blocks needed: [(0, 506)]
1578356.00ns INFO     cocotb.regression                  test_keccak_sampler.test_sample_ntt_bit_exact passed
1602142.00ns INFO     cocotb.keccak_sampler              6 polynomials that need a 4th XOF block (rho values from a fixed PRNG seed) equal to the golden; perm_cnt_o = 4
1602142.00ns INFO     cocotb.regression                  test_keccak_sampler.test_four_block_polynomials passed
2777498.00ns INFO     cocotb.keccak_sampler              500 CBD2 polynomials (sigma || N) equal to the golden fed with hashlib SHAKE256; exactly 16 sponge words taken each time
2777498.00ns INFO     cocotb.regression                  test_keccak_sampler.test_cbd_bit_exact passed
2816124.00ns INFO     cocotb.keccak_sampler              20 CBD polynomials: the sponge word handshake count is 16 up to 30 cycles after done_o
2816124.00ns INFO     cocotb.regression                  test_keccak_sampler.test_cbd_words_17th_not_taken passed
2821130.00ns INFO     cocotb.keccak_sampler              after done_o the sponge is idle (stop_i issued) and its permutation counter is stable, SampleNTT and CBD
2821130.00ns INFO     cocotb.regression                  test_keccak_sampler.test_stop_wipes_sponge passed
4318386.00ns INFO     cocotb.keccak_sampler              CBD cycles identical at 102 points: 164; SampleNTT repeatable (40 repeats); r = cycles - base per blocks: B=3: [85], B=4: [109]
4318386.00ns INFO     cocotb.regression                  test_keccak_sampler.test_constant_cycles_and_cycle_table passed
4352762.01ns INFO     cocotb.keccak_sampler              abort at 5 points per kind and reset in the middle: busy low, window/word/output registers zero, sponge idle, the next polynomial correct
4352762.01ns INFO     cocotb.regression                  test_keccak_sampler.test_abort_reset_zeroisation passed
4355208.01ns INFO     cocotb.keccak_sampler              start requests while busy (both kinds) are ignored; the polynomial is unchanged
4355208.01ns INFO     cocotb.regression                  test_keccak_sampler.test_start_while_busy passed
  1826.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_crafted_streams failed
 23362.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_random_xof_streams failed
 38498.00ns INFO     cocotb.sample_ntt_core             6 polynomials that need a 4th XOF block equal to the golden
 38498.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_four_block_streams passed
 50944.00ns INFO     cocotb.sample_ntt_core             abort at 4 points and reset in the middle clear the window, triple and output registers; the core runs again
 50944.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_abort_reset_zeroisation passed
 55930.00ns INFO     cocotb.sample_ntt_core             start while busy ignored; back-to-back polynomials correct
 55930.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_start_while_busy_and_back_to_back passed
 57536.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_w2_pool_coverage failed
  6126.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_crafted_streams failed
 17072.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_random_xof_streams failed
 32208.00ns INFO     cocotb.sample_ntt_core             6 polynomials that need a 4th XOF block equal to the golden
 32208.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_four_block_streams passed
 44654.00ns INFO     cocotb.sample_ntt_core             abort at 4 points and reset in the middle clear the window, triple and output registers; the core runs again
 44654.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_abort_reset_zeroisation passed
 49640.00ns INFO     cocotb.sample_ntt_core             start while busy ignored; back-to-back polynomials correct
 49640.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_start_while_busy_and_back_to_back passed
 67136.01ns WARNING  cocotb.regression                  test_sample_ntt_core.test_w2_pool_coverage failed
  2006.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_crafted_streams failed
  3632.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_random_xof_streams failed
  5548.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_four_block_streams failed
  7194.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_abort_reset_zeroisation failed
  8840.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_start_while_busy_and_back_to_back failed
 10766.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_w2_pool_coverage failed
  1376.00ns WARNING  cocotb.regression                  test_cbd2_core.test_nibble_table_and_special_streams failed
  2752.00ns WARNING  cocotb.regression                  test_cbd2_core.test_random_streams failed
  6828.00ns WARNING  cocotb.regression                  test_cbd2_core.test_cycles_independent_of_data failed
  8204.00ns WARNING  cocotb.regression                  test_cbd2_core.test_abort_reset_zeroisation failed
1380766.00ns INFO     cocotb.keccak_sampler              500 SampleNTT polynomials (rho || j || i) and 6 other message lengths equal to the golden fed with hashlib SHAKE128; perm_cnt_o minus blocks needed: [(0, 505), (1, 1)]
1380766.00ns INFO     cocotb.regression                  test_keccak_sampler.test_sample_ntt_bit_exact passed
1401952.00ns INFO     cocotb.keccak_sampler              6 polynomials that need a 4th XOF block (rho values from a fixed PRNG seed) equal to the golden; perm_cnt_o = 4
1401952.00ns INFO     cocotb.regression                  test_keccak_sampler.test_four_block_polynomials passed
1403528.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_cbd_bit_exact failed
1405364.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_cbd_words_17th_not_taken failed
1409490.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_stop_wipes_sponge failed
1411066.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_constant_cycles_and_cycle_table failed
1429992.01ns WARNING  cocotb.regression                  test_keccak_sampler.test_abort_reset_zeroisation failed
1432078.01ns INFO     cocotb.keccak_sampler              start requests while busy (both kinds) are ignored; the polynomial is unchanged
1432078.01ns INFO     cocotb.regression                  test_keccak_sampler.test_start_while_busy passed
  5206.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_sample_ntt_bit_exact failed
 10492.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_four_block_polynomials failed
 14598.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_cbd_bit_exact failed
 18114.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_cbd_words_17th_not_taken failed
 20309.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_stop_wipes_sponge failed
 23305.01ns WARNING  cocotb.regression                  test_keccak_sampler.test_constant_cycles_and_cycle_table failed
 42101.01ns WARNING  cocotb.regression                  test_keccak_sampler.test_abort_reset_zeroisation failed
 44187.01ns INFO     cocotb.keccak_sampler              start requests while busy (both kinds) are ignored; the polynomial is unchanged
 44187.01ns INFO     cocotb.regression                  test_keccak_sampler.test_start_while_busy passed
  2366.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_crafted_streams failed
  4002.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_random_xof_streams failed
  5918.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_four_block_streams failed
  7614.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_abort_reset_zeroisation failed
  9250.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_start_while_busy_and_back_to_back failed
 11356.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_w2_pool_coverage failed
 12106.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_crafted_streams failed
 79731.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_random_xof_streams failed
 89337.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_four_block_streams failed
 91033.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_abort_reset_zeroisation failed
 96019.00ns INFO     cocotb.sample_ntt_core             start while busy ignored; back-to-back polynomials correct
 96019.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_start_while_busy_and_back_to_back passed
107785.01ns WARNING  cocotb.regression                  test_sample_ntt_core.test_w2_pool_coverage failed
[icarus] ntt (OUTW=2): 6/6 PASS
[icarus] cbd (OUTW=2): 4/4 PASS
[icarus] top1 (OUTW=2): 8/8 PASS
[icarus] top0 (OUTW=2): 8/8 PASS
[icarus] nclt: test_crafted_streams failed as required: True; failed=['test_crafted_streams', 'test_random_xof_streams', 'test_w2_pool_coverage']
[icarus] nc2nd: test_crafted_streams failed as required: True; failed=['test_crafted_streams', 'test_random_xof_streams', 'test_w2_pool_coverage']
[icarus] ncord: test_crafted_streams failed as required: True; failed=['test_crafted_streams', 'test_random_xof_streams', 'test_four_block_streams', 'test_abort_reset_zeroisation', 'test_start_while_busy_and_back_to_back', 'test_w2_pool_coverage']
[icarus] nccbd: test_nibble_table_and_special_streams failed as required: True; failed=['test_nibble_table_and_special_streams', 'test_random_streams', 'test_cycles_independent_of_data', 'test_abort_reset_zeroisation']
[icarus] nc17: test_cbd_words_17th_not_taken failed as required: True; failed=['test_cbd_bit_exact', 'test_cbd_words_17th_not_taken', 'test_stop_wipes_sponge', 'test_constant_cycles_and_cycle_table', 'test_abort_reset_zeroisation']
[icarus] ncstop: test_stop_wipes_sponge failed as required: True; failed=['test_sample_ntt_bit_exact', 'test_four_block_polynomials', 'test_cbd_bit_exact', 'test_cbd_words_17th_not_taken', 'test_stop_wipes_sponge', 'test_constant_cycles_and_cycle_table', 'test_abort_reset_zeroisation']
[icarus] nccarry: test_crafted_streams failed as required: True; failed=['test_crafted_streams', 'test_random_xof_streams', 'test_four_block_streams', 'test_abort_reset_zeroisation', 'test_start_while_busy_and_back_to_back', 'test_w2_pool_coverage']
[icarus] ncleak: test_abort_reset_zeroisation failed as required: True; failed=['test_crafted_streams', 'test_random_xof_streams', 'test_four_block_streams', 'test_abort_reset_zeroisation', 'test_w2_pool_coverage']
[icarus] TOTAL: 34/34 passed
rc=0
## V10 rerun of the W1 test set against the current RTL (OUTW = 1) verilator
888816.00ns INFO     cocotb.sample_ntt_core             196 crafted runs equal to the golden (coefficients and consumed bytes)
888816.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_crafted_streams passed
2942282.00ns INFO     cocotb.sample_ntt_core             500 XOF streams equal to the golden; blocks needed: [(3, 496), (4, 4)]
2942282.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_random_xof_streams passed
2965228.00ns INFO     cocotb.sample_ntt_core             6 polynomials that need a 4th XOF block equal to the golden
2965228.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_four_block_streams passed
2983614.00ns INFO     cocotb.sample_ntt_core             abort at 4 points and reset in the middle clear the window, triple and output registers; the core runs again
2983614.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_abort_reset_zeroisation passed
2991690.00ns INFO     cocotb.sample_ntt_core             start while busy ignored; back-to-back polynomials correct
2991690.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_start_while_busy_and_back_to_back passed
1046976.00ns INFO     cocotb.cbd2_core                   133 special streams equal to the golden; the 16 nibble values give only [0, 1, 2, 3327, 3328]
1046976.00ns INFO     cocotb.regression                  test_cbd2_core.test_nibble_table_and_special_streams passed
3043352.00ns INFO     cocotb.cbd2_core                   500 random streams equal to the golden; exactly 16 words taken each time
3043352.00ns INFO     cocotb.regression                  test_cbd2_core.test_random_streams passed
3156468.00ns INFO     cocotb.cbd2_core                   cycles per polynomial with a stream word available every cycle: 262, the same for 43 inputs
3156468.00ns INFO     cocotb.regression                  test_cbd2_core.test_cycles_independent_of_data passed
3175054.00ns INFO     cocotb.cbd2_core                   abort at 4 points and reset in the middle clear the word and output registers; the core runs again
3175054.00ns INFO     cocotb.regression                  test_cbd2_core.test_abort_reset_zeroisation passed
2207036.00ns INFO     cocotb.keccak_sampler              500 SampleNTT polynomials (rho || j || i) and 6 other message lengths equal to the golden fed with hashlib SHAKE128; perm_cnt_o minus blocks needed: [(0, 506)]
2207036.00ns INFO     cocotb.regression                  test_keccak_sampler.test_sample_ntt_bit_exact passed
2233822.00ns INFO     cocotb.keccak_sampler              6 polynomials that need a 4th XOF block (rho values from a fixed PRNG seed) equal to the golden; perm_cnt_o = 4
2233822.00ns INFO     cocotb.regression                  test_keccak_sampler.test_four_block_polynomials passed
4331498.00ns INFO     cocotb.keccak_sampler              500 CBD2 polynomials (sigma || N) equal to the golden fed with hashlib SHAKE256; exactly 16 sponge words taken each time
4331498.00ns INFO     cocotb.regression                  test_keccak_sampler.test_cbd_bit_exact passed
4393324.00ns INFO     cocotb.keccak_sampler              20 CBD polynomials: the sponge word handshake count is 16 up to 30 cycles after done_o
4393324.00ns INFO     cocotb.regression                  test_keccak_sampler.test_cbd_words_17th_not_taken passed
4400060.00ns INFO     cocotb.keccak_sampler              after done_o the sponge is idle (stop_i issued) and its permutation counter is stable, SampleNTT and CBD
4400060.00ns INFO     cocotb.regression                  test_keccak_sampler.test_stop_wipes_sponge passed
6353256.00ns INFO     cocotb.keccak_sampler              CBD cycles identical at 102 points: 280; SampleNTT repeatable (40 repeats); r = cycles - base per blocks: B=3: [41, 42, 43, 44, 45, 46, 47, 48], B=4: [52, 53, 54, 57]
6353256.00ns INFO     cocotb.regression                  test_keccak_sampler.test_constant_cycles_and_cycle_table passed
6400092.01ns INFO     cocotb.keccak_sampler              abort at 5 points per kind and reset in the middle: busy low, window/word/output registers zero, sponge idle, the next polynomial correct
6400092.01ns INFO     cocotb.regression                  test_keccak_sampler.test_abort_reset_zeroisation passed
6403198.01ns INFO     cocotb.keccak_sampler              start requests while busy (both kinds) are ignored; the polynomial is unchanged
6403198.01ns INFO     cocotb.regression                  test_keccak_sampler.test_start_while_busy passed
2395796.00ns INFO     cocotb.keccak_sampler              500 SampleNTT polynomials (rho || j || i) and 6 other message lengths equal to the golden fed with hashlib SHAKE128; perm_cnt_o minus blocks needed: [(0, 505), (1, 1)]
2395796.00ns INFO     cocotb.regression                  test_keccak_sampler.test_sample_ntt_bit_exact passed
2429472.00ns INFO     cocotb.keccak_sampler              6 polynomials that need a 4th XOF block (rho values from a fixed PRNG seed) equal to the golden; perm_cnt_o = 4
2429472.00ns INFO     cocotb.regression                  test_keccak_sampler.test_four_block_polynomials passed
4590028.00ns INFO     cocotb.keccak_sampler              500 CBD2 polynomials (sigma || N) equal to the golden fed with hashlib SHAKE256; exactly 16 sponge words taken each time
4590028.00ns INFO     cocotb.regression                  test_keccak_sampler.test_cbd_bit_exact passed
4654254.00ns INFO     cocotb.keccak_sampler              20 CBD polynomials: the sponge word handshake count is 16 up to 30 cycles after done_o
4654254.00ns INFO     cocotb.regression                  test_keccak_sampler.test_cbd_words_17th_not_taken passed
4661470.00ns INFO     cocotb.keccak_sampler              after done_o the sponge is idle (stop_i issued) and its permutation counter is stable, SampleNTT and CBD
4661470.00ns INFO     cocotb.regression                  test_keccak_sampler.test_stop_wipes_sponge passed
6821156.00ns INFO     cocotb.keccak_sampler              CBD cycles identical at 102 points: 292; SampleNTT repeatable (40 repeats); r = cycles - base per blocks: B=3: [77, 78, 79, 80, 81, 82, 83, 84]
6821156.00ns INFO     cocotb.regression                  test_keccak_sampler.test_constant_cycles_and_cycle_table passed
6871352.01ns INFO     cocotb.keccak_sampler              abort at 5 points per kind and reset in the middle: busy low, window/word/output registers zero, sponge idle, the next polynomial correct
6871352.01ns INFO     cocotb.regression                  test_keccak_sampler.test_abort_reset_zeroisation passed
6874818.01ns INFO     cocotb.keccak_sampler              start requests while busy (both kinds) are ignored; the polynomial is unchanged
6874818.01ns INFO     cocotb.regression                  test_keccak_sampler.test_start_while_busy passed
  2786.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_crafted_streams failed
 17052.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_random_xof_streams failed
 39998.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_four_block_streams failed
 58384.00ns INFO     cocotb.sample_ntt_core             abort at 4 points and reset in the middle clear the window, triple and output registers; the core runs again
 58384.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_abort_reset_zeroisation passed
 66460.00ns INFO     cocotb.sample_ntt_core             start while busy ignored; back-to-back polynomials correct
 66460.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_start_while_busy_and_back_to_back passed
  3096.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_crafted_streams failed
  5812.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_random_xof_streams failed
  9168.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_four_block_streams failed
 11864.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_abort_reset_zeroisation failed
 14540.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_start_while_busy_and_back_to_back failed
  2846.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_crafted_streams failed
  5542.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_random_xof_streams failed
  8428.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_four_block_streams failed
 11134.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_abort_reset_zeroisation failed
 13820.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_start_while_busy_and_back_to_back failed
  2656.00ns WARNING  cocotb.regression                  test_cbd2_core.test_nibble_table_and_special_streams failed
  5312.00ns WARNING  cocotb.regression                  test_cbd2_core.test_random_streams failed
 13228.00ns WARNING  cocotb.regression                  test_cbd2_core.test_cycles_independent_of_data failed
 15884.00ns WARNING  cocotb.regression                  test_cbd2_core.test_abort_reset_zeroisation failed
2207036.00ns INFO     cocotb.keccak_sampler              500 SampleNTT polynomials (rho || j || i) and 6 other message lengths equal to the golden fed with hashlib SHAKE128; perm_cnt_o minus blocks needed: [(0, 506)]
2207036.00ns INFO     cocotb.regression                  test_keccak_sampler.test_sample_ntt_bit_exact passed
2233822.00ns INFO     cocotb.keccak_sampler              6 polynomials that need a 4th XOF block (rho values from a fixed PRNG seed) equal to the golden; perm_cnt_o = 4
2233822.00ns INFO     cocotb.regression                  test_keccak_sampler.test_four_block_polynomials passed
2236678.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_cbd_bit_exact failed
2239794.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_cbd_words_17th_not_taken failed
2246130.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_stop_wipes_sponge failed
2248986.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_constant_cycles_and_cycle_table failed
2276052.01ns WARNING  cocotb.regression                  test_keccak_sampler.test_abort_reset_zeroisation failed
2279158.01ns INFO     cocotb.keccak_sampler              start requests while busy (both kinds) are ignored; the polynomial is unchanged
2279158.01ns INFO     cocotb.regression                  test_keccak_sampler.test_start_while_busy passed
  8966.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_sample_ntt_bit_exact failed
 17742.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_four_block_polynomials failed
 25848.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_cbd_bit_exact failed
 31854.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_cbd_words_17th_not_taken failed
 34979.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_stop_wipes_sponge failed
 40465.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_constant_cycles_and_cycle_table failed
 67331.01ns WARNING  cocotb.regression                  test_keccak_sampler.test_abort_reset_zeroisation failed
 70437.01ns INFO     cocotb.keccak_sampler              start requests while busy (both kinds) are ignored; the polynomial is unchanged
 70437.01ns INFO     cocotb.regression                  test_keccak_sampler.test_start_while_busy passed
[verilator] ntt (OUTW=1): 5/5 PASS
[verilator] cbd (OUTW=1): 4/4 PASS
[verilator] top1 (OUTW=1): 8/8 PASS
[verilator] top0 (OUTW=1): 8/8 PASS
[verilator] nclt: test_crafted_streams failed as required: True; failed=['test_crafted_streams', 'test_random_xof_streams', 'test_four_block_streams']
[verilator] nc2nd: test_crafted_streams failed as required: True; failed=['test_crafted_streams', 'test_random_xof_streams', 'test_four_block_streams', 'test_abort_reset_zeroisation', 'test_start_while_busy_and_back_to_back']
[verilator] ncord: test_crafted_streams failed as required: True; failed=['test_crafted_streams', 'test_random_xof_streams', 'test_four_block_streams', 'test_abort_reset_zeroisation', 'test_start_while_busy_and_back_to_back']
[verilator] nccbd: test_nibble_table_and_special_streams failed as required: True; failed=['test_nibble_table_and_special_streams', 'test_random_streams', 'test_cycles_independent_of_data', 'test_abort_reset_zeroisation']
[verilator] nc17: test_cbd_words_17th_not_taken failed as required: True; failed=['test_cbd_bit_exact', 'test_cbd_words_17th_not_taken', 'test_stop_wipes_sponge', 'test_constant_cycles_and_cycle_table', 'test_abort_reset_zeroisation']
[verilator] ncstop: test_stop_wipes_sponge failed as required: True; failed=['test_sample_ntt_bit_exact', 'test_four_block_polynomials', 'test_cbd_bit_exact', 'test_cbd_words_17th_not_taken', 'test_stop_wipes_sponge', 'test_constant_cycles_and_cycle_table', 'test_abort_reset_zeroisation']
[verilator] TOTAL: 31/31 passed
rc=0
## V10 rerun of the W1 test set against the current RTL (OUTW = 1) icarus
888816.00ns INFO     cocotb.sample_ntt_core             196 crafted runs equal to the golden (coefficients and consumed bytes)
888816.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_crafted_streams passed
2942282.00ns INFO     cocotb.sample_ntt_core             500 XOF streams equal to the golden; blocks needed: [(3, 496), (4, 4)]
2942282.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_random_xof_streams passed
2965228.00ns INFO     cocotb.sample_ntt_core             6 polynomials that need a 4th XOF block equal to the golden
2965228.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_four_block_streams passed
2983614.00ns INFO     cocotb.sample_ntt_core             abort at 4 points and reset in the middle clear the window, triple and output registers; the core runs again
2983614.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_abort_reset_zeroisation passed
2991690.00ns INFO     cocotb.sample_ntt_core             start while busy ignored; back-to-back polynomials correct
2991690.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_start_while_busy_and_back_to_back passed
1046976.00ns INFO     cocotb.cbd2_core                   133 special streams equal to the golden; the 16 nibble values give only [0, 1, 2, 3327, 3328]
1046976.00ns INFO     cocotb.regression                  test_cbd2_core.test_nibble_table_and_special_streams passed
3043352.00ns INFO     cocotb.cbd2_core                   500 random streams equal to the golden; exactly 16 words taken each time
3043352.00ns INFO     cocotb.regression                  test_cbd2_core.test_random_streams passed
3156468.00ns INFO     cocotb.cbd2_core                   cycles per polynomial with a stream word available every cycle: 262, the same for 43 inputs
3156468.00ns INFO     cocotb.regression                  test_cbd2_core.test_cycles_independent_of_data passed
3175054.00ns INFO     cocotb.cbd2_core                   abort at 4 points and reset in the middle clear the word and output registers; the core runs again
3175054.00ns INFO     cocotb.regression                  test_cbd2_core.test_abort_reset_zeroisation passed
2207036.00ns INFO     cocotb.keccak_sampler              500 SampleNTT polynomials (rho || j || i) and 6 other message lengths equal to the golden fed with hashlib SHAKE128; perm_cnt_o minus blocks needed: [(0, 506)]
2207036.00ns INFO     cocotb.regression                  test_keccak_sampler.test_sample_ntt_bit_exact passed
2233822.00ns INFO     cocotb.keccak_sampler              6 polynomials that need a 4th XOF block (rho values from a fixed PRNG seed) equal to the golden; perm_cnt_o = 4
2233822.00ns INFO     cocotb.regression                  test_keccak_sampler.test_four_block_polynomials passed
4331498.00ns INFO     cocotb.keccak_sampler              500 CBD2 polynomials (sigma || N) equal to the golden fed with hashlib SHAKE256; exactly 16 sponge words taken each time
4331498.00ns INFO     cocotb.regression                  test_keccak_sampler.test_cbd_bit_exact passed
4393324.00ns INFO     cocotb.keccak_sampler              20 CBD polynomials: the sponge word handshake count is 16 up to 30 cycles after done_o
4393324.00ns INFO     cocotb.regression                  test_keccak_sampler.test_cbd_words_17th_not_taken passed
4400060.00ns INFO     cocotb.keccak_sampler              after done_o the sponge is idle (stop_i issued) and its permutation counter is stable, SampleNTT and CBD
4400060.00ns INFO     cocotb.regression                  test_keccak_sampler.test_stop_wipes_sponge passed
6353256.00ns INFO     cocotb.keccak_sampler              CBD cycles identical at 102 points: 280; SampleNTT repeatable (40 repeats); r = cycles - base per blocks: B=3: [41, 42, 43, 44, 45, 46, 47, 48], B=4: [52, 53, 54, 57]
6353256.00ns INFO     cocotb.regression                  test_keccak_sampler.test_constant_cycles_and_cycle_table passed
6400092.01ns INFO     cocotb.keccak_sampler              abort at 5 points per kind and reset in the middle: busy low, window/word/output registers zero, sponge idle, the next polynomial correct
6400092.01ns INFO     cocotb.regression                  test_keccak_sampler.test_abort_reset_zeroisation passed
6403198.01ns INFO     cocotb.keccak_sampler              start requests while busy (both kinds) are ignored; the polynomial is unchanged
6403198.01ns INFO     cocotb.regression                  test_keccak_sampler.test_start_while_busy passed
2395796.00ns INFO     cocotb.keccak_sampler              500 SampleNTT polynomials (rho || j || i) and 6 other message lengths equal to the golden fed with hashlib SHAKE128; perm_cnt_o minus blocks needed: [(0, 505), (1, 1)]
2395796.00ns INFO     cocotb.regression                  test_keccak_sampler.test_sample_ntt_bit_exact passed
2429472.00ns INFO     cocotb.keccak_sampler              6 polynomials that need a 4th XOF block (rho values from a fixed PRNG seed) equal to the golden; perm_cnt_o = 4
2429472.00ns INFO     cocotb.regression                  test_keccak_sampler.test_four_block_polynomials passed
4590028.00ns INFO     cocotb.keccak_sampler              500 CBD2 polynomials (sigma || N) equal to the golden fed with hashlib SHAKE256; exactly 16 sponge words taken each time
4590028.00ns INFO     cocotb.regression                  test_keccak_sampler.test_cbd_bit_exact passed
4654254.00ns INFO     cocotb.keccak_sampler              20 CBD polynomials: the sponge word handshake count is 16 up to 30 cycles after done_o
4654254.00ns INFO     cocotb.regression                  test_keccak_sampler.test_cbd_words_17th_not_taken passed
4661470.00ns INFO     cocotb.keccak_sampler              after done_o the sponge is idle (stop_i issued) and its permutation counter is stable, SampleNTT and CBD
4661470.00ns INFO     cocotb.regression                  test_keccak_sampler.test_stop_wipes_sponge passed
6821156.00ns INFO     cocotb.keccak_sampler              CBD cycles identical at 102 points: 292; SampleNTT repeatable (40 repeats); r = cycles - base per blocks: B=3: [77, 78, 79, 80, 81, 82, 83, 84]
6821156.00ns INFO     cocotb.regression                  test_keccak_sampler.test_constant_cycles_and_cycle_table passed
6871352.01ns INFO     cocotb.keccak_sampler              abort at 5 points per kind and reset in the middle: busy low, window/word/output registers zero, sponge idle, the next polynomial correct
6871352.01ns INFO     cocotb.regression                  test_keccak_sampler.test_abort_reset_zeroisation passed
6874818.01ns INFO     cocotb.keccak_sampler              start requests while busy (both kinds) are ignored; the polynomial is unchanged
6874818.01ns INFO     cocotb.regression                  test_keccak_sampler.test_start_while_busy passed
  2786.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_crafted_streams failed
 17052.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_random_xof_streams failed
 39998.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_four_block_streams failed
 58384.00ns INFO     cocotb.sample_ntt_core             abort at 4 points and reset in the middle clear the window, triple and output registers; the core runs again
 58384.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_abort_reset_zeroisation passed
 66460.00ns INFO     cocotb.sample_ntt_core             start while busy ignored; back-to-back polynomials correct
 66460.00ns INFO     cocotb.regression                  test_sample_ntt_core.test_start_while_busy_and_back_to_back passed
  3096.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_crafted_streams failed
  5812.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_random_xof_streams failed
  9168.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_four_block_streams failed
 11864.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_abort_reset_zeroisation failed
 14540.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_start_while_busy_and_back_to_back failed
  2846.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_crafted_streams failed
  5542.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_random_xof_streams failed
  8428.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_four_block_streams failed
 11134.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_abort_reset_zeroisation failed
 13820.00ns WARNING  cocotb.regression                  test_sample_ntt_core.test_start_while_busy_and_back_to_back failed
  2656.00ns WARNING  cocotb.regression                  test_cbd2_core.test_nibble_table_and_special_streams failed
  5312.00ns WARNING  cocotb.regression                  test_cbd2_core.test_random_streams failed
 13228.00ns WARNING  cocotb.regression                  test_cbd2_core.test_cycles_independent_of_data failed
 15884.00ns WARNING  cocotb.regression                  test_cbd2_core.test_abort_reset_zeroisation failed
2207036.00ns INFO     cocotb.keccak_sampler              500 SampleNTT polynomials (rho || j || i) and 6 other message lengths equal to the golden fed with hashlib SHAKE128; perm_cnt_o minus blocks needed: [(0, 506)]
2207036.00ns INFO     cocotb.regression                  test_keccak_sampler.test_sample_ntt_bit_exact passed
2233822.00ns INFO     cocotb.keccak_sampler              6 polynomials that need a 4th XOF block (rho values from a fixed PRNG seed) equal to the golden; perm_cnt_o = 4
2233822.00ns INFO     cocotb.regression                  test_keccak_sampler.test_four_block_polynomials passed
2236678.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_cbd_bit_exact failed
2239794.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_cbd_words_17th_not_taken failed
2246130.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_stop_wipes_sponge failed
2248986.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_constant_cycles_and_cycle_table failed
2276052.01ns WARNING  cocotb.regression                  test_keccak_sampler.test_abort_reset_zeroisation failed
2279158.01ns INFO     cocotb.keccak_sampler              start requests while busy (both kinds) are ignored; the polynomial is unchanged
2279158.01ns INFO     cocotb.regression                  test_keccak_sampler.test_start_while_busy passed
  8966.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_sample_ntt_bit_exact failed
 17742.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_four_block_polynomials failed
 25848.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_cbd_bit_exact failed
 31854.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_cbd_words_17th_not_taken failed
 34979.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_stop_wipes_sponge failed
 40465.00ns WARNING  cocotb.regression                  test_keccak_sampler.test_constant_cycles_and_cycle_table failed
 67331.01ns WARNING  cocotb.regression                  test_keccak_sampler.test_abort_reset_zeroisation failed
 70437.01ns INFO     cocotb.keccak_sampler              start requests while busy (both kinds) are ignored; the polynomial is unchanged
 70437.01ns INFO     cocotb.regression                  test_keccak_sampler.test_start_while_busy passed
[icarus] ntt (OUTW=1): 5/5 PASS
[icarus] cbd (OUTW=1): 4/4 PASS
[icarus] top1 (OUTW=1): 8/8 PASS
[icarus] top0 (OUTW=1): 8/8 PASS
[icarus] nclt: test_crafted_streams failed as required: True; failed=['test_crafted_streams', 'test_random_xof_streams', 'test_four_block_streams']
[icarus] nc2nd: test_crafted_streams failed as required: True; failed=['test_crafted_streams', 'test_random_xof_streams', 'test_four_block_streams', 'test_abort_reset_zeroisation', 'test_start_while_busy_and_back_to_back']
[icarus] ncord: test_crafted_streams failed as required: True; failed=['test_crafted_streams', 'test_random_xof_streams', 'test_four_block_streams', 'test_abort_reset_zeroisation', 'test_start_while_busy_and_back_to_back']
[icarus] nccbd: test_nibble_table_and_special_streams failed as required: True; failed=['test_nibble_table_and_special_streams', 'test_random_streams', 'test_cycles_independent_of_data', 'test_abort_reset_zeroisation']
[icarus] nc17: test_cbd_words_17th_not_taken failed as required: True; failed=['test_cbd_bit_exact', 'test_cbd_words_17th_not_taken', 'test_stop_wipes_sponge', 'test_constant_cycles_and_cycle_table', 'test_abort_reset_zeroisation']
[icarus] ncstop: test_stop_wipes_sponge failed as required: True; failed=['test_sample_ntt_bit_exact', 'test_four_block_polynomials', 'test_cbd_bit_exact', 'test_cbd_words_17th_not_taken', 'test_stop_wipes_sponge', 'test_constant_cycles_and_cycle_table', 'test_abort_reset_zeroisation']
[icarus] TOTAL: 31/31 passed
rc=0
## V9 formal: formal/run/run_formal_phase8b.py (W1 and W2 rows)
| Group | Proof | Expected | Result | Engine detail | Time (s) | As expected |
| A Phase 8b W1 | sample_ntt_core OUTW=1 (S1, S2, S3, S4, S5) | PASS | PASS | basecase=pass, induction=pass | 9.5 | yes |
| A Phase 8b W1 | cbd2_core OUTW=1 (S1, S2 with at most 16 words, S3, S4, S5) | PASS | PASS | basecase=pass, induction=pass | 6.5 | yes |
| B Negative control W1 | NC-S1: a candidate equal to q is accepted (S1 range), OUTW=1 | FAIL | FAIL | basecase=FAIL; failed assert sample_ntt_core_formal_top.sv:146 | 1.1 | yes |
| B Negative control W1 | NC-S2: the coefficient count starts at 1 (S2 count relation: last on the last beat), OUTW=1 | FAIL | FAIL | basecase=FAIL; failed assert sample_ntt_core_formal_top.sv:127 | 0.7 | yes |
| A Phase 8b W2 | sample_ntt_core OUTW=2 (S1, S2, S3, S4, S5, S6 carry) | PASS | PASS | basecase=pass, induction=pass | 10.7 | yes |
| A Phase 8b W2 | cbd2_core OUTW=2 (S1, S2 with at most 16 words, S3, S4, S5) | PASS | PASS | basecase=pass, induction=pass | 5.5 | yes |
| B Negative control W2 | NC-S1: a candidate equal to q is accepted (S1 range), OUTW=2 | FAIL | FAIL | basecase=FAIL; failed assert sample_ntt_core_formal_top.sv:146 | 0.7 | yes |
| B Negative control W2 | NC-S2: the coefficient count starts at 1 (S2 count relation: last on the last beat), OUTW=2 | FAIL | FAIL | basecase=FAIL; failed assert sample_ntt_core_formal_top.sv:127 | 0.8 | yes |
ALL AS EXPECTED
rc=0
OVERALL: PASS
```
