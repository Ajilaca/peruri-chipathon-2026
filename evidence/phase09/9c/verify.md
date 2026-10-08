# Run verifikasi Fase 9c (V1, V2, V10), `scripts/test/phase9c_verify.sh` dengan P9C_SIMS=0, 2026-10-03/04

MEASURED. Run simulator V3-V8 ada di `sim_verilator.md` dan `sim_icarus.md` (dihasilkan oleh `tb/mlkem/run_core_tests.py`; run Icarus untuk seluruh himpunan memakan sekitar satu jam, lihat Amandemen A1 butir 5 test plan). Regresi menjalankan skrip 9a tanpa bagian formalnya dan skrip 9b dengan bagian formalnya; tidak ada file blok beku yang berbeda dari main.

```
## V1 verilator --lint-only -Wall mlkem_core (whole design)
rc=0
## V1 slang mlkem_core (whole design)
Build succeeded: 0 errors, 0 warnings
rc=0
## V2 ROM equals the generated ROM, static checks
rtl/mlkem/mlkem_ctl_rom.sv equals the generated ROM; static checks passed
rc=0
## V2 golden control model against ACVP and the unmodified golden
4 passed in 1.12s
rc=0
## V10 regression: scripts/test/phase9a_verify.sh (without formal)
rc=0
rc=0
rc=0
Build succeeded: 0 errors, 0 warnings
rc=0
7 passed in 1.75s
rc=0
1000396.00ns INFO     cocotb.regression                  test_mlkem_pack.test_random_and_special_all_d_all_modes passed
1195982.00ns INFO     cocotb.regression                  test_mlkem_pack.test_every_mode_pair passed
1369608.00ns INFO     cocotb.regression                  test_mlkem_pack.test_exhaustive_compress passed
1396554.00ns INFO     cocotb.regression                  test_mlkem_pack.test_start_and_dsel_while_busy_ignored passed
1404060.00ns INFO     cocotb.regression                  test_mlkem_pack.test_reset_in_the_middle_then_clean_run passed
1962086.00ns INFO     cocotb.regression                  test_mlkem_pack.test_constant_cycles_and_cycle_table passed
3511356.00ns INFO     cocotb.regression                  test_mlkem_unpack.test_random_all_d_all_modes passed
3710532.00ns INFO     cocotb.regression                  test_mlkem_unpack.test_every_mode_pair passed
3790798.00ns INFO     cocotb.regression                  test_mlkem_unpack.test_exhaustive_decompress_and_all_12_bit_values passed
5379984.00ns INFO     cocotb.regression                  test_mlkem_unpack.test_roundtrip_through_both_modules passed
5406560.00ns INFO     cocotb.regression                  test_mlkem_unpack.test_start_and_dsel_while_busy_ignored passed
5413826.00ns INFO     cocotb.regression                  test_mlkem_unpack.test_reset_in_the_middle_then_clean_run passed
6645852.01ns INFO     cocotb.regression                  test_mlkem_unpack.test_constant_cycles_and_cycle_table passed
 27746.00ns WARNING  cocotb.regression                  test_mlkem_pack.test_random_and_special_all_d_all_modes failed
 30392.00ns WARNING  cocotb.regression                  test_mlkem_pack.test_every_mode_pair failed
 40898.00ns WARNING  cocotb.regression                  test_mlkem_pack.test_exhaustive_compress failed
 46254.00ns WARNING  cocotb.regression                  test_mlkem_pack.test_start_and_dsel_while_busy_ignored failed
 49380.00ns WARNING  cocotb.regression                  test_mlkem_pack.test_reset_in_the_middle_then_clean_run failed
 54646.00ns WARNING  cocotb.regression                  test_mlkem_pack.test_constant_cycles_and_cycle_table failed
 45506.00ns WARNING  cocotb.regression                  test_mlkem_pack.test_random_and_special_all_d_all_modes failed
 48152.00ns WARNING  cocotb.regression                  test_mlkem_pack.test_every_mode_pair failed
 58658.00ns WARNING  cocotb.regression                  test_mlkem_pack.test_exhaustive_compress failed
 64014.00ns WARNING  cocotb.regression                  test_mlkem_pack.test_start_and_dsel_while_busy_ignored failed
 67140.00ns WARNING  cocotb.regression                  test_mlkem_pack.test_reset_in_the_middle_then_clean_run failed
 77646.01ns WARNING  cocotb.regression                  test_mlkem_pack.test_constant_cycles_and_cycle_table failed
 20026.00ns WARNING  cocotb.regression                  test_mlkem_unpack.test_random_all_d_all_modes failed
 32372.00ns WARNING  cocotb.regression                  test_mlkem_unpack.test_every_mode_pair failed
104878.00ns WARNING  cocotb.regression                  test_mlkem_unpack.test_exhaustive_decompress_and_all_12_bit_values failed
1694064.00ns INFO     cocotb.regression                  test_mlkem_unpack.test_roundtrip_through_both_modules passed
1720640.00ns WARNING  cocotb.regression                  test_mlkem_unpack.test_start_and_dsel_while_busy_ignored failed
1727906.00ns WARNING  cocotb.regression                  test_mlkem_unpack.test_reset_in_the_middle_then_clean_run failed
2579692.01ns WARNING  cocotb.regression                  test_mlkem_unpack.test_constant_cycles_and_cycle_table failed
  5336.00ns WARNING  cocotb.regression                  test_mlkem_pack.test_random_and_special_all_d_all_modes failed
  7982.00ns WARNING  cocotb.regression                  test_mlkem_pack.test_every_mode_pair failed
 10628.00ns WARNING  cocotb.regression                  test_mlkem_pack.test_exhaustive_compress failed
 15984.00ns WARNING  cocotb.regression                  test_mlkem_pack.test_start_and_dsel_while_busy_ignored failed
 19110.00ns WARNING  cocotb.regression                  test_mlkem_pack.test_reset_in_the_middle_then_clean_run failed
 21756.01ns WARNING  cocotb.regression                  test_mlkem_pack.test_constant_cycles_and_cycle_table failed
[verilator] pack: 6/6 PASS
[verilator] unpack: 7/7 PASS
[verilator] ncrnd: test_exhaustive_compress failed as required: True; failed=['test_random_and_special_all_d_all_modes', 'test_every_mode_pair', 'test_exhaustive_compress', 'test_start_and_dsel_while_
[verilator] ncord: test_random_and_special_all_d_all_modes failed as required: True; failed=['test_random_and_special_all_d_all_modes', 'test_every_mode_pair', 'test_exhaustive_compress', 'test_start_
[verilator] ncmod: test_exhaustive_decompress_and_all_12_bit_values failed as required: True; failed=['test_random_all_d_all_modes', 'test_every_mode_pair', 'test_exhaustive_decompress_and_all_12_bit_
[verilator] nccnt: test_random_and_special_all_d_all_modes failed as required: True; failed=['test_random_and_special_all_d_all_modes', 'test_every_mode_pair', 'test_exhaustive_compress', 'test_start_
[verilator] TOTAL: 17/17 passed
rc=0
1000396.00ns INFO     cocotb.regression                  test_mlkem_pack.test_random_and_special_all_d_all_modes passed
1195982.00ns INFO     cocotb.regression                  test_mlkem_pack.test_every_mode_pair passed
1369608.00ns INFO     cocotb.regression                  test_mlkem_pack.test_exhaustive_compress passed
1396554.00ns INFO     cocotb.regression                  test_mlkem_pack.test_start_and_dsel_while_busy_ignored passed
1404060.00ns INFO     cocotb.regression                  test_mlkem_pack.test_reset_in_the_middle_then_clean_run passed
1962086.00ns INFO     cocotb.regression                  test_mlkem_pack.test_constant_cycles_and_cycle_table passed
3511356.00ns INFO     cocotb.regression                  test_mlkem_unpack.test_random_all_d_all_modes passed
3710532.00ns INFO     cocotb.regression                  test_mlkem_unpack.test_every_mode_pair passed
3790798.00ns INFO     cocotb.regression                  test_mlkem_unpack.test_exhaustive_decompress_and_all_12_bit_values passed
5379984.00ns INFO     cocotb.regression                  test_mlkem_unpack.test_roundtrip_through_both_modules passed
5406560.00ns INFO     cocotb.regression                  test_mlkem_unpack.test_start_and_dsel_while_busy_ignored passed
5413826.00ns INFO     cocotb.regression                  test_mlkem_unpack.test_reset_in_the_middle_then_clean_run passed
6645852.01ns INFO     cocotb.regression                  test_mlkem_unpack.test_constant_cycles_and_cycle_table passed
 27746.00ns WARNING  cocotb.regression                  test_mlkem_pack.test_random_and_special_all_d_all_modes failed
 30392.00ns WARNING  cocotb.regression                  test_mlkem_pack.test_every_mode_pair failed
 40898.00ns WARNING  cocotb.regression                  test_mlkem_pack.test_exhaustive_compress failed
 46254.00ns WARNING  cocotb.regression                  test_mlkem_pack.test_start_and_dsel_while_busy_ignored failed
 49380.00ns WARNING  cocotb.regression                  test_mlkem_pack.test_reset_in_the_middle_then_clean_run failed
 54646.00ns WARNING  cocotb.regression                  test_mlkem_pack.test_constant_cycles_and_cycle_table failed
 45506.00ns WARNING  cocotb.regression                  test_mlkem_pack.test_random_and_special_all_d_all_modes failed
 48152.00ns WARNING  cocotb.regression                  test_mlkem_pack.test_every_mode_pair failed
 58658.00ns WARNING  cocotb.regression                  test_mlkem_pack.test_exhaustive_compress failed
 64014.00ns WARNING  cocotb.regression                  test_mlkem_pack.test_start_and_dsel_while_busy_ignored failed
 67140.00ns WARNING  cocotb.regression                  test_mlkem_pack.test_reset_in_the_middle_then_clean_run failed
 77646.01ns WARNING  cocotb.regression                  test_mlkem_pack.test_constant_cycles_and_cycle_table failed
 20026.00ns WARNING  cocotb.regression                  test_mlkem_unpack.test_random_all_d_all_modes failed
 32372.00ns WARNING  cocotb.regression                  test_mlkem_unpack.test_every_mode_pair failed
104878.00ns WARNING  cocotb.regression                  test_mlkem_unpack.test_exhaustive_decompress_and_all_12_bit_values failed
1694064.00ns INFO     cocotb.regression                  test_mlkem_unpack.test_roundtrip_through_both_modules passed
1720640.00ns WARNING  cocotb.regression                  test_mlkem_unpack.test_start_and_dsel_while_busy_ignored failed
1727906.00ns WARNING  cocotb.regression                  test_mlkem_unpack.test_reset_in_the_middle_then_clean_run failed
2579692.01ns WARNING  cocotb.regression                  test_mlkem_unpack.test_constant_cycles_and_cycle_table failed
  5336.00ns WARNING  cocotb.regression                  test_mlkem_pack.test_random_and_special_all_d_all_modes failed
  7982.00ns WARNING  cocotb.regression                  test_mlkem_pack.test_every_mode_pair failed
 10628.00ns WARNING  cocotb.regression                  test_mlkem_pack.test_exhaustive_compress failed
 15984.00ns WARNING  cocotb.regression                  test_mlkem_pack.test_start_and_dsel_while_busy_ignored failed
 19110.00ns WARNING  cocotb.regression                  test_mlkem_pack.test_reset_in_the_middle_then_clean_run failed
 21756.01ns WARNING  cocotb.regression                  test_mlkem_pack.test_constant_cycles_and_cycle_table failed
[icarus] pack: 6/6 PASS
[icarus] unpack: 7/7 PASS
[icarus] ncrnd: test_exhaustive_compress failed as required: True; failed=['test_random_and_special_all_d_all_modes', 'test_every_mode_pair', 'test_exhaustive_compress', 'test_start_and_dsel_while_bus
[icarus] ncord: test_random_and_special_all_d_all_modes failed as required: True; failed=['test_random_and_special_all_d_all_modes', 'test_every_mode_pair', 'test_exhaustive_compress', 'test_start_and
[icarus] ncmod: test_exhaustive_decompress_and_all_12_bit_values failed as required: True; failed=['test_random_all_d_all_modes', 'test_every_mode_pair', 'test_exhaustive_decompress_and_all_12_bit_val
[icarus] nccnt: test_random_and_special_all_d_all_modes failed as required: True; failed=['test_random_and_special_all_d_all_modes', 'test_every_mode_pair', 'test_exhaustive_compress', 'test_start_and
[icarus] TOTAL: 17/17 passed
rc=0
OVERALL: PASS
rc=0
## V10 regression: scripts/test/phase9b_verify.sh (with formal)
rc=0
rc=0
rc=0
rc=0
Build succeeded: 0 errors, 0 warnings
rc=0
3 passed in 4.59s
rc=0
 75236.00ns INFO     cocotb.regression                  test_mlkem_hash.test_required_lengths_all_modes passed
141852.00ns INFO     cocotb.regression                  test_mlkem_hash.test_boundary_and_random_lengths passed
151278.00ns INFO     cocotb.regression                  test_mlkem_hash.test_start_sel_len_while_busy_ignored passed
156264.00ns INFO     cocotb.regression                  test_mlkem_hash.test_reset_in_the_middle_then_clean_run passed
224510.00ns INFO     cocotb.regression                  test_mlkem_hash.test_j_then_h_then_g_in_a_row passed
473736.01ns INFO     cocotb.regression                  test_mlkem_hash.test_constant_cycles_and_cycle_table passed
 92476.00ns INFO     cocotb.regression                  test_mlkem_hash.test_required_lengths_all_modes passed
179532.00ns INFO     cocotb.regression                  test_mlkem_hash.test_boundary_and_random_lengths passed
191158.00ns INFO     cocotb.regression                  test_mlkem_hash.test_start_sel_len_while_busy_ignored passed
197704.00ns INFO     cocotb.regression                  test_mlkem_hash.test_reset_in_the_middle_then_clean_run passed
290460.00ns INFO     cocotb.regression                  test_mlkem_hash.test_j_then_h_then_g_in_a_row passed
635686.01ns INFO     cocotb.regression                  test_mlkem_hash.test_constant_cycles_and_cycle_table passed
 61677.00ns INFO     cocotb.regression                  test_mlkem_fo_cmp.test_equal_and_random_pairs_with_gaps passed
12073224.00ns INFO     cocotb.regression                  test_mlkem_fo_cmp.test_every_single_bit_difference passed
12095331.00ns INFO     cocotb.regression                  test_mlkem_fo_cmp.test_first_last_all_beats_and_special_keys passed
12100296.00ns INFO     cocotb.regression                  test_mlkem_fo_cmp.test_start_while_busy_ignored_reset_and_hold passed
12183123.00ns INFO     cocotb.regression                  test_mlkem_fo_cmp.test_constant_cycles_and_cycle_table passed
240945.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_required_lengths_all_modes failed
488100.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_boundary_and_random_lengths failed
693565.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_start_sel_len_while_busy_ignored failed
893940.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_reset_in_the_middle_then_clean_run failed
1093985.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_j_then_h_then_g_in_a_row failed
1433230.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_constant_cycles_and_cycle_table failed
200045.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_required_lengths_all_modes failed
420300.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_boundary_and_random_lengths failed
620345.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_start_sel_len_while_busy_ignored failed
823800.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_reset_in_the_middle_then_clean_run failed
1029425.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_j_then_h_then_g_in_a_row failed
1229470.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_constant_cycles_and_cycle_table failed
 43396.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_required_lengths_all_modes failed
 90762.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_boundary_and_random_lengths failed
 99978.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_start_sel_len_while_busy_ignored failed
102804.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_reset_in_the_middle_then_clean_run failed
105300.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_j_then_h_then_g_in_a_row failed
246996.01ns WARNING  cocotb.regression                  test_mlkem_hash.test_constant_cycles_and_cycle_table failed
 61677.00ns INFO     cocotb.regression                  test_mlkem_fo_cmp.test_equal_and_random_pairs_with_gaps passed
107244.00ns WARNING  cocotb.regression                  test_mlkem_fo_cmp.test_every_single_bit_difference failed
114171.00ns WARNING  cocotb.regression                  test_mlkem_fo_cmp.test_first_last_all_beats_and_special_keys failed
119136.00ns INFO     cocotb.regression                  test_mlkem_fo_cmp.test_start_while_busy_ignored_reset_and_hold passed
123303.00ns WARNING  cocotb.regression                  test_mlkem_fo_cmp.test_constant_cycles_and_cycle_table failed
  1407.00ns WARNING  cocotb.regression                  test_mlkem_fo_cmp.test_equal_and_random_pairs_with_gaps failed
  2814.00ns WARNING  cocotb.regression                  test_mlkem_fo_cmp.test_every_single_bit_difference failed
  4221.00ns WARNING  cocotb.regression                  test_mlkem_fo_cmp.test_first_last_all_beats_and_special_keys failed
  7028.00ns WARNING  cocotb.regression                  test_mlkem_fo_cmp.test_start_while_busy_ignored_reset_and_hold failed
  8435.00ns WARNING  cocotb.regression                  test_mlkem_fo_cmp.test_constant_cycles_and_cycle_table failed
  1437.00ns WARNING  cocotb.regression                  test_mlkem_fo_cmp.test_equal_and_random_pairs_with_gaps failed
  1494.00ns WARNING  cocotb.regression                  test_mlkem_fo_cmp.test_every_single_bit_difference failed
  1551.00ns WARNING  cocotb.regression                  test_mlkem_fo_cmp.test_first_last_all_beats_and_special_keys failed
  1648.00ns WARNING  cocotb.regression                  test_mlkem_fo_cmp.test_start_while_busy_ignored_reset_and_hold failed
  3085.00ns WARNING  cocotb.regression                  test_mlkem_fo_cmp.test_constant_cycles_and_cycle_table failed
[verilator] hash1: 6/6 PASS
[verilator] hash0: 6/6 PASS
[verilator] fo: 5/5 PASS
[verilator] ncstop: test_required_lengths_all_modes failed as required: True; failed=['test_required_lengths_all_modes', 'test_boundary_and_random_lengths', 'test_start_sel_len_while_busy_ignored', 't
[verilator] nclast: test_required_lengths_all_modes failed as required: True; failed=['test_required_lengths_all_modes', 'test_boundary_and_random_lengths', 'test_start_sel_len_while_busy_ignored', 't
[verilator] ncsel: test_required_lengths_all_modes failed as required: True; failed=['test_required_lengths_all_modes', 'test_boundary_and_random_lengths', 'test_start_sel_len_while_busy_ignored', 'te
[verilator] ncmask: test_every_single_bit_difference failed as required: True; failed=['test_every_single_bit_difference', 'test_first_last_all_beats_and_special_keys', 'test_constant_cycles_and_cycle
[verilator] ncswap: test_equal_and_random_pairs_with_gaps failed as required: True; failed=['test_equal_and_random_pairs_with_gaps', 'test_every_single_bit_difference', 'test_first_last_all_beats_and_
[verilator] ncearly: test_constant_cycles_and_cycle_table failed as required: True; failed=['test_equal_and_random_pairs_with_gaps', 'test_every_single_bit_difference', 'test_first_last_all_beats_and_
[verilator] TOTAL: 23/23 passed
rc=0
 75236.00ns INFO     cocotb.regression                  test_mlkem_hash.test_required_lengths_all_modes passed
141852.00ns INFO     cocotb.regression                  test_mlkem_hash.test_boundary_and_random_lengths passed
151278.00ns INFO     cocotb.regression                  test_mlkem_hash.test_start_sel_len_while_busy_ignored passed
156264.00ns INFO     cocotb.regression                  test_mlkem_hash.test_reset_in_the_middle_then_clean_run passed
224510.00ns INFO     cocotb.regression                  test_mlkem_hash.test_j_then_h_then_g_in_a_row passed
473736.01ns INFO     cocotb.regression                  test_mlkem_hash.test_constant_cycles_and_cycle_table passed
 92476.00ns INFO     cocotb.regression                  test_mlkem_hash.test_required_lengths_all_modes passed
179532.00ns INFO     cocotb.regression                  test_mlkem_hash.test_boundary_and_random_lengths passed
191158.00ns INFO     cocotb.regression                  test_mlkem_hash.test_start_sel_len_while_busy_ignored passed
197704.00ns INFO     cocotb.regression                  test_mlkem_hash.test_reset_in_the_middle_then_clean_run passed
290460.00ns INFO     cocotb.regression                  test_mlkem_hash.test_j_then_h_then_g_in_a_row passed
635686.01ns INFO     cocotb.regression                  test_mlkem_hash.test_constant_cycles_and_cycle_table passed
 61677.00ns INFO     cocotb.regression                  test_mlkem_fo_cmp.test_equal_and_random_pairs_with_gaps passed
12073224.00ns INFO     cocotb.regression                  test_mlkem_fo_cmp.test_every_single_bit_difference passed
12095331.00ns INFO     cocotb.regression                  test_mlkem_fo_cmp.test_first_last_all_beats_and_special_keys passed
12100296.00ns INFO     cocotb.regression                  test_mlkem_fo_cmp.test_start_while_busy_ignored_reset_and_hold passed
12183123.00ns INFO     cocotb.regression                  test_mlkem_fo_cmp.test_constant_cycles_and_cycle_table passed
240945.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_required_lengths_all_modes failed
488100.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_boundary_and_random_lengths failed
693565.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_start_sel_len_while_busy_ignored failed
893940.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_reset_in_the_middle_then_clean_run failed
1093985.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_j_then_h_then_g_in_a_row failed
1433230.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_constant_cycles_and_cycle_table failed
200045.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_required_lengths_all_modes failed
420300.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_boundary_and_random_lengths failed
620345.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_start_sel_len_while_busy_ignored failed
823800.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_reset_in_the_middle_then_clean_run failed
1029425.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_j_then_h_then_g_in_a_row failed
1229470.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_constant_cycles_and_cycle_table failed
 43396.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_required_lengths_all_modes failed
 90762.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_boundary_and_random_lengths failed
 99978.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_start_sel_len_while_busy_ignored failed
102804.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_reset_in_the_middle_then_clean_run failed
105300.00ns WARNING  cocotb.regression                  test_mlkem_hash.test_j_then_h_then_g_in_a_row failed
246996.01ns WARNING  cocotb.regression                  test_mlkem_hash.test_constant_cycles_and_cycle_table failed
 61677.00ns INFO     cocotb.regression                  test_mlkem_fo_cmp.test_equal_and_random_pairs_with_gaps passed
107244.00ns WARNING  cocotb.regression                  test_mlkem_fo_cmp.test_every_single_bit_difference failed
114171.00ns WARNING  cocotb.regression                  test_mlkem_fo_cmp.test_first_last_all_beats_and_special_keys failed
119136.00ns INFO     cocotb.regression                  test_mlkem_fo_cmp.test_start_while_busy_ignored_reset_and_hold passed
123303.00ns WARNING  cocotb.regression                  test_mlkem_fo_cmp.test_constant_cycles_and_cycle_table failed
  1407.00ns WARNING  cocotb.regression                  test_mlkem_fo_cmp.test_equal_and_random_pairs_with_gaps failed
  2814.00ns WARNING  cocotb.regression                  test_mlkem_fo_cmp.test_every_single_bit_difference failed
  4221.00ns WARNING  cocotb.regression                  test_mlkem_fo_cmp.test_first_last_all_beats_and_special_keys failed
  7028.00ns WARNING  cocotb.regression                  test_mlkem_fo_cmp.test_start_while_busy_ignored_reset_and_hold failed
  8435.00ns WARNING  cocotb.regression                  test_mlkem_fo_cmp.test_constant_cycles_and_cycle_table failed
  1437.00ns WARNING  cocotb.regression                  test_mlkem_fo_cmp.test_equal_and_random_pairs_with_gaps failed
  1494.00ns WARNING  cocotb.regression                  test_mlkem_fo_cmp.test_every_single_bit_difference failed
  1551.00ns WARNING  cocotb.regression                  test_mlkem_fo_cmp.test_first_last_all_beats_and_special_keys failed
  1648.00ns WARNING  cocotb.regression                  test_mlkem_fo_cmp.test_start_while_busy_ignored_reset_and_hold failed
  3085.00ns WARNING  cocotb.regression                  test_mlkem_fo_cmp.test_constant_cycles_and_cycle_table failed
[icarus] hash1: 6/6 PASS
[icarus] hash0: 6/6 PASS
[icarus] fo: 5/5 PASS
[icarus] ncstop: test_required_lengths_all_modes failed as required: True; failed=['test_required_lengths_all_modes', 'test_boundary_and_random_lengths', 'test_start_sel_len_while_busy_ignored', 'test
[icarus] nclast: test_required_lengths_all_modes failed as required: True; failed=['test_required_lengths_all_modes', 'test_boundary_and_random_lengths', 'test_start_sel_len_while_busy_ignored', 'test
[icarus] ncsel: test_required_lengths_all_modes failed as required: True; failed=['test_required_lengths_all_modes', 'test_boundary_and_random_lengths', 'test_start_sel_len_while_busy_ignored', 'test_
[icarus] ncmask: test_every_single_bit_difference failed as required: True; failed=['test_every_single_bit_difference', 'test_first_last_all_beats_and_special_keys', 'test_constant_cycles_and_cycle_ta
[icarus] ncswap: test_equal_and_random_pairs_with_gaps failed as required: True; failed=['test_equal_and_random_pairs_with_gaps', 'test_every_single_bit_difference', 'test_first_last_all_beats_and_spe
[icarus] ncearly: test_constant_cycles_and_cycle_table failed as required: True; failed=['test_equal_and_random_pairs_with_gaps', 'test_every_single_bit_difference', 'test_first_last_all_beats_and_spe
[icarus] TOTAL: 23/23 passed
rc=0
| Group | Proof | Expected | Result | Engine detail | Time (s) | As expected |
| C Reachability | mlkem_hash: a digest word after 3 accepted words and done_o for H, G and J are reachable (the proof is not vacuous) | PASS | PASS | bmc=pass | 1.3 | yes |
| A Phase 9b | mlkem_hash (H1 digest word count, H2 done, H3 held word, H4 idle, H5 sponge idle after the last word) | PASS | PASS | basecase=pass, induction=pass | 6.0 | yes |
| B Negative control | NC-H1: G stops after 4 digest words (H1 last word) | FAIL | FAIL | basecase=FAIL; failed assert mlkem_hash_formal_top.sv:104 | 0.6 | yes |
| B Negative control | NC-H5: J never stops the squeeze (H5 sponge idle) | FAIL | FAIL | basecase=FAIL; failed assert mlkem_hash_formal_top.sv:91 | 0.6 | yes |
| C Reachability | mlkem_fo_cmp: done_o with neq_o = 1 and with neq_o = 0 are reachable (the proof is not vacuous) | PASS | PASS | bmc=pass | 1.1 | yes |
| A Phase 9b | mlkem_fo_cmp (F1 beats and done, F2 held result, F3 accumulator and neq, F4 mask select) | PASS | PASS | basecase=pass, induction=pass | 11.0 | yes |
| B Negative control | NC-F3: the compare looks at the low 32 bits only (F3 accumulator) | FAIL | FAIL | basecase=FAIL; failed assert mlkem_fo_cmp_formal_top.sv:84 | 0.7 | yes |
| B Negative control | NC-F4: the key select is inverted (F4) | FAIL | FAIL | basecase=FAIL; failed assert mlkem_fo_cmp_formal_top.sv:105 | 1.3 | yes |
| B Negative control | NC-F1: the compare ends at the first difference (F1 done after exactly WORDS beats) | FAIL | FAIL | basecase=FAIL; failed assert mlkem_fo_cmp_formal_top.sv:90 | 0.6 | yes |
ALL AS EXPECTED
rc=0
OVERALL: PASS
rc=0
## V10 frozen blocks: files of rtl/sched rtl/ntt rtl/mem rtl/arith rtl/sample rtl/keccak that differ from main
differing files: 0
OVERALL: PASS
```
