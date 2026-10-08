# Run simulator Fase 9F S2b, 2026-10-05 (V1-V3, V5-V7; run dibuat pada 2026-10-04 dan 2026-10-05)

MEASURED (hanya simulasi). Perintah: V2 dan V3 `tb/s10/run_s10_tests.py <sim> s10p6a ncar`; V5 `KP_VAR=2 KP_CORE_R2=0 KP_NTT_P6=1 KP_NTT_AR=1 tb/smp/run_smp_tests.py <sim> top nchaz`; V6 lingkungan `CORE_TOP=mlkem_core3 CORE_SMP0=1 CORE_K0=1 CORE_W2=1 CORE_P6=1 CORE_AR=1`: `tb/mlkem/run_core_tests.py <sim> core` (Verilator juga `nclen ncoff ncrom`, Icarus juga `nclen`); V7 nilai bawaan tanpa lingkungan: `tb/s10/run_s10_tests.py verilator` dan `tb/mlkem/run_core_tests.py verilator core`. File siklus mentah: `cycles_*_k3.json` di direktori ini.

## V2-V3 inti NTT pada P = 6 dengan alamat issue terregistrasi
```
[verilator] s10p6a: 6/6 PASS  {'P': 6, 'RDLAT': 2, 'WRDLY': 4, 'cycles_NTT': 119, 'cycles_INTT': 119, 'stall_NTT': 0, 'stall_INTT': 0}
[verilator] ncar: bit-exact NTT and INTT failed as required: True; failed=['test_ntt_bit_exact', 'test_intt_bit_exact', 'test_ntt_intt_roundtrip', 'test_boundary_directed', 'test_cycle_count_constant', 'test_intt_unit_vectors']
[verilator] TOTAL: 7/7 passed
[icarus] s10p6a: 6/6 PASS  {'P': 6, 'RDLAT': 2, 'WRDLY': 4, 'cycles_NTT': 119, 'cycles_INTT': 119, 'stall_NTT': 0, 'stall_INTT': 0}
[icarus] ncar: bit-exact NTT and INTT failed as required: True; failed=['test_ntt_bit_exact', 'test_intt_bit_exact', 'test_ntt_intt_roundtrip', 'test_boundary_directed', 'test_cycle_count_constant', 'test_intt_unit_vectors']
```
Catatan run: rantai Icarus 2026-10-05 (`s10p6a ncar`) berakhir setelah `s10p6a` tanpa kontrol (prosesnya hilang, tanpa baris total); kontrol dijalankan ulang sendiri pagi yang sama (baris `ncar` di atas). Kontrol (alamat terregistrasi diambil dari nilai siklus saat ini, terlambat satu siklus) gagal di kedua simulator sesuai syarat.

## V5 test sequencer, `NTT_P6 = 1`, `NTT_AR = 1`, sampler K0
```
[verilator] top (VAR=2): 3/3 PASS
[verilator] nchaz: test_programs_bit_exact failed as required: True; failed=['test_programs_bit_exact', 'test_constant_cycles_fixed_rho']
[verilator] TOTAL: 4/4 passed
[icarus] top (VAR=2): 3/3 PASS
[icarus] nchaz: test_programs_bit_exact failed as required: True; failed=['test_programs_bit_exact', 'test_constant_cycles_fixed_rho']
[icarus] TOTAL: 4/4 passed
```

## V6 inti `mlkem_core3` pada K3 (`NTT_P6 = 1`, `NTT_AR = 1`)
Verilator (run Icarus mencetak nilai yang sama):
```
ACVP keyGen: 25 vectors equal
ACVP encapsulation: 25 vectors equal
ACVP decapsulation: 10 vectors equal
20 random cases equal (keygen, encaps, decaps valid and modified, chain)
constant cycles: Encaps [10194], Decaps [15563]; KeyGen over the ACVP seeds: min 8344, max 8397
[verilator] core: 6/6 PASS
[verilator] nclen: failed as required: True   (test_acvp_encaps and the others fail)
[verilator] ncoff: failed as required: True
[verilator] ncrom: failed as required: True
[verilator] TOTAL: 9/9 passed
[icarus] core: 6/6 PASS
[icarus] nclen: test_acvp_encaps failed as required: True
[icarus] TOTAL: 7/7 passed
```
Jumlah siklus masukan uji identik dengan K2 (Encaps 10.194, Decaps 15.563, KeyGen 8.344-8.397): alamat terregistrasi tidak mengubah siklus mana pun. Masukan profil (`profile_k3_verilator.json`) memberi 8.416 / 10.250 / 15.619, seperti K2.

## V7 regresi pada nilai bawaan (Verilator)
```
[verilator] mem (RD_LAT=2, WR_DELAY=3): 4/4 PASS
[verilator] s10: 6/6 PASS  {'P': 5, 'RDLAT': 2, 'WRDLY': 3, 'cycles_NTT': 118, 'cycles_INTT': 118, 'stall_NTT': 0, 'stall_INTT': 0}
[verilator] ncm / ncw: bit-exact NTT and INTT failed as required: True
[verilator] p6 (Phase 6 top with S10): 1/1 PASS  {'keygen': 5475, 'encrypt': 6789, 'decrypt': 3109}
[verilator] TOTAL: 13/13 passed
[verilator] core (mlkem_core defaults): 6/6 PASS   constant cycles: Encaps [10691], Decaps [16623]; KeyGen 9,035-9,076
```
Nilai bawaan (`AREG = 0`, `NTT_AR = 0`) mempertahankan inti 118 siklus dan inti Fase 9; profil K1b dan K2 tidak berubah (`../9s2/`).

## Yang tidak ditunjukkan ini
Hanya simulasi; argumen kesetaraan (alamat terregistrasi = alamat kombinasional pada setiap siklus sebuah run) diuji oleh hasil bit-exact dan kesetaraan siklus dengan K2, dan oleh properti formal sisi memori (`formal.md`); tidak dibuktikan untuk setiap urutan masukan.
