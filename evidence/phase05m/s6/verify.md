# MEASURED (simulation / lint, not hardware): Phase 5M S6 verification, scripts/test/phase5m_verify.sh at git 4382a5f, 2026-10-02

```
## V1 verilator --lint-only -Wall ntt_core_m6_p6
rc=0
## V1 slang ntt_core_m6_p6
Build succeeded: 0 errors, 0 warnings
rc=0
## V3 golden intt_halving vs intt (pytest)
12 passed in 0.63s
rc=0
## V4 twiddle_rom_half (generated, golden-derived)
check_half_rom: OK, 256 entries (NTT half = frozen ROM, INTT half = zeta/2 mod q), generator reproduces the file
rc=0
## V2/V5/V6/V7 verilator
[verilator] half (half_mod): 1/1 PASS
[verilator] halfneg: exhaustive test failed as required: ['test_half_mod_exhaustive']
[verilator] m6 test_ntt_core_c3: 5/5 PASS  {'P': 6, 'RDLAT': 3, 'WRDLY': 3, 'cycles_NTT': 119, 'cycles_INTT': 119, 'stall_NTT': 0, 'stall_INTT': -256}
[verilator] m6 test_m6_basis: 1/1 PASS
[verilator] nch: INTT bit-exact failed as required: True; NTT bit-exact failed: False; failed=['test_intt_bit_exact', 'test_ntt_intt_roundtrip', 'test_boundary_directed']
[verilator] ncr: INTT bit-exact failed as required: True; NTT bit-exact failed: False; failed=['test_intt_bit_exact', 'test_ntt_intt_roundtrip', 'test_boundary_directed']
[verilator] TOTAL: 10/10 passed
rc=0
## V2/V5/V6/V7 icarus
[icarus] half (half_mod): 1/1 PASS
[icarus] halfneg: exhaustive test failed as required: ['test_half_mod_exhaustive']
[icarus] m6 test_ntt_core_c3: 5/5 PASS  {'P': 6, 'RDLAT': 3, 'WRDLY': 3, 'cycles_NTT': 119, 'cycles_INTT': 119, 'stall_NTT': 0, 'stall_INTT': -256}
[icarus] m6 test_m6_basis: 1/1 PASS
[icarus] nch: INTT bit-exact failed as required: True; NTT bit-exact failed: False; failed=['test_intt_bit_exact', 'test_ntt_intt_roundtrip', 'test_boundary_directed']
[icarus] ncr: INTT bit-exact failed as required: True; NTT bit-exact failed: False; failed=['test_intt_bit_exact', 'test_ntt_intt_roundtrip', 'test_boundary_directed']
[icarus] TOTAL: 10/10 passed
rc=0
OVERALL: PASS
```
