## Per seed, S10 at 40.000 ns (MEASURED)
| Seed | ALM | Registers | M10K | DSP | Worst setup / hold (ns) | Timing met @ 40 ns | Fmax lowest slow corner (MHz) | Evidence |
|---|---|---|---|---|---|---|---|---|
| 1 | 5,091 | 545 | 24 | 16 | 17.662 / 0.089 | yes | 44.77 | `quartus_S10_20261002.md` |
| 2 | 5,088 | 543 | 24 | 16 | 16.382 / 0.132 | yes | 42.34 | `quartus_S10-s2_20261002.md` |
| 3 | 5,069 | 555 | 24 | 16 | 18.376 / 0.095 | yes | 46.24 | `quartus_S10-s3_20261002.md` |
| 4 | 5,082 | 548 | 24 | 16 | 16.865 / 0.111 | yes | 43.22 | `quartus_S10-s4_20261002.md` |
| 5 | 5,045 | 552 | 24 | 16 | 17.205 / 0.106 | yes | 43.87 | `quartus_S10-s5_20261002.md` |
| 6 | 5,072 | 554 | 24 | 16 | 18.565 / 0.155 | yes | 46.65 | `quartus_S10-s6_20261002.md` |

## Comparison with S7 (medians over seeds 1-6; INFERENCE)
| | ALM median (min-max) | DSP | Fmax median (min-max) MHz | cycles NTT / INTT | t_NTT / t_INTT at median Fmax (us) |
|---|---|---|---|---|---|
| S7 (previous step) | 9,391.0 (9,361-9,405) | 16 | 38.720 (37.89-40.29) | 120 / 120 | 3.099 / 3.099 |
| S10 (16 x 1R1W, P = 5) | 5,077.0 (5,045-5,091) | 16 | 44.320 (42.34-46.65) | 118 / 118 | 2.662 / 2.662 |

## Adoption rule (test plan section 4)
- PASS: correct (verification_status.json: V1-V6 incl. the Phase 6 top with S10)
- PASS: cycles exactly NTT 118 / INTT 118
- PASS: ALM <= 12,573 at every seed
- PASS: timing met at 40.000 ns at every seed
- PASS: ADR 0012, t_NTT 2.662 < 3.099 us (S7 median Fmax 38.720 MHz; S10 median 44.320 MHz must exceed 38.075 MHz)
- PASS: ADR 0012, t_INTT 2.662 < 3.099 us

**Rule result: S10 ADOPTED.**
Seed spread of S10 Fmax: 4.31 MHz (min-max).

## Information: 20.000 ns compiles (not part of the rule; 50 MHz needs worst setup slack >= 0 at 20 ns)
| Revision | seeds | worst setup (ns) per seed | timing met at 20 ns | Fmax lowest slow corner per seed (MHz) | median |
|---|---|---|---|---|---|
| S7-20 | 1-6 | -1.388, -1.655, -2.296, -2.431, -1.933, -1.615 | 0/6 | 46.76, 46.18, 44.85, 44.58, 45.59, 46.26 | 45.885 |
| S10-20 | 1-6 | 1.176, 1.718, 0.984, 1.050, 1.241, 0.792 | 6/6 | 53.12, 54.70, 52.59, 52.77, 53.31, 52.06 | 52.945 |
