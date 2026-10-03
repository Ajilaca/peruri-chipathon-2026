<!-- claim-lint: skip-file (internal evidence record, not proposal text) -->
# Phase 8c selection worksheet, 2026-10-03

Command: `python3 scripts/select_8cd.py` (rules of `test_plan_8c.md` section 5, fixed before measuring; every value read from the evidence files named in the tables). Labels: MEASURED (Quartus reports, simulation); medians, t = cycles / Fmax and the rule are INFERENCE / perhitungan tim.
t is in microseconds (cycles divided by MHz); it covers the arithmetic of the program plus the sampling, in one sequencer, simulation cycles with the Fmax of the kernel-only compile.

## 8c: STREAM (A_hat sampled straight into the PWM unit) against STORE (A_hat sampled into slots)
| Seed | Config | ALM | Registers | M10K | DSP | Worst setup / hold (ns) | Timing met @ 40 ns | Fmax lowest slow corner (MHz) | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| 1 | STORE | 10,967 | 3364 | 55 | 26 | 15.734 / 0.131 | yes | 41.21 | `quartus_SMP0_20261003.md` |
| 2 | STORE | 10,969 | 3342 | 55 | 26 | 16.417 / 0.098 | yes | 42.40 | `quartus_SMP0-s2_20261003.md` |
| 3 | STORE | 10,959 | 3362 | 55 | 26 | 15.789 / 0.094 | yes | 41.30 | `quartus_SMP0-s3_20261003.md` |
| 4 | STORE | 10,944 | 3345 | 55 | 26 | 17.415 / 0.125 | yes | 44.28 | `quartus_SMP0-s4_20261003.md` |
| 5 | STORE | 10,941 | 3354 | 55 | 26 | 16.272 / 0.134 | yes | 42.14 | `quartus_SMP0-s5_20261003.md` |
| 6 | STORE | 10,957 | 3378 | 55 | 26 | 17.119 / 0.091 | yes | 43.70 | `quartus_SMP0-s6_20261003.md` |
| 1 | STREAM | 10,975 | 3385 | 44 | 26 | 17.441 / 0.091 | yes | 44.33 | `quartus_SMP1_20261003.md` |
| 2 | STREAM | 10,989 | 3389 | 44 | 26 | 18.100 / 0.096 | yes | 45.66 | `quartus_SMP1-s2_20261003.md` |
| 3 | STREAM | 10,958 | 3377 | 44 | 26 | 16.616 / 0.085 | yes | 42.76 | `quartus_SMP1-s3_20261003.md` |
| 4 | STREAM | 11,002 | 3395 | 44 | 26 | 17.243 / 0.130 | yes | 43.94 | `quartus_SMP1-s4_20261003.md` |
| 5 | STREAM | 11,032 | 3391 | 44 | 26 | 15.231 / 0.103 | yes | 40.37 | `quartus_SMP1-s5_20261003.md` |
| 6 | STREAM | 11,018 | 3385 | 44 | 26 | 16.621 / 0.094 | yes | 42.77 | `quartus_SMP1-s6_20261003.md` |

| | ALM median (min-max) | Registers | M10K | DSP | Fmax median (min-max) MHz | KeyGen cycles (mean) | Encrypt cycles (mean) | Decrypt cycles (mean) | t KeyGen (us) | t Encrypt (us) |
|---|---|---|---|---|---|---|---|---|---|---|
| STORE | 10,958.0 (10,941-10,969) | 3342-3378 | 55-55 | 26-26 | 42.270 (41.21-44.28) | 8268.1 | 9727.6 | 3109.0 | 195.6031 | 230.1294 |
| STREAM | 10,995.5 (10,958-11,032) | 3377-3395 | 44-44 | 26-26 | 43.355 (40.37-45.66) | 7089.1 | 8548.6 | 3109.0 | 163.5138 | 197.1761 |

Cycle sources: `cycles_v0_2026-10-03.json`, `cycles_v1_2026-10-03.json` (same inputs for every variant).

### Adoption rule (STREAM over STORE)
- PASS: correct (verification_status: V1-V8, both simulators, controls fail, formal)
- PASS: fit succeeded for both and timing met at 40.000 ns at every seed for STREAM
- PASS: t = c / F lower for STREAM than for STORE for KeyGen (163.5138 < 195.6031 us) and for Encrypt (197.1761 < 230.1294 us)
- PASS: M10K(STREAM) <= M10K(STORE) at every seed

**Rule result: STREAM ADOPTED.**

- information STORE (SMP0-20, 20.000 ns, seed 1): ALM 11,058, M10K 55, worst setup 0.992 ns (met), Fmax lowest slow corner 52.61 MHz, `quartus_SMP0-20_20261003.md`
- information STREAM (SMP1-20, 20.000 ns, seed 1): ALM 11,031, M10K 44, worst setup 1.783 ns (met), Fmax lowest slow corner 54.89 MHz, `quartus_SMP1-20_20261003.md`

