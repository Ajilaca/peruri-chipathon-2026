# Run simulator inti Fase 9M-1 (V3, V5), `CORE_W2=1 tb/mlkem/run_core_tests.py icarus core ncwcore`, 2026-10-04

MEASURED (hanya simulasi), inti dengan `CODEC_W2 = 1` (tugas muat / simpan dua byte). Baris `[icarus] core` adalah seluruh himpunan (ACVP keyGen 25, encapsulation 25, decapsulation 10; uji silang acak dengan CORE_N=20; protokol; siklus konstan); `ncwcore` adalah kontrol negatif NC-W-CORE (pemuat menulis indeks koefisien + 1), yang harus menggagalkan test enkapsulasi ACVP. Hanya baris hasil log yang disimpan; awalan path repository pada traceback kegagalan kontrol yang diharapkan dipendekkan menjadi <repo>.

```
2150515.00ns INFO     cocotb.mlkem_core                  ACVP keyGen: 25 vectors equal
2150515.00ns INFO     cocotb.regression                  test_mlkem_core.test_acvp_keygen passed
4755890.00ns INFO     cocotb.mlkem_core                  ACVP encapsulation: 25 vectors equal
4755890.00ns INFO     cocotb.regression                  test_mlkem_core.test_acvp_encaps passed
6348565.00ns INFO     cocotb.mlkem_core                  ACVP decapsulation: 10 vectors equal
6348565.00ns INFO     cocotb.regression                  test_mlkem_core.test_acvp_decaps passed
V4: random KeyGen, Encaps, Decaps (valid and one-bit-changed ciphertexts) against the unmodified golden, and the chain KeyGen -> Encaps -> Decaps through the RTL.
16521460.00ns INFO     cocotb.regression                  test_mlkem_core.test_random_cross_check_and_chain passed
V5: start, op and host write while busy are ignored; reset in the middle then a clean operation; back to back operations with other keys.
17005695.00ns INFO     cocotb.regression                  test_mlkem_core.test_protocol_corner_cases passed
17005695.00ns INFO     cocotb.regression                  running test_mlkem_core.test_constant_cycles (6/6)
V6: Decaps cycles identical for valid and rejected ciphertexts and for different secret keys with the same ek; Encaps identical for different m with the same ek; KeyGen spread reported.
22932310.00ns INFO     cocotb.mlkem_core                  constant cycles: Encaps [10115], Decaps [15471]; KeyGen over the ACVP seeds: min 8267, max 8308
22932310.00ns INFO     cocotb.regression                  test_mlkem_core.test_constant_cycles passed
** test_mlkem_core.test_constant_cycles                PASS     5926615.00         771.09       7686.02  **
172215.00ns INFO     cocotb.mlkem_core                  ACVP keyGen: 2 vectors equal
172215.00ns INFO     cocotb.regression                  test_mlkem_core.test_acvp_keygen passed
276590.00ns WARNING  cocotb.regression                  test_mlkem_core.test_acvp_encaps failed
436215.00ns WARNING  cocotb.regression                  test_mlkem_core.test_acvp_decaps failed
V4: random KeyGen, Encaps, Decaps (valid and one-bit-changed ciphertexts) against the unmodified golden, and the chain KeyGen -> Encaps -> Decaps through the RTL.
626000.00ns WARNING  cocotb.regression                  test_mlkem_core.test_random_cross_check_and_chain failed
V5: start, op and host write while busy are ignored; reset in the middle then a clean operation; back to back operations with other keys.
730375.00ns WARNING  cocotb.regression                  test_mlkem_core.test_protocol_corner_cases failed
730375.00ns INFO     cocotb.regression                  running test_mlkem_core.test_constant_cycles (6/6)
V6: Decaps cycles identical for valid and rejected ciphertexts and for different secret keys with the same ek; Encaps identical for different m with the same ek; KeyGen spread reported.
834570.01ns WARNING  cocotb.regression                  test_mlkem_core.test_constant_cycles failed
File "<repo>/tb/mlkem/test_mlkem_core.py", line 166, in test_constant_cycles
** test_mlkem_core.test_constant_cycles                FAIL      104195.00          16.28       6401.68  **
[icarus] core: 6/6 PASS
[icarus] ncwcore: test_acvp_encaps failed as required: True; failed=['test_acvp_encaps', 'test_acvp_decaps', 'test_random_cross_check_and_chain', 'test_protocol_corner_cases', 'test_constant_cycles']
[icarus] TOTAL: 7/7 passed
```
