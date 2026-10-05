<!-- claim-lint: skip-file (internal evidence record, not proposal text) -->
# C5 (8a) cycle counts, 2026-10-03

## 1. Measured cycle table (MEASURED, simulation; `cycles_c5.json`, 306 points, identical on Verilator and Icarus; K0 from `evidence/phase07/cycles_k0.json`)
Same definition as for K0 (cycles from the `start_i` cycle to the cycle that accepts the last output word, no back-pressure). Three messages per point gave one count: the cycle count depends only on the public length and the number of output words.

| Mode | Message bytes | Output words | K0 cycles | C5 cycles | Change |
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

All 306 points equal the K0 formula with 26 replaced by p = 14 (1 run + 12 busy + 1 done). A permutation is 14 cycles instead of 26 (ratio 0.538); a whole call shrinks by less because the word transfers and the control cycles do not.

## 2. Keccak cycles of one ML-KEM-768 operation (perhitungan tim from the measured formula; `scripts/test/phase7_op_cycles.py 200 <p>`; no new measurement)
K0 (p = 26):

| Call | Mode | Message bytes | Output words | Permutations | Cycles (formula) |
|---|---|---|---|---|---|
| G 33 B (KeyGen) | sha3_512 | 33 | 8 | 1 | 41 |
| G 64 B | sha3_512 | 64 | 8 | 1 | 44 |
| H(ek) 1184 B | sha3_256 | 1184 | 4 | 9 | 389 |
| PRF 33 B -> 128 B | shake_256 | 33 | 16 | 1 | 49 |
| J 1120 B -> 32 B | shake_256 | 1120 | 4 | 9 | 381 |
| SampleNTT x 9 (matrix), 200 random rho | shake_128 | 34 each | by rejection | min 27, median 27, max 29 | min 1289, median 1302, max 1364 |

| Operation | Keccak cycles without SampleNTT | + SampleNTT (min / median / max) | Total Keccak cycles (min / median / max) | Permutations (median total) |
|---|---|---|---|---|
| KeyGen | 724 | 1289 / 1302 / 1364 | 2013 / 2026 / 2088 | 43 |
| Encaps | 776 | 1289 / 1302 / 1364 | 2065 / 2078 / 2140 | 44 |
| Decaps | 768 | 1289 / 1302 / 1364 | 2057 / 2070 / 2132 | 44 |

C5 (p = 14):

| Call | Mode | Message bytes | Output words | Permutations | Cycles (formula) |
|---|---|---|---|---|---|
| G 33 B (KeyGen) | sha3_512 | 33 | 8 | 1 | 29 |
| G 64 B | sha3_512 | 64 | 8 | 1 | 32 |
| H(ek) 1184 B | sha3_256 | 1184 | 4 | 9 | 281 |
| PRF 33 B -> 128 B | shake_256 | 33 | 16 | 1 | 37 |
| J 1120 B -> 32 B | shake_256 | 1120 | 4 | 9 | 273 |
| SampleNTT x 9 (matrix), 200 random rho | shake_128 | 34 each | by rejection | min 27, median 27, max 29 | min 965, median 978, max 1016 |

| Operation | Keccak cycles without SampleNTT | + SampleNTT (min / median / max) | Total Keccak cycles (min / median / max) | Permutations (median total) |
|---|---|---|---|---|
| KeyGen | 532 | 965 / 978 / 1016 | 1497 / 1510 / 1548 | 43 |
| Encaps | 572 | 965 / 978 / 1016 | 1537 / 1550 / 1588 | 44 |
| Decaps | 564 | 965 / 978 / 1016 | 1529 / 1542 / 1580 | 44 |

Reading (INFERENCE): about 1,500 Keccak cycles per operation with C5 against about 2,000 with K0 (-25 %), as the test plan estimated (about 1,500; the 1,200 quoted in chat omitted the transfers and control cycles).
