## Per seed at 40.000 ns (MEASURED)
| Seed | ALM | Registers | M10K blocks | Block memory bits | DSP | Worst setup / hold (ns) | Timing met @ 40 ns | Fmax lowest slow corner (MHz) | Critical warnings | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 17,613 | 8210 | 54 | 120,350 | 28 | 20.272 / 0.096 | yes | 50.69 | 1 | `quartus_MC-20261003.md` |
| 2 | 17,636 | 8272 | 54 | 120,350 | 28 | 19.010 / 0.075 | yes | 47.64 | 1 | `quartus_MC-s2-20261003.md` |
| 3 | 17,630 | 8365 | 54 | 120,350 | 28 | 19.395 / 0.104 | yes | 48.53 | 1 | `quartus_MC-s3-20261003.md` |
| 4 | 17,623 | 8232 | 54 | 120,350 | 28 | 19.815 / 0.133 | yes | 49.54 | 1 | `quartus_MC-s4-20261003.md` |
| 5 | 17,608 | 8272 | 54 | 120,350 | 28 | 20.671 / 0.106 | yes | 51.74 | 1 | `quartus_MC-s5-20261003.md` |
| 6 | 17,618 | 8248 | 54 | 120,350 | 28 | 19.599 / 0.104 | yes | 49.02 | 1 | `quartus_MC-s6-20261003.md` |

ALM median (min-max): 17,620.5 (17,608-17,636); registers 8210-8365; M10K 54-54; DSP 28-28; Fmax median (min-max): 49.280 (47.64-51.74) MHz

### Pass rule (test plan section 5, items 2 and 3)
- PASS: the fit succeeded at every seed
- PASS: timing met at 40.000 ns at every seed (worst setup and hold slack of all corners non-negative)
- reported as MEASURED: resource counts and Fmax (median of the lowest slow-corner Fmax over seeds 1-6) above
- information MC-20 (20.000 ns), seed 1: ALM 17,650, registers 8374, worst setup 4.419 ns (met), Fmax lowest slow corner 64.18 MHz, `quartus_MC-20-20261003.md`

## Cycles per operation (MEASURED in simulation; no host stalls; one operation from start_i to done_o as seen by the test driver)
| Operation | Icarus | Verilator |
|---|---|---|
| Encaps (constant for every m with the same ek) | [10691] | [10691] |
| Decaps (constant for valid and rejected ciphertexts and for different secret keys with the same ek) | [16623] | [16623] |
| KeyGen over the 25 ACVP seeds (depends on the public rho only), min - max | 9035 - 9076 | 9035 - 9076 |
| Encaps over the ACVP vectors (different ek), min - max | 10664 - 10727 | 10664 - 10727 |
| Decaps over the ACVP vectors (different dk), min - max | 16601 - 16663 | 16601 - 16663 |
