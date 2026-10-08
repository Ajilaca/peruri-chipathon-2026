<!-- claim-lint: skip-file (internal evidence record, not proposal text) -->
# Run verifikasi Fase 7 (test plan V1-V7, V9), 2026-10-03

Perintah: `. scripts/env.sh && scripts/test/phase7_verify.sh` (KK_SEEDS = 20). Lingkungan: Ubuntu 24.04, OSS CAD Suite (Verilator 5.053, Icarus, slang, SymbiYosys), cocotb 2.1.0.
Label: MEASURED (keluaran simulasi dan lint run ini; bukan perangkat keras). Keluaran skrip (difilter oleh skrip sendiri):

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

Pembacaan:
- V1 lint: Verilator `-Wall` dan slang bersih untuk `keccak_f1600` dan `keccak_sponge` (0 peringatan, 0 kesalahan).
- V2: `tb/golden/keccak.py` acuan sama dengan hashlib (16 kasus pytest: setiap panjang 0..3 rate + 1 per mode, panjang ML-KEM, panjang acak hingga 2.000 byte, panjang keluaran SHAKE, jejak per ronde, 1.600 state satu-bit
  semuanya berbeda setelah permutasi, konstanta ronde dan offset rho terhadap nilai FIPS 202).
- V3: `rtl/keccak/keccak_pkg.sv` dibangkitkan ulang dari model acuan, 0 selisih.
- V4 (`perm`): state nol, state semua-satu, 1.600 state satu-bit, 200 state acak dan rantai 10: state setelah setiap ronde sama dengan jejak acuan; `busy_o` tinggi tepat 24 siklus dan `done_o` berpulsa sekali
  untuk setiap state; port baca lane, xor ke lane >= 25 diabaikan, xor dan run saat sibuk diabaikan, clear di tengah permutasi.
- V5 (`sponge`): keempat mode bit-exact terhadap hashlib dan sponge acuan untuk panjang batas test plan, panjang ML-KEM, 20 panjang acak per mode dan semua ukuran keluaran rencana; counter permutasi
  sama dengan hitungan acuan; back-pressure acak di kedua antarmuka; sampah di byte yang diabaikan pada word terakhir; stop di absorb, di permutasi, dan di squeeze (termasuk antara dua blok squeeze);
  start saat sibuk diabaikan; reset di tengah pesan.
- V6: 306 titik (mode, panjang, word keluaran), masing-masing dengan tiga pesan (acak, semua-0x00, semua-0xFF) dan jumlah siklus identik; setiap titik sama dengan rumus FSM (`cycles_k0.json`, `cycles_k0_table.md`).
- V7: kontrol negatif gagal sesuai syarat di kedua simulator: NC-RC (satu bit konstanta ronde 1), NC-R (23 ronde, juga menggagalkan pemeriksaan 24 siklus), NC-PAD (byte domain SHA3 0x1F).
- V9: `check_params.py`: semua parameter terkunci cocok. Tidak ada file RTL atau test yang ada yang diubah di Fase 7 (hanya file baru), jadi regresi Fase 0-6 tidak diperlukan (Amandemen A1 Fase 5M).
