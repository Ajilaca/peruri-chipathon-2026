## W1: per seed at 40.000 ns (MEASURED)
| Seed | ALM | Registers | M10K | DSP | Worst setup / hold (ns) | Timing met @ 40 ns | Fmax lowest slow corner (MHz) | Evidence |
|---|---|---|---|---|---|---|---|---|
| 1 | 5,276 | 1913 | 0 | 0 | 20.399 / 0.161 | yes | 51.02 | `quartus_SM1_20261003.md` |
| 2 | 5,271 | 1913 | 0 | 0 | 20.470 / 0.162 | yes | 51.20 | `quartus_SM1-s2_20261003.md` |
| 3 | 5,298 | 1913 | 0 | 0 | 20.789 / 0.162 | yes | 52.05 | `quartus_SM1-s3_20261003.md` |
| 4 | 5,311 | 1913 | 0 | 0 | 20.038 / 0.163 | yes | 50.10 | `quartus_SM1-s4_20261003.md` |
| 5 | 5,282 | 1913 | 0 | 0 | 20.484 / 0.162 | yes | 51.24 | `quartus_SM1-s5_20261003.md` |
| 6 | 5,273 | 1913 | 0 | 0 | 22.075 / 0.161 | yes | 55.79 | `quartus_SM1-s6_20261003.md` |

ALM median (min-max): 5,279.0 (5,271-5,311); registers 1913-1913; Fmax median (min-max): 51.220 (50.10-55.79) MHz

### W1 acceptance gate (test plan section 4)
- PASS: correct (verification_status: V1-V10, both simulators, controls fail, formal, regression)
- PASS: M10K = 0 and DSP = 0 at every seed
- PASS: ALM <= 12,573 at every seed (working cap)
- PASS: timing met at 40.000 ns at every seed
- PASS: median Fmax 51.220 MHz >= S10 median 44.320 MHz

**W1 gate result: PASSED.**

Cycles (C5 top, `cycles_w1_c5_2026-10-03.json`; coef_ready always high): SampleNTT mean 305.23 cycles over 500 polynomials; CBD [280] cycles.

- information SM1-20 (20.000 ns), seed 1: ALM 5,296, worst setup 3.892 ns (met), Fmax lowest slow corner 62.08 MHz, `quartus_SM1-20_20261003.md`
- information SM1-K0 (K0 sponge), seed 1: ALM 3,470, worst setup 23.928 ns (met), Fmax lowest slow corner 62.22 MHz, `quartus_SM1-K0_20261003.md`

## W2: per seed at 40.000 ns (MEASURED)
| Seed | ALM | Registers | M10K | DSP | Worst setup / hold (ns) | Timing met @ 40 ns | Fmax lowest slow corner (MHz) | Evidence |
|---|---|---|---|---|---|---|---|---|
| 1 | 5,290 | 1947 | 0 | 0 | 21.280 / 0.162 | yes | 53.42 | `quartus_SM2_20261003.md` |
| 2 | 5,308 | 1947 | 0 | 0 | 19.989 / 0.152 | yes | 49.97 | `quartus_SM2-s2_20261003.md` |
| 3 | 5,282 | 1947 | 0 | 0 | 20.358 / 0.162 | yes | 50.91 | `quartus_SM2-s3_20261003.md` |
| 4 | 5,290 | 1947 | 0 | 0 | 19.364 / 0.162 | yes | 48.46 | `quartus_SM2-s4_20261003.md` |
| 5 | 5,305 | 1947 | 0 | 0 | 20.187 / 0.162 | yes | 50.47 | `quartus_SM2-s5_20261003.md` |
| 6 | 5,284 | 1947 | 0 | 0 | 19.371 / 0.161 | yes | 48.48 | `quartus_SM2-s6_20261003.md` |

ALM median (min-max): 5,290.0 (5,282-5,308); registers 1947-1947; Fmax median (min-max): 50.220 (48.46-53.42) MHz

### W2 acceptance gate (test plan section 4)
- PASS: correct (verification_status: V1-V10, both simulators, controls fail, formal, regression)
- PASS: M10K = 0 and DSP = 0 at every seed
- PASS: ALM <= 12,573 at every seed (working cap)
- PASS: timing met at 40.000 ns at every seed
- PASS: median Fmax 50.220 MHz >= S10 median 44.320 MHz

**W2 gate result: PASSED.**

Cycles (C5 top, `cycles_w2_c5_2026-10-03.json`; coef_ready always high): SampleNTT mean 206.48 cycles over 500 polynomials; CBD [152] cycles.

- information SM2-20 (20.000 ns), seed 1: ALM 5,320, worst setup 4.214 ns (met), Fmax lowest slow corner 63.35 MHz, `quartus_SM2-20_20261003.md`
- information SM2-K0 (K0 sponge), seed 1: ALM 3,551, worst setup 23.461 ns (met), Fmax lowest slow corner 60.46 MHz, `quartus_SM2-K0_20261003.md`

Reference: S10 (NTT/INTT core) Fmax median 44.320 MHz over seeds 1-6 (recomputed from `docs/evidence/phase06-scheduling/s10/`).

## Selection W1 versus W2 (test plan section 5)
- W1: t(SampleNTT) = 305.23 / 51.220 = 5.9593 us; t(CBD) = 280 / 51.220 = 5.4666 us
- W2: t(SampleNTT) = 206.48 / 50.220 = 4.1114 us; t(CBD) = 152 / 50.220 = 3.0267 us

**Selection result: W2 CHOSEN (passes the gate and t is lower than W1 for SampleNTT and for CBD).**
