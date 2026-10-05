## Per seed, S8 (MEASURED)
| Seed | ALM | Registers | M10K | DSP | Worst setup / hold (ns) | Timing met @ 40 ns | Fmax lowest slow corner (MHz) | Evidence |
|---|---|---|---|---|---|---|---|---|
| 1 | 9,464 | 4144 | 33 | 16 | 15.135 / 0.073 | yes | 40.22 | `quartus_S8.md` |
| 2 | 9,423 | 4136 | 33 | 16 | 13.759 / 0.107 | yes | 38.11 | `quartus_S8-s2.md` |
| 3 | 9,471 | 4139 | 33 | 16 | 13.017 / 0.090 | yes | 37.06 | `quartus_S8-s3.md` |
| 4 | 9,402 | 4137 | 33 | 16 | 12.794 / 0.131 | yes | 36.76 | `quartus_S8-s4.md` |
| 5 | 9,469 | 4138 | 33 | 16 | 13.772 / 0.140 | yes | 38.13 | `quartus_S8-s5.md` |
| 6 | 9,419 | 4130 | 33 | 16 | 13.593 / 0.152 | yes | 37.87 | `quartus_S8-s6.md` |

## Comparison with the earlier steps (medians over seeds 1-6; INFERENCE; the rule compares with S7 only)
| | ALM median (min-max) | DSP | Fmax median (min-max) MHz | cycles NTT / INTT | t_NTT / t_INTT at median Fmax (us) |
|---|---|---|---|---|---|
| C4b-B (Phase 5) | 9,171.0 (9,166-9,208) | 18 | 34.515 (33.46-34.84) | 119 / 375 | 3.448 / 10.865 |
| M6 (S6) | 9,421.5 (9,394-9,441) | 16 | 34.430 (32.35-35.04) | 119 / 119 | 3.456 / 3.456 |
| S7 (previous step) | 9,391.0 (9,361-9,405) | 16 | 38.720 (37.89-40.29) | 120 / 120 | 3.099 / 3.099 |
| S8 (write register, P = 8, one bubble) | 9,443.5 (9,402-9,471) | 16 | 37.990 (36.76-40.22) | 122 / 122 | 3.211 / 3.211 |

## Adoption rule (test plan section 4)
- PASS: correct (verification_status.json: V1-V8, the regression V8 run once at S8 by Amendment A1)
- PASS: cycles exactly NTT 122 / INTT 122
- PASS: ALM <= 12,573 at every seed
- PASS: timing met at 40.000 ns at every seed
- FAIL: ADR 0012, t_NTT 3.211 < 3.099 us (S7 median Fmax 38.720 MHz; S8 median 37.990 MHz must exceed 39.365 MHz)
- FAIL: ADR 0012, t_INTT 3.211 < 3.099 us

**Rule result: S8 NOT adopted by the rule (no tolerance was added).**
Seed spread of S8 Fmax: 3.46 MHz (min-max).
