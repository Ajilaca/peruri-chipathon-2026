# Phase 8b W2: cycles per polynomial (MEASURED in simulation, coef_ready_i always high; operation sums are perhitungan tim)

| Sponge | Kind | Polynomials | Mean | Min | Max | Distinct values |
|---|---|---|---|---|---|---|
| C5 | sample_ntt | 500 | 206.48 | 194 | 231 | 24 |
| C5 | cbd | 102 | 152.00 | 152 | 152 | 1 |

C5: r = cycles - triples consumed per XOF blocks B: B=3: [49], B=4: [61]

| K0 | sample_ntt | 500 | 242.71 | 230 | 279 | 24 |
| K0 | cbd | 102 | 164.00 | 164 | 164 | 1 |

K0: r = cycles - triples consumed per XOF blocks B: B=3: [85], B=4: [109]

## Sampling cycles per operation (perhitungan tim)
| Sponge | KeyGen (9 SampleNTT + 6 CBD) | Encaps (9 + 7) | Decaps (repeats the Encaps sampling) |
|---|---|---|---|
| C5 | 2,770 | 2,922 | 2,922 |
| K0 | 3,168 | 3,332 | 3,332 |
