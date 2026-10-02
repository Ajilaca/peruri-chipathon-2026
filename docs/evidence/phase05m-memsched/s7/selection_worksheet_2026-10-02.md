## Per seed, S7 (MEASURED)
| Seed | ALM | Registers | M10K | DSP | Worst setup / hold (ns) | Timing met @ 40 ns | Fmax lowest slow corner (MHz) | Evidence |
|---|---|---|---|---|---|---|---|---|
| 1 | 9,394 | 4317 | 31 | 16 | 14.439 / 0.128 | yes | 39.12 | `quartus_S7_20261002.md` |
| 2 | 9,388 | 4317 | 31 | 16 | 13.906 / 0.118 | yes | 38.32 | `quartus_S7-s2_20261002.md` |
| 3 | 9,361 | 4302 | 31 | 16 | 13.894 / 0.113 | yes | 38.31 | `quartus_S7-s3_20261002.md` |
| 4 | 9,405 | 4296 | 31 | 16 | 13.606 / 0.111 | yes | 37.89 | `quartus_S7-s4_20261002.md` |
| 5 | 9,362 | 4298 | 31 | 16 | 14.545 / 0.130 | yes | 39.29 | `quartus_S7-s5_20261002.md` |
| 6 | 9,396 | 4324 | 31 | 16 | 15.178 / 0.088 | yes | 40.29 | `quartus_S7-s6_20261002.md` |

## Comparison with M6 (medians over seeds 1-6; INFERENCE)
| | ALM median (min-max) | DSP | Fmax median (min-max) MHz | cycles NTT / INTT | t_NTT / t_INTT at median Fmax (us) |
|---|---|---|---|---|---|
| M6 (previous step) | 9,421.5 (9,394-9,441) | 16 | 34.430 (32.35-35.04) | 119 / 119 | 3.456 / 3.456 |
| S7 (RD_SPLIT = 1, P = 7) | 9,391.0 (9,361-9,405) | 16 | 38.720 (37.89-40.29) | 120 / 120 | 3.099 / 3.099 |

## Adoption rule (test plan section 4)
- PASS: correct (verification_status.json: V1-V6; V7 not run for S7, Amendment A1)
- PASS: cycles exactly NTT 120 / INTT 120
- PASS: ALM <= 12,573 at every seed
- PASS: timing met at 40.000 ns at every seed
- PASS: ADR 0012, t_NTT 3.099 < 3.456 us (M6 median Fmax 34.430 MHz; needs S7 median 38.720 MHz > 34.719 MHz)
- PASS: ADR 0012, t_INTT 3.099 < 3.456 us

**Rule result: S7 ADOPTED.**
Seed spread of S7 Fmax: 2.40 MHz (min-max).
