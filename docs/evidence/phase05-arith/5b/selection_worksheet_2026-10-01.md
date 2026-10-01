## Per seed (MEASURED; qualification per ADR 0011 D8)
| Candidate | Seed | ALM | Registers | M10K | DSP | Worst setup / hold (ns) | Timing met @ 40 ns | Fmax lowest slow corner (MHz) | t_NTT (us) | Qualifies | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Barrett | 1 | 9,208 | 4115 | 29 | 18 | 11.044 / 0.120 | yes | 34.54 | 3.445 | yes | `quartus_C4b-B_20261001.md` |
| Barrett | 2 | 9,168 | 4102 | 29 | 18 | 10.832 / 0.130 | yes | 34.28 | 3.471 | yes | `quartus_C4b-B-s2_20261001.md` |
| Barrett | 3 | 9,167 | 4098 | 29 | 18 | 11.175 / 0.134 | yes | 34.69 | 3.430 | yes | `quartus_C4b-B-s3_20261001.md` |
| Barrett | 4 | 9,174 | 4089 | 29 | 18 | 10.112 / 0.134 | yes | 33.46 | 3.556 | yes | `quartus_C4b-B-s4_20261001.md` |
| Barrett | 5 | 9,166 | 4089 | 29 | 18 | 11.300 / 0.142 | yes | 34.84 | 3.416 | yes | `quartus_C4b-B-s5_20261001.md` |
| Barrett | 6 | 9,188 | 4083 | 29 | 18 | 11.009 / 0.100 | yes | 34.49 | 3.450 | yes | `quartus_C4b-B-s6_20261001.md` |
| Montgomery | 1 | 9,249 | 4297 | 29 | 9 | 9.526 / 0.107 | yes | 32.81 | 3.627 | yes | `quartus_C4b-M_20261001.md` |
| Montgomery | 2 | 9,287 | 4287 | 29 | 9 | 10.669 / 0.134 | yes | 34.09 | 3.491 | yes | `quartus_C4b-M-s2_20261001.md` |
| Montgomery | 3 | 9,276 | 4292 | 29 | 9 | 10.404 / 0.143 | yes | 33.79 | 3.522 | yes | `quartus_C4b-M-s3_20261001.md` |
| Montgomery | 4 | 9,286 | 4294 | 29 | 9 | 9.884 / 0.112 | yes | 33.20 | 3.584 | yes | `quartus_C4b-M-s4_20261001.md` |
| Montgomery | 5 | 9,297 | 4299 | 29 | 9 | 10.387 / 0.102 | yes | 33.77 | 3.524 | yes | `quartus_C4b-M-s5_20261001.md` |
| Montgomery | 6 | 9,296 | 4284 | 29 | 9 | 10.806 / 0.158 | yes | 34.25 | 3.474 | yes | `quartus_C4b-M-s6_20261001.md` |

## Per candidate (medians over seeds 1-6; INFERENCE from the rows above)
| Candidate | Correct | Cycles NTT / INTT | Qualifier (all seeds) | ALM median (min-max) | Fmax median (min-max) MHz | t_NTT at median Fmax (us) |
|---|---|---|---|---|---|---|
| Barrett | PASS | 119 / 375 | yes | 9,171.0 (9,166-9,208) | 34.515 (33.46-34.84) | 3.448 |
| Montgomery | PASS | 119 / 375 | yes | 9,286.5 (9,249-9,297) | 33.780 (32.81-34.25) | 3.523 |

## Rule result
Higher median Fmax: Barrett (34.515 MHz); Montgomery is 2.13 % lower.
Near tie (<= 5 %). Median ALM: Barrett 9,171.0, Montgomery 9,286.5 (difference 115.5).
Lower median ALM wins: **Barrett** is selected by the rule.
