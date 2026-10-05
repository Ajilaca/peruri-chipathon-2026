## Per seed at 40.000 ns (MEASURED)
| Seed | Config | ALM | Registers | M10K | DSP | Worst setup / hold (ns) | Timing met @ 40 ns | Fmax lowest slow corner (MHz) | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| 1 | K0 | 3,572 | 1653 | 0 | 0 | 22.452 / 0.163 | yes | 56.99 | `quartus_K0.md` |
| 2 | K0 | 3,569 | 1653 | 0 | 0 | 24.373 / 0.164 | yes | 63.99 | `quartus_K0-s2.md` |
| 3 | K0 | 3,566 | 1653 | 0 | 0 | 25.196 / 0.162 | yes | 67.55 | `quartus_K0-s3.md` |
| 4 | K0 | 3,558 | 1653 | 0 | 0 | 25.794 / 0.164 | yes | 70.39 | `quartus_K0-s4.md` |
| 5 | K0 | 3,567 | 1653 | 0 | 0 | 25.646 / 0.163 | yes | 69.67 | `quartus_K0-s5.md` |
| 6 | K0 | 3,561 | 1653 | 0 | 0 | 25.251 / 0.164 | yes | 67.80 | `quartus_K0-s6.md` |
| 1 | C5 | 6,169 | 1652 | 0 | 0 | 19.952 / 0.162 | yes | 49.88 | `quartus_C5.md` |
| 2 | C5 | 6,166 | 1652 | 0 | 0 | 20.648 / 0.162 | yes | 51.67 | `quartus_C5-s2.md` |
| 3 | C5 | 6,152 | 1652 | 0 | 0 | 20.557 / 0.162 | yes | 51.43 | `quartus_C5-s3.md` |
| 4 | C5 | 6,169 | 1652 | 0 | 0 | 20.582 / 0.162 | yes | 51.50 | `quartus_C5-s4.md` |
| 5 | C5 | 6,155 | 1652 | 0 | 0 | 19.145 / 0.162 | yes | 47.95 | `quartus_C5-s5.md` |
| 6 | C5 | 6,168 | 1652 | 0 | 0 | 18.894 / 0.162 | yes | 47.38 | `quartus_C5-s6.md` |

## Comparison with K0 (medians over seeds 1-6; INFERENCE)
| | ALM median (min-max) | Registers | Fmax median (min-max) MHz | cycles per permutation (sponge) | t per permutation at median Fmax (us) |
|---|---|---|---|---|---|
| K0 (previous step) | 3,566.5 (3,558-3,572) | 1653-1653 | 67.675 (56.99-70.39) | 26 | 0.3842 |
| C5 (two rounds per cycle) | 6,167.0 (6,152-6,169) | 1652-1652 | 50.655 (47.38-51.67) | 14 | 0.2764 |

## Adoption rule (test plan section 4)
- PASS: correct (verification_status.json: V1-V9, both simulators, controls fail, formal)
- PASS: busy exactly 12 cycles and 14 cycles per permutation in the sponge
- PASS: ALM <= 12,573 at every seed (working cap)
- PASS: timing met at 40.000 ns at every seed
- PASS: ADR 0012 style: t = 14 / F_C5 = 0.2764 us < 26 / F_K0 = 0.3842 us (K0 median Fmax 67.675 MHz; C5 median 50.655 MHz must exceed 36.440 MHz)

**Rule result: C5 ADOPTED.**
Seed spread of C5 Fmax: 4.29 MHz (min-max); K0: 13.40 MHz.

## Information: 20.000 ns compiles (not part of the rule)
- K0-20 (seed 1): ALM 3,573, worst setup 6.893 ns (met), Fmax lowest slow corner 76.30 MHz, `quartus_K0-20.md`
- C5-20 (seed 1): ALM 6,178, worst setup 4.591 ns (met), Fmax lowest slow corner 64.90 MHz, `quartus_C5-20.md`
