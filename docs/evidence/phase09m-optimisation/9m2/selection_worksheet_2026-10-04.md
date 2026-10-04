## Phase 9 core (`CODEC_W2 = 0`) at 20.000 ns (MEASURED, kernel-only, virtual pins)
| Seed | ALM | Registers | RAM blocks | DSP | Worst setup / hold (ns) | Timing met @ 20 ns | Fmax lowest slow corner (MHz) | Critical warnings | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 17,650 | 8374 | 54 | 28 | 4.419 / 0.113 | yes | 64.18 | 1 | `docs/evidence/phase09-integration/9c/quartus_MC-20-20261003.md` |
| 2 | 17,780 | 8465 | 54 | 28 | 4.155 / 0.102 | yes | 63.11 | 1 | `docs/evidence/phase09m-optimisation/9m2/quartus_MC-20-s2-20261004.md` |
| 3 | 17,694 | 8431 | 54 | 28 | 4.534 / 0.094 | yes | 64.66 | 1 | `docs/evidence/phase09m-optimisation/9m2/quartus_MC-20-s3-20261004.md` |
| 4 | 17,729 | 8369 | 54 | 28 | 3.730 / 0.121 | yes | 61.46 | 1 | `docs/evidence/phase09m-optimisation/9m2/quartus_MC-20-s4-20261004.md` |
| 5 | 17,682 | 8461 | 54 | 28 | 4.522 / 0.109 | yes | 64.61 | 1 | `docs/evidence/phase09m-optimisation/9m2/quartus_MC-20-s5-20261004.md` |
| 6 | 17,723 | 8504 | 54 | 28 | 3.831 / 0.077 | yes | 61.85 | 1 | `docs/evidence/phase09m-optimisation/9m2/quartus_MC-20-s6-20261004.md` |

ALM median (min-max) 17,708.5 (17,650-17,780); registers 8369-8504; RAM blocks 54-54; DSP 28-28
Worst setup slack over seeds 3.730 ns; Fmax lowest slow corner median (min-max) 63.645 (61.46-64.66) MHz
**Timing met at 20.000 ns at 6 of 6 seeds**

Latency at the median Fmax of this table (perhitungan tim; profile-input cycles; kernel-only static timing, not a board measurement):
KeyGen 9,095 cycles = 142.9 us; Encaps 10,735 = 168.7 us; Decaps 16,667 = 261.9 us

## 9M-1 core (`CODEC_W2 = 1`) at 20.000 ns (MEASURED, kernel-only, virtual pins)
| Seed | ALM | Registers | RAM blocks | DSP | Worst setup / hold (ns) | Timing met @ 20 ns | Fmax lowest slow corner (MHz) | Critical warnings | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 17,808 | 8487 | 54 | 28 | 4.355 / 0.081 | yes | 63.92 | 1 | `docs/evidence/phase09m-optimisation/9m1/quartus_MW-20-20261004.md` |
| 2 | 17,756 | 8411 | 54 | 28 | 4.972 / 0.088 | yes | 66.54 | 1 | `docs/evidence/phase09m-optimisation/9m2/quartus_MW-20-s2-20261004.md` |
| 3 | 17,800 | 8447 | 54 | 28 | 4.236 / 0.131 | yes | 63.44 | 1 | `docs/evidence/phase09m-optimisation/9m2/quartus_MW-20-s3-20261004.md` |
| 4 | 17,759 | 8460 | 54 | 28 | 4.498 / 0.112 | yes | 64.51 | 1 | `docs/evidence/phase09m-optimisation/9m2/quartus_MW-20-s4-20261004.md` |
| 5 | 17,845 | 8481 | 54 | 28 | 4.184 / 0.100 | yes | 63.23 | 1 | `docs/evidence/phase09m-optimisation/9m2/quartus_MW-20-s5-20261004.md` |
| 6 | 17,728 | 8407 | 54 | 28 | 4.389 / 0.080 | yes | 64.06 | 1 | `docs/evidence/phase09m-optimisation/9m2/quartus_MW-20-s6-20261004.md` |

ALM median (min-max) 17,779.5 (17,728-17,845); registers 8407-8487; RAM blocks 54-54; DSP 28-28
Worst setup slack over seeds 4.184 ns; Fmax lowest slow corner median (min-max) 63.990 (63.23-66.54) MHz
**Timing met at 20.000 ns at 6 of 6 seeds**

Latency at the median Fmax of this table (perhitungan tim; profile-input cycles; kernel-only static timing, not a board measurement):
KeyGen 8,327 cycles = 130.1 us; Encaps 10,159 = 158.8 us; Decaps 15,515 = 242.5 us

### Rule (test plan section 5)
- met: the statement 'timing met at 20.000 ns' holds for a configuration only if all six seeds meet it; see the line 'Timing met at 20.000 ns at k of 6 seeds' of each table
