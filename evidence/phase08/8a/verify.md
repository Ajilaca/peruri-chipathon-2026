<!-- claim-lint: skip-file (internal evidence record, not proposal text) -->
# Run verifikasi Fase 8a (test plan V1, V4-V7, V9), 2026-10-03

Perintah: `. scripts/env.sh && scripts/test/phase8a_verify.sh` (KK_SEEDS = 20). Skrip lebih dulu menjalankan ulang verifikasi K0 (`scripts/test/phase7_verify.sh`, regresi V9: file test K0 kini menerima parameter lingkungan yang nilai bawaannya mereproduksi
K0), lalu me-lint dan menguji `keccak_f1600_r2` dan `keccak_sponge_r2` (dua ronde per siklus) dengan `KK_RPC=2`. Lingkungan: Ubuntu 24.04, OSS CAD Suite (Verilator 5.053, Icarus 14.0, slang, SymbiYosys), cocotb 2.1.0.
Label: MEASURED (keluaran simulasi dan lint run ini; bukan perangkat keras). Keluaran skrip yang difilter:

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

Pembacaan:
- Regresi V9: verifikasi K0 (lint, acuan lawan hashlib 16 pytest, konstanta 0 selisih, permutasi dan sponge K0 di kedua simulator dengan tiga kontrol negatif, `check_params`) kembali OVERALL: PASS setelah perubahan file test.
- V1: Verilator `-Wall` dan slang bersih untuk `keccak_f1600_r2` dan `keccak_sponge_r2` (0 peringatan, 0 kesalahan).
- V4 (`perm`, C5): nol, semua-satu, 1.600 satu-bit, 200 state acak dan rantai 10: state setelah setiap siklus sama dengan jejak acuan setelah ronde 1, 3, ..., 23, keluaran ronde pertama `mid` sama dengan jejak acuan
  setelah ronde 0, 2, ..., 22 (jadi semua 24 ronde dibandingkan), `busy_o` tinggi tepat 12 siklus, `done_o` berpulsa sekali; test port (baca, lane >= 25, xor dan run saat sibuk, clear di tengah permutasi).
- V5 dan V6 (`sponge`, C5): keempat mode bit-exact terhadap hashlib dan sponge acuan; jumlah permutasi sama dengan hitungan acuan; back-pressure, stop, start saat sibuk, reset; 306 titik (mode, panjang, keluaran) dengan jumlah siklus
  identik untuk tiga pesan masing-masing, setiap titik sama dengan rumus dengan p = 14 (`cycles_c5.json`). Identik di Verilator dan Icarus.
- V7: NC-RC (satu bit konstanta ronde 1, dipakai ronde kedua siklus 0), NC-R (11 siklus) dan NC-PAD gagal sesuai syarat di kedua simulator.
