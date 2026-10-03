# Phase 8b W1: cycles per polynomial (MEASURED in simulation, coef_ready_i always high; operation sums are perhitungan tim)

| Sponge | Kind | Polynomials | Mean | Min | Max | Distinct values |
|---|---|---|---|---|---|---|
| C5 | sample_ntt | 500 | 305.23 | 298 | 323 | 21 |
| C5 | cbd | 102 | 280.00 | 280 | 280 | 1 |

C5: r = cycles - sum of max(1, accepted) per XOF blocks B: B=3: [41, 42, 43, 44, 45, 46, 47, 48], B=4: [52, 53, 54, 57]

| K0 | sample_ntt | 500 | 341.30 | 333 | 356 | 18 |
| K0 | cbd | 102 | 292.00 | 292 | 292 | 1 |

K0: r = cycles - sum of max(1, accepted) per XOF blocks B: B=3: [77, 78, 79, 80, 81, 82, 83, 84]

## Sampling cycles per operation (perhitungan tim)
| Sponge | KeyGen (9 SampleNTT + 6 CBD) | Encaps (9 + 7) | Decaps (repeats the Encaps sampling) |
|---|---|---|---|
| C5 | 4,427 | 4,707 | 4,707 |
| K0 | 4,824 | 5,116 | 5,116 |
