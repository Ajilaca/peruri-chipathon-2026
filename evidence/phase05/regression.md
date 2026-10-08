# MEASURED - Regresi Fase 0-4 + Fase 5 (5a, 5b, 5c), CRG-5 (simulasi / formal; bukan perangkat keras)

- Tanggal: 2026-10-01, git SHA `b418d1e81cb47f2e30d21160364eb03967f07f6d` (branch phase5-arith). rtl/, tb/, formal/, scripts/, quartus/ tidak punya perubahan yang belum di-commit (diperiksa dengan git status); yang belum di-commit saat itu: hanya dokumen (.gitignore, docs/AI_TOOLING_RESEARCH.md, evidence analisis jalur 5c baru, ADR 0015).
- Perintah: `scripts/test/phase5_regression.sh`, `scripts/test/phase5_verify.sh`, `formal/run/run_formal_phase5.py` (keluaran mentah di bawah, tidak diedit).
- Hasil: regresi Fase 0-4 OVERALL: PASS (21 langkah, 0 gagal); verifikasi Fase 5 OVERALL: PASS (17 langkah, 0 gagal); formal Fase 5: semua hasil sesuai harapan (14/14).

## Fase 0-4 (scripts/test/phase5_regression.sh)
```
## check_params
check_params: all locked parameters match.
rc=0
## pytest tb/golden
23 passed in 25.48s
rc=0
## run_ntt_tests verilator
     5.00ns INFO     cocotb.regression                  test_modmul.test_modmul_corners passed
  2005.00ns INFO     cocotb.regression                  test_modmul.test_modmul_random passed
     6.00ns INFO     cocotb.regression                  test_base_case_multiply.test_base_case_multiply_corners passed
   506.00ns INFO     cocotb.regression                  test_base_case_multiply.test_base_case_multiply_random passed
    12.00ns INFO     cocotb.regression                  test_butterfly.test_butterfly_corners passed
  2012.00ns INFO     cocotb.regression                  test_butterfly.test_butterfly_random passed
1239056.00ns INFO     cocotb.regression                  test_ntt_core.test_ntt_bit_exact passed
2746912.00ns INFO     cocotb.regression                  test_ntt_core.test_intt_bit_exact passed
4054968.00ns INFO     cocotb.regression                  test_ntt_core.test_ntt_intt_roundtrip passed
cycles: NTT=897 INTT=1153
4696518.00ns INFO     cocotb.regression                  test_ntt_core.test_constant_cycle_count passed
[verilator] modmul_reduce (test_modmul): 2/2 PASS
[verilator] base_case_multiply (test_base_case_multiply): 2/2 PASS
[verilator] butterfly (test_butterfly): 2/2 PASS
[verilator] ntt_core (test_ntt_core): 4/4 PASS
[verilator] TOTAL: 10/10 passed
rc=0
## run_mem_tests verilator
   256.00ns INFO     cocotb.regression                  test_bank_map.test_bank_map_exhaustive passed
   261.00ns INFO     cocotb.regression                  test_bank_map.test_bank_map_corners passed
   256.00ns INFO     cocotb.regression                  test_bank_map.test_bank_map_exhaustive passed
   261.00ns INFO     cocotb.regression                  test_bank_map.test_bank_map_corners passed
   256.00ns INFO     cocotb.regression                  test_bank_map.test_bank_map_exhaustive passed
   261.00ns INFO     cocotb.regression                  test_bank_map.test_bank_map_corners passed
   256.00ns INFO     cocotb.regression                  test_bank_map.test_bank_map_exhaustive passed
   261.00ns INFO     cocotb.regression                  test_bank_map.test_bank_map_corners passed
1239056.00ns INFO     cocotb.regression                  test_ntt_core_c1.test_ntt_bit_exact passed
2746912.00ns INFO     cocotb.regression                  test_ntt_core_c1.test_intt_bit_exact passed
4054968.00ns INFO     cocotb.regression                  test_ntt_core_c1.test_ntt_intt_roundtrip passed
cycles: NTT=897 (C0: 897) INTT=1153 (C0: 1153)  stall cycles = 0
4696518.00ns INFO     cocotb.regression                  test_ntt_core_c1.test_cycle_count_matches_c0_exactly passed
[verilator] bank_map_rom NUM_BANKS=1: 2/2 PASS
[verilator] bank_map_rom NUM_BANKS=2: 2/2 PASS
[verilator] bank_map_rom NUM_BANKS=4: 2/2 PASS
[verilator] bank_map_rom NUM_BANKS=8: 2/2 PASS
[verilator] ntt_core_c1: 4/4 PASS
[verilator] TOTAL: 12/12 passed
rc=0
## run_ntt_c2_tests verilator c2
1239056.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_bit_exact passed
2746912.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_intt_bit_exact passed
4054968.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_intt_roundtrip passed
L=1 cycles: NTT=897 INTT=1153
4696518.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_cycle_count_constant passed
768656.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_bit_exact passed
1806112.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_intt_bit_exact passed
2666168.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_intt_roundtrip passed
L=2 cycles: NTT=449 INTT=705
3083718.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_cycle_count_constant passed
533456.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_bit_exact passed
1335712.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_intt_bit_exact passed
1971768.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_intt_roundtrip passed
L=4 cycles: NTT=225 INTT=481
2277318.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_cycle_count_constant passed
415856.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_bit_exact passed
1100512.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_intt_bit_exact passed
1624568.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_intt_roundtrip passed
L=8 cycles: NTT=113 INTT=369
1874118.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_cycle_count_constant passed
[verilator] ntt_core_c2 L=1: 4/4 PASS
[verilator] ntt_core_c2 L=2: 4/4 PASS
[verilator] ntt_core_c2 L=4: 4/4 PASS
[verilator] ntt_core_c2 L=8: 4/4 PASS
[verilator] TOTAL: 16/16 passed
rc=0
## run_ntt_c2_tests verilator k2
1239056.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_bit_exact passed
2746912.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_intt_bit_exact passed
4054968.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_intt_roundtrip passed
L=1 cycles: NTT=897 INTT=1153
4696518.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_cycle_count_constant passed
768656.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_bit_exact passed
1806112.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_intt_bit_exact passed
2666168.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_intt_roundtrip passed
L=2 cycles: NTT=449 INTT=705
3083718.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_cycle_count_constant passed
533456.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_bit_exact passed
1335712.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_intt_bit_exact passed
1971768.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_intt_roundtrip passed
L=4 cycles: NTT=225 INTT=481
2277318.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_cycle_count_constant passed
415856.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_bit_exact passed
1100512.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_intt_bit_exact passed
1624568.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_intt_roundtrip passed
L=8 cycles: NTT=113 INTT=369
1874118.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_cycle_count_constant passed
[verilator] ntt_core_c2_k2 L=1: 4/4 PASS
[verilator] ntt_core_c2_k2 L=2: 4/4 PASS
[verilator] ntt_core_c2_k2 L=4: 4/4 PASS
[verilator] ntt_core_c2_k2 L=8: 4/4 PASS
[verilator] TOTAL: 16/16 passed
rc=0
## run_ntt_c2_tests verilator k1
1239056.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_bit_exact passed
2746912.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_intt_bit_exact passed
4054968.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_intt_roundtrip passed
L=1 cycles: NTT=897 INTT=1153
4696518.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_cycle_count_constant passed
768656.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_bit_exact passed
1806112.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_intt_bit_exact passed
2666168.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_intt_roundtrip passed
L=2 cycles: NTT=449 INTT=705
3083718.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_cycle_count_constant passed
533456.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_bit_exact passed
1335712.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_intt_bit_exact passed
1971768.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_intt_roundtrip passed
L=4 cycles: NTT=225 INTT=481
2277318.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_cycle_count_constant passed
415856.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_bit_exact passed
1100512.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_intt_bit_exact passed
1624568.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_intt_roundtrip passed
L=8 cycles: NTT=113 INTT=369
1874118.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_cycle_count_constant passed
[verilator] ntt_core_c2_k2_k1 L=1: 4/4 PASS
[verilator] ntt_core_c2_k2_k1 L=2: 4/4 PASS
[verilator] ntt_core_c2_k2_k1 L=4: 4/4 PASS
[verilator] ntt_core_c2_k2_k1 L=8: 4/4 PASS
[verilator] TOTAL: 16/16 passed
rc=0
## run_k1_unit_tests verilator
    12.00ns INFO     cocotb.regression                  test_butterfly.test_butterfly_corners passed
  2012.00ns INFO     cocotb.regression                  test_butterfly.test_butterfly_random passed
[verilator] butterfly_shared (test_butterfly): 2/2 PASS
rc=0
## run_p4_unit_tests verilator
   136.00ns INFO     cocotb.regression                  test_modmul_staged.test_corners_and_latency passed
 20132.00ns INFO     cocotb.regression                  test_modmul_staged.test_random_back_to_back passed
   146.00ns INFO     cocotb.regression                  test_modmul_staged.test_corners_and_latency passed
 20152.00ns INFO     cocotb.regression                  test_modmul_staged.test_random_back_to_back passed
   156.00ns INFO     cocotb.regression                  test_modmul_staged.test_corners_and_latency passed
 20172.00ns INFO     cocotb.regression                  test_modmul_staged.test_random_back_to_back passed
   166.00ns INFO     cocotb.regression                  test_modmul_staged.test_corners_and_latency passed
 20192.00ns INFO     cocotb.regression                  test_modmul_staged.test_random_back_to_back passed
   236.00ns INFO     cocotb.regression                  test_butterfly_pipe.test_corners passed
 20232.00ns INFO     cocotb.regression                  test_butterfly_pipe.test_random_back_to_back passed
   256.00ns INFO     cocotb.regression                  test_butterfly_pipe.test_corners passed
 20272.00ns INFO     cocotb.regression                  test_butterfly_pipe.test_random_back_to_back passed
   276.00ns INFO     cocotb.regression                  test_butterfly_pipe.test_corners passed
 20312.00ns INFO     cocotb.regression                  test_butterfly_pipe.test_random_back_to_back passed
   296.00ns INFO     cocotb.regression                  test_butterfly_pipe.test_corners passed
 20352.00ns INFO     cocotb.regression                  test_butterfly_pipe.test_random_back_to_back passed
 82116.00ns INFO     cocotb.regression                  test_poly_mem_pipe.test_every_address_every_port passed
 88252.00ns INFO     cocotb.regression                  test_poly_mem_pipe.test_scheduled_traffic passed
 88578.00ns INFO     cocotb.regression                  test_poly_mem_pipe.test_read_after_write_next_cycle passed
 88644.00ns INFO     cocotb.regression                  test_poly_mem_pipe.test_overflow_flag_works passed
 82456.00ns INFO     cocotb.regression                  test_poly_mem_pipe.test_every_address_every_port passed
 88652.00ns INFO     cocotb.regression                  test_poly_mem_pipe.test_scheduled_traffic passed
 89228.00ns INFO     cocotb.regression                  test_poly_mem_pipe.test_read_after_write_next_cycle passed
 89314.00ns INFO     cocotb.regression                  test_poly_mem_pipe.test_overflow_flag_works passed
 82796.00ns INFO     cocotb.regression                  test_poly_mem_pipe.test_every_address_every_port passed
 89052.00ns INFO     cocotb.regression                  test_poly_mem_pipe.test_scheduled_traffic passed
 89878.00ns INFO     cocotb.regression                  test_poly_mem_pipe.test_read_after_write_next_cycle passed
 89984.00ns INFO     cocotb.regression                  test_poly_mem_pipe.test_overflow_flag_works passed
 83136.00ns INFO     cocotb.regression                  test_poly_mem_pipe.test_every_address_every_port passed
 89452.00ns INFO     cocotb.regression                  test_poly_mem_pipe.test_scheduled_traffic passed
 90528.00ns INFO     cocotb.regression                  test_poly_mem_pipe.test_read_after_write_next_cycle passed
 90654.00ns INFO     cocotb.regression                  test_poly_mem_pipe.test_overflow_flag_works passed
[verilator] modmul_reduce_staged REG_AFTER=0 (P=-): 2/2 PASS
[verilator] modmul_reduce_staged REG_AFTER=8 (P=2): 2/2 PASS
[verilator] modmul_reduce_staged REG_AFTER=129 (P=4): 2/2 PASS
[verilator] modmul_reduce_staged REG_AFTER=2081 (P=6): 2/2 PASS
[verilator] butterfly_shared_pipe MUL_REG=0 (P=-): 2/2 PASS
[verilator] butterfly_shared_pipe MUL_REG=8 (P=2): 2/2 PASS
[verilator] butterfly_shared_pipe MUL_REG=129 (P=4): 2/2 PASS
[verilator] butterfly_shared_pipe MUL_REG=2081 (P=6): 2/2 PASS
[verilator] poly_mem_multiport_pipe ARB_REG=0x0 WR_DELAY=0 (P=-): 4/4 PASS
[verilator] poly_mem_multiport_pipe ARB_REG=0x2000 WR_DELAY=1 (P=2): 4/4 PASS
[verilator] poly_mem_multiport_pipe ARB_REG=0x10080 WR_DELAY=2 (P=4): 4/4 PASS
[verilator] poly_mem_multiport_pipe ARB_REG=0x10810 WR_DELAY=3 (P=6): 4/4 PASS
[verilator] TOTAL: 32/32 passed
rc=0
## run_ntt_c3_tests verilator
662595.00ns INFO     cocotb.regression                  test_ntt_core_c3.test_ntt_bit_exact passed
1593990.00ns INFO     cocotb.regression                  test_ntt_core_c3.test_intt_bit_exact passed
2353035.00ns INFO     cocotb.regression                  test_ntt_core_c3.test_ntt_intt_roundtrip passed
2656680.00ns INFO     cocotb.regression                  test_ntt_core_c3.test_boundary_directed passed
3036225.00ns INFO     cocotb.ntt_core_c3_p2              P=2 cycles: NTT=115 INTT=371 stall vs plan: {'NTT': 0, 'INTT': 0}
3036225.00ns INFO     cocotb.regression                  test_ntt_core_c3.test_cycle_count_constant passed
666795.00ns INFO     cocotb.regression                  test_ntt_core_c3.test_ntt_bit_exact passed
1602390.00ns INFO     cocotb.regression                  test_ntt_core_c3.test_intt_bit_exact passed
2365435.00ns INFO     cocotb.regression                  test_ntt_core_c3.test_ntt_intt_roundtrip passed
2670680.00ns INFO     cocotb.regression                  test_ntt_core_c3.test_boundary_directed passed
3052225.00ns INFO     cocotb.ntt_core_c3_p4              P=4 cycles: NTT=117 INTT=373 stall vs plan: {'NTT': 0, 'INTT': 0}
3052225.00ns INFO     cocotb.regression                  test_ntt_core_c3.test_cycle_count_constant passed
670995.00ns INFO     cocotb.regression                  test_ntt_core_c3.test_ntt_bit_exact passed
1610790.00ns INFO     cocotb.regression                  test_ntt_core_c3.test_intt_bit_exact passed
2377835.00ns INFO     cocotb.regression                  test_ntt_core_c3.test_ntt_intt_roundtrip passed
2684680.00ns INFO     cocotb.regression                  test_ntt_core_c3.test_boundary_directed passed
3068225.00ns INFO     cocotb.ntt_core_c3_p6              P=6 cycles: NTT=119 INTT=375 stall vs plan: {'NTT': 0, 'INTT': 0}
3068225.00ns INFO     cocotb.regression                  test_ntt_core_c3.test_cycle_count_constant passed
 77146.00ns INFO     cocotb.regression                  test_ntt_core_c3.test_negative_control_must_fail passed
[verilator] p2 (ntt_core_c3_p2): 5/5 PASS  {'P': 2, 'RDLAT': 1, 'WRDLY': 1, 'cycles_NTT': 115, 'cycles_INTT': 371, 'stall_NTT': 0, 'stall_INTT': 0}
[verilator] p4 (ntt_core_c3_p4): 5/5 PASS  {'P': 4, 'RDLAT': 2, 'WRDLY': 2, 'cycles_NTT': 117, 'cycles_INTT': 373, 'stall_NTT': 0, 'stall_INTT': 0}
[verilator] p6 (ntt_core_c3_p6): 5/5 PASS  {'P': 6, 'RDLAT': 3, 'WRDLY': 3, 'cycles_NTT': 119, 'cycles_INTT': 375, 'stall_NTT': 0, 'stall_INTT': 0}
[verilator] negctl (ntt_core_c3): 1/1 PASS  {'negctl_P': 8, 'violations_NTT': 640, 'wrong_NTT': 5, 'violations_INTT': 640, 'wrong_INTT': 5}
[verilator] TOTAL: 16/16 passed
rc=0
## run_ntt_tests icarus
     5.00ns INFO     cocotb.regression                  test_modmul.test_modmul_corners passed
  2005.00ns INFO     cocotb.regression                  test_modmul.test_modmul_random passed
     6.00ns INFO     cocotb.regression                  test_base_case_multiply.test_base_case_multiply_corners passed
   506.00ns INFO     cocotb.regression                  test_base_case_multiply.test_base_case_multiply_random passed
    12.00ns INFO     cocotb.regression                  test_butterfly.test_butterfly_corners passed
  2012.00ns INFO     cocotb.regression                  test_butterfly.test_butterfly_random passed
1239056.00ns INFO     cocotb.regression                  test_ntt_core.test_ntt_bit_exact passed
2746912.00ns INFO     cocotb.regression                  test_ntt_core.test_intt_bit_exact passed
4054968.00ns INFO     cocotb.regression                  test_ntt_core.test_ntt_intt_roundtrip passed
cycles: NTT=897 INTT=1153
4696518.00ns INFO     cocotb.regression                  test_ntt_core.test_constant_cycle_count passed
[icarus] modmul_reduce (test_modmul): 2/2 PASS
[icarus] base_case_multiply (test_base_case_multiply): 2/2 PASS
[icarus] butterfly (test_butterfly): 2/2 PASS
[icarus] ntt_core (test_ntt_core): 4/4 PASS
[icarus] TOTAL: 10/10 passed
rc=0
## run_mem_tests icarus
   256.00ns INFO     cocotb.regression                  test_bank_map.test_bank_map_exhaustive passed
   261.00ns INFO     cocotb.regression                  test_bank_map.test_bank_map_corners passed
   256.00ns INFO     cocotb.regression                  test_bank_map.test_bank_map_exhaustive passed
   261.00ns INFO     cocotb.regression                  test_bank_map.test_bank_map_corners passed
   256.00ns INFO     cocotb.regression                  test_bank_map.test_bank_map_exhaustive passed
   261.00ns INFO     cocotb.regression                  test_bank_map.test_bank_map_corners passed
   256.00ns INFO     cocotb.regression                  test_bank_map.test_bank_map_exhaustive passed
   261.00ns INFO     cocotb.regression                  test_bank_map.test_bank_map_corners passed
1239056.00ns INFO     cocotb.regression                  test_ntt_core_c1.test_ntt_bit_exact passed
2746912.00ns INFO     cocotb.regression                  test_ntt_core_c1.test_intt_bit_exact passed
4054968.00ns INFO     cocotb.regression                  test_ntt_core_c1.test_ntt_intt_roundtrip passed
cycles: NTT=897 (C0: 897) INTT=1153 (C0: 1153)  stall cycles = 0
4696518.00ns INFO     cocotb.regression                  test_ntt_core_c1.test_cycle_count_matches_c0_exactly passed
[icarus] bank_map_rom NUM_BANKS=1: 2/2 PASS
[icarus] bank_map_rom NUM_BANKS=2: 2/2 PASS
[icarus] bank_map_rom NUM_BANKS=4: 2/2 PASS
[icarus] bank_map_rom NUM_BANKS=8: 2/2 PASS
[icarus] ntt_core_c1: 4/4 PASS
[icarus] TOTAL: 12/12 passed
rc=0
## run_ntt_c2_tests icarus c2
1239056.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_bit_exact passed
2746912.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_intt_bit_exact passed
4054968.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_intt_roundtrip passed
L=1 cycles: NTT=897 INTT=1153
4696518.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_cycle_count_constant passed
768656.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_bit_exact passed
1806112.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_intt_bit_exact passed
2666168.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_intt_roundtrip passed
L=2 cycles: NTT=449 INTT=705
3083718.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_cycle_count_constant passed
533456.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_bit_exact passed
1335712.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_intt_bit_exact passed
1971768.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_intt_roundtrip passed
L=4 cycles: NTT=225 INTT=481
2277318.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_cycle_count_constant passed
415856.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_bit_exact passed
1100512.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_intt_bit_exact passed
1624568.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_intt_roundtrip passed
L=8 cycles: NTT=113 INTT=369
1874118.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_cycle_count_constant passed
[icarus] ntt_core_c2 L=1: 4/4 PASS
[icarus] ntt_core_c2 L=2: 4/4 PASS
[icarus] ntt_core_c2 L=4: 4/4 PASS
[icarus] ntt_core_c2 L=8: 4/4 PASS
[icarus] TOTAL: 16/16 passed
rc=0
## run_ntt_c2_tests icarus k2
1239056.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_bit_exact passed
2746912.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_intt_bit_exact passed
4054968.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_intt_roundtrip passed
L=1 cycles: NTT=897 INTT=1153
4696518.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_cycle_count_constant passed
768656.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_bit_exact passed
1806112.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_intt_bit_exact passed
2666168.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_intt_roundtrip passed
L=2 cycles: NTT=449 INTT=705
3083718.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_cycle_count_constant passed
533456.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_bit_exact passed
1335712.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_intt_bit_exact passed
1971768.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_intt_roundtrip passed
L=4 cycles: NTT=225 INTT=481
2277318.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_cycle_count_constant passed
415856.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_bit_exact passed
1100512.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_intt_bit_exact passed
1624568.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_intt_roundtrip passed
L=8 cycles: NTT=113 INTT=369
1874118.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_cycle_count_constant passed
[icarus] ntt_core_c2_k2 L=1: 4/4 PASS
[icarus] ntt_core_c2_k2 L=2: 4/4 PASS
[icarus] ntt_core_c2_k2 L=4: 4/4 PASS
[icarus] ntt_core_c2_k2 L=8: 4/4 PASS
[icarus] TOTAL: 16/16 passed
rc=0
## run_ntt_c2_tests icarus k1
1239056.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_bit_exact passed
2746912.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_intt_bit_exact passed
4054968.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_intt_roundtrip passed
L=1 cycles: NTT=897 INTT=1153
4696518.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_cycle_count_constant passed
768656.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_bit_exact passed
1806112.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_intt_bit_exact passed
2666168.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_intt_roundtrip passed
L=2 cycles: NTT=449 INTT=705
3083718.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_cycle_count_constant passed
533456.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_bit_exact passed
1335712.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_intt_bit_exact passed
1971768.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_intt_roundtrip passed
L=4 cycles: NTT=225 INTT=481
2277318.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_cycle_count_constant passed
415856.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_bit_exact passed
1100512.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_intt_bit_exact passed
1624568.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_ntt_intt_roundtrip passed
L=8 cycles: NTT=113 INTT=369
1874118.00ns INFO     cocotb.regression                  test_ntt_core_c2.test_cycle_count_constant passed
[icarus] ntt_core_c2_k2_k1 L=1: 4/4 PASS
[icarus] ntt_core_c2_k2_k1 L=2: 4/4 PASS
[icarus] ntt_core_c2_k2_k1 L=4: 4/4 PASS
[icarus] ntt_core_c2_k2_k1 L=8: 4/4 PASS
[icarus] TOTAL: 16/16 passed
rc=0
## run_k1_unit_tests icarus
    12.00ns INFO     cocotb.regression                  test_butterfly.test_butterfly_corners passed
  2012.00ns INFO     cocotb.regression                  test_butterfly.test_butterfly_random passed
[icarus] butterfly_shared (test_butterfly): 2/2 PASS
rc=0
## run_p4_unit_tests icarus
   136.00ns INFO     cocotb.regression                  test_modmul_staged.test_corners_and_latency passed
 20132.00ns INFO     cocotb.regression                  test_modmul_staged.test_random_back_to_back passed
   146.00ns INFO     cocotb.regression                  test_modmul_staged.test_corners_and_latency passed
 20152.00ns INFO     cocotb.regression                  test_modmul_staged.test_random_back_to_back passed
   156.00ns INFO     cocotb.regression                  test_modmul_staged.test_corners_and_latency passed
 20172.00ns INFO     cocotb.regression                  test_modmul_staged.test_random_back_to_back passed
   166.00ns INFO     cocotb.regression                  test_modmul_staged.test_corners_and_latency passed
 20192.00ns INFO     cocotb.regression                  test_modmul_staged.test_random_back_to_back passed
   236.00ns INFO     cocotb.regression                  test_butterfly_pipe.test_corners passed
 20232.00ns INFO     cocotb.regression                  test_butterfly_pipe.test_random_back_to_back passed
   256.00ns INFO     cocotb.regression                  test_butterfly_pipe.test_corners passed
 20272.00ns INFO     cocotb.regression                  test_butterfly_pipe.test_random_back_to_back passed
   276.00ns INFO     cocotb.regression                  test_butterfly_pipe.test_corners passed
 20312.00ns INFO     cocotb.regression                  test_butterfly_pipe.test_random_back_to_back passed
   296.00ns INFO     cocotb.regression                  test_butterfly_pipe.test_corners passed
 20352.00ns INFO     cocotb.regression                  test_butterfly_pipe.test_random_back_to_back passed
 82116.00ns INFO     cocotb.regression                  test_poly_mem_pipe.test_every_address_every_port passed
 88252.00ns INFO     cocotb.regression                  test_poly_mem_pipe.test_scheduled_traffic passed
 88578.00ns INFO     cocotb.regression                  test_poly_mem_pipe.test_read_after_write_next_cycle passed
 88644.00ns INFO     cocotb.regression                  test_poly_mem_pipe.test_overflow_flag_works passed
 82456.00ns INFO     cocotb.regression                  test_poly_mem_pipe.test_every_address_every_port passed
 88652.00ns INFO     cocotb.regression                  test_poly_mem_pipe.test_scheduled_traffic passed
 89228.00ns INFO     cocotb.regression                  test_poly_mem_pipe.test_read_after_write_next_cycle passed
 89314.00ns INFO     cocotb.regression                  test_poly_mem_pipe.test_overflow_flag_works passed
 82796.00ns INFO     cocotb.regression                  test_poly_mem_pipe.test_every_address_every_port passed
 89052.00ns INFO     cocotb.regression                  test_poly_mem_pipe.test_scheduled_traffic passed
 89878.00ns INFO     cocotb.regression                  test_poly_mem_pipe.test_read_after_write_next_cycle passed
 89984.00ns INFO     cocotb.regression                  test_poly_mem_pipe.test_overflow_flag_works passed
 83136.00ns INFO     cocotb.regression                  test_poly_mem_pipe.test_every_address_every_port passed
 89452.00ns INFO     cocotb.regression                  test_poly_mem_pipe.test_scheduled_traffic passed
 90528.00ns INFO     cocotb.regression                  test_poly_mem_pipe.test_read_after_write_next_cycle passed
 90654.00ns INFO     cocotb.regression                  test_poly_mem_pipe.test_overflow_flag_works passed
[icarus] modmul_reduce_staged REG_AFTER=0 (P=-): 2/2 PASS
[icarus] modmul_reduce_staged REG_AFTER=8 (P=2): 2/2 PASS
[icarus] modmul_reduce_staged REG_AFTER=129 (P=4): 2/2 PASS
[icarus] modmul_reduce_staged REG_AFTER=2081 (P=6): 2/2 PASS
[icarus] butterfly_shared_pipe MUL_REG=0 (P=-): 2/2 PASS
[icarus] butterfly_shared_pipe MUL_REG=8 (P=2): 2/2 PASS
[icarus] butterfly_shared_pipe MUL_REG=129 (P=4): 2/2 PASS
[icarus] butterfly_shared_pipe MUL_REG=2081 (P=6): 2/2 PASS
[icarus] poly_mem_multiport_pipe ARB_REG=0x0 WR_DELAY=0 (P=-): 4/4 PASS
[icarus] poly_mem_multiport_pipe ARB_REG=0x2000 WR_DELAY=1 (P=2): 4/4 PASS
[icarus] poly_mem_multiport_pipe ARB_REG=0x10080 WR_DELAY=2 (P=4): 4/4 PASS
[icarus] poly_mem_multiport_pipe ARB_REG=0x10810 WR_DELAY=3 (P=6): 4/4 PASS
[icarus] TOTAL: 32/32 passed
rc=0
## run_ntt_c3_tests icarus
662595.00ns INFO     cocotb.regression                  test_ntt_core_c3.test_ntt_bit_exact passed
1593990.00ns INFO     cocotb.regression                  test_ntt_core_c3.test_intt_bit_exact passed
2353035.00ns INFO     cocotb.regression                  test_ntt_core_c3.test_ntt_intt_roundtrip passed
2656680.00ns INFO     cocotb.regression                  test_ntt_core_c3.test_boundary_directed passed
3036225.00ns INFO     cocotb.ntt_core_c3_p2              P=2 cycles: NTT=115 INTT=371 stall vs plan: {'NTT': 0, 'INTT': 0}
3036225.00ns INFO     cocotb.regression                  test_ntt_core_c3.test_cycle_count_constant passed
666795.00ns INFO     cocotb.regression                  test_ntt_core_c3.test_ntt_bit_exact passed
1602390.00ns INFO     cocotb.regression                  test_ntt_core_c3.test_intt_bit_exact passed
2365435.00ns INFO     cocotb.regression                  test_ntt_core_c3.test_ntt_intt_roundtrip passed
2670680.00ns INFO     cocotb.regression                  test_ntt_core_c3.test_boundary_directed passed
3052225.00ns INFO     cocotb.ntt_core_c3_p4              P=4 cycles: NTT=117 INTT=373 stall vs plan: {'NTT': 0, 'INTT': 0}
3052225.00ns INFO     cocotb.regression                  test_ntt_core_c3.test_cycle_count_constant passed
670995.00ns INFO     cocotb.regression                  test_ntt_core_c3.test_ntt_bit_exact passed
1610790.00ns INFO     cocotb.regression                  test_ntt_core_c3.test_intt_bit_exact passed
2377835.00ns INFO     cocotb.regression                  test_ntt_core_c3.test_ntt_intt_roundtrip passed
2684680.00ns INFO     cocotb.regression                  test_ntt_core_c3.test_boundary_directed passed
3068225.00ns INFO     cocotb.ntt_core_c3_p6              P=6 cycles: NTT=119 INTT=375 stall vs plan: {'NTT': 0, 'INTT': 0}
3068225.00ns INFO     cocotb.regression                  test_ntt_core_c3.test_cycle_count_constant passed
 77146.00ns INFO     cocotb.regression                  test_ntt_core_c3.test_negative_control_must_fail passed
[icarus] p2 (ntt_core_c3_p2): 5/5 PASS  {'P': 2, 'RDLAT': 1, 'WRDLY': 1, 'cycles_NTT': 115, 'cycles_INTT': 371, 'stall_NTT': 0, 'stall_INTT': 0}
[icarus] p4 (ntt_core_c3_p4): 5/5 PASS  {'P': 4, 'RDLAT': 2, 'WRDLY': 2, 'cycles_NTT': 117, 'cycles_INTT': 373, 'stall_NTT': 0, 'stall_INTT': 0}
[icarus] p6 (ntt_core_c3_p6): 5/5 PASS  {'P': 6, 'RDLAT': 3, 'WRDLY': 3, 'cycles_NTT': 119, 'cycles_INTT': 375, 'stall_NTT': 0, 'stall_INTT': 0}
[icarus] negctl (ntt_core_c3): 1/1 PASS  {'negctl_P': 8, 'violations_NTT': 640, 'wrong_NTT': 5, 'violations_INTT': 640, 'wrong_INTT': 5}
[icarus] TOTAL: 16/16 passed
rc=0
## Phase 4 exhaustive staged reducer
REG_AFTER=0     latency=0 pairs_checked=16777216 (of which a,b<3329: 11082241) mismatches=0 modmul_reduce_vs_formula_mismatches=0
REG_AFTER=8     latency=1 pairs_checked=16777216 (of which a,b<3329: 11082241) mismatches=0 modmul_reduce_vs_formula_mismatches=0
REG_AFTER=129   latency=2 pairs_checked=16777216 (of which a,b<3329: 11082241) mismatches=0 modmul_reduce_vs_formula_mismatches=0
REG_AFTER=2081  latency=3 pairs_checked=16777216 (of which a,b<3329: 11082241) mismatches=0 modmul_reduce_vs_formula_mismatches=0
RESULT: PASS
rc=0
## formal Phase 1-3 (run_formal_slang.py)
| Group | Proof | Expected | Result | Engine detail | Time (s) | As expected |
| A Phase 3 | C2 L=1 | PASS | PASS | basecase=pass, induction=pass | 0.8 | yes |
| A Phase 3 | C2 L=2 | PASS | PASS | basecase=pass, induction=pass | 1.1 | yes |
| A Phase 3 | C2 L=4 | PASS | PASS | basecase=pass, induction=pass | 1.7 | yes |
| A Phase 3 | C2 L=8 | PASS | PASS | basecase=pass, induction=pass | 4.8 | yes |
| A Phase 3 | C2-K2 L=1 | PASS | PASS | basecase=pass, induction=pass | 0.6 | yes |
| A Phase 3 | C2-K2 L=2 | PASS | PASS | basecase=pass, induction=pass | 1.0 | yes |
| A Phase 3 | C2-K2 L=4 | PASS | PASS | basecase=pass, induction=pass | 1.8 | yes |
| A Phase 3 | C2-K2 L=8 | PASS | PASS | basecase=pass, induction=pass | 4.8 | yes |
| A Phase 3 | C2-K2-K1 L=1 | PASS | PASS | basecase=pass, induction=pass | 0.6 | yes |
| A Phase 3 | C2-K2-K1 L=2 | PASS | PASS | basecase=pass, induction=pass | 0.9 | yes |
| A Phase 3 | C2-K2-K1 L=4 | PASS | PASS | basecase=pass, induction=pass | 2.0 | yes |
| A Phase 3 | C2-K2-K1 L=8 | PASS | PASS | basecase=pass, induction=pass | 4.8 | yes |
| B Negative control | NC-A: bank_map_rom copy, NUM_BANKS=2: bank(128) 1 -> 0 (violation in the first NTT cycle -> must be caught by the base case) | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c2_formal_top.sv:57 | 1.0 | yes |
| B Negative control | NC-B: bank_map_rom copy, NUM_BANKS=2: bank(40) 0 -> 1 (violation beyond depth 6 -> base case passes, induction must fail) | UNKNOWN | UNKNOWN | basecase=pass, induction=FAIL; failed assert ntt_core_c2_formal_top.sv:57 | 1.3 | yes |
| B Negative control | NC-B/bmc60: bank_map_rom copy, NUM_BANKS=2: bank(40) 0 -> 1 (same corruption, BMC depth 60 -> the violation is real and reachable) | FAIL | FAIL | bmc=FAIL; failed assert ntt_core_c2_formal_top.sv:57 | 3.5 | yes |
| B Negative control | NC-C: bank_map_rom copy, NUM_BANKS=8: bank(128) 2 -> 3 (selected config C2-K2-K1 L=8, violation in the first NTT cycle) | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c2_k2_k1_formal_top.sv:58 | 5.1 | yes |
| C Phase 1/2 re-run | Phase 1 ntt_core (C0) FSM safety | PASS | PASS | basecase=pass, induction=pass | 0.4 | yes |
| C Phase 1/2 re-run | Phase 2 ntt_core_c1 (C1) FSM safety | PASS | PASS | basecase=pass, induction=pass | 0.6 | yes |
| C Phase 1/2 re-run | Phase 2 bank_map_rom own-pair (NUM_BANKS=8) | PASS | PASS | bmc=pass | 0.3 | yes |
OVERALL: all results as expected (19/19)
rc=0
## formal Phase 4 (run_formal_phase4.py)
| Group | Proof | Expected | Result | Engine detail | Time (s) | As expected |
| A Phase 4 | C3 P=2 (H, O, R, A, B, C) | PASS | PASS | basecase=pass, induction=pass | 5.5 | yes |
| A Phase 4 | C3 P=4 (H, O, R, A, B, C) | PASS | PASS | basecase=pass, induction=pass | 7.9 | yes |
| A Phase 4 | C3 P=6 (H, O, R, A, B, C) | PASS | PASS | basecase=pass, induction=pass | 11.7 | yes |
| B Negative control | NC-O P=2: bank_map_rom copy, NUM_BANKS=8: bank(128) 2 -> 3 | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c3_formal_top.sv:144 | 6.5 | yes |
| B Negative control | NC-O P=6: bank_map_rom copy, NUM_BANKS=8: bank(128) 2 -> 3 | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c3_formal_top.sv:144 | 8.7 | yes |
| B Negative control | NC-A P=2: delay model of property A one cycle short | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c3_formal_top.sv:145 | 6.1 | yes |
| B Negative control | NC-B P=2: drain one cycle short (induction must fail) | UNKNOWN | UNKNOWN | basecase=pass, induction=FAIL; failed assert ntt_core_c3_formal_top.sv:147 | 10.0 | yes |
| B Negative control | NC-B/bmc125 P=2: same mutant, BMC depth 125 (violation reachable) | FAIL | FAIL | bmc=FAIL; failed assert ntt_core_c3_formal_top.sv:147 | 1913.2 | yes |
| B Negative control | NC-C P=2: scaling pass may repeat an address (induction must fail) | UNKNOWN | UNKNOWN | basecase=pass, induction=FAIL; failed assert ntt_core_c3_formal_top.sv:150 | 12.7 | yes |
OVERALL: all results as expected (9/9)
rc=0
OVERALL: PASS
```
## Verifikasi Fase 5 (scripts/test/phase5_verify.sh)
```
## V1 verilator --lint-only -Wall ntt_core_c4a
rc=0
## V1 slang ntt_core_c4a
Build succeeded: 0 errors, 0 warnings
rc=0
## V1 verilator --lint-only -Wall ntt_core_c4b_b
rc=0
## V1 slang ntt_core_c4b_b
Build succeeded: 0 errors, 0 warnings
rc=0
## V1 verilator --lint-only -Wall ntt_core_c4b_m
rc=0
## V1 slang ntt_core_c4b_m
Build succeeded: 0 errors, 0 warnings
rc=0
## V1 verilator --lint-only -Wall ntt_core_c4c
rc=0
## V1 slang ntt_core_c4c
Build succeeded: 0 errors, 0 warnings
rc=0
## V1 verilator --lint-only -Wall ntt_core_c4
rc=0
## V1 slang ntt_core_c4
Build succeeded: 0 errors, 0 warnings
rc=0
## V2 exhaustive reducer (tb/arith/reducer_exhaustive)
kind=1 REG_AFTER=0    real             latency=0 pairs_checked=16777216 in_range(a,b<3329)=11082241 mismatches_in_range=0 mismatches_out_of_range(info)=0 modmul_reduce_vs_formula_mismatches=0
kind=1 REG_AFTER=41   real             latency=3 pairs_checked=16777216 in_range(a,b<3329)=11082241 mismatches_in_range=0 mismatches_out_of_range(info)=0 modmul_reduce_vs_formula_mismatches=0
kind=1 REG_AFTER=41   negative_control MISMATCH a=2 b=2048 dut=768 modmul_reduce=767 formula=767
latency=3 pairs_checked=16777216 in_range(a,b<3329)=11082241 mismatches_in_range=11042411 mismatches_out_of_range(info)=5690522 modmul_reduce_vs_formula_mismatches=0
negative control failed as required
kind=2 REG_AFTER=0    real             latency=0 pairs_checked=16777216 in_range(a,b<3329)=11082241 mismatches_in_range=0 mismatches_out_of_range(info)=0 modmul_reduce_vs_formula_mismatches=0
kind=2 REG_AFTER=7    real             latency=3 pairs_checked=16777216 in_range(a,b<3329)=11082241 mismatches_in_range=0 mismatches_out_of_range(info)=0 modmul_reduce_vs_formula_mismatches=0
kind=2 REG_AFTER=7    negative_control MISMATCH a=2 b=1665 dut=2 modmul_reduce=1 formula=1
latency=3 pairs_checked=16777216 in_range(a,b<3329)=11082241 mismatches_in_range=11048075 mismatches_out_of_range(info)=5692448 modmul_reduce_vs_formula_mismatches=0
negative control failed as required
kind=3 REG_AFTER=0    real             latency=0 pairs_checked=16777216 in_range(a,b<3329)=11082241 mismatches_in_range=0 mismatches_out_of_range(info)=0 modmul_reduce_vs_formula_mismatches=0
kind=3 REG_AFTER=7    real             latency=3 pairs_checked=16777216 in_range(a,b<3329)=11082241 mismatches_in_range=0 mismatches_out_of_range(info)=0 modmul_reduce_vs_formula_mismatches=0
kind=3 REG_AFTER=7    negative_control MISMATCH a=1 b=1 dut=624 modmul_reduce=1 formula=1
latency=3 pairs_checked=16777216 in_range(a,b<3329)=11082241 mismatches_in_range=11059475 mismatches_out_of_range(info)=5684425 modmul_reduce_vs_formula_mismatches=0
negative control failed as required
RESULT: PASS
rc=0
## V2-lazy exhaustive Barrett lazy (tb/arith/lazy_exhaustive)
REG_AFTER=0  real             latency=0 pairs_checked=33554432 lazy_domain(a<q,b<2q)=22164482 mismatches_lazy=0 d6_subset(a,b<q)=11082241 mismatches_d6=0 mismatches_other(info)=240701
REG_AFTER=7  real             latency=3 pairs_checked=33554432 lazy_domain(a<q,b<2q)=22164482 mismatches_lazy=0 d6_subset(a,b<q)=11082241 mismatches_d6=0 mismatches_other(info)=240701
latency=3 pairs_checked=33554432 lazy_domain(a<q,b<2q)=22164482 mismatches_lazy=22124671 d6_subset(a,b<q)=11082241 mismatches_d6=11048075 mismatches_other(info)=11384896
negative control failed as required
RESULT: PASS
rc=0
## V7 Montgomery ROM (tb/arith/check_mont_rom.py)
check 1+2 (Montgomery relation and range, 256 entries): PASS
check 3 (generator reproduces the file): PASS
check 4 (negative control, rom_zeta[17] + 1): fails as required
RESULT: PASS
rc=0
## V3/V4 unit tests verilator
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/ntt/modmul_reduce_staged.sv:42:18: Signal unoptimizable: Circular combinational logic: 'modmul_c4_tb.u_dut.g_staged.u_red.s_in'
%Warning-WIDTHTRUNC: /home/ajil/FPGA/Projects/CHIPATON/tb/arith/c4_tb_wrappers.sv:12:28: Operator VAR 'REG_AFTER' expects 16 bits on the Initial value, but Initial value's CONST '32'h821' generates 32 bits.
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/ntt/modmul_reduce_staged.sv:43:18: Signal unoptimizable: Circular combinational logic: 'modmul_c4_tb.u_dut.g_staged.u_red.s_cut'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/ntt/modmul_reduce_staged.sv:42:18: Signal unoptimizable: Circular combinational logic: 'butterfly_c4_tb.u_dut.u_mul.g_staged.u_red.s_in'
%Warning-WIDTHTRUNC: /home/ajil/FPGA/Projects/CHIPATON/tb/arith/c4_tb_wrappers.sv:27:28: Operator VAR 'MUL_REG' expects 16 bits on the Initial value, but Initial value's CONST '32'h821' generates 32 bits.
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/ntt/modmul_reduce_staged.sv:43:18: Signal unoptimizable: Circular combinational logic: 'butterfly_c4_tb.u_dut.u_mul.g_staged.u_red.s_cut'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_fold.sv:68:18: Signal unoptimizable: Circular combinational logic: 'modmul_c4_tb.u_dut.g_fold.u_red.r'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_fold.sv:43:18: Signal unoptimizable: Circular combinational logic: 'modmul_c4_tb.u_dut.g_fold.u_red.s_in'
%Warning-WIDTHTRUNC: /home/ajil/FPGA/Projects/CHIPATON/tb/arith/c4_tb_wrappers.sv:12:28: Operator VAR 'REG_AFTER' expects 16 bits on the Initial value, but Initial value's CONST '32'h29' generates 32 bits.
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_fold.sv:44:18: Signal unoptimizable: Circular combinational logic: 'modmul_c4_tb.u_dut.g_fold.u_red.s_cut'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_fold.sv:68:18: Signal unoptimizable: Circular combinational logic: 'butterfly_c4_tb.u_dut.u_mul.g_fold.u_red.r'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_fold.sv:43:18: Signal unoptimizable: Circular combinational logic: 'butterfly_c4_tb.u_dut.u_mul.g_fold.u_red.s_in'
%Warning-WIDTHTRUNC: /home/ajil/FPGA/Projects/CHIPATON/tb/arith/c4_tb_wrappers.sv:27:28: Operator VAR 'MUL_REG' expects 16 bits on the Initial value, but Initial value's CONST '32'h29' generates 32 bits.
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_fold.sv:44:18: Signal unoptimizable: Circular combinational logic: 'butterfly_c4_tb.u_dut.u_mul.g_fold.u_red.s_cut'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_barrett.sv:60:18: Signal unoptimizable: Circular combinational logic: 'modmul_c4_tb.u_dut.g_barrett.u_red.p3'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_barrett.sv:52:22: Signal unoptimizable: Circular combinational logic: 'modmul_c4_tb.u_dut.g_barrett.u_red.r2'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_barrett.sv:40:18: Signal unoptimizable: Circular combinational logic: 'modmul_c4_tb.u_dut.g_barrett.u_red.s_in'
%Warning-WIDTHTRUNC: /home/ajil/FPGA/Projects/CHIPATON/tb/arith/c4_tb_wrappers.sv:12:28: Operator VAR 'REG_AFTER' expects 16 bits on the Initial value, but Initial value's CONST '32'h7' generates 32 bits.
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_barrett.sv:41:18: Signal unoptimizable: Circular combinational logic: 'modmul_c4_tb.u_dut.g_barrett.u_red.s_cut'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_barrett.sv:60:18: Signal unoptimizable: Circular combinational logic: 'butterfly_c4_tb.u_dut.u_mul.g_barrett.u_red.p3'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_barrett.sv:52:22: Signal unoptimizable: Circular combinational logic: 'butterfly_c4_tb.u_dut.u_mul.g_barrett.u_red.r2'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_barrett.sv:40:18: Signal unoptimizable: Circular combinational logic: 'butterfly_c4_tb.u_dut.u_mul.g_barrett.u_red.s_in'
%Warning-WIDTHTRUNC: /home/ajil/FPGA/Projects/CHIPATON/tb/arith/c4_tb_wrappers.sv:27:28: Operator VAR 'MUL_REG' expects 16 bits on the Initial value, but Initial value's CONST '32'h7' generates 32 bits.
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_barrett.sv:41:18: Signal unoptimizable: Circular combinational logic: 'butterfly_c4_tb.u_dut.u_mul.g_barrett.u_red.s_cut'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_montgomery.sv:61:18: Signal unoptimizable: Circular combinational logic: 'modmul_c4_tb.u_dut.g_mont.u_red.p3'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_montgomery.sv:53:22: Signal unoptimizable: Circular combinational logic: 'modmul_c4_tb.u_dut.g_mont.u_red.sum2'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_montgomery.sv:40:18: Signal unoptimizable: Circular combinational logic: 'modmul_c4_tb.u_dut.g_mont.u_red.s_in'
%Warning-WIDTHTRUNC: /home/ajil/FPGA/Projects/CHIPATON/tb/arith/c4_tb_wrappers.sv:12:28: Operator VAR 'REG_AFTER' expects 16 bits on the Initial value, but Initial value's CONST '32'h7' generates 32 bits.
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_montgomery.sv:41:18: Signal unoptimizable: Circular combinational logic: 'modmul_c4_tb.u_dut.g_mont.u_red.s_cut'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_montgomery.sv:61:18: Signal unoptimizable: Circular combinational logic: 'butterfly_c4_tb.u_dut.u_mul.g_mont.u_red.p3'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_montgomery.sv:53:22: Signal unoptimizable: Circular combinational logic: 'butterfly_c4_tb.u_dut.u_mul.g_mont.u_red.sum2'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_montgomery.sv:40:18: Signal unoptimizable: Circular combinational logic: 'butterfly_c4_tb.u_dut.u_mul.g_mont.u_red.s_in'
%Warning-WIDTHTRUNC: /home/ajil/FPGA/Projects/CHIPATON/tb/arith/c4_tb_wrappers.sv:27:28: Operator VAR 'MUL_REG' expects 16 bits on the Initial value, but Initial value's CONST '32'h7' generates 32 bits.
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_montgomery.sv:41:18: Signal unoptimizable: Circular combinational logic: 'butterfly_c4_tb.u_dut.u_mul.g_mont.u_red.s_cut'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_barrett_lazy.sv:59:18: Signal unoptimizable: Circular combinational logic: 'modmul_barrett_lazy.p3'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_barrett_lazy.sv:51:22: Signal unoptimizable: Circular combinational logic: 'modmul_barrett_lazy.r2'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_barrett_lazy.sv:39:18: Signal unoptimizable: Circular combinational logic: 'modmul_barrett_lazy.s_in'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_barrett_lazy.sv:59:18: Signal unoptimizable: Circular combinational logic: 'butterfly_c4_lazy.u_mul.p3'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_barrett_lazy.sv:51:22: Signal unoptimizable: Circular combinational logic: 'butterfly_c4_lazy.u_mul.r2'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_barrett_lazy.sv:39:18: Signal unoptimizable: Circular combinational logic: 'butterfly_c4_lazy.u_mul.s_in'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_barrett_lazy.sv:59:18: Signal unoptimizable: Circular combinational logic: 'butterfly_c4_lazy.u_mul.p3'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_barrett_lazy.sv:51:22: Signal unoptimizable: Circular combinational logic: 'butterfly_c4_lazy.u_mul.r2'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_barrett_lazy.sv:39:18: Signal unoptimizable: Circular combinational logic: 'butterfly_c4_lazy.u_mul.s_in'
%Warning-WIDTHTRUNC: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_barrett_lazy.sv:25:27: Operator VAR 'REG_AFTER' expects 4 bits on the Initial value, but Initial value's CONST '32'h7' generates 32 bits.
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_barrett_lazy.sv:40:18: Signal unoptimizable: Circular combinational logic: 'modmul_barrett_lazy.s_cut'
%Warning-WIDTHTRUNC: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/butterfly_c4_lazy.sv:20:28: Operator VAR 'MUL_REG' expects 16 bits on the Initial value, but Initial value's CONST '32'h7' generates 32 bits.
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_barrett_lazy.sv:40:18: Signal unoptimizable: Circular combinational logic: 'butterfly_c4_lazy.u_mul.s_cut'
%Warning-WIDTHTRUNC: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/butterfly_c4_lazy.sv:20:28: Operator VAR 'MUL_REG' expects 16 bits on the Initial value, but Initial value's CONST '32'h7' generates 32 bits.
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_barrett_lazy.sv:40:18: Signal unoptimizable: Circular combinational logic: 'butterfly_c4_lazy.u_mul.s_cut'
[verilator] modmul_c4_tb RED_KIND=0 REG_AFTER=0: 3/3 PASS
[verilator] modmul_c4_tb RED_KIND=0 REG_AFTER=2081: 3/3 PASS
[verilator] butterfly_c4_tb RED_KIND=0 MUL_REG=0: 2/2 PASS
[verilator] butterfly_c4_tb RED_KIND=0 MUL_REG=2081: 2/2 PASS
[verilator] modmul_c4_tb RED_KIND=1 REG_AFTER=0: 3/3 PASS
[verilator] modmul_c4_tb RED_KIND=1 REG_AFTER=41: 3/3 PASS
[verilator] butterfly_c4_tb RED_KIND=1 MUL_REG=0: 2/2 PASS
[verilator] butterfly_c4_tb RED_KIND=1 MUL_REG=41: 2/2 PASS
[verilator] modmul_c4_tb RED_KIND=2 REG_AFTER=0: 3/3 PASS
[verilator] modmul_c4_tb RED_KIND=2 REG_AFTER=7: 3/3 PASS
[verilator] butterfly_c4_tb RED_KIND=2 MUL_REG=0: 2/2 PASS
[verilator] butterfly_c4_tb RED_KIND=2 MUL_REG=7: 2/2 PASS
[verilator] modmul_c4_tb RED_KIND=3 REG_AFTER=0: 3/3 PASS
[verilator] modmul_c4_tb RED_KIND=3 REG_AFTER=7: 3/3 PASS
[verilator] butterfly_c4_tb RED_KIND=3 MUL_REG=0: 2/2 PASS
[verilator] butterfly_c4_tb RED_KIND=3 MUL_REG=7: 2/2 PASS
[verilator] modmul_barrett_lazy REG_AFTER=0 (a<q, b<q regression of 5b): 3/3 PASS
[verilator] butterfly_c4_lazy MUL_REG=0 [test_butterfly_pipe]: 2/2 PASS
[verilator] butterfly_c4_lazy MUL_REG=0 [test_lazy_corners]: 1/1 PASS
[verilator] modmul_barrett_lazy REG_AFTER=7 (a<q, b<q regression of 5b): 3/3 PASS
[verilator] butterfly_c4_lazy MUL_REG=7 [test_butterfly_pipe]: 2/2 PASS
[verilator] butterfly_c4_lazy MUL_REG=7 [test_lazy_corners]: 1/1 PASS
[verilator] TOTAL: 52/52 passed
rc=0
## V5/V6/V7 core tests verilator
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:74:33: 'en_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:75:33: 'wr_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:76:33: 'bank_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:77:33: 'off_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:78:33: 'slot_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:79:33: 'count_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:76:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4a.u_core.u_mem.bank_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:94:31: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4a.u_core.u_mem.g_arb[0].count_in'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:78:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4a.u_core.u_mem.slot_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:74:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4a.u_core.u_mem.en_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_fold.sv:44:18: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4a.u_core.g_lane[7].g_bfly.u_bfly.u_mul.g_fold.u_red.s_cut'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:75:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4a.u_core.u_mem.wr_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:77:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4a.u_core.u_mem.off_s'
                                                            V7 negative control: a depth beyond the schedule's slack. This test PASSES only if the scoreboard
%Warning-WIDTHEXPAND: /home/ajil/FPGA/Projects/CHIPATON/rtl/ntt/ntt_core_c4.sv:31:28: Operator VAR 'ARB_REG' expects 33 bits on the Initial value, but Initial value's CONST '32'h10810' generates 32 bits.
%Warning-WIDTHTRUNC: /home/ajil/FPGA/Projects/CHIPATON/rtl/ntt/ntt_core_c4.sv:34:28: Operator VAR 'MUL_REG' expects 16 bits on the Initial value, but Initial value's CONST '32'h821' generates 32 bits.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:74:33: 'en_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:75:33: 'wr_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:76:33: 'bank_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:77:33: 'off_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:78:33: 'slot_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:79:33: 'count_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:76:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4.u_mem.bank_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:94:31: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4.u_mem.g_arb[0].count_in'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:78:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4.u_mem.slot_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:74:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4.u_mem.en_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/ntt/modmul_reduce_staged.sv:43:18: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4.g_lane[7].g_bfly.u_bfly.u_mul.g_staged.u_red.s_cut'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:75:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4.u_mem.wr_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:77:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4.u_mem.off_s'
                                                            V7 negative control: a depth beyond the schedule's slack. This test PASSES only if the scoreboard
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:74:33: 'en_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:75:33: 'wr_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:76:33: 'bank_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:77:33: 'off_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:78:33: 'slot_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:79:33: 'count_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:76:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4b_b.u_core.u_mem.bank_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:94:31: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4b_b.u_core.u_mem.g_arb[0].count_in'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:78:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4b_b.u_core.u_mem.slot_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:74:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4b_b.u_core.u_mem.en_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_barrett.sv:41:18: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4b_b.u_core.g_lane[7].g_bfly.u_bfly.u_mul.g_barrett.u_red.s_cut'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:75:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4b_b.u_core.u_mem.wr_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:77:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4b_b.u_core.u_mem.off_s'
                                                            V7 negative control: a depth beyond the schedule's slack. This test PASSES only if the scoreboard
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:74:33: 'en_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:75:33: 'wr_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:76:33: 'bank_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:77:33: 'off_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:78:33: 'slot_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:79:33: 'count_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:76:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4b_m.u_core.u_mem.bank_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:94:31: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4b_m.u_core.u_mem.g_arb[0].count_in'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:78:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4b_m.u_core.u_mem.slot_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:74:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4b_m.u_core.u_mem.en_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_montgomery.sv:41:18: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4b_m.u_core.g_lane[7].g_bfly.u_bfly.u_mul.g_mont.u_red.s_cut'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:75:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4b_m.u_core.u_mem.wr_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:77:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4b_m.u_core.u_mem.off_s'
                                                            V7 negative control: a depth beyond the schedule's slack. This test PASSES only if the scoreboard
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:74:33: 'en_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:75:33: 'wr_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:76:33: 'bank_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:77:33: 'off_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:78:33: 'slot_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:79:33: 'count_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:76:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4c.u_core.u_mem.bank_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:94:31: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4c.u_core.u_mem.g_arb[0].count_in'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:78:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4c.u_core.u_mem.slot_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:74:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4c.u_core.u_mem.en_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_barrett_lazy.sv:40:18: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4c.u_core.g_lane[7].g_bfly_lazy.u_bfly.u_mul.s_cut'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_barrett.sv:41:18: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4c.u_core.u_scale_mul.g_barrett.u_red.s_cut'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:75:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4c.u_core.u_mem.wr_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:77:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4c.u_core.u_mem.off_s'
                                                            V7 negative control: a depth beyond the schedule's slack. This test PASSES only if the scoreboard
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:74:33: 'en_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:75:33: 'wr_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:76:33: 'bank_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:77:33: 'off_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:78:33: 'slot_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:79:33: 'count_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:76:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4b_m.u_core.u_mem.bank_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:94:31: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4b_m.u_core.u_mem.g_arb[0].count_in'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:78:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4b_m.u_core.u_mem.slot_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:74:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4b_m.u_core.u_mem.en_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_montgomery.sv:41:18: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4b_m.u_core.g_lane[7].g_bfly.u_bfly.u_mul.g_mont.u_red.s_cut'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:75:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4b_m.u_core.u_mem.wr_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:77:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4b_m.u_core.u_mem.off_s'
                                                            V7 negative control: a depth beyond the schedule's slack. This test PASSES only if the scoreboard
%Warning-WIDTHTRUNC: /home/ajil/FPGA/Projects/CHIPATON/rtl/ntt/ntt_core_c4.sv:34:28: Operator VAR 'MUL_REG' expects 16 bits on the Initial value, but Initial value's CONST '32'hff' generates 32 bits.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:74:33: 'en_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:75:33: 'wr_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:76:33: 'bank_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:77:33: 'off_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:78:33: 'slot_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:79:33: 'count_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:76:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4.u_mem.bank_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:94:31: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4.u_mem.g_arb[0].count_in'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:78:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4.u_mem.slot_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:74:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4.u_mem.en_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/ntt/modmul_reduce_staged.sv:43:18: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4.g_lane[7].g_bfly.u_bfly.u_mul.g_staged.u_red.s_cut'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:75:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4.u_mem.wr_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_pipe.sv:77:33: Signal unoptimizable: Circular combinational logic: 'ntt_core_c4.u_mem.off_s'
                                                            V7 negative control: a depth beyond the schedule's slack. This test PASSES only if the scoreboard
 77146.00ns INFO     cocotb.ntt_core_c4                 negative control P=8: (violations, wrong results of 5) = {'NTT': (640, 5), 'INTT': (640, 5)}; first violation: ('read-issued-before-write-landed', 329, 8, 329)
[verilator] c4a (ntt_core_c4a): 5/5 PASS  {'P': 6, 'RDLAT': 3, 'WRDLY': 3, 'cycles_NTT': 119, 'cycles_INTT': 375, 'stall_NTT': 0, 'stall_INTT': 0}
[verilator] c4k0 (ntt_core_c4): 5/5 PASS  {'P': 6, 'RDLAT': 3, 'WRDLY': 3, 'cycles_NTT': 119, 'cycles_INTT': 375, 'stall_NTT': 0, 'stall_INTT': 0}
[verilator] c4bb (ntt_core_c4b_b): 5/5 PASS  {'P': 6, 'RDLAT': 3, 'WRDLY': 3, 'cycles_NTT': 119, 'cycles_INTT': 375, 'stall_NTT': 0, 'stall_INTT': 0}
[verilator] c4bm (ntt_core_c4b_m): 5/5 PASS  {'P': 6, 'RDLAT': 3, 'WRDLY': 3, 'cycles_NTT': 119, 'cycles_INTT': 375, 'stall_NTT': 0, 'stall_INTT': 0}
[verilator] c4c (ntt_core_c4c): 5/5 PASS  {'P': 6, 'RDLAT': 3, 'WRDLY': 3, 'cycles_NTT': 119, 'cycles_INTT': 375, 'stall_NTT': 0, 'stall_INTT': 0}
[verilator] negrom (ntt_core_c4b_m): bit-exact tests failed as required: ['test_ntt_bit_exact', 'test_intt_bit_exact']
[verilator] negctl (ntt_core_c4): 1/1 PASS  {'negctl_P': 8, 'violations_NTT': 640, 'wrong_NTT': 5, 'violations_INTT': 640, 'wrong_INTT': 5}
[verilator] TOTAL: 27/27 passed
rc=0
## V3/V4 unit tests icarus
[icarus] modmul_c4_tb RED_KIND=0 REG_AFTER=0: 3/3 PASS
[icarus] modmul_c4_tb RED_KIND=0 REG_AFTER=2081: 3/3 PASS
[icarus] butterfly_c4_tb RED_KIND=0 MUL_REG=0: 2/2 PASS
[icarus] butterfly_c4_tb RED_KIND=0 MUL_REG=2081: 2/2 PASS
[icarus] modmul_c4_tb RED_KIND=1 REG_AFTER=0: 3/3 PASS
[icarus] modmul_c4_tb RED_KIND=1 REG_AFTER=41: 3/3 PASS
[icarus] butterfly_c4_tb RED_KIND=1 MUL_REG=0: 2/2 PASS
[icarus] butterfly_c4_tb RED_KIND=1 MUL_REG=41: 2/2 PASS
[icarus] modmul_c4_tb RED_KIND=2 REG_AFTER=0: 3/3 PASS
[icarus] modmul_c4_tb RED_KIND=2 REG_AFTER=7: 3/3 PASS
[icarus] butterfly_c4_tb RED_KIND=2 MUL_REG=0: 2/2 PASS
[icarus] butterfly_c4_tb RED_KIND=2 MUL_REG=7: 2/2 PASS
[icarus] modmul_c4_tb RED_KIND=3 REG_AFTER=0: 3/3 PASS
[icarus] modmul_c4_tb RED_KIND=3 REG_AFTER=7: 3/3 PASS
[icarus] butterfly_c4_tb RED_KIND=3 MUL_REG=0: 2/2 PASS
[icarus] butterfly_c4_tb RED_KIND=3 MUL_REG=7: 2/2 PASS
[icarus] modmul_barrett_lazy REG_AFTER=0 (a<q, b<q regression of 5b): 3/3 PASS
[icarus] butterfly_c4_lazy MUL_REG=0 [test_butterfly_pipe]: 2/2 PASS
[icarus] butterfly_c4_lazy MUL_REG=0 [test_lazy_corners]: 1/1 PASS
[icarus] modmul_barrett_lazy REG_AFTER=7 (a<q, b<q regression of 5b): 3/3 PASS
[icarus] butterfly_c4_lazy MUL_REG=7 [test_butterfly_pipe]: 2/2 PASS
[icarus] butterfly_c4_lazy MUL_REG=7 [test_lazy_corners]: 1/1 PASS
[icarus] TOTAL: 52/52 passed
rc=0
## V5/V6/V7 core tests icarus
                                                            V7 negative control: a depth beyond the schedule's slack. This test PASSES only if the scoreboard
                                                            V7 negative control: a depth beyond the schedule's slack. This test PASSES only if the scoreboard
                                                            V7 negative control: a depth beyond the schedule's slack. This test PASSES only if the scoreboard
                                                            V7 negative control: a depth beyond the schedule's slack. This test PASSES only if the scoreboard
                                                            V7 negative control: a depth beyond the schedule's slack. This test PASSES only if the scoreboard
                                                            V7 negative control: a depth beyond the schedule's slack. This test PASSES only if the scoreboard
                                                            V7 negative control: a depth beyond the schedule's slack. This test PASSES only if the scoreboard
 77146.00ns INFO     cocotb.ntt_core_c4                 negative control P=8: (violations, wrong results of 5) = {'NTT': (640, 5), 'INTT': (640, 5)}; first violation: ('read-issued-before-write-landed', 329, 8, 329)
[icarus] c4a (ntt_core_c4a): 5/5 PASS  {'P': 6, 'RDLAT': 3, 'WRDLY': 3, 'cycles_NTT': 119, 'cycles_INTT': 375, 'stall_NTT': 0, 'stall_INTT': 0}
[icarus] c4k0 (ntt_core_c4): 5/5 PASS  {'P': 6, 'RDLAT': 3, 'WRDLY': 3, 'cycles_NTT': 119, 'cycles_INTT': 375, 'stall_NTT': 0, 'stall_INTT': 0}
[icarus] c4bb (ntt_core_c4b_b): 5/5 PASS  {'P': 6, 'RDLAT': 3, 'WRDLY': 3, 'cycles_NTT': 119, 'cycles_INTT': 375, 'stall_NTT': 0, 'stall_INTT': 0}
[icarus] c4bm (ntt_core_c4b_m): 5/5 PASS  {'P': 6, 'RDLAT': 3, 'WRDLY': 3, 'cycles_NTT': 119, 'cycles_INTT': 375, 'stall_NTT': 0, 'stall_INTT': 0}
[icarus] c4c (ntt_core_c4c): 5/5 PASS  {'P': 6, 'RDLAT': 3, 'WRDLY': 3, 'cycles_NTT': 119, 'cycles_INTT': 375, 'stall_NTT': 0, 'stall_INTT': 0}
[icarus] negrom (ntt_core_c4b_m): bit-exact tests failed as required: ['test_ntt_bit_exact', 'test_intt_bit_exact']
[icarus] negctl (ntt_core_c4): 1/1 PASS  {'negctl_P': 8, 'violations_NTT': 640, 'wrong_NTT': 5, 'violations_INTT': 640, 'wrong_INTT': 5}
[icarus] TOTAL: 27/27 passed
rc=0
OVERALL: PASS
```
## Formal Fase 5 (formal/run/run_formal_phase5.py)
```
| Group | Proof | Expected | Result | Engine detail | Time (s) | As expected |
|---|---|---|---|---|---|---|
| A Phase 5 | c4a (H, O, R, A, B, C) | PASS | PASS | basecase=pass, induction=pass | 10.3 | yes |
| B Negative control | NC-O c4a: bank_map_rom copy, NUM_BANKS=8: bank(128) 2 -> 3 | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c4_formal_top.sv:145 | 8.0 | yes |
| B Negative control | NC-A c4a: delay model of property A one cycle short | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c4_formal_top.sv:146 | 9.2 | yes |
| A Phase 5 | c4b_b (H, O, R, A, B, C) | PASS | PASS | basecase=pass, induction=pass | 25.7 | yes |
| B Negative control | NC-O c4b_b: bank_map_rom copy, NUM_BANKS=8: bank(128) 2 -> 3 | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c4_formal_top.sv:145 | 9.9 | yes |
| B Negative control | NC-A c4b_b: delay model of property A one cycle short | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c4_formal_top.sv:146 | 11.2 | yes |
| A Phase 5 | c4b_m (H, O, R, A, B, C) | PASS | PASS | basecase=pass, induction=pass | 9.9 | yes |
| B Negative control | NC-O c4b_m: bank_map_rom copy, NUM_BANKS=8: bank(128) 2 -> 3 | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c4_formal_top.sv:145 | 7.8 | yes |
| B Negative control | NC-A c4b_m: delay model of property A one cycle short | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c4_formal_top.sv:146 | 8.5 | yes |
| A Phase 5 | c4c (H, O, R, A, B, C) | PASS | PASS | basecase=pass, induction=pass | 47.2 | yes |
| B Negative control | NC-O c4c: bank_map_rom copy, NUM_BANKS=8: bank(128) 2 -> 3 | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c4_formal_top.sv:145 | 9.4 | yes |
| B Negative control | NC-A c4c: delay model of property A one cycle short | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c4_formal_top.sv:146 | 11.3 | yes |
| A Phase 5c | lazy_bfly_io bounds (P1-P3) | PASS | PASS | basecase=pass, induction=pass | 0.6 | yes |
| B Negative control | NC-L: INTT output side value not reduced | FAIL | FAIL | basecase=FAIL, induction=FAIL; failed assert lazy_bfly_io_formal_top.sv:54 | 0.3 | yes |

OVERALL: all results as expected (14/14)
```
