## Per seed at 40.000 ns, C5 sponge (MEASURED)
| Seed | ALM | Registers | Block memory bits | DSP | Worst setup / hold (ns) | Timing met @ 40 ns | Fmax lowest slow corner (MHz) | Critical warnings | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 6,745 | 1976 | 0 | 0 | 19.095 / 0.163 | yes | 47.84 | 1 | `quartus_HF-20261003.md` |
| 2 | 6,728 | 1976 | 0 | 0 | 19.122 / 0.161 | yes | 47.90 | 1 | `quartus_HF-s2-20261003.md` |
| 3 | 6,737 | 1976 | 0 | 0 | 20.400 / 0.162 | yes | 51.02 | 1 | `quartus_HF-s3-20261003.md` |
| 4 | 6,712 | 1976 | 0 | 0 | 20.090 / 0.162 | yes | 50.23 | 1 | `quartus_HF-s4-20261003.md` |
| 5 | 6,737 | 1976 | 0 | 0 | 20.794 / 0.162 | yes | 52.07 | 1 | `quartus_HF-s5-20261003.md` |
| 6 | 6,732 | 1976 | 0 | 0 | 20.508 / 0.162 | yes | 51.30 | 1 | `quartus_HF-s6-20261003.md` |

ALM median (min-max): 6,734.5 (6,712-6,745); registers 1976-1976; DSP 0-0; Fmax median (min-max): 50.625 (47.84-52.07) MHz

### Pass rule (test plan section 5, items 2 and 3)
- PASS: the fit succeeded at every seed
- PASS: timing met at 40.000 ns at every seed (worst setup and hold slack of all corners non-negative)
- reported as MEASURED: resource counts and Fmax (median of the lowest slow-corner Fmax over seeds 1-6) above; no alternative is chosen in this block
- information HF-20 (20.000 ns, C5 sponge), seed 1: ALM 6,745, registers 1976, worst setup 3.843 ns (met), Fmax lowest slow corner 61.89 MHz, `quartus_HF-20-20261003.md`
- information HF-K0 (40.000 ns, K0 sponge (the second hash instance with the smaller core)), seed 1: ALM 4,221, registers 1977, worst setup 25.719 ns (met), Fmax lowest slow corner 70.02 MHz, `quartus_HF-K0-20261003.md`

## Cycles (MEASURED in simulation, always-ready sink, no input gaps; identical for every data value of one operation: test V6)
| Operation | C5 sponge, Icarus | C5 sponge, Verilator | K0 sponge, Icarus | K0 sponge, Verilator |
|---|---|---|---|---|
| G of 33 bytes | 30 | 30 | 42 | 42 |
| G of 64 bytes | 33 | 33 | 45 | 45 |
| H of 1184 bytes | 282 | 282 | 390 | 390 |
| J of 1120 bytes | 274 | 274 | 382 | 382 |
| compare of 1,088 bytes (136 beats) | 137 | 137 | - | - |
