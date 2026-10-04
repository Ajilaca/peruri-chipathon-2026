## S0: the 9M-1 core (`CODEC_W2 = 1`, C5 hash and sampler) under tighter constraints (MEASURED, kernel-only, virtual pins)
| Revision | Constraint (ns) | Effort | ALM | Registers | RAM blocks | DSP | Worst setup / hold (ns) | Timing met | Fmax lowest slow corner (MHz) | Critical warnings | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F16-s1 | 16.000 | defaults | 17,980 | 8635 | 53 | 28 | 1.992 / 0.118 | yes | 71.39 | 1 | `docs/evidence/phase09m-optimisation/9f0/quartus_F16-s1-20261004.md` |
| F16-s2 | 16.000 | defaults | 17,888 | 8575 | 53 | 28 | 2.075 / 0.108 | yes | 71.81 | 1 | `docs/evidence/phase09m-optimisation/9f0/quartus_F16-s2-20261004.md` |
| F15-s1 | 15.000 | defaults | 17,971 | 8719 | 53 | 28 | 1.475 / 0.102 | yes | 73.94 | 1 | `docs/evidence/phase09m-optimisation/9f0/quartus_F15-s1-20261004.md` |
| F15-s2 | 15.000 | defaults | 17,926 | 8700 | 53 | 28 | 1.363 / 0.071 | yes | 73.33 | 1 | `docs/evidence/phase09m-optimisation/9f0/quartus_F15-s2-20261004.md` |
| F14-s1 | 14.000 | defaults | 17,907 | 8770 | 53 | 28 | 0.721 / 0.109 | yes | 75.31 | 1 | `docs/evidence/phase09m-optimisation/9f0/quartus_F14-s1-20261004.md` |
| F14-s2 | 14.000 | defaults | 17,889 | 8669 | 53 | 28 | 1.062 / 0.108 | yes | 77.29 | 1 | `docs/evidence/phase09m-optimisation/9f0/quartus_F14-s2-20261004.md` |
| H14-s1 | 14.000 | high performance | 18,876 | 10966 | 49 | 28 | 0.826 / 0.090 | yes | 75.91 | 1 | `docs/evidence/phase09m-optimisation/9f0/quartus_H14-s1-20261004.md` |
| H14-s2 | 14.000 | high performance | 18,897 | 10935 | 49 | 28 | 0.423 / 0.107 | yes | 73.65 | 1 | `docs/evidence/phase09m-optimisation/9f0/quartus_H14-s2-20261004.md` |
| F13-s1 | 13.000 | defaults | 17,900 | 8807 | 53 | 28 | 0.227 / 0.112 | yes | 78.29 | 1 | `docs/evidence/phase09m-optimisation/9f0/quartus_F13-s1-20261004.md` |
| F13-s2 | 13.000 | defaults | 17,891 | 8873 | 53 | 28 | -0.213 / 0.100 | **NO** | 75.68 | 3 | `docs/evidence/phase09m-optimisation/9f0/quartus_F13-s2-20261004.md` |

### Per constraint
| Group | Constraint (ns) | Met at k of 2 seeds | Lower Fmax of the two (MHz) | Worst setup of the two (ns) | ALM (min-max) | Latency KeyGen / Encaps / Decaps at the lower Fmax (us, perhitungan tim) |
|---|---|---|---|---|---|---|
| F16 | 16.000 | 2 of 2 | 71.39 | 1.992 | 17,888-17,980 | 116.6 / 142.3 / 217.3 |
| F15 | 15.000 | 2 of 2 | 73.33 | 1.363 | 17,926-17,971 | 113.6 / 138.5 / 211.6 |
| F14 | 14.000 | 2 of 2 | 75.31 | 0.721 | 17,889-17,907 | 110.6 / 134.9 / 206.0 |
| H14 | 14.000 | 2 of 2 | 73.65 | 0.423 | 18,876-18,897 | 113.1 / 137.9 / 210.7 |
| F13 | 13.000 | 1 of 2 | 75.68 | -0.213 | 17,891-17,900 | 110.0 / 134.2 / 205.0 |

### Rule (test plan section 5)
- Information, no adoption. The limit of the existing design is the tightest constraint met at both seeds: F16 (16 ns), F15 (15 ns), F14 (14 ns), H14 (14 ns).
- Amendment A2 (extended sweep, rule: stop at the first constraint not met): the sweep stopped at 13 ns (seed 1 met, seed 2 not met); the limit lies between 13 and 14 ns for this design and these settings.
