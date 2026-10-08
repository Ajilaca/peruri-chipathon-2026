# MEASURED (simulasi / lint, bukan perangkat keras): Verifikasi Fase 5M S7, scripts/test/phase5m_verify_s7.sh pada git b53309d, 2026-10-02

```
## V1 verilator --lint-only -Wall ntt_core_s7_p7
rc=0
## V1 slang ntt_core_s7_p7
Build succeeded: 0 errors, 0 warnings
rc=0
## V2/V3/V4/V5 verilator
%Warning-WIDTHEXPAND: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:37:28: Operator VAR 'ARB_REG' expects 33 bits on the Initial value, but Initial value's CONST '32'h10810' generates 32 bits.
 83306.00ns INFO     cocotb.regression                  test_poly_mem_split.test_every_address_every_port passed
 89652.00ns INFO     cocotb.regression                  test_poly_mem_split.test_scheduled_traffic passed
 90828.00ns INFO     cocotb.regression                  test_poly_mem_split.test_read_after_write_next_cycle passed
 90964.00ns INFO     cocotb.regression                  test_poly_mem_split.test_overflow_flag_works passed
%Warning-WIDTHEXPAND: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:37:28: Operator VAR 'ARB_REG' expects 33 bits on the Initial value, but Initial value's CONST '32'h10810' generates 32 bits.
 83136.00ns INFO     cocotb.regression                  test_poly_mem_split.test_every_address_every_port passed
 89452.00ns INFO     cocotb.regression                  test_poly_mem_split.test_scheduled_traffic passed
 90528.00ns INFO     cocotb.regression                  test_poly_mem_split.test_read_after_write_next_cycle passed
 90654.00ns INFO     cocotb.regression                  test_poly_mem_split.test_overflow_flag_works passed
%Warning-WIDTHEXPAND: /home/ajil/FPGA/Projects/CHIPATON/tb/phase5m/mem_diff_top.sv:6:28: Operator VAR 'ARB_REG' expects 33 bits on the Initial value, but Initial value's CONST '32'h10810' generates 32 bits.
 60026.00ns INFO     cocotb.regression                  test_poly_mem_diff.test_equal_to_frozen_memory passed
674145.00ns INFO     cocotb.regression                  test_ntt_core_s7.test_ntt_bit_exact passed
1348290.00ns INFO     cocotb.regression                  test_ntt_core_s7.test_intt_bit_exact passed
1990335.00ns INFO     cocotb.regression                  test_ntt_core_s7.test_ntt_intt_roundtrip passed
2247180.00ns INFO     cocotb.regression                  test_ntt_core_s7.test_boundary_directed passed
2568225.00ns INFO     cocotb.regression                  test_ntt_core_s7.test_cycle_count_constant passed
5855310.00ns INFO     cocotb.regression                  test_ntt_core_s7.test_intt_unit_vectors passed
 12885.00ns WARNING  cocotb.regression                  test_ntt_core_s7.test_ntt_bit_exact failed
 25770.00ns WARNING  cocotb.regression                  test_ntt_core_s7.test_intt_bit_exact failed
 38655.00ns WARNING  cocotb.regression                  test_ntt_core_s7.test_ntt_intt_roundtrip failed
 45120.00ns WARNING  cocotb.regression                  test_ntt_core_s7.test_boundary_directed failed
366165.00ns INFO     cocotb.regression                  test_ntt_core_s7.test_cycle_count_constant passed
372630.01ns WARNING  cocotb.regression                  test_ntt_core_s7.test_intt_unit_vectors failed
 12885.00ns WARNING  cocotb.regression                  test_ntt_core_s7.test_ntt_bit_exact failed
 25770.00ns WARNING  cocotb.regression                  test_ntt_core_s7.test_intt_bit_exact failed
 38655.00ns WARNING  cocotb.regression                  test_ntt_core_s7.test_ntt_intt_roundtrip failed
 45120.00ns WARNING  cocotb.regression                  test_ntt_core_s7.test_boundary_directed failed
366165.00ns INFO     cocotb.regression                  test_ntt_core_s7.test_cycle_count_constant passed
372630.01ns WARNING  cocotb.regression                  test_ntt_core_s7.test_intt_unit_vectors failed
[verilator] mem1 (RD_SPLIT=1): 4/4 PASS
[verilator] mem0 (RD_SPLIT=0): 4/4 PASS
[verilator] memdiff: 1/1 PASS
[verilator] s7: 6/6 PASS  {'P': 7, 'RDLAT': 4, 'WRDLY': 3, 'cycles_NTT': 120, 'cycles_INTT': 120, 'stall_NTT': 0, 'stall_INTT': 0}
[verilator] ncd: bit-exact NTT and INTT failed as required: True; failed=['test_ntt_bit_exact', 'test_intt_bit_exact', 'test_ntt_intt_roundtrip', 'test_boundary_directed', 'test_intt_unit_vectors']
[verilator] ncs: bit-exact NTT and INTT failed as required: True; failed=['test_ntt_bit_exact', 'test_intt_bit_exact', 'test_ntt_intt_roundtrip', 'test_boundary_directed', 'test_intt_unit_vectors']
[verilator] TOTAL: 17/17 passed
rc=0
## V2/V3/V4/V5 icarus
 83306.00ns INFO     cocotb.regression                  test_poly_mem_split.test_every_address_every_port passed
 89652.00ns INFO     cocotb.regression                  test_poly_mem_split.test_scheduled_traffic passed
 90828.00ns INFO     cocotb.regression                  test_poly_mem_split.test_read_after_write_next_cycle passed
 90964.00ns INFO     cocotb.regression                  test_poly_mem_split.test_overflow_flag_works passed
 83136.00ns INFO     cocotb.regression                  test_poly_mem_split.test_every_address_every_port passed
 89452.00ns INFO     cocotb.regression                  test_poly_mem_split.test_scheduled_traffic passed
 90528.00ns INFO     cocotb.regression                  test_poly_mem_split.test_read_after_write_next_cycle passed
 90654.00ns INFO     cocotb.regression                  test_poly_mem_split.test_overflow_flag_works passed
 60026.00ns INFO     cocotb.regression                  test_poly_mem_diff.test_equal_to_frozen_memory passed
674145.00ns INFO     cocotb.regression                  test_ntt_core_s7.test_ntt_bit_exact passed
1348290.00ns INFO     cocotb.regression                  test_ntt_core_s7.test_intt_bit_exact passed
1990335.00ns INFO     cocotb.regression                  test_ntt_core_s7.test_ntt_intt_roundtrip passed
2247180.00ns INFO     cocotb.regression                  test_ntt_core_s7.test_boundary_directed passed
2568225.00ns INFO     cocotb.regression                  test_ntt_core_s7.test_cycle_count_constant passed
5855310.00ns INFO     cocotb.regression                  test_ntt_core_s7.test_intt_unit_vectors passed
 12885.00ns WARNING  cocotb.regression                  test_ntt_core_s7.test_ntt_bit_exact failed
 25770.00ns WARNING  cocotb.regression                  test_ntt_core_s7.test_intt_bit_exact failed
 38655.00ns WARNING  cocotb.regression                  test_ntt_core_s7.test_ntt_intt_roundtrip failed
 45120.00ns WARNING  cocotb.regression                  test_ntt_core_s7.test_boundary_directed failed
366165.00ns INFO     cocotb.regression                  test_ntt_core_s7.test_cycle_count_constant passed
372630.01ns WARNING  cocotb.regression                  test_ntt_core_s7.test_intt_unit_vectors failed
 12885.00ns WARNING  cocotb.regression                  test_ntt_core_s7.test_ntt_bit_exact failed
 25770.00ns WARNING  cocotb.regression                  test_ntt_core_s7.test_intt_bit_exact failed
 38655.00ns WARNING  cocotb.regression                  test_ntt_core_s7.test_ntt_intt_roundtrip failed
 45120.00ns WARNING  cocotb.regression                  test_ntt_core_s7.test_boundary_directed failed
366165.00ns INFO     cocotb.regression                  test_ntt_core_s7.test_cycle_count_constant passed
372630.01ns WARNING  cocotb.regression                  test_ntt_core_s7.test_intt_unit_vectors failed
[icarus] mem1 (RD_SPLIT=1): 4/4 PASS
[icarus] mem0 (RD_SPLIT=0): 4/4 PASS
[icarus] memdiff: 1/1 PASS
[icarus] s7: 6/6 PASS  {'P': 7, 'RDLAT': 4, 'WRDLY': 3, 'cycles_NTT': 120, 'cycles_INTT': 120, 'stall_NTT': 0, 'stall_INTT': 0}
[icarus] ncd: bit-exact NTT and INTT failed as required: True; failed=['test_ntt_bit_exact', 'test_intt_bit_exact', 'test_ntt_intt_roundtrip', 'test_boundary_directed', 'test_intt_unit_vectors']
[icarus] ncs: bit-exact NTT and INTT failed as required: True; failed=['test_ntt_bit_exact', 'test_intt_bit_exact', 'test_ntt_intt_roundtrip', 'test_boundary_directed', 'test_intt_unit_vectors']
[icarus] TOTAL: 17/17 passed
rc=0
OVERALL: PASS
```

Catatan: baris `%Warning-WIDTHEXPAND` berasal dari build cocotb Verilator untuk top uji (runner dibangun dengan `-Wno-fatal`; parameter ARB_REG diberikan sebagai konstanta 32 bit ke parameter 33 bit oleh runner). Baris itu bukan bagian lint V1 untuk RTL, yang 0 peringatan (dua langkah pertama). Baris cocotb yang berulang adalah log per-test simulator; kegagalan di blok `ncd` / `ncs` adalah kontrol negatif dan memang diharuskan.
