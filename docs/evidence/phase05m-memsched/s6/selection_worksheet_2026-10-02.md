## Per seed, M6 (MEASURED)
| Seed | ALM | Registers | M10K | DSP | Worst setup / hold (ns) | Timing met @ 40 ns | Fmax lowest slow corner (MHz) | Evidence |
|---|---|---|---|---|---|---|---|---|
| 1 | 9,426 | 4041 | 29 | 16 | 11.161 / 0.145 | yes | 34.68 | `quartus_M6_20261002.md` |
| 2 | 9,394 | 4030 | 29 | 16 | 10.942 / 0.126 | yes | 34.41 | `quartus_M6-s2_20261002.md` |
| 3 | 9,417 | 4063 | 29 | 16 | 10.721 / 0.143 | yes | 34.15 | `quartus_M6-s3_20261002.md` |
| 4 | 9,409 | 4080 | 29 | 16 | 9.090 / 0.120 | yes | 32.35 | `quartus_M6-s4_20261002.md` |
| 5 | 9,441 | 4049 | 29 | 16 | 11.464 / 0.126 | yes | 35.04 | `quartus_M6-s5_20261002.md` |
| 6 | 9,429 | 4036 | 29 | 16 | 10.972 / 0.084 | yes | 34.45 | `quartus_M6-s6_20261002.md` |

## Comparison with C4b-B (medians over seeds 1-6; INFERENCE)
| | ALM median (min-max) | DSP | Fmax median (min-max) MHz | cycles NTT / INTT | t_NTT / t_INTT at median Fmax (us) |
|---|---|---|---|---|---|
| C4b-B (previous step) | 9,171.0 (9,166-9,208) | 18 | 34.515 (33.46-34.84) | 119 / 375 | 3.448 / 10.865 |
| M6 (INTT without scaling pass) | 9,421.5 (9,394-9,441) | 16 | 34.430 (32.35-35.04) | 119 / 119 | 3.456 / 3.456 |

## Adoption rule (test plan section 4)
- PASS: correct (verification_status.json: V1-V8; V9 not run for S6, Amendment A1)
- PASS: cycles exactly NTT 119 / INTT 119
- PASS: ALM <= 12,573 at every seed
- PASS: timing met at 40.000 ns at every seed
- PASS: ADR 0012, t_INTT 3.456 < 10.865 us (C4b-B median Fmax 34.515 MHz)
- FAIL: ADR 0012, t_NTT 3.456 < 3.448 us (needs M6 median Fmax 34.430 MHz > 34.515 MHz)

**Rule result: M6 NOT adopted by the rule (no tolerance was added).**
Only the NTT part of ADR 0012 failed (NTT mode is unchanged in cycles; the margin is the median Fmax). Test plan section 4: reported as measured; any other rule is a new decision of the team.
