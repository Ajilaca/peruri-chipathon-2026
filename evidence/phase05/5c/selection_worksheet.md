## Per seed, C4c (MEASURED)
| Seed | ALM | Registers | M10K | DSP | Worst setup / hold (ns) | Timing met @ 40 ns | Fmax lowest slow corner (MHz) | Evidence |
|---|---|---|---|---|---|---|---|---|
| 1 | 9,043 | 4076 | 29 | 18 | 9.682 / 0.098 | yes | 32.98 | `quartus_C4c.md` |
| 2 | 9,032 | 4078 | 29 | 18 | 11.636 / 0.129 | yes | 35.26 | `quartus_C4c-s2.md` |
| 3 | 9,094 | 4087 | 29 | 18 | 9.016 / 0.117 | yes | 32.27 | `quartus_C4c-s3.md` |
| 4 | 9,051 | 4080 | 29 | 18 | 9.242 / 0.107 | yes | 32.51 | `quartus_C4c-s4.md` |
| 5 | 9,068 | 4081 | 29 | 18 | 11.011 / 0.133 | yes | 34.50 | `quartus_C4c-s5.md` |
| 6 | 9,084 | 4091 | 29 | 18 | 9.895 / 0.095 | yes | 33.22 | `quartus_C4c-s6.md` |

## Comparison with Barrett 5b (C4b-B, medians over seeds 1-6; INFERENCE)
| | ALM median (min-max) | Fmax median (min-max) MHz | t_NTT / t_INTT at median Fmax (us) |
|---|---|---|---|
| C4b-B (Barrett, 5b) | 9,171.0 (9,166-9,208) | 34.515 (33.46-34.84) | 3.448 / 10.865 |
| C4c (lazy INTT inputs) | 9,059.5 (9,032-9,094) | 33.100 (32.27-35.26) | 3.595 / 11.329 |

## Adoption rule (ADR 0014 §4)
- PASS: correct (verification_status.json)
- PASS: cycles exactly 119 / 375
- PASS: ALM <= 12,573 at every seed
- PASS: timing met at 40.000 ns at every seed
- FAIL: median Fmax 33.100 MHz > 34.84 MHz (Barrett 5b top; recomputed top 34.84)
- FAIL: ADR 0012: t_NTT 3.595 < 3.448 us and t_INTT 11.329 < 10.865 us

**Rule result: C4c NOT adopted (C4b-B stays the C4 configuration).**
