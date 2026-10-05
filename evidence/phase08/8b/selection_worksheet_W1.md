## W1: per seed at 40.000 ns (MEASURED)
| Seed | ALM | Registers | M10K | DSP | Worst setup / hold (ns) | Timing met @ 40 ns | Fmax lowest slow corner (MHz) | Evidence |
|---|---|---|---|---|---|---|---|---|
| 1 | 5,276 | 1913 | 0 | 0 | 20.399 / 0.161 | yes | 51.02 | `quartus_SM1.md` |
| 2 | 5,271 | 1913 | 0 | 0 | 20.470 / 0.162 | yes | 51.20 | `quartus_SM1-s2.md` |
| 3 | 5,298 | 1913 | 0 | 0 | 20.789 / 0.162 | yes | 52.05 | `quartus_SM1-s3.md` |
| 4 | 5,311 | 1913 | 0 | 0 | 20.038 / 0.163 | yes | 50.10 | `quartus_SM1-s4.md` |
| 5 | 5,282 | 1913 | 0 | 0 | 20.484 / 0.162 | yes | 51.24 | `quartus_SM1-s5.md` |
| 6 | 5,273 | 1913 | 0 | 0 | 22.075 / 0.161 | yes | 55.79 | `quartus_SM1-s6.md` |

ALM median (min-max): 5,279.0 (5,271-5,311); registers 1913-1913; Fmax median (min-max): 51.220 (50.10-55.79) MHz

### W1 acceptance gate (test plan section 4)
- PASS: correct (verification_status: V1-V10, both simulators, controls fail, formal, regression)
- PASS: M10K = 0 and DSP = 0 at every seed
- PASS: ALM <= 12,573 at every seed (working cap)
- PASS: timing met at 40.000 ns at every seed
- PASS: median Fmax 51.220 MHz >= S10 median 44.320 MHz

**W1 gate result: PASSED.**

Cycles (C5 top, `cycles_w1_c5.json`; coef_ready always high): SampleNTT mean 305.23 cycles over 500 polynomials; CBD [280] cycles.

- information SM1-20 (20.000 ns), seed 1: ALM 5,296, worst setup 3.892 ns (met), Fmax lowest slow corner 62.08 MHz, `quartus_SM1-20.md`
- information SM1-K0 (K0 sponge), seed 1: ALM 3,470, worst setup 23.928 ns (met), Fmax lowest slow corner 62.22 MHz, `quartus_SM1-K0.md`

## W2: not measured (no evidence files)

Reference: S10 (NTT/INTT core) Fmax median 44.320 MHz over seeds 1-6 (recomputed from `evidence/phase06/s10/`).

## Selection W1 versus W2 (test plan section 5)
- W2 not measured yet. W1 gate: passed.
