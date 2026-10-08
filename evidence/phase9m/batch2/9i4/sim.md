# Run simulator Fase 9I butir 4, 2026-10-05 (V1-V7)

MEASURED (hanya simulasi). Lingkungan run K4: `CORE_TOP=mlkem_core4 CORE_SMP0=1 CORE_K0=1 CORE_W2=1 CORE_P6=1 CORE_AR=1` (parameter K3). File siklus mentah: `cycles_verilator_core_k4.json`, `cycles_icarus_core_k4.json`; profil `profile_k4_verilator.json`.

## V1 lint, V2 model (dijalankan ulang 2026-10-05 untuk laporan ini)
- `verilator --lint-only -Wall --top-module mlkem_core4 -GCODEC_W2=1 -GNTT_P6=1 -GNTT_AR={0,1} -GSMP_C5=0 -GHASH_C5=0` pada daftar file `tb/mlkem/run_core_tests.py`: rc 0, 0 peringatan pada kedua nilai `NTT_AR`. `slang --top mlkem_core4` (parameter sama, `NTT_AR = 1`): `Build succeeded: 0 errors, 0 warnings`.
- `python3 scripts/build/gen_mlkem_ctl_rom3.py --check`: `rtl/mlkem/mlkem_ctl_rom3.sv equals the generated ROM; static checks passed` (`check_static3`). Perbandingan `mlkem_ctl_model3` dengan `mlkem_ctl_model2` pada empat varian operasi dibuat saat model dibangun dan tidak dijalankan ulang di sini.
- Catatan: build Verilator untuk run profil mencetak peringatan `UNOPTFLAT` untuk `kpke_sched_smp4` (`tb_we_i` lewat grant ke `tb_wready_o`; loop kombinasional pada analisis waktu build, bukan error: simulasi lulus). Peringatan itu tidak muncul pada run `--lint-only` di atas, yang memakai `-Wall` tanpa `--timing`.

## V3 inti K4 (seluruh target `core`)
Verilator dan Icarus mencetak nilai yang sama:
```
ACVP keyGen: 25 vectors equal
ACVP encapsulation: 25 vectors equal
ACVP decapsulation: 10 vectors equal
20 random cases equal (keygen, encaps, decaps valid and modified, chain)
constant cycles: Encaps [9555], Decaps [12933]; KeyGen over the ACVP seeds: min 8344, max 8397
[verilator] core: 6/6 PASS
[icarus] core: 6/6 PASS
[icarus] nclen: test_acvp_encaps failed as required: True
[icarus] TOTAL: 7/7 passed
```
Jumlah siklus Encaps dan Decaps identik di semua masukan yang diuji (K3: 10,194 dan 15,563; jadi -639 dan -2,630 siklus pada masukan test, selisih yang sama seperti pada masukan profil). Run Icarus adalah set ACVP penuh (sekitar 1 jam); run Verilator memakai set yang sama.

## V4 profil pada K4 (Verilator; siklus per state pengendali, masukan tetap)
| Operasi | Total (siklus) | State dengan lebih dari 100 siklus |
|---|---|---|
| KeyGen | 8,416 | RUN 6,740, STP 1,578 (tidak berubah dari K3) |
| Encaps | 9,611 | RUNJ 6,245, LDP 2,068, STP 1,052 |
| Decaps | 12,989 | RUNJ 6,367, LDP 5,047, STP 1,315, CMP 138 |
State `RUNJ` adalah join: ia menghitung siklus saat pengendali menunggu mesin setelah load yang berjalan di belakangnya; load itu dihitung di `LDP` seperti sebelumnya. Detail siklus selain ini ada di json. K3 sebagai pembanding (`../9s2b/profile_k3_verilator.json`): Encaps RUN 8,060 + LDP 1,044; Decaps RUN 11,177 + LDP 2,871.

## Kontrol V5 dan V6 pada `mlkem_core4` (Verilator; RTL repository tidak pernah dimutasi, hanya salinan)
```
[verilator] nclen:   failed as required: True
[verilator] ncoff:   failed as required: True
[verilator] ncrom:   failed as required: True
[verilator] ncprio:  failed as required: True
[verilator] ncwr:    failed as required: True
[verilator] ncjob:   failed as required: True
[verilator] ncthr:   throttled sidecar passes the whole core target: True
[verilator] ncilk:   (host port throttled, interlock removed) failed as required: True
[verilator] ncthrld: (host port granted one cycle in eight, interlock intact) passes the whole core target: True
[verilator] ncgrant: (host write written although the sequencer writes) failed as required: True
[verilator] ncjoin:  (RUNJ does not wait for the engine) failed as required: True
```
Catatan run: run pertama kontrol butir 4 (`ctl_v.log`) memberi 9 dari 11: `ncthrld` gagal pada test siklus konstan dan `ncgrant` tidak gagal. Keduanya adalah kesalahan kontrol, bukan desain: counter throttle `ncthrld` berjalan bebas dan tidak di-reset saat pengendali idle, sehingga jumlah siklus bergantung pada fase counter; dan `ncgrant` memutasi gerbang yang sudah diterapkan loader (mutasinya batal). Keduanya diperbaiki di `tb/mlkem/run_core_tests.py` (counter di-reset saat idle; mutasi dipindah ke `mlkem_ldpoly2o.sv`) dan kontrol dijalankan ulang (`ctl2_v.log`, 3 dari 3 seperti terdaftar di atas, dengan Encaps 11,559 dan Decaps 27,444 siklus pada kasus `ncthrld` yang di-throttle, konstan di semua masukan). Sebelas hasil di atas adalah run kedua untuk `ncilk`, `ncthrld`, dan `ncgrant` dan run pertama untuk yang lain.

## V7 regresi
- `mlkem_core3` pada K3 memberi profil K3 (8,416 / 10,250 / 15,619; `../9s2b/sim.md`), file-nya tidak diubah oleh butir 4.
- `mlkem_core` pada nilai bawaan (Fase 9, Verilator): 6/6 PASS, Encaps 10,691 dan Decaps 16,623 pada masukan test (`../9s2b/sim.md`); nilai bawaan file bersama (`NTT_P6 = 0`, `NTT_AR = 0`) tidak berubah.
- Test sequencer mesin K-PKE dengan parameter K3: 3/3 di kedua simulator (`../9s2b/sim.md`). Varian mesin `kpke_sched_smp4` hanya diuji lewat `mlkem_core4`; ia tidak punya unit test sequencer terpisah (dinyatakan).

## Yang tidak ditunjukkan ini
Hanya simulasi. Interlock diuji oleh ACVP dan kontrol `ncilk` / `ncthrld`; port host yang di-throttle menguji satu pola stall (satu grant dalam delapan siklus), bukan semuanya. Evidence formal ada di `formal.md`.
