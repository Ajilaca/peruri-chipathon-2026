<!-- claim-lint: skip-file (internal evidence record, not proposal text) -->
# K0 cycle counts (Phase 7, test plan V6), 2026-10-03

## 1. Measured cycle table (MEASURED, simulation; `cycles_k0_2026-10-03.json`, 306 points, identical on Verilator and Icarus)
Cycles from the cycle that carries `start_i` to the cycle that accepts the last output word, no back-pressure. For every (mode, length, output words) three messages (random, all-0x00, all-0xFF) gave the
**same** count: the cycle count depends only on the public length and the number of output words, never on data (CRG-7). Selected points:

| Mode | Message bytes | Output words | Cycles |
|---|---|---|---|
| sha3_256 | 0 | 4 | 33 |
| sha3_256 | 32 | 4 | 37 |
| sha3_256 | 135 | 4 | 48 |
| sha3_256 | 136 | 4 | 76 |
| sha3_256 | 137 | 4 | 76 |
| sha3_256 | 1184 | 4 | 389 |
| sha3_512 | 0 | 8 | 37 |
| sha3_512 | 64 | 8 | 44 |
| sha3_512 | 72 | 8 | 72 |
| shake_128 | 34 | 21 | 54 |
| shake_128 | 34 | 22 | 81 |
| shake_128 | 0 | 1 | 30 |
| shake_256 | 34 | 16 | 49 |
| shake_256 | 33 | 16 | 49 |
| shake_256 | 1120 | 4 | 381 |

All 306 points equal the formula derived from the FSM of `rtl/keccak/keccak_sponge.sv` (formula written after the RTL, then checked against every point; it was not tuned):

    cycles = 1 + (len div 8 + 1) + pad2 + 26 * (len div rate + 1) + out_words + 26 * ((out_words - 1) div rate_words)
    pad2   = 0 when (len mod rate) div 8 = rate_words - 1, else 1;   rate_words = rate / 8

One permutation is 26 cycles as seen by the controller: 1 run cycle, 24 cycles with `keccak_f1600.busy_o` high (V4: exactly 24 for every state), 1 done cycle. The pre-measurement ESTIMATE of the test plan
used 24 per permutation and about 370 cycles for H(ek); the measured value is **389** cycles (+5 %). The estimate was optimistic by the 2 control cycles per permutation; it is superseded, not tuned.

## 2. Keccak cycles of one ML-KEM-768 operation with K0 (perhitungan tim, computed by `scripts/phase7_op_cycles.py` from the measured formula; no new measurement)
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

Reading (INFERENCE): about 2,000 Keccak cycles per operation when every call runs on its own and nothing overlaps. The pre-measurement figure of about 1,060 cycles (44 permutations x 24) omitted the
2 control cycles per permutation, the word-by-word transfers (H(ek) alone moves 148 words in and 4 out) and the restart of the sponge for every call; this table replaces it. Compare, in the same units,
with the arithmetic of Phase 6 with S10: KeyGen 5,475, Encrypt 6,789, Decrypt 3,109 cycles (MEASURED, simulation, `docs/evidence/phase06-scheduling/verify_2026-10-03.md`); the two blocks are not connected yet.
