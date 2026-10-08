# Run simulator Fase 9F S2, 2026-10-04 (V2, V3, V4, V6, V7, V8)

MEASURED (hanya simulasi). Perintah: V2-V4 `tb/s10/run_s10_tests.py <sim> mem6 s10p6 ncm6 ncw6`; V6 `KP_VAR=2 KP_CORE_R2=0 KP_NTT_P6=1 tb/smp/run_smp_tests.py <sim> top nchaz`; V7 lingkungan `CORE_TOP=mlkem_core3 CORE_SMP0=1 CORE_K0=1 CORE_W2=1 CORE_P6=1`: `tb/mlkem/run_core_tests.py verilator core nclen ncoff ncrom` dan `... icarus core nclen`; V8 nilai bawaan tanpa variabel itu: `tb/s10/run_s10_tests.py verilator` dan `tb/mlkem/run_core_tests.py verilator core`. Pada log inti Icarus satu baris `test_constant_cycles FAIL` milik kontrol `nclen` (harus gagal); baris `[icarus] core: 6/6 PASS` adalah run nyata.

## V2-V4 inti NTT dan memori pada P = 6, Verilator
```
[verilator] mem6 (RD_LAT=2, WR_DELAY=4): 4/4 PASS
[verilator] s10p6: 6/6 PASS  {'P': 6, 'RDLAT': 2, 'WRDLY': 4, 'cycles_NTT': 119, 'cycles_INTT': 119, 'stall_NTT': 0, 'stall_INTT': 0}
[verilator] ncm6: bit-exact NTT and INTT failed as required: True; failed=['test_ntt_bit_exact', 'test_intt_bit_exact', 'test_ntt_intt_roundtrip', 'test_boundary_directed', 'test_cycle_count_constant', 'test_intt_unit_vectors']
[verilator] ncw6: bit-exact NTT and INTT failed as required: True; failed=['test_ntt_bit_exact', 'test_intt_bit_exact', 'test_ntt_intt_roundtrip', 'test_boundary_directed', 'test_intt_unit_vectors']
[verilator] TOTAL: 12/12 passed
```

## V2-V4, Icarus
```
[icarus] mem6 (RD_LAT=2, WR_DELAY=4): 4/4 PASS
[icarus] s10p6: 6/6 PASS  {'P': 6, 'RDLAT': 2, 'WRDLY': 4, 'cycles_NTT': 119, 'cycles_INTT': 119, 'stall_NTT': 0, 'stall_INTT': 0}
[icarus] ncm6: bit-exact NTT and INTT failed as required: True; failed=['test_ntt_bit_exact', 'test_intt_bit_exact', 'test_ntt_intt_roundtrip', 'test_boundary_directed', 'test_cycle_count_constant', 'test_intt_unit_vectors']
[icarus] ncw6: bit-exact NTT and INTT failed as required: True; failed=['test_ntt_bit_exact', 'test_intt_bit_exact', 'test_ntt_intt_roundtrip', 'test_boundary_directed', 'test_intt_unit_vectors']
[icarus] TOTAL: 12/12 passed
```

## V6 test sequencer, NTT_P6 = 1, sampler K0
```
[verilator] top (VAR=2): 3/3 PASS
[verilator] nchaz: test_programs_bit_exact failed as required: True; failed=['test_programs_bit_exact', 'test_constant_cycles_fixed_rho']
[verilator] TOTAL: 4/4 passed
[icarus] top (VAR=2): 3/3 PASS
[icarus] nchaz: test_programs_bit_exact failed as required: True; failed=['test_programs_bit_exact', 'test_constant_cycles_fixed_rho']
[icarus] TOTAL: 4/4 passed
```

