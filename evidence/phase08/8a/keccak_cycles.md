<!-- claim-lint: skip-file (internal evidence record, not proposal text) -->
# Jumlah siklus C5 (8a), 2026-10-03

## 1. Tabel siklus terukur (MEASURED, simulasi; `cycles_c5.json`, 306 titik, identik di Verilator dan Icarus; K0 dari `evidence/phase07/cycles_k0.json`)
Definisi sama seperti K0 (siklus dari siklus `start_i` sampai siklus yang menerima word keluaran terakhir, tanpa back-pressure). Tiga pesan per titik memberi satu hitungan: jumlah siklus hanya bergantung pada panjang publik dan jumlah word keluaran.

| Mode | Byte pesan | Word keluaran | Siklus K0 | Siklus C5 | Perubahan |
|---|---|---|---|---|---|
| sha3_256 | 0 | 4 | 33 | 21 | -36 % |
| sha3_256 | 32 | 4 | 37 | 25 | -32 % |
| sha3_256 | 136 | 4 | 76 | 52 | -32 % |
| sha3_256 | 1184 | 4 | 389 | 281 | -28 % |
| sha3_512 | 64 | 8 | 44 | 32 | -27 % |
| shake_256 | 33 | 16 | 49 | 37 | -24 % |
| shake_256 | 1120 | 4 | 381 | 273 | -28 % |
| shake_128 | 34 | 21 | 54 | 42 | -22 % |
| shake_128 | 34 | 22 | 81 | 57 | -30 % |

Semua 306 titik sama dengan rumus K0 dengan 26 diganti p = 14 (1 run + 12 busy + 1 done). Satu permutasi 14 siklus sebagai ganti 26 (rasio 0,538); satu panggilan utuh menyusut lebih sedikit karena transfer word dan siklus kendali tidak ikut menyusut.

## 2. Siklus Keccak satu operasi ML-KEM-768 (perhitungan tim dari rumus terukur; `scripts/test/phase7_op_cycles.py 200 <p>`; tanpa pengukuran baru)
K0 (p = 26):

| Panggilan | Mode | Byte pesan | Word keluaran | Permutasi | Siklus (rumus) |
|---|---|---|---|---|---|
| G 33 B (KeyGen) | sha3_512 | 33 | 8 | 1 | 41 |
| G 64 B | sha3_512 | 64 | 8 | 1 | 44 |
| H(ek) 1184 B | sha3_256 | 1184 | 4 | 9 | 389 |
| PRF 33 B -> 128 B | shake_256 | 33 | 16 | 1 | 49 |
| J 1120 B -> 32 B | shake_256 | 1120 | 4 | 9 | 381 |
| SampleNTT x 9 (matrix), 200 random rho | shake_128 | 34 each | by rejection | min 27, median 27, max 29 | min 1289, median 1302, max 1364 |

| Operasi | Siklus Keccak tanpa SampleNTT | + SampleNTT (min / median / max) | Total siklus Keccak (min / median / maks) | Permutasi (total median) |
|---|---|---|---|---|
| KeyGen | 724 | 1289 / 1302 / 1364 | 2013 / 2026 / 2088 | 43 |
| Encaps | 776 | 1289 / 1302 / 1364 | 2065 / 2078 / 2140 | 44 |
| Decaps | 768 | 1289 / 1302 / 1364 | 2057 / 2070 / 2132 | 44 |

C5 (p = 14):

| Panggilan | Mode | Byte pesan | Word keluaran | Permutasi | Siklus (rumus) |
|---|---|---|---|---|---|
| G 33 B (KeyGen) | sha3_512 | 33 | 8 | 1 | 29 |
| G 64 B | sha3_512 | 64 | 8 | 1 | 32 |
| H(ek) 1184 B | sha3_256 | 1184 | 4 | 9 | 281 |
| PRF 33 B -> 128 B | shake_256 | 33 | 16 | 1 | 37 |
| J 1120 B -> 32 B | shake_256 | 1120 | 4 | 9 | 273 |
| SampleNTT x 9 (matrix), 200 random rho | shake_128 | 34 each | by rejection | min 27, median 27, max 29 | min 965, median 978, max 1016 |

| Operasi | Siklus Keccak tanpa SampleNTT | + SampleNTT (min / median / max) | Total siklus Keccak (min / median / maks) | Permutasi (total median) |
|---|---|---|---|---|
| KeyGen | 532 | 965 / 978 / 1016 | 1497 / 1510 / 1548 | 43 |
| Encaps | 572 | 965 / 978 / 1016 | 1537 / 1550 / 1588 | 44 |
| Decaps | 564 | 965 / 978 / 1016 | 1529 / 1542 / 1580 | 44 |

Pembacaan (INFERENCE): sekitar 1.500 siklus Keccak per operasi dengan C5 lawan sekitar 2.000 dengan K0 (-25 %), seperti diestimasi test plan (sekitar 1.500; angka 1.200 yang disebut di chat melewatkan transfer dan siklus kendali).
