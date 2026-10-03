<!-- claim-lint: skip-file (internal evidence record, not proposal text) -->
# Phase 8d selection worksheet, 2026-10-03

Command: `python3 scripts/select_8cd.py` (rules of `test_plan_8d.md` section 5, fixed before measuring; every value read from the evidence files named in the tables). Labels: MEASURED (Quartus reports, simulation); medians, t = cycles / Fmax and the rule are INFERENCE / perhitungan tim.
t is in microseconds (cycles divided by MHz); it covers the arithmetic of the program plus the sampling, in one sequencer, simulation cycles with the Fmax of the kernel-only compile.

## 8d: OVERLAP (noise sampling during the transforms) against STREAM
| Seed | Config | ALM | Registers | M10K | DSP | Worst setup / hold (ns) | Timing met @ 40 ns | Fmax lowest slow corner (MHz) | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| 1 | STREAM | 10,975 | 3385 | 44 | 26 | 17.441 / 0.091 | yes | 44.33 | `quartus_SMP1_20261003.md` |
| 2 | STREAM | 10,989 | 3389 | 44 | 26 | 18.100 / 0.096 | yes | 45.66 | `quartus_SMP1-s2_20261003.md` |
| 3 | STREAM | 10,958 | 3377 | 44 | 26 | 16.616 / 0.085 | yes | 42.76 | `quartus_SMP1-s3_20261003.md` |
| 4 | STREAM | 11,002 | 3395 | 44 | 26 | 17.243 / 0.130 | yes | 43.94 | `quartus_SMP1-s4_20261003.md` |
| 5 | STREAM | 11,032 | 3391 | 44 | 26 | 15.231 / 0.103 | yes | 40.37 | `quartus_SMP1-s5_20261003.md` |
| 6 | STREAM | 11,018 | 3385 | 44 | 26 | 16.621 / 0.094 | yes | 42.77 | `quartus_SMP1-s6_20261003.md` |
| 1 | OVERLAP | 10,987 | 3405 | 44 | 26 | 17.049 / 0.146 | yes | 43.57 | `quartus_SMP2_20261003.md` |
| 2 | OVERLAP | 10,963 | 3414 | 44 | 26 | 17.242 / 0.086 | yes | 43.94 | `quartus_SMP2-s2_20261003.md` |
| 3 | OVERLAP | 11,009 | 3402 | 44 | 26 | 18.440 / 0.086 | yes | 46.38 | `quartus_SMP2-s3_20261003.md` |
| 4 | OVERLAP | 11,012 | 3387 | 44 | 26 | 16.269 / 0.082 | yes | 42.14 | `quartus_SMP2-s4_20261003.md` |
| 5 | OVERLAP | 10,998 | 3399 | 44 | 26 | 17.037 / 0.075 | yes | 43.55 | `quartus_SMP2-s5_20261003.md` |
| 6 | OVERLAP | 10,954 | 3368 | 44 | 26 | 17.925 / 0.082 | yes | 45.30 | `quartus_SMP2-s6_20261003.md` |

| | ALM median (min-max) | Registers | M10K | DSP | Fmax median (min-max) MHz | KeyGen cycles (mean) | Encrypt cycles (mean) | Decrypt cycles (mean) | t KeyGen (us) | t Encrypt (us) |
|---|---|---|---|---|---|---|---|---|---|---|
| STREAM | 10,995.5 (10,958-11,032) | 3377-3395 | 44-44 | 26-26 | 43.355 (40.37-45.66) | 7089.1 | 8548.6 | 3109.0 | 163.5138 | 197.1761 |
| OVERLAP | 10,992.5 (10,954-11,012) | 3368-3414 | 44-44 | 26-26 | 43.755 (42.14-46.38) | 6344.1 | 7654.6 | 3109.0 | 144.9924 | 174.9416 |

Cycle sources: `cycles_v1_2026-10-03.json`, `cycles_v2_2026-10-03.json` (same inputs for every variant).

### Adoption rule (OVERLAP over STREAM)
- PASS: correct (verification_status: V1-V8, both simulators, controls fail, formal)
- PASS: fit succeeded for both and timing met at 40.000 ns at every seed for OVERLAP
- PASS: t = c / F lower for OVERLAP than for STREAM for KeyGen (144.9924 < 163.5138 us) and for Encrypt (174.9416 < 197.1761 us)
- PASS: M10K(OVERLAP) <= M10K(STREAM) at every seed

**Rule result: OVERLAP ADOPTED.**

- information STREAM (SMP1-20, 20.000 ns, seed 1): ALM 11,031, M10K 44, worst setup 1.783 ns (met), Fmax lowest slow corner 54.89 MHz, `quartus_SMP1-20_20261003.md`
- information OVERLAP (SMP2-20, 20.000 ns, seed 1): ALM 11,049, M10K 44, worst setup 1.535 ns (met), Fmax lowest slow corner 54.16 MHz, `quartus_SMP2-20_20261003.md`