## V7 inti mlkem_core3 pada K2 (NTT_P6 = 1), Verilator
```
2169885.00ns INFO     cocotb.mlkem_core3                 ACVP keyGen: 25 vectors equal
4795610.00ns INFO     cocotb.mlkem_core3                 ACVP encapsulation: 25 vectors equal
6397605.00ns INFO     cocotb.mlkem_core3                 ACVP decapsulation: 10 vectors equal
16638980.00ns INFO     cocotb.mlkem_core3                 20 random cases equal (keygen, encaps, decaps valid and modified, chain)
23089220.00ns INFO     cocotb.mlkem_core3                 constant cycles: Encaps [10194], Decaps [15563]; KeyGen over the ACVP seeds: min 8344, max 8397
[verilator] core: 6/6 PASS
[verilator] nclen: test_acvp_encaps failed as required: True; failed=['test_acvp_keygen', 'test_acvp_encaps', 'test_acvp_decaps', 'test_random_cross_check_and_chain', 'test_protocol_corner_cases', 'test_constant_cycles']
[verilator] ncoff: test_acvp_decaps failed as required: True; failed=['test_acvp_decaps', 'test_random_cross_check_and_chain', 'test_constant_cycles']
[verilator] ncrom: test_acvp_encaps failed as required: True; failed=['test_acvp_encaps', 'test_acvp_decaps', 'test_random_cross_check_and_chain', 'test_protocol_corner_cases', 'test_constant_cycles']
[verilator] TOTAL: 9/9 passed
```

## V7, Icarus
```
2169885.00ns INFO     cocotb.mlkem_core3                 ACVP keyGen: 25 vectors equal
4795610.00ns INFO     cocotb.mlkem_core3                 ACVP encapsulation: 25 vectors equal
6397605.00ns INFO     cocotb.mlkem_core3                 ACVP decapsulation: 10 vectors equal
16638980.00ns INFO     cocotb.mlkem_core3                 20 random cases equal (keygen, encaps, decaps valid and modified, chain)
23089220.00ns INFO     cocotb.mlkem_core3                 constant cycles: Encaps [10194], Decaps [15563]; KeyGen over the ACVP seeds: min 8344, max 8397
[icarus] core: 6/6 PASS
[icarus] nclen: test_acvp_encaps failed as required: True; failed=['test_acvp_keygen', 'test_acvp_encaps', 'test_acvp_decaps', 'test_random_cross_check_and_chain', 'test_protocol_corner_cases', 'test_constant_cycles']
[icarus] TOTAL: 7/7 passed
```

## V8 regresi bawaan (Verilator)
```
[verilator] mem (RD_LAT=2, WR_DELAY=3): 4/4 PASS
[verilator] s10: 6/6 PASS  {'P': 5, 'RDLAT': 2, 'WRDLY': 3, 'cycles_NTT': 118, 'cycles_INTT': 118, 'stall_NTT': 0, 'stall_INTT': 0}
[verilator] ncm: bit-exact NTT and INTT failed as required: True; failed=['test_ntt_bit_exact', 'test_intt_bit_exact', 'test_ntt_intt_roundtrip', 'test_boundary_directed', 'test_cycle_count_constant', 'test_intt_unit_vectors']
[verilator] ncw: bit-exact NTT and INTT failed as required: True; failed=['test_ntt_bit_exact', 'test_intt_bit_exact', 'test_ntt_intt_roundtrip', 'test_boundary_directed', 'test_intt_unit_vectors']
[verilator] p6 (Phase 6 top with S10): 1/1 PASS  {'keygen': 5475, 'encrypt': 6789, 'decrypt': 3109}
[verilator] TOTAL: 13/13 passed
24558550.00ns INFO     cocotb.mlkem_core                  constant cycles: Encaps [10691], Decaps [16623]; KeyGen over the ACVP seeds: min 9035, max 9076
[verilator] core: 6/6 PASS
[verilator] TOTAL: 6/6 passed
```

Profil (`profile_*.json`): K2 8.416 / 10.250 / 15.619; `NTT_P6 = 0` pada daftar file yang sama 8.404 / 10.236 / 15.597 (sama dengan `../../batch1/9f1b/profile_k1b_verilator.json`); bawaan `mlkem_core` 9.095 / 10.735 / 16.667 (sama dengan Fase 9). Terhadap K1b hanya hitungan RUN yang berubah: +12 / +14 / +22 (2 per transformasi untuk 6 / 7 / 11 transformasi; INFERENCE untuk sebabnya: satu siklus hold-off `hw_q` setelah penulisan host terakhir sebelum start dan satu siklus pengosongan, keduanya ditetapkan oleh `Pipe`). Siklus konstan pada K2 untuk masukan rentang ACVP: Encaps 10.194 dan Decaps 15.563 (K1b 10.180 dan 15.541: +14, +22), KeyGen 8.344-8.397 (K1b 8.332-8.385: +12).
