<!-- claim-lint: skip-file (internal evidence, not proposal text) -->
# Profil Fase 9M inti ML-KEM-768, 2026-10-04

MEASURED dalam simulasi (Verilator dan Icarus memberi angka identik), `tb/mlkem/profile_core.py` dengan `tb/mlkem/test_profile_core.py` pada `rtl/mlkem/mlkem_core.sv` sebagaimana digabung di PR #9 (main 49bebf7). Masukan tetap d = 00..1f, z = 20..3f, m = 40..5f; satu KeyGen, lalu Encaps dengan ek-nya, lalu Decaps ciphertext itu. Siklus dihitung pada setiap falling edge di dalam `run_op` di `tb/mlkem/core_tb.py` (hitungan yang sama dengan test Fase 9). Jumlah siklus ini bergantung pada rho (sampling matriks); rentang ACVP Fase 9 adalah KeyGen 9,035-9,076, Encaps 10,664-10,727, Decaps 16,601-16,663. Data mentah: `profile_verilator.json`.

## Siklus per state pengendali

| State | KeyGen | Encaps | Decaps |
|---|---|---|---|
| RUN | 6,380 | 7,698 | 10,807 |
| LDP | 0 | 1,428 | 3,831 |
| STP | 2,346 | 1,244 | 1,507 |
| HFD | 268 | 271 | 264 |
| HGT | 43 | 43 | 43 |
| CMP | 0 | 0 | 138 |
| CMPK | 0 | 0 | 4 |
| WR32 | 12 | 0 | 0 |
| RD32 | 0 | 5 | 5 |
| SDL | 8 | 8 | 8 |
| FETCH | 18 | 18 | 29 |
| DISP | 19 | 19 | 30 |
| IDLE | 1 | 1 | 1 |
| total | 9,095 | 10,735 | 16,667 |

RUN adalah mesin K-PKE (Fase 8d, tidak berubah); LDP memuat satu polinomial dari buffer byte ke slot mesin (unpack + decompress), STP menyimpan satu (compress + pack); HFD / HGT memberi makan hash dan mengambilnya; CMP / CMPK membandingkan ciphertext dan memilih kunci.

## Siklus per operasi mikro

Format sebuah operasi: seperti `tb/golden/mlkem_ctl_model.py` (LDP / STP: slot, region, offset word, d).

### keygen (9,095 siklus)

| pc | Operasi | Siklus |
|---|---|---|
| 0 | `HST 1 33` | 1 |
| 1 | `HFD 3 0 4` | 7 |
| 2 | `HFD 4 0 1` | 4 |
| 3 | `HGT 3 4` | 25 |
| 4 | `SDL` | 10 |
| 5 | `RUN 0` | 6,382 |
| 6 | `STP 3 0 144 12` | 393 |
| 7 | `STP 4 0 192 12` | 393 |
| 8 | `STP 5 0 240 12` | 393 |
| 9 | `STP 0 0 0 12` | 393 |
| 10 | `STP 1 0 48 12` | 393 |
| 11 | `STP 2 0 96 12` | 393 |
| 12 | `WR32 3 288` | 6 |
| 13 | `HST 0 1184` | 2 |
| 14 | `HFD 0 144 148` | 263 |
| 15 | `HGT 7 0` | 22 |
| 16 | `WR32 7 292` | 6 |
| 17 | `WR32 1 296` | 6 |
| 18 | `END` | 3 |

### encaps (10,735 siklus)

| pc | Operasi | Siklus |
|---|---|---|
| 0 | `HST 0 1184` | 1 |
| 1 | `HFD 0 144 148` | 263 |
| 2 | `HGT 7 0` | 22 |
| 3 | `HST 1 64` | 2 |
| 4 | `HFD 3 8 4` | 7 |
| 5 | `HFD 3 28 4` | 7 |
| 6 | `HGT 5 4` | 25 |
| 7 | `RD32 3 288` | 7 |
| 8 | `LDP 7 0 144 12` | 391 |
| 9 | `LDP 8 0 192 12` | 391 |
| 10 | `LDP 9 0 240 12` | 391 |
| 11 | `LDP 11 3 8 1` | 263 |
| 12 | `SDL` | 10 |
| 13 | `RUN 1` | 7,700 |
| 14 | `STP 3 1 0 10` | 329 |
| 15 | `STP 4 1 40 10` | 329 |
| 16 | `STP 5 1 80 10` | 329 |
| 17 | `STP 10 1 120 4` | 265 |
| 18 | `END` | 3 |

### decaps (16,667 siklus)

| pc | Operasi | Siklus |
|---|---|---|
| 0 | `LDP 3 1 0 10` | 326 |
| 1 | `LDP 4 1 40 10` | 327 |
| 2 | `LDP 5 1 80 10` | 327 |
| 3 | `LDP 10 1 120 4` | 263 |
| 4 | `LDP 0 0 0 12` | 391 |
| 5 | `LDP 1 0 48 12` | 391 |
| 6 | `LDP 2 0 96 12` | 391 |
| 7 | `RUN 2` | 3,111 |
| 8 | `STP 10 3 8 1` | 265 |
| 9 | `HST 1 64` | 2 |
| 10 | `HFD 3 8 4` | 7 |
| 11 | `HFD 0 292 4` | 7 |
| 12 | `HGT 5 4` | 25 |
| 13 | `HST 2 1120` | 2 |
| 14 | `HFD 0 296 4` | 7 |
| 15 | `HFD 1 0 136` | 251 |
| 16 | `HGT 6 0` | 22 |
| 17 | `RD32 3 288` | 7 |
| 18 | `LDP 7 0 144 12` | 391 |
| 19 | `LDP 8 0 192 12` | 391 |
| 20 | `LDP 9 0 240 12` | 391 |
| 21 | `LDP 11 3 8 1` | 263 |
| 22 | `SDL` | 10 |
| 23 | `RUN 1` | 7,700 |
| 24 | `STP 3 2 0 10` | 329 |
| 25 | `STP 4 2 40 10` | 329 |
| 26 | `STP 5 2 80 10` | 329 |
| 27 | `STP 10 2 120 4` | 265 |
| 28 | `CMP` | 144 |
| 29 | `END` | 3 |

## Pembacaan (INFERENCE)
- Memuat atau menyimpan satu polinomial memakan 391-393 siklus pada d = 12, 326-329 pada d = 10, dan 263-265 pada d = 1 atau 4. Port mesin menerima satu koefisien per siklus (256 siklus per polinomial); codec memindahkan satu byte per siklus, yaitu 384 byte pada d = 12 dan 320 pada d = 10. Pada d = 12 dan d = 10 jalur byte adalah batasnya, pada d = 1 dan 4 port koefisien.
- Porsi siklus: KeyGen RUN 70 %, STP 26 %; Encaps RUN 72 %, LDP 13 %, STP 12 %; Decaps RUN 65 %, LDP 23 %, STP 9 %; hashing dan pembandingan masing-masing sekitar 3 %.
- Port host mesin hanya bekerja saat mesin idle (`evidence/phase09/phase9_plan.md` bagian 3), sehingga load dan store tidak dapat tumpang tindih dengan RUN tanpa varian mesin baru.
